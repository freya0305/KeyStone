"""B2B Onboarding API - Tenant registration, Stripe subscription, and user invitation.

Supports:
1. Self-service registration for recruiters/universities
2. B2B Stripe subscription checkout and portal
3. Invite link generation and activation
4. JD generation limit enforcement per tier
"""
import uuid
import secrets
from datetime import datetime, timedelta
from typing import Optional

import stripe
import structlog
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from keystone.models.base import get_db
from keystone.models.entities import (
    B2BTenant,
    B2BUser,
    User,
    InviteLink,
    AccessLevel,
)
from keystone.core import get_settings
from keystone.services.clerk_auth import get_current_user, get_current_b2b_user, AuthUser

logger = structlog.get_logger()
router = APIRouter(prefix="/recruiter", tags=["recruiter"])


# =============================================================================
# REQUEST/RESPONSE MODELS
# =============================================================================


class TenantRegisterRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    tenant_type: str = Field(..., pattern="^(UNIVERSITY|AGENCY|WSG)$")
    email: str = Field(..., min_length=1, max_length=255)  # Admin email


class TenantRegisterResponse(BaseModel):
    tenant_id: uuid.UUID
    name: str
    tenant_type: str
    created_at: datetime


class B2BCheckoutRequest(BaseModel):
    tier: str = Field(..., pattern="^(basic|pro|team)$")
    company_name: str = Field(..., min_length=1, max_length=255)


class B2BCheckoutResponse(BaseModel):
    checkout_url: str


class B2BPortalResponse(BaseModel):
    portal_url: str


class B2BTeamInviteRequest(BaseModel):
    email: str = Field(..., min_length=1, max_length=255)
    access_level: str = Field(default="MEMBER", pattern="^(ADMIN|MEMBER)$")


class B2BTeamInviteResponse(BaseModel):
    invite_token: str
    invite_url: str
    expires_at: datetime
    seat_count: int
    seat_limit: int


class B2BInviteAcceptRequest(BaseModel):
    invite_token: str
    name: str = Field(..., min_length=1, max_length=255)


class B2BInviteAcceptResponse(BaseModel):
    user_id: uuid.UUID
    tenant_id: uuid.UUID
    tenant_name: str
    access_level: str


class InviteGenerateRequest(BaseModel):
    email: str = Field(..., min_length=1, max_length=255)
    access_level: str = Field(default="MEMBER", pattern="^(ADMIN|MEMBER)$")


class InviteGenerateResponse(BaseModel):
    invite_token: str
    invite_url: str
    expires_at: datetime


class InviteAcceptRequest(BaseModel):
    invite_token: str


class InviteAcceptResponse(BaseModel):
    user_id: uuid.UUID
    tenant_id: uuid.UUID
    tenant_name: str
    access_level: str


class TenantInfoResponse(BaseModel):
    id: uuid.UUID
    name: str
    tenant_type: str
    tier: str
    seat_count: int
    seat_limit: int
    jd_generation_count: int
    jd_limit: int
    jd_limit_reset_at: Optional[datetime] = None
    is_suspended: bool
    stripe_subscription_id: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None


class TenantUpdateRequest(BaseModel):
    seat_count: Optional[int] = None


class SubscriptionTierInfo(BaseModel):
    tier: str
    seat_limit: int
    jd_limit: int
    price_sgd: int


# =============================================================================
# CONSTANTS
# =============================================================================

INVITE_TOKEN_LENGTH = 32
INVITE_EXPIRY_HOURS = 72
DEFAULT_SEAT_LIMIT = 10

# Tier configuration
TIER_CONFIG = {
    "basic": {"seat_limit": 1, "jd_limit": 50, "price_sgd": 79},
    "pro": {"seat_limit": 1, "jd_limit": -1, "price_sgd": 199},
    "team": {"seat_limit": 5, "jd_limit": -1, "price_sgd": 449},
}


# =============================================================================
# HELPERS
# =============================================================================


def _get_stripe_client():
    """Get Stripe client."""
    settings = get_settings()
    return stripe.StripeClient(settings.stripe_secret_key)


def _get_price_id_for_tier(tier: str) -> str:
    """Get Stripe price ID for a tier."""
    settings = get_settings()
    price_map = {
        "basic": getattr(settings, "stripe_price_b2b_basic", "price_b2b_basic"),
        "pro": getattr(settings, "stripe_price_b2b_pro", "price_b2b_pro"),
        "team": getattr(settings, "stripe_price_b2b_team", "price_b2b_team"),
    }
    return price_map.get(tier, "price_b2b_basic")


def _get_seat_limit_for_tier(tier: str) -> int:
    """Get seat limit for a tier."""
    return TIER_CONFIG.get(tier, {}).get("seat_limit", 1)


def _get_jd_limit_for_tier(tier: str) -> int:
    """Get JD generation limit for a tier."""
    return TIER_CONFIG.get(tier, {}).get("jd_limit", -1)


# =============================================================================
# SUBSCRIPTION TIER INFO
# =============================================================================


@router.get("/subscription-tiers")
async def get_subscription_tiers():
    """Get available B2B subscription tiers and their limits."""
    return {
        tier: SubscriptionTierInfo(
            tier=tier,
            seat_limit=info["seat_limit"],
            jd_limit=info["jd_limit"],
            price_sgd=info["price_sgd"],
        )
        for tier, info in TIER_CONFIG.items()
    }


# =============================================================================
# B2B CHECKOUT
# =============================================================================


@router.post("/b2b/checkout", response_model=B2BCheckoutResponse)
async def create_b2b_checkout(
    request: B2BCheckoutRequest,
    user: AuthUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create Stripe Checkout session for B2B subscription.

    Creates a new B2B tenant if one doesn't exist for this user,
    then creates a Stripe Checkout session for the selected tier.

    Tiers:
    - basic (Agency Team): SGD 79/mo, 5 users, 100 JD/month
    - pro (Agency Pro): SGD 199/mo, 10 users, 400 JD/month
    - team (Agency Enterprise): SGD 449/mo, unlimited users, unlimited JD
    """
    settings = get_settings()

    if not user.job_seeker_id:
        raise HTTPException(status_code=401, detail="User not found")

    # Validate tier
    if request.tier not in TIER_CONFIG:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid tier. Must be one of: {list(TIER_CONFIG.keys())}",
        )

    # Get user record
    result = await db.execute(select(User).where(User.id == user.job_seeker_id))
    db_user = result.scalar_one_or_none()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if user already has a B2B tenant
    existing_b2b = await db.execute(
        select(B2BUser).where(B2BUser.user_id == user.job_seeker_id)
    )
    existing_tenant_user = existing_b2b.scalar_one_or_none()

    # Get or create tenant
    if existing_tenant_user:
        # User already has a tenant - get it
        tenant_result = await db.execute(
            select(B2BTenant).where(B2BTenant.id == existing_tenant_user.tenant_id)
        )
        tenant = tenant_result.scalar_one_or_none()
        if not tenant:
            raise HTTPException(status_code=404, detail="Tenant not found")
    else:
        # Create new tenant
        tenant = B2BTenant(
            id=uuid.uuid4(),
            name=request.company_name,
            tenant_type="AGENCY",
            seat_count=1,
            tier="free",
            jd_limit=20,
            jd_generation_count=0,
        )
        db.add(tenant)
        await db.flush()

        # Create admin user for this tenant
        b2b_user = B2BUser(
            id=uuid.uuid4(),
            user_id=user.job_seeker_id,
            tenant_id=tenant.id,
            access_level=AccessLevel.ADMIN,
            invited_at=datetime.utcnow(),
            joined_at=datetime.utcnow(),
        )
        db.add(b2b_user)

    # Create or get Stripe customer
    if not db_user.stripe_customer_id:
        client = _get_stripe_client()
        customer = client.customers.create(
            email=db_user.email,
            name=db_user.name,
            metadata={"user_id": str(db_user.id), "tenant_id": str(tenant.id)},
        )
        db_user.stripe_customer_id = customer.id
        await db.flush()
    else:
        client = _get_stripe_client()
        # Update customer metadata with tenant_id
        try:
            client.customers.update(
                db_user.stripe_customer_id,
                metadata={"user_id": str(db_user.id), "tenant_id": str(tenant.id)},
            )
        except Exception as e:
            logger.warning("stripe_customer_update_failed", error=str(e))

    # Get price ID for tier
    price_id = _get_price_id_for_tier(request.tier)

    base_url = getattr(settings, "app_base_url", "http://localhost:3000")

    # Create checkout session
    client = _get_stripe_client()
    session = client.checkout.sessions.create(
        customer=db_user.stripe_customer_id,
        mode="subscription",
        line_items=[{"price": price_id, "quantity": 1}],
        success_url=f"{base_url}/recruiter/welcome?session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url=f"{base_url}/recruiter/pricing",
        metadata={
            "user_id": str(db_user.id),
            "tenant_id": str(tenant.id),
            "tier": request.tier,
        },
        currency="sgd",
        tax_behavior="exclusive",
        allow_promotion_codes=True,
    )

    logger.info(
        "b2b_checkout_created",
        user_id=str(db_user.id),
        tenant_id=str(tenant.id),
        tier=request.tier,
        session_id=session.id,
    )

    return B2BCheckoutResponse(checkout_url=session.url)


# =============================================================================
# B2B PORTAL
# =============================================================================


@router.post("/b2b/portal", response_model=B2BPortalResponse)
async def get_b2b_portal(
    user: AuthUser = Depends(get_current_b2b_user),
    db: AsyncSession = Depends(get_db),
):
    """Get Stripe Customer Portal URL for B2B subscription management.

    Allows tenant admins to manage their subscription, seats, and billing.
    """
    settings = get_settings()

    # Get user's B2B record and tenant
    result = await db.execute(
        select(B2BUser, B2BTenant).join(
            B2BTenant, B2BUser.tenant_id == B2BTenant.id
        ).where(B2BUser.user_id == user.job_seeker_id)
    )
    row = result.one_or_none()
    if not row:
        raise HTTPException(status_code=404, detail="No B2B tenant found")

    b2b_user, tenant = row

    if b2b_user.access_level != AccessLevel.ADMIN:
        raise HTTPException(status_code=403, detail="Only admins can access billing portal")

    if not tenant.stripe_subscription_id:
        raise HTTPException(status_code=400, detail="No active subscription found")

    # Get Stripe customer from tenant owner (first user)
    owner_result = await db.execute(
        select(User).join(B2BUser, B2BUser.user_id == User.id)
        .where(B2BUser.tenant_id == tenant.id, B2BUser.access_level == AccessLevel.ADMIN)
        .limit(1)
    )
    owner = owner_result.scalar_one_or_none()
    if not owner or not owner.stripe_customer_id:
        raise HTTPException(status_code=400, detail="No billing account found")

    base_url = getattr(settings, "app_base_url", "http://localhost:3000")

    client = _get_stripe_client()
    portal_session = client.billing_portal.sessions.create(
        customer=owner.stripe_customer_id,
        return_url=f"{base_url}/recruiter/settings",
    )

    logger.info(
        "b2b_portal_created",
        tenant_id=str(tenant.id),
        user_id=str(user.job_seeker_id),
    )

    return B2BPortalResponse(portal_url=portal_session.url)


# =============================================================================
# B2B SUBSCRIPTION STATUS
# =============================================================================


@router.get("/b2b/subscription", response_model=TenantInfoResponse)
async def get_b2b_subscription(
    user: AuthUser = Depends(get_current_b2b_user),
    db: AsyncSession = Depends(get_db),
):
    """Get current user's B2B subscription status."""
    result = await db.execute(
        select(B2BTenant, B2BUser).join(
            B2BTenant, B2BUser.tenant_id == B2BTenant.id
        ).where(B2BUser.user_id == user.job_seeker_id)
    )
    row = result.one_or_none()
    if not row:
        raise HTTPException(status_code=404, detail="No B2B tenant found")

    tenant, b2b_user = row

    seat_limit = _get_seat_limit_for_tier(tenant.tier) if tenant.tier in TIER_CONFIG else DEFAULT_SEAT_LIMIT

    return TenantInfoResponse(
        id=tenant.id,
        name=tenant.name,
        tenant_type=tenant.tenant_type,
        tier=tenant.tier,
        seat_count=tenant.seat_count,
        seat_limit=seat_limit,
        jd_generation_count=tenant.jd_generation_count,
        jd_limit=tenant.jd_limit,
        jd_limit_reset_at=tenant.jd_limit_reset_at,
        is_suspended=tenant.is_suspended,
        stripe_subscription_id=tenant.stripe_subscription_id,
        created_at=tenant.created_at,
        updated_at=tenant.updated_at,
    )


# =============================================================================
# TEAM INVITE FLOW (AGENCY TEAM ONLY)
# =============================================================================


@router.post("/b2b/invite", response_model=B2BTeamInviteResponse)
async def invite_team_member(
    request: B2BTeamInviteRequest,
    user: AuthUser = Depends(get_current_b2b_user),
    db: AsyncSession = Depends(get_db),
):
    """Invite a team member to the B2B tenant.

    Only available for Agency Team tier (5 users).
    Only ADMIN users can generate invites.
    """
    settings = get_settings()

    # Get user's B2B record and tenant
    result = await db.execute(
        select(B2BUser, B2BTenant).join(
            B2BTenant, B2BUser.tenant_id == B2BTenant.id
        ).where(B2BUser.user_id == user.job_seeker_id)
    )
    row = result.one_or_none()
    if not row:
        raise HTTPException(status_code=403, detail="B2B user not found")

    b2b_user, tenant = row

    if b2b_user.access_level != AccessLevel.ADMIN:
        raise HTTPException(status_code=403, detail="Only admins can invite team members")

    # Check if tenant is Team tier
    if tenant.tier != "team":
        raise HTTPException(
            status_code=403,
            detail="Team invite is only available for Team tier subscribers",
        )

    seat_limit = _get_seat_limit_for_tier("team")

    # Check seat count
    if tenant.seat_count >= seat_limit:
        raise HTTPException(
            status_code=400,
            detail=f"Seat limit reached ({seat_limit} seats)",
        )

    # Check if email is already a member
    existing_member = await db.execute(
        select(B2BUser)
        .join(User, B2BUser.user_id == User.id)
        .where(B2BUser.tenant_id == tenant.id, User.email == request.email)
    )
    if existing_member.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="User is already a team member")

    # Generate invite token
    invite_token = secrets.token_urlsafe(INVITE_TOKEN_LENGTH)
    expires_at = datetime.utcnow() + timedelta(hours=INVITE_EXPIRY_HOURS)

    # Create invite link record
    invite_link = InviteLink(
        id=uuid.uuid4(),
        tenant_id=tenant.id,
        token=invite_token,
        email=request.email,
        access_level=AccessLevel(request.access_level),
        expires_at=expires_at,
        created_by_id=b2b_user.id,
    )
    db.add(invite_link)
    await db.commit()

    # Build invite URL
    base_url = getattr(settings, "app_base_url", "http://localhost:3000")
    invite_url = f"{base_url}/invite/{invite_token}"

    logger.info(
        "b2b_team_invite_generated",
        tenant_id=str(tenant.id),
        invited_email=request.email,
        access_level=request.access_level,
    )

    return B2BTeamInviteResponse(
        invite_token=invite_token,
        invite_url=invite_url,
        expires_at=expires_at,
        seat_count=tenant.seat_count,
        seat_limit=seat_limit,
    )


@router.post("/b2b/accept-invite", response_model=B2BInviteAcceptResponse)
async def accept_b2b_invite(
    request: B2BInviteAcceptRequest,
    user: AuthUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Accept a B2B team invite and join a tenant.

    Validates the invite token, updates the user's name if provided,
    and creates a B2BUser record with joined_at timestamp.
    """
    if not user.job_seeker_id:
        raise HTTPException(status_code=401, detail="User not found")

    # Look up invite token
    result = await db.execute(
        select(InviteLink, B2BTenant).join(
            B2BTenant, InviteLink.tenant_id == B2BTenant.id
        ).where(InviteLink.token == request.invite_token)
    )
    row = result.one_or_none()
    if not row:
        raise HTTPException(status_code=404, detail="Invite not found")

    invite, tenant = row

    # Check if already used
    if invite.used_at is not None:
        raise HTTPException(status_code=400, detail="Invite already used")

    # Check if expired
    if invite.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Invite expired")

    # Check if user already belongs to a tenant
    existing_b2b = await db.execute(
        select(B2BUser).where(B2BUser.user_id == user.job_seeker_id)
    )
    if existing_b2b.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="User already belongs to a tenant")

    # Mark invite as used
    invite.used_at = datetime.utcnow()

    # Update user's name if provided and different
    user_result = await db.execute(
        select(User).where(User.id == user.job_seeker_id)
    )
    db_user = user_result.scalar_one_or_none()
    if db_user and request.name and db_user.name != request.name:
        db_user.name = request.name

    # Create B2BUser record with joined_at
    b2b_user = B2BUser(
        id=uuid.uuid4(),
        user_id=user.job_seeker_id,
        tenant_id=invite.tenant_id,
        access_level=invite.access_level,
        invited_at=invite.created_at,
        joined_at=datetime.utcnow(),
    )
    db.add(b2b_user)

    # Increment tenant seat count
    tenant.seat_count += 1

    await db.commit()

    logger.info(
        "b2b_invite_accepted",
        tenant_id=str(invite.tenant_id),
        user_id=str(user.job_seeker_id),
    )

    return B2BInviteAcceptResponse(
        user_id=user.job_seeker_id,
        tenant_id=invite.tenant_id,
        tenant_name=tenant.name,
        access_level=invite.access_level.value,
    )


# =============================================================================
# TENANT REGISTRATION (SELF-SERVICE)
# =============================================================================


@router.post("/onboarding/tenant/register", response_model=TenantRegisterResponse)
async def register_tenant(
    request: TenantRegisterRequest,
    user: AuthUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Register a new tenant organization (university or recruitment agency).

    The current user becomes the tenant admin.
    Note: For paid subscriptions, use /b2b/checkout instead.
    """
    settings = get_settings()

    # Check if internal user exists (provisioned by Clerk auth)
    if not user.job_seeker_id:
        raise HTTPException(status_code=401, detail="User not found")

    # Check if user already belongs to a tenant
    existing_b2b = await db.execute(
        select(B2BUser).where(B2BUser.user_id == user.job_seeker_id)
    )
    if existing_b2b.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="User already belongs to a tenant")

    # Check if tenant name already exists
    existing_tenant = await db.execute(
        select(B2BTenant).where(B2BTenant.name == request.name)
    )
    if existing_tenant.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Tenant name already exists")

    # Create tenant
    tenant = B2BTenant(
        id=uuid.uuid4(),
        name=request.name,
        tenant_type=request.tenant_type,
        seat_count=1,
        tier="free",
        jd_limit=20,
        jd_generation_count=0,
    )
    db.add(tenant)

    # Create admin user for this tenant
    b2b_user = B2BUser(
        id=uuid.uuid4(),
        user_id=user.job_seeker_id,
        tenant_id=tenant.id,
        access_level=AccessLevel.ADMIN,
        invited_at=datetime.utcnow(),
        joined_at=datetime.utcnow(),
    )
    db.add(b2b_user)

    await db.commit()
    await db.refresh(tenant)

    logger.info("b2b.tenant_registered", tenant_id=str(tenant.id), tenant_type=request.tenant_type)

    return TenantRegisterResponse(
        tenant_id=tenant.id,
        name=tenant.name,
        tenant_type=tenant.tenant_type,
        created_at=tenant.created_at,
    )


# =============================================================================
# INVITE LINK MANAGEMENT (LEGACY)
# =============================================================================


@router.post("/onboarding/invite/generate", response_model=InviteGenerateResponse)
async def generate_invite(
    request: InviteGenerateRequest,
    user: AuthUser = Depends(get_current_b2b_user),
    db: AsyncSession = Depends(get_db),
):
    """Generate an invite link for a new team member.

    Only ADMIN users can generate invites.
    """
    settings = get_settings()

    # Get user's B2B record and tenant
    result = await db.execute(
        select(B2BUser, B2BTenant).join(
            B2BTenant, B2BUser.tenant_id == B2BTenant.id
        ).where(B2BUser.user_id == user.job_seeker_id)
    )
    row = result.one_or_none()
    if not row:
        raise HTTPException(status_code=403, detail="B2B user not found")

    b2b_user, tenant = row

    if b2b_user.access_level != AccessLevel.ADMIN:
        raise HTTPException(status_code=403, detail="Only admins can generate invites")

    # Check seat count
    if tenant.seat_count >= DEFAULT_SEAT_LIMIT:
        raise HTTPException(status_code=400, detail="Seat limit reached")

    # Generate invite token
    invite_token = secrets.token_urlsafe(INVITE_TOKEN_LENGTH)
    expires_at = datetime.utcnow() + timedelta(hours=INVITE_EXPIRY_HOURS)

    # Create invite link record
    invite_link = InviteLink(
        id=uuid.uuid4(),
        tenant_id=tenant.id,
        token=invite_token,
        email=request.email,
        access_level=AccessLevel(request.access_level),
        expires_at=expires_at,
        created_by_id=b2b_user.id,
    )
    db.add(invite_link)
    await db.commit()

    # Build invite URL
    base_url = getattr(settings, "app_base_url", "http://localhost:3000")
    invite_url = f"{base_url}/invite/{invite_token}"

    logger.info("b2b.invite_generated", tenant_id=str(tenant.id), invited_email=request.email)

    return InviteGenerateResponse(
        invite_token=invite_token,
        invite_url=invite_url,
        expires_at=expires_at,
    )


@router.post("/onboarding/invite/accept", response_model=InviteAcceptResponse)
async def accept_invite(
    request: InviteAcceptRequest,
    user: AuthUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Accept an invite and join a tenant.

    Validates the invite token and creates a B2BUser record.
    """
    if not user.job_seeker_id:
        raise HTTPException(status_code=401, detail="User not found")

    # Look up invite token
    result = await db.execute(
        select(InviteLink).where(InviteLink.token == request.invite_token)
    )
    invite = result.scalar_one_or_none()

    if not invite:
        raise HTTPException(status_code=404, detail="Invite not found")

    # Check if already used
    if invite.used_at is not None:
        raise HTTPException(status_code=400, detail="Invite already used")

    # Check if expired
    if invite.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Invite expired")

    # Check if user already belongs to a tenant
    existing_b2b = await db.execute(
        select(B2BUser).where(B2BUser.user_id == user.job_seeker_id)
    )
    if existing_b2b.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="User already belongs to a tenant")

    # Mark invite as used
    invite.used_at = datetime.utcnow()

    # Get internal user to update name if needed
    user_result = await db.execute(
        select(User).where(User.id == user.job_seeker_id)
    )
    internal_user = user_result.scalar_one_or_none()

    # Create B2BUser record
    b2b_user = B2BUser(
        id=uuid.uuid4(),
        user_id=user.job_seeker_id,
        tenant_id=invite.tenant_id,
        access_level=invite.access_level,
        invited_at=invite.created_at,
        joined_at=datetime.utcnow(),
    )
    db.add(b2b_user)

    # Increment tenant seat count
    tenant_result = await db.execute(
        select(B2BTenant).where(B2BTenant.id == invite.tenant_id)
    )
    tenant = tenant_result.scalar_one()
    tenant.seat_count += 1

    await db.commit()

    logger.info("b2b.invite_accepted", tenant_id=str(invite.tenant_id), user_id=str(user.job_seeker_id))

    return InviteAcceptResponse(
        user_id=user.job_seeker_id,
        tenant_id=invite.tenant_id,
        tenant_name=tenant.name,
        access_level=invite.access_level.value,
    )


@router.get("/onboarding/tenant/me", response_model=TenantInfoResponse)
async def get_my_tenant(
    user: AuthUser = Depends(get_current_b2b_user),
    db: AsyncSession = Depends(get_db),
):
    """Get current user's tenant info."""

    result = await db.execute(
        select(B2BTenant, B2BUser).join(
            B2BTenant, B2BUser.tenant_id == B2BTenant.id
        ).where(B2BUser.user_id == user.job_seeker_id)
    )
    row = result.one_or_none()
    if not row:
        raise HTTPException(status_code=404, detail="No tenant found")

    tenant, b2b_user = row

    seat_limit = _get_seat_limit_for_tier(tenant.tier) if tenant.tier in TIER_CONFIG else DEFAULT_SEAT_LIMIT

    return TenantInfoResponse(
        id=tenant.id,
        name=tenant.name,
        tenant_type=tenant.tenant_type,
        tier=tenant.tier,
        seat_count=tenant.seat_count,
        seat_limit=seat_limit,
        jd_generation_count=tenant.jd_generation_count,
        jd_limit=tenant.jd_limit,
        jd_limit_reset_at=tenant.jd_limit_reset_at,
        is_suspended=tenant.is_suspended,
        stripe_subscription_id=tenant.stripe_subscription_id,
        created_at=tenant.created_at,
        updated_at=tenant.updated_at,
    )


@router.put("/onboarding/tenant/me", response_model=TenantInfoResponse)
async def update_my_tenant(
    request: TenantUpdateRequest,
    user: AuthUser = Depends(get_current_b2b_user),
    db: AsyncSession = Depends(get_db),
):
    """Update current user's tenant info (admin only)."""

    result = await db.execute(
        select(B2BTenant, B2BUser).join(
            B2BTenant, B2BUser.tenant_id == B2BTenant.id
        ).where(B2BUser.user_id == user.job_seeker_id)
    )
    row = result.one_or_none()
    if not row:
        raise HTTPException(status_code=404, detail="No tenant found")

    tenant, b2b_user = row

    if b2b_user.access_level != AccessLevel.ADMIN:
        raise HTTPException(status_code=403, detail="Only admins can update tenant")

    if request.seat_count is not None:
        if request.seat_count < tenant.seat_count:
            raise HTTPException(status_code=400, detail="Cannot reduce seat count below current usage")
        tenant.seat_count = request.seat_count

    await db.commit()
    await db.refresh(tenant)

    seat_limit = _get_seat_limit_for_tier(tenant.tier) if tenant.tier in TIER_CONFIG else DEFAULT_SEAT_LIMIT

    return TenantInfoResponse(
        id=tenant.id,
        name=tenant.name,
        tenant_type=tenant.tenant_type,
        tier=tenant.tier,
        seat_count=tenant.seat_count,
        seat_limit=seat_limit,
        jd_generation_count=tenant.jd_generation_count,
        jd_limit=tenant.jd_limit,
        jd_limit_reset_at=tenant.jd_limit_reset_at,
        is_suspended=tenant.is_suspended,
        stripe_subscription_id=tenant.stripe_subscription_id,
        created_at=tenant.created_at,
        updated_at=tenant.updated_at,
    )

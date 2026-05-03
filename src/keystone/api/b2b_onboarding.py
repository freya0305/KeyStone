"""B2B Onboarding API - Tenant registration and user invitation.

Supports:
1. Self-service registration for recruiters/universities
2. Invite link generation and activation
"""
import uuid
import secrets
from datetime import datetime, timedelta
from typing import Optional

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
from keystone.services.clerk_auth import get_current_user, AuthUser

router = APIRouter(prefix="/recruiter/onboarding", tags=["recruiter"])


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
    seat_count: int
    created_at: datetime


class TenantUpdateRequest(BaseModel):
    seat_count: Optional[int] = None


# =============================================================================
# CONSTANTS
# =============================================================================

INVITE_TOKEN_LENGTH = 32
INVITE_EXPIRY_HOURS = 72
DEFAULT_SEAT_LIMIT = 10


# =============================================================================
# TENANT REGISTRATION (SELF-SERVICE)
# =============================================================================


@router.post("/tenant/register", response_model=TenantRegisterResponse)
async def register_tenant(
    request: TenantRegisterRequest,
    user: AuthUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Register a new tenant organization (university or recruitment agency).

    The current user becomes the tenant admin.
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
    )
    db.add(tenant)

    # Create admin user for this tenant
    b2b_user = B2BUser(
        id=uuid.uuid4(),
        user_id=user.job_seeker_id,
        tenant_id=tenant.id,
        access_level=AccessLevel.ADMIN,
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
# INVITE LINK MANAGEMENT
# =============================================================================


@router.post("/invite/generate", response_model=InviteGenerateResponse)
async def generate_invite(
    request: InviteGenerateRequest,
    user: AuthUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Generate an invite link for a new team member.

    Only ADMIN users can generate invites.
    """
    settings = get_settings()

    if not user.is_b2b:
        raise HTTPException(status_code=403, detail="B2B access required")

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


@router.post("/invite/accept", response_model=InviteAcceptResponse)
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


@router.get("/tenant/me", response_model=TenantInfoResponse)
async def get_my_tenant(
    user: AuthUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get current user's tenant info."""
    if not user.is_b2b:
        raise HTTPException(status_code=403, detail="B2B access required")

    result = await db.execute(
        select(B2BTenant, B2BUser).join(
            B2BTenant, B2BUser.tenant_id == B2BTenant.id
        ).where(B2BUser.user_id == user.job_seeker_id)
    )
    row = result.one_or_none()
    if not row:
        raise HTTPException(status_code=404, detail="No tenant found")

    tenant, b2b_user = row

    return TenantInfoResponse(
        id=tenant.id,
        name=tenant.name,
        tenant_type=tenant.tenant_type,
        seat_count=tenant.seat_count,
        created_at=tenant.created_at,
    )


@router.put("/tenant/me", response_model=TenantInfoResponse)
async def update_my_tenant(
    request: TenantUpdateRequest,
    user: AuthUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update current user's tenant info (admin only)."""
    if not user.is_b2b:
        raise HTTPException(status_code=403, detail="B2B access required")

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

    return TenantInfoResponse(
        id=tenant.id,
        name=tenant.name,
        tenant_type=tenant.tenant_type,
        seat_count=tenant.seat_count,
        created_at=tenant.created_at,
    )


# Import logger at module level
import structlog
logger = structlog.get_logger()

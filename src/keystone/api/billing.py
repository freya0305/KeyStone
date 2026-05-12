"""Billing API - Stripe subscription management.

Implements M6.1:
- POST /billing/create-checkout-session
- POST /billing/create-portal-session
- GET /billing/subscription
"""
import stripe
import structlog
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from keystone.core import get_settings
from keystone.models.base import get_db
from keystone.models.entities import User, SubscriptionTier
from keystone.services.clerk_auth import get_current_user, AuthUser

logger = structlog.get_logger()

router = APIRouter(prefix="/billing", tags=["billing"])


# =============================================================================
# REQUEST/RESPONSE MODELS
# =============================================================================


class CheckoutSessionResponse(BaseModel):
    checkout_url: str


class PortalSessionResponse(BaseModel):
    portal_url: str


class SubscriptionResponse(BaseModel):
    tier: str
    stripe_customer_id: str | None
    stripe_subscription_id: str | None
    has_active_subscription: bool


class TrialCheckoutResponse(BaseModel):
    checkout_url: str


# =============================================================================
# STRIPE CLIENT
# =============================================================================


def _get_stripe():
    settings = get_settings()
    return stripe.StripeClient(settings.stripe_secret_key)


# =============================================================================
# CREATE CHECKOUT SESSION
# =============================================================================


@router.post("/create-checkout-session", response_model=CheckoutSessionResponse)
async def create_checkout_session(
    plan: str,
    user: AuthUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create Stripe Checkout session for Pro subscription.

    Plans: 'monthly' (SGD 12/mo). Annual plan is not available.
    """
    settings = get_settings()
    client = _get_stripe()

    # Look up user
    result = await db.execute(select(User).where(User.id == user.job_seeker_id))
    db_user = result.scalar_one_or_none()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Price IDs (use env-configured values)
    price_monthly = getattr(settings, "stripe_price_pro_monthly", "price_pro_monthly")

    if plan != "monthly":
        raise HTTPException(status_code=400, detail="Invalid plan. Use 'monthly' only — annual plan is cancelled")

    # Create or get Stripe customer
    if not db_user.stripe_customer_id:
        customer = client.customers.create(
            email=db_user.email,
            name=db_user.name,
            metadata={"user_id": str(db_user.id)},
        )
        db_user.stripe_customer_id = customer.id
        await db.commit()

    base_url = getattr(settings, "app_base_url", "http://localhost:3000")

    session = client.checkout.sessions.create(
        customer=db_user.stripe_customer_id,
        mode="subscription",
        line_items=[{"price": price_monthly, "quantity": 1}],
        success_url=f"{base_url}/pro/welcome?session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url=f"{base_url}/pricing",
        metadata={"user_id": str(db_user.id), "plan": plan},
        currency="sgd",
        tax_behavior="exclusive",
    )

    return CheckoutSessionResponse(checkout_url=session.url)


# =============================================================================
# CREATE PORTAL SESSION
# =============================================================================


@router.post("/create-portal-session", response_model=PortalSessionResponse)
async def create_portal_session(
    user: AuthUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create Stripe Customer Portal session for subscription management."""
    settings = get_settings()
    client = _get_stripe()

    result = await db.execute(select(User).where(User.id == user.job_seeker_id))
    db_user = result.scalar_one_or_none()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if not db_user.stripe_customer_id:
        raise HTTPException(status_code=400, detail="No billing account found")

    base_url = getattr(settings, "app_base_url", "http://localhost:3000")

    session = client.billing_portal.sessions.create(
        customer=db_user.stripe_customer_id,
        return_url=f"{base_url}/app/settings",
    )

    return PortalSessionResponse(portal_url=session.url)


# =============================================================================
# GET SUBSCRIPTION STATUS
# =============================================================================


@router.get("/subscription", response_model=SubscriptionResponse)
async def get_subscription(
    user: AuthUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get current user's subscription status."""
    result = await db.execute(select(User).where(User.id == user.job_seeker_id))
    db_user = result.scalar_one_or_none()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    return SubscriptionResponse(
        tier=db_user.subscription_tier.value,
        stripe_customer_id=db_user.stripe_customer_id,
        stripe_subscription_id=db_user.stripe_subscription_id,
        has_active_subscription=db_user.stripe_subscription_id is not None,
    )


# =============================================================================
# CREATE 3-DAY TRIAL (no card required)
# =============================================================================


@router.post("/create-trial", response_model=CheckoutSessionResponse)
async def create_trial(
    user: AuthUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a 3-day Pro trial (no payment method required).

    Creates Stripe customer + subscription with trial period.
    """
    settings = get_settings()
    client = _get_stripe()

    result = await db.execute(select(User).where(User.id == user.job_seeker_id))
    db_user = result.scalar_one_or_none()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    price_trial = getattr(settings, "stripe_price_pro_monthly", "price_pro_monthly")

    # Create Stripe customer if not exists
    if not db_user.stripe_customer_id:
        customer = client.customers.create(
            email=db_user.email,
            name=db_user.name,
            metadata={"user_id": str(db_user.id)},
        )
        db_user.stripe_customer_id = customer.id

    # Create subscription with 3-day trial
    subscription = client.subscriptions.create(
        customer=db_user.stripe_customer_id,
        items=[{"price": price_trial}],
        trial_period_days=3,
        metadata={"user_id": str(db_user.id)},
    )

    db_user.stripe_subscription_id = subscription.id
    db_user.subscription_tier = SubscriptionTier.PRO
    await db.commit()

    base_url = getattr(settings, "app_base_url", "http://localhost:3000")

    return CheckoutSessionResponse(checkout_url=f"{base_url}/pro/welcome?trial=activated")

"""Stripe webhook handler.

Red team finding: Stripe webhook must be implemented BEFORE launch.
Missing webhook = payments not confirmed = revenue loss.

SECURITY FIXES:
- Redis-based idempotency (in-memory set fails under multi-worker)
- Subscription tier updates actually persist to database
"""
import asyncio
import json
from datetime import datetime
from typing import Callable, Optional
import uuid

import stripe
import structlog
import redis
from fastapi import Request, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from stripe import Event

from keystone.core import get_settings
from keystone.models.entities import User, SubscriptionTier

logger = structlog.get_logger()

# Event types we handle
CHECKOUT_COMPLETED = "checkout.session.completed"
SUBSCRIPTION_DELETED = "customer.subscription.deleted"
SUBSCRIPTION_UPDATED = "customer.subscription.updated"

# Price ID to tier mapping
PRICE_TO_TIER = {
    "price_solo": SubscriptionTier.SOLO,
    "price_pro": SubscriptionTier.PRO,
    "price_team": SubscriptionTier.TEAM,
}


def _get_redis() -> redis.Redis:
    """Get Redis client for idempotency."""
    settings = get_settings()
    return redis.from_url(settings.redis_url, decode_responses=True)


async def verify_stripe_signature(request: Request) -> Event:
    """Verify Stripe webhook signature.

    Raises HTTPException if signature is invalid.
    """
    settings = get_settings()
    body = await request.body()

    try:
        event = stripe.Webhook.construct_event(
            body,
            request.headers.get("stripe-signature", ""),
            settings.stripe_webhook_secret,
        )
    except ValueError as e:
        logger.error("stripe_invalid_payload", error=str(e))
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError as e:
        logger.error("stripe_invalid_signature", error=str(e))
        raise HTTPException(status_code=400, detail="Invalid signature")

    return event


async def is_event_processed(event_id: str) -> bool:
    """Check if event was already processed (idempotency) using Redis.

    Uses Redis SET NX with expiry for distributed idempotency across workers.
    """
    r = _get_redis()
    key = f"stripe:processed:{event_id}"
    # SET NX returns True if key was set (not exists), False if already exists
    was_set = r.set(key, "1", nx=True, ex=86400 * 7)  # 7 day expiry
    return not was_set


async def handle_checkout_completed(event: Event, db: AsyncSession) -> None:
    """Handle successful checkout session.

    Updates user's subscription_tier based on price_id and records
    stripe_customer_id and stripe_subscription_id for future events.
    """
    session = event.data.object

    logger.info(
        "stripe_checkout_completed",
        session_id=session.id,
        customer_id=session.customer,
        subscription_id=session.subscription,
        amount_total=session.amount_total,
        currency=session.currency,
    )

    # Get user by client_reference_id (user_id)
    user_id = session.client_reference_id
    if not user_id:
        logger.warning("stripe_checkout_no_user_reference", session_id=session.id)
        return

    # Get price_id from line items
    price_id = None
    if session.line_items and session.line_items.data:
        price_id = session.line_items.data[0].price.id

    tier = PRICE_TO_TIER.get(price_id, SubscriptionTier.FREE)

    # Find and update user
    result = await db.execute(
        select(User).where(User.id == uuid.UUID(user_id))
    )
    user = result.scalar_one_or_none()
    if user:
        user.subscription_tier = tier
        user.stripe_customer_id = session.customer
        user.stripe_subscription_id = session.subscription
        await db.commit()
        logger.info("stripe_user_subscription_updated", user_id=user_id, tier=tier.value)
    else:
        logger.warning("stripe_checkout_user_not_found", user_id=user_id)


async def handle_subscription_deleted(event: Event, db: AsyncSession) -> None:
    """Handle subscription cancellation.

    Sets user's subscription_tier back to FREE.
    """
    subscription = event.data.object

    logger.info(
        "stripe_subscription_deleted",
        subscription_id=subscription.id,
        customer_id=subscription.customer,
        status=subscription.status,
    )

    # Find user by stripe_customer_id and reset to free tier
    result = await db.execute(
        select(User).where(User.stripe_customer_id == subscription.customer)
    )
    user = result.scalar_one_or_none()
    if user:
        user.subscription_tier = SubscriptionTier.FREE
        user.stripe_subscription_id = None
        await db.commit()
        logger.info("stripe_subscription_cancelled", user_id=str(user.id))
    else:
        logger.warning("stripe_subscription_customer_not_found", customer_id=subscription.customer)


async def handle_subscription_updated(event: Event, db: AsyncSession) -> None:
    """Handle subscription changes (e.g., plan changes).

    Updates user's subscription_tier if the price_id changed.
    """
    subscription = event.data.object

    logger.info(
        "stripe_subscription_updated",
        subscription_id=subscription.id,
        customer_id=subscription.customer,
        status=subscription.status,
    )

    # Get new price_id from subscription items
    price_id = None
    if subscription.items and subscription.items.data:
        price_id = subscription.items.data[0].price.id

    tier = PRICE_TO_TIER.get(price_id, SubscriptionTier.FREE)

    # Find and update user
    result = await db.execute(
        select(User).where(User.stripe_customer_id == subscription.customer)
    )
    user = result.scalar_one_or_none()
    if user:
        user.subscription_tier = tier
        user.stripe_subscription_id = subscription.id
        await db.commit()
        logger.info("stripe_subscription_updated_user", user_id=str(user.id), tier=tier.value)
    else:
        logger.warning("stripe_subscription_customer_not_found", customer_id=subscription.customer)


HANDLERS: dict[str, Callable[[Event, AsyncSession], None]] = {
    CHECKOUT_COMPLETED: handle_checkout_completed,
    SUBSCRIPTION_DELETED: handle_subscription_deleted,
    SUBSCRIPTION_UPDATED: handle_subscription_updated,
}


async def process_webhook(event: Event, db: AsyncSession) -> dict:
    """Process a Stripe webhook event idempotently.

    Uses Redis for distributed idempotency check across workers.
    Requires db session for user subscription updates.

    Returns:
        dict with status and message
    """
    event_id = event.id

    # Idempotency check using Redis
    if await is_event_processed(event_id):
        logger.info("stripe_event_already_processed", event_id=event_id)
        return {"status": "already_processed", "event_id": event_id}

    handler = HANDLERS.get(event.type)
    if handler is None:
        logger.info("stripe_unhandled_event_type", event_type=event.type)
        return {"status": "unhandled", "event_type": event.type}

    try:
        await handler(event, db)
        logger.info("stripe_event_processed", event_id=event_id, event_type=event.type)
        return {"status": "processed", "event_id": event_id, "event_type": event.type}
    except Exception as e:
        logger.error(
            "stripe_event_processing_failed",
            event_id=event_id,
            event_type=event.type,
            error=str(e),
        )
        raise


def create_checkout_session(
    price_id: str,
    user_id: str,
    success_url: str,
    cancel_url: str,
) -> str:
    """Create a Stripe Checkout session.

    Returns:
        URL to redirect user to for payment
    """
    settings = get_settings()

    session = stripe.checkout.Session.create(
        mode="subscription",
        payment_method_types=["card"],
        line_items=[{"price": price_id, "quantity": 1}],
        success_url=success_url,
        cancel_url=cancel_url,
        client_reference_id=user_id,  # For looking up user after payment
        customer_email=None,  # Will be collected by Stripe
        stripe_version="2024-04-10",
    )

    logger.info(
        "stripe_checkout_created",
        session_id=session.id,
        price_id=price_id,
        user_id=user_id,
    )

    return session.url


def cancel_subscription(subscription_id: str) -> None:
    """Cancel a Stripe subscription."""
    stripe.Subscription.delete(subscription_id)
    logger.info("stripe_subscription_cancelled", subscription_id=subscription_id)

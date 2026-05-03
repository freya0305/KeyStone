"""Stripe webhook endpoint.

CRITICAL: This must be implemented before launch.
Red team finding: Missing webhook = payments not confirmed.

SECURITY: Signature verification is done using raw request body
before JSON parsing, preventing body tampering attacks.
"""
from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from keystone.models.base import get_db
from keystone.services.stripe_service import verify_stripe_signature, process_webhook

router = APIRouter(prefix="/webhooks", tags=["webhooks"])


@router.post("/stripe")
async def stripe_webhook(request: Request, db: AsyncSession = Depends(get_db)):
    """Handle Stripe webhook events.

    Processes:
    - checkout.session.completed
    - customer.subscription.deleted
    - customer.subscription.updated

    Idempotent: same event processed only once (Redis-based).
    """
    try:
        event = await verify_stripe_signature(request)
    except HTTPException:
        raise

    result = await process_webhook(event, db)
    return result

"""Suggestion signals service - gates signal logging on AI_TRAINING consent.

Implements: B2C Training Consent Checkbox § Backend: gate suggestion_signals on consent
"""
import hashlib
import uuid
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from keystone.models.entities import SuggestionSignal, ConsentType, UserConsent
from keystone.services.consent import ConsentService

import structlog

logger = structlog.get_logger()

# Sentinel value for anonymized_user_id when consent is not granted
ANONYMOUS_SENTINEL = "ANONYMOUS"


def _hash_user_id(user_id: uuid.UUID) -> str:
    """Hash user_id for anonymized storage per PDPA."""
    return hashlib.sha256(str(user_id).encode()).hexdigest()[:16]


async def log_signal(
    db: AsyncSession,
    user_id: uuid.UUID,
    suggestion_id: uuid.UUID,
    action: str,
    modified_text: str | None = None,
    context_company_type: str | None = None,
    context_role_level: str | None = None,
    context_industry: str | None = None,
    context_ns_related: bool = False,
) -> SuggestionSignal:
    """Log a suggestion signal, gating on AI_TRAINING consent.

    If user has granted AI_TRAINING consent, the signal is stored with their
    anonymized user ID for product improvement purposes.

    If user has NOT granted AI_TRAINING consent, the signal is stored with
    ANONYMOUS_SENTINEL - no user association is stored.
    """
    consent_service = ConsentService(db)
    has_consent = await consent_service.has_consent(user_id, ConsentType.AI_TRAINING)

    if has_consent:
        # User opted in to AI training - include anonymized user ID
        anonymized_id = _hash_user_id(user_id)
        logger.info(
            "suggestion_signal.logged_with_consent",
            user_id=str(user_id)[:8],
            suggestion_id=str(suggestion_id)[:8],
            action=action,
        )
    else:
        # User did not opt in - log anonymously
        anonymized_id = ANONYMOUS_SENTINEL
        logger.info(
            "suggestion_signal.logged_anonymous",
            suggestion_id=str(suggestion_id)[:8],
            action=action,
        )

    signal = SuggestionSignal(
        anonymized_user_id=anonymized_id,
        suggestion_id=suggestion_id,
        action=action,
        modified_text=modified_text,
        context_company_type=context_company_type,
        context_role_level=context_role_level,
        context_industry=context_industry,
        context_ns_related=context_ns_related,
        created_at=datetime.utcnow(),
    )
    db.add(signal)
    await db.commit()
    await db.refresh(signal)
    return signal


async def get_signals_for_suggestion(
    db: AsyncSession,
    suggestion_id: uuid.UUID,
) -> list[SuggestionSignal]:
    """Get all signals for a suggestion."""
    result = await db.execute(
        select(SuggestionSignal)
        .where(SuggestionSignal.suggestion_id == suggestion_id)
        .order_by(SuggestionSignal.created_at.desc())
    )
    return list(result.scalars().all())


async def get_anonymous_signals_count(db: AsyncSession) -> int:
    """Get count of anonymously logged signals (for analytics)."""
    result = await db.execute(
        select(SuggestionSignal).where(
            SuggestionSignal.anonymized_user_id == ANONYMOUS_SENTINEL
        )
    )
    return len(list(result.scalars().all()))

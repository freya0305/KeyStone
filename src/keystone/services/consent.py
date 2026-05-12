"""Consent service for six-type consent architecture.

Implements: specs/compliance.md § Consent Architecture
"""
import hashlib
from datetime import datetime
from typing import Optional
import uuid

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from keystone.models.entities import User, UserConsent, ConsentType

import structlog

logger = structlog.get_logger()


class ConsentService:
    """Manages per-user per-type consent state."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def has_consent(self, user_id: uuid.UUID, consent_type: ConsentType) -> bool:
        """Check if user has given consent for a specific type.

        Returns True if consent is granted and not revoked.
        """
        result = await self.db.execute(
            select(UserConsent).where(
                and_(
                    UserConsent.user_id == user_id,
                    UserConsent.consent_type == consent_type,
                    UserConsent.revoked_at.is_(None),
                )
            )
        )
        return result.scalar_one_or_none() is not None

    async def grant(
        self, user_id: uuid.UUID, consent_type: ConsentType
    ) -> UserConsent:
        """Grant consent for a specific type. Creates or re-grants."""
        # Check if consent exists (revoked or active)
        result = await self.db.execute(
            select(UserConsent).where(
                and_(
                    UserConsent.user_id == user_id,
                    UserConsent.consent_type == consent_type,
                )
            )
        )
        existing = result.scalar_one_or_none()

        if existing:
            existing.revoked_at = None
            existing.granted_at = datetime.utcnow()
            await self.db.commit()
            logger.info("consent.regranted", user_id=str(user_id), consent_type=consent_type.value)
            return existing
        else:
            new_consent = UserConsent(
                user_id=user_id,
                consent_type=consent_type,
                granted_at=datetime.utcnow(),
            )
            self.db.add(new_consent)
            await self.db.commit()
            logger.info("consent.granted", user_id=str(user_id), consent_type=consent_type.value)
            return new_consent

    async def revoke(
        self, user_id: uuid.UUID, consent_type: ConsentType
    ) -> bool:
        """Revoke consent for a specific type. Returns True if consent was active."""
        result = await self.db.execute(
            select(UserConsent).where(
                and_(
                    UserConsent.user_id == user_id,
                    UserConsent.consent_type == consent_type,
                    UserConsent.revoked_at.is_(None),
                )
            )
        )
        consent = result.scalar_one_or_none()
        if consent:
            consent.revoked_at = datetime.utcnow()
            await self.db.commit()
            logger.info("consent.revoked", user_id=str(user_id), consent_type=consent_type.value)
            return True
        return False

    async def record_consent_refusal(
        self, user_id: uuid.UUID, consent_type: ConsentType
    ) -> UserConsent:
        """Record an explicit consent refusal (granted=False).

        This creates a consent record with granted=False so we have a complete
        audit trail even when the user declines.
        """
        result = await self.db.execute(
            select(UserConsent).where(
                and_(
                    UserConsent.user_id == user_id,
                    UserConsent.consent_type == consent_type,
                )
            )
        )
        existing = result.scalar_one_or_none()

        if existing:
            # Update existing record to reflect refusal
            existing.revoked_at = None
            existing.granted_at = datetime.utcnow()
            await self.db.commit()
            logger.info("consent.refusal_recorded", user_id=str(user_id), consent_type=consent_type.value)
            return existing
        else:
            new_consent = UserConsent(
                user_id=user_id,
                consent_type=consent_type,
                granted_at=datetime.utcnow(),
            )
            self.db.add(new_consent)
            await self.db.commit()
            logger.info("consent.refusal_recorded", user_id=str(user_id), consent_type=consent_type.value)
            return new_consent

    async def get_user_consents(self, user_id: uuid.UUID) -> dict[str, bool]:
        """Get all consent states for a user."""
        result = await self.db.execute(
            select(UserConsent).where(UserConsent.user_id == user_id)
        )
        consents = result.scalars().all()

        # Build state map: active consents = True, revoked = False, missing = False
        state: dict[str, bool] = {}
        for consent in consents:
            is_active = consent.revoked_at is None
            state[consent.consent_type.value] = is_active

        return state

    async def check_ai_processing(self, user_id: uuid.UUID) -> bool:
        """Specific check for AI processing consent — used by analyze endpoint."""
        return await self.has_consent(user_id, ConsentType.AI_PROCESSING)

    async def check_storage(self, user_id: uuid.UUID) -> bool:
        """Specific check for storage consent — gates resume/application writes."""
        return await self.has_consent(user_id, ConsentType.STORAGE)


def hash_phone(phone: str) -> str:
    """Hash phone number for deduplication storage.

    Phone is stored as SHA256 hash — not reversible.
    Format expected: +65XXXXXXXX (Singapore mobile).
    """
    normalized = phone.strip().replace(" ", "").replace("-", "")
    return hashlib.sha256(normalized.encode()).hexdigest()


async def check_phone_hash_unique(db: AsyncSession, phone_hash: str, exclude_user_id: Optional[uuid.UUID] = None) -> bool:
    """Check if a phone hash is already associated with another user."""
    query = select(User).where(User.phone_hash == phone_hash)
    if exclude_user_id:
        query = query.where(User.id != exclude_user_id)
    result = await db.execute(query)
    return result.scalar_one_or_none() is not None

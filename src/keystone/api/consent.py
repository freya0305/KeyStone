"""Consent API for PDPA six-type consent collection.

Endpoints for users to view and manage their consent preferences.
"""
import uuid
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from keystone.models.base import get_db
from keystone.models.entities import ConsentType, UserConsent
from keystone.services.clerk_auth import get_current_user, AuthUser
from keystone.services.consent import ConsentService

router = APIRouter(prefix="/consent", tags=["consent"])


class ConsentStateResponse(BaseModel):
    consent_type: str
    granted: bool
    granted_at: Optional[str] = None
    revoked_at: Optional[str] = None


class ConsentListResponse(BaseModel):
    consents: list[ConsentStateResponse]


class GrantConsentResponse(BaseModel):
    consent_type: str
    granted: bool


class RevokeConsentResponse(BaseModel):
    consent_type: str
    revoked: bool


@router.get("", response_model=ConsentListResponse)
async def list_consents(
    user: AuthUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List all consent states for the current user."""
    if not user.job_seeker_id:
        raise HTTPException(status_code=401, detail="User not found")

    service = ConsentService(db)
    consents = await service.get_user_consents(user.job_seeker_id)

    return ConsentListResponse(
        consents=[
            ConsentStateResponse(
                consent_type=c.consent_type.value,
                granted=c.revoked_at is None,
                granted_at=c.granted_at.isoformat() if c.granted_at else None,
                revoked_at=c.revoked_at.isoformat() if c.revoked_at else None,
            )
            for c in consents
        ]
    )


@router.post("/{consent_type}/grant", response_model=GrantConsentResponse)
async def grant_consent(
    consent_type: str,
    user: AuthUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Grant a specific consent type."""
    if not user.job_seeker_id:
        raise HTTPException(status_code=401, detail="User not found")

    try:
        ct = ConsentType(consent_type)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid consent type: {consent_type}. Valid types: {[e.value for e in ConsentType]}"
        )

    service = ConsentService(db)
    await service.grant(user.job_seeker_id, ct)

    return GrantConsentResponse(consent_type=consent_type, granted=True)


@router.post("/{consent_type}/revoke", response_model=RevokeConsentResponse)
async def revoke_consent(
    consent_type: str,
    user: AuthUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Revoke a specific consent type."""
    if not user.job_seeker_id:
        raise HTTPException(status_code=401, detail="User not found")

    try:
        ct = ConsentType(consent_type)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid consent type: {consent_type}. Valid types: {[e.value for e in ConsentType]}"
        )

    service = ConsentService(db)
    await service.revoke(user.job_seeker_id, ct)

    return RevokeConsentResponse(consent_type=consent_type, revoked=True)

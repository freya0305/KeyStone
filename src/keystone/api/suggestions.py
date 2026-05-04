"""Suggestion Signals API - accept/reject/modify suggestions.

Writes to suggestion_signals table for the learning loop.
Supports anonymous users (anon_session_id) and authenticated users (hashed user_id).
"""
import hashlib
import uuid
from datetime import datetime
from typing import Optional

import structlog
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from keystone.models.base import get_db
from keystone.models.entities import Suggestion, SuggestionSignal, JobAnalysis
from keystone.services.clerk_auth import AuthUser, get_current_user

logger = structlog.get_logger()

router = APIRouter(prefix="/api/suggestions", tags=["suggestions"])


# =============================================================================
# REQUEST/RESPONSE MODELS
# =============================================================================


class SignalContextRequest(BaseModel):
    """Optional context when submitting a signal."""

    company_type: Optional[str] = Field(
        None,
        description="GLC/MNC/SME/STARTUP/GOVERNMENT",
    )
    role_level: Optional[str] = Field(
        None,
        description="ENTRY/MID/SENIOR/MANAGEMENT",
    )
    industry: Optional[str] = Field(
        None,
        description="Industry sector",
    )
    ns_related: bool = Field(
        False,
        description="Whether this suggestion is NS-related (National Service)",
    )


class SuggestionSignalResponse(BaseModel):
    """Response after recording a suggestion signal."""

    signal_id: uuid.UUID
    suggestion_id: uuid.UUID
    action: str
    created_at: datetime


class SuggestionDetailResponse(BaseModel):
    """Suggestion details for reference."""

    id: uuid.UUID
    section: str
    original_text: str
    suggested_text: str
    rationale: Optional[str]
    match_level: Optional[str]


# =============================================================================
# HELPERS
# =============================================================================


def _hash_user_id(user_id: str) -> str:
    """Anonymize user ID for suggestion signals (PDPA compliance).

    Uses SHA256 and takes first 16 chars - enough for uniqueness,
    not enough to identify the user.
    """
    return hashlib.sha256(user_id.encode()).hexdigest()[:16]


async def _get_suggestion_with_context(
    suggestion_id: uuid.UUID,
    db: AsyncSession,
) -> tuple[Suggestion, Optional[JobAnalysis]]:
    """Fetch suggestion and its parent job analysis for context."""

    result = await db.execute(
        select(Suggestion).where(Suggestion.id == suggestion_id)
    )
    suggestion = result.scalar_one_or_none()
    if not suggestion:
        raise HTTPException(status_code=404, detail="Suggestion not found")

    # Get job analysis for context fields
    job_analysis_result = await db.execute(
        select(JobAnalysis).where(JobAnalysis.id == suggestion.job_analysis_id)
    )
    job_analysis = job_analysis_result.scalar_one_or_none()

    return suggestion, job_analysis


def _extract_context_from_job_analysis(
    job_analysis: Optional[JobAnalysis],
    request_context: SignalContextRequest,
) -> dict:
    """Extract context from job analysis, falling back to request context."""

    if job_analysis and job_analysis.job_parsed_json:
        parsed = job_analysis.job_parsed_json
        return {
            "context_company_type": request_context.company_type
            or parsed.get("company_type"),
            "context_role_level": request_context.role_level
            or parsed.get("seniority"),
            "context_industry": request_context.industry
            or parsed.get("industry"),
            "context_ns_related": request_context.ns_related,
        }

    return {
        "context_company_type": request_context.company_type,
        "context_role_level": request_context.role_level,
        "context_industry": request_context.industry,
        "context_ns_related": request_context.ns_related,
    }


async def _record_signal(
    suggestion_id: uuid.UUID,
    action: str,
    modified_text: Optional[str],
    context: dict,
    anonymized_user_id: str,
    db: AsyncSession,
) -> SuggestionSignal:
    """Record a suggestion signal to the database."""

    signal = SuggestionSignal(
        id=uuid.uuid4(),
        anonymized_user_id=anonymized_user_id,
        suggestion_id=suggestion_id,
        action=action,
        modified_text=modified_text,
        context_company_type=context.get("context_company_type"),
        context_role_level=context.get("context_role_level"),
        context_industry=context.get("context_industry"),
        context_ns_related=context.get("context_ns_related", False),
        created_at=datetime.utcnow(),
    )
    db.add(signal)
    await db.commit()
    await db.refresh(signal)

    return signal


# =============================================================================
# ENDPOINTS
# =============================================================================


@router.get("/{suggestion_id}", response_model=SuggestionDetailResponse)
async def get_suggestion(
    suggestion_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    """Get suggestion details by ID.

    Used by the frontend to display suggestion text before acting on it.
    """

    result = await db.execute(
        select(Suggestion).where(Suggestion.id == suggestion_id)
    )
    suggestion = result.scalar_one_or_none()
    if not suggestion:
        raise HTTPException(status_code=404, detail="Suggestion not found")

    return SuggestionDetailResponse(
        id=suggestion.id,
        section=suggestion.section,
        original_text=suggestion.original_text,
        suggested_text=suggestion.suggested_text,
        rationale=suggestion.rationale,
        match_level=suggestion.match_level,
    )


@router.post("/{suggestion_id}/accept", response_model=SuggestionSignalResponse)
async def accept_suggestion(
    suggestion_id: uuid.UUID,
    context: Optional[SignalContextRequest] = None,
    user: Optional[AuthUser] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Accept a suggestion.

    Records ACCEPTED signal to suggestion_signals table.
    User is hashed for PDPA compliance.
    """

    if context is None:
        context = SignalContextRequest()

    suggestion, job_analysis = await _get_suggestion_with_context(suggestion_id, db)

    # Determine user identifier
    if user:
        anonymized_user_id = _hash_user_id(user.id)
    else:
        raise HTTPException(
            status_code=401,
            detail="Authentication required for accepting suggestions",
        )

    # Extract context from job analysis or request
    context_data = _extract_context_from_job_analysis(job_analysis, context)

    # Record the signal
    signal = await _record_signal(
        suggestion_id=suggestion_id,
        action="ACCEPTED",
        modified_text=None,
        context=context_data,
        anonymized_user_id=anonymized_user_id,
        db=db,
    )

    logger.info(
        "suggestion.accepted",
        signal_id=str(signal.id),
        suggestion_id=str(suggestion_id),
        anonymized_user_id=anonymized_user_id,
        context_company_type=context_data.get("context_company_type"),
        context_role_level=context_data.get("context_role_level"),
        context_industry=context_data.get("context_industry"),
        context_ns_related=context_data.get("context_ns_related"),
    )

    return SuggestionSignalResponse(
        signal_id=signal.id,
        suggestion_id=signal.suggestion_id,
        action=signal.action,
        created_at=signal.created_at,
    )


@router.post("/{suggestion_id}/reject", response_model=SuggestionSignalResponse)
async def reject_suggestion(
    suggestion_id: uuid.UUID,
    context: Optional[SignalContextRequest] = None,
    user: Optional[AuthUser] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Reject a suggestion.

    Records REJECTED signal to suggestion_signals table.
    User is hashed for PDPA compliance.
    """

    if context is None:
        context = SignalContextRequest()

    suggestion, job_analysis = await _get_suggestion_with_context(suggestion_id, db)

    # Determine user identifier
    if user:
        anonymized_user_id = _hash_user_id(user.id)
    else:
        raise HTTPException(
            status_code=401,
            detail="Authentication required for rejecting suggestions",
        )

    # Extract context from job analysis or request
    context_data = _extract_context_from_job_analysis(job_analysis, context)

    # Record the signal
    signal = await _record_signal(
        suggestion_id=suggestion_id,
        action="REJECTED",
        modified_text=None,
        context=context_data,
        anonymized_user_id=anonymized_user_id,
        db=db,
    )

    logger.info(
        "suggestion.rejected",
        signal_id=str(signal.id),
        suggestion_id=str(suggestion_id),
        anonymized_user_id=anonymized_user_id,
        context_company_type=context_data.get("context_company_type"),
        context_role_level=context_data.get("context_role_level"),
        context_industry=context_data.get("context_industry"),
        context_ns_related=context_data.get("context_ns_related"),
    )

    return SuggestionSignalResponse(
        signal_id=signal.id,
        suggestion_id=signal.suggestion_id,
        action=signal.action,
        created_at=signal.created_at,
    )


class ModifyRequest(BaseModel):
    """Request body for modifying a suggestion."""

    modified_text: str = Field(
        ...,
        min_length=1,
        description="The user's edited version of the suggestion text",
    )


@router.post("/{suggestion_id}/modify", response_model=SuggestionSignalResponse)
async def modify_suggestion(
    suggestion_id: uuid.UUID,
    request: ModifyRequest,
    context: Optional[SignalContextRequest] = None,
    user: Optional[AuthUser] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Modify a suggestion with user-edited text.

    Records MODIFIED signal to suggestion_signals table with the user's
    edited text. User is hashed for PDPA compliance.
    """

    if context is None:
        context = SignalContextRequest()

    suggestion, job_analysis = await _get_suggestion_with_context(suggestion_id, db)

    # Determine user identifier
    if user:
        anonymized_user_id = _hash_user_id(user.id)
    else:
        raise HTTPException(
            status_code=401,
            detail="Authentication required for modifying suggestions",
        )

    # Extract context from job analysis or request
    context_data = _extract_context_from_job_analysis(job_analysis, context)

    # Record the signal
    signal = await _record_signal(
        suggestion_id=suggestion_id,
        action="MODIFIED",
        modified_text=request.modified_text,
        context=context_data,
        anonymized_user_id=anonymized_user_id,
        db=db,
    )

    logger.info(
        "suggestion.modified",
        signal_id=str(signal.id),
        suggestion_id=str(suggestion_id),
        anonymized_user_id=anonymized_user_id,
        modified_text_length=len(request.modified_text),
        context_company_type=context_data.get("context_company_type"),
        context_role_level=context_data.get("context_role_level"),
        context_industry=context_data.get("context_industry"),
        context_ns_related=context_data.get("context_ns_related"),
    )

    return SuggestionSignalResponse(
        signal_id=signal.id,
        suggestion_id=signal.suggestion_id,
        action=signal.action,
        created_at=signal.created_at,
    )
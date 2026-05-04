"""JD Generation API for recruiters.

Simplified: Only JD generation and version history.
Share links and ranking removed based on user feedback.
"""
import uuid
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from keystone.models.base import get_db
from keystone.models.entities import (
    B2BJobDescription,
    B2BVersion,
    B2BUser,
)
from keystone.core import get_settings
from keystone.services.claude_client import get_claude_client, ClaudeResponse
from keystone.services.circuit_breaker import CircuitBreakerError
from keystone.services.clerk_auth import get_current_user, get_current_b2b_user, AuthUser

router = APIRouter(prefix="/recruiter/jd", tags=["recruiter"])


# =============================================================================
# REQUEST/RESPONSE MODELS
# =============================================================================


class JDGenerateRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    company: str = Field(..., min_length=1, max_length=255)
    company_type: Optional[str] = Field(None, pattern="^(banking|fintech|startup|mnc|other)$")
    skills: list[str] = Field(..., min_length=1, max_length=20)
    seniority: str = Field(..., pattern="^(junior|mid|senior|lead)$")
    template_id: Optional[uuid.UUID] = None


class JDGenerateResponse(BaseModel):
    id: uuid.UUID
    title: str
    company: str
    content: str
    word_count: int
    generated_at: datetime


class VersionResponse(BaseModel):
    id: uuid.UUID
    version_number: int
    content: str
    created_at: datetime


# =============================================================================
# SYSTEM PROMPT FOR JD GENERATION
# =============================================================================

JD_GENERATION_SYSTEM_PROMPT = """You are an expert job description writer specializing in Singapore recruitment.

Generate professional, compelling job descriptions that:
1. Are 300-600 words
2. Use clear section headers (Overview, Responsibilities, Requirements, Nice to Have)
3. Incorporate skills contextually (not just a bullet list)
4. Use gender-neutral language
5. Include Singapore-specific context where relevant (MOM guidelines, local qualifications)

Output ONLY the job description content. No preamble or explanation."""


# =============================================================================
# JD GENERATION
# =============================================================================


@router.post("/generate", response_model=JDGenerateResponse)
async def generate_jd(
    request: JDGenerateRequest,
    user: AuthUser = Depends(get_current_b2b_user),
    db: AsyncSession = Depends(get_db),
):
    """Generate a job description using Claude Haiku."""
    client = get_claude_client()
    settings = get_settings()

    # Build user prompt
    skills_str = ", ".join(request.skills)
    user_prompt = f"""Write a job description for:
- Title: {request.title}
- Company: {request.company}
- Company Type: {request.company_type or 'Other'}
- Required Skills: {skills_str}
- Seniority: {request.seniority}

Format with these sections: Overview, Responsibilities, Requirements, Nice to Have"""

    try:
        response: ClaudeResponse = await client.generate(
            model=settings.anthropic_model_haiku,
            system_prompt=JD_GENERATION_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            max_tokens=4096,
        )
    except CircuitBreakerError as e:
        raise HTTPException(status_code=503, detail=f"AI service temporarily unavailable: {e}")

    # Save to database (tenant_id from authenticated B2B user)
    jd = B2BJobDescription(
        id=uuid.uuid4(),
        tenant_id=user.tenant_id,
        created_by_id=user.b2b_user_id,
        title=request.title,
        company=request.company,
        company_type=request.company_type,
        skills_json=request.skills,
        seniority=request.seniority,
        content=response.content,
        brand_template_id=request.template_id,
    )
    db.add(jd)
    await db.commit()
    await db.refresh(jd)

    return JDGenerateResponse(
        id=jd.id,
        title=jd.title,
        company=jd.company,
        content=jd.content,
        word_count=len(response.content.split()),
        generated_at=jd.created_at,
    )


# =============================================================================
# VERSION HISTORY
# =============================================================================


@router.post("/{jd_id}/versions", response_model=VersionResponse)
async def save_version(
    jd_id: uuid.UUID,
    user: AuthUser = Depends(get_current_b2b_user),
    db: AsyncSession = Depends(get_db),
):
    """Save current JD content as a new version."""
    result = await db.execute(
        select(B2BJobDescription).where(B2BJobDescription.id == jd_id)
    )
    jd = result.scalar_one_or_none()
    if not jd:
        raise HTTPException(status_code=404, detail="Job description not found")

    if jd.tenant_id != user.tenant_id:
        raise HTTPException(status_code=403, detail="Access denied to this job description")

    # Get next version number
    version_result = await db.execute(
        select(B2BVersion)
        .where(B2BVersion.jd_id == jd_id)
        .order_by(B2BVersion.version_number.desc())
        .limit(1)
    )
    latest_version = version_result.scalar_one_or_none()
    next_version = (latest_version.version_number + 1) if latest_version else 1

    version = B2BVersion(
        id=uuid.uuid4(),
        jd_id=jd_id,
        content=jd.content,
        version_number=next_version,
    )
    db.add(version)
    await db.commit()
    await db.refresh(version)

    return VersionResponse(
        id=version.id,
        version_number=version.version_number,
        content=version.content,
        created_at=version.created_at,
    )


@router.get("/{jd_id}/versions")
async def list_versions(
    jd_id: uuid.UUID,
    user: AuthUser = Depends(get_current_b2b_user),
    db: AsyncSession = Depends(get_db),
):
    """List all versions for a job description."""
    jd_result = await db.execute(
        select(B2BJobDescription).where(B2BJobDescription.id == jd_id)
    )
    jd = jd_result.scalar_one_or_none()
    if not jd:
        raise HTTPException(status_code=404, detail="Job description not found")

    if jd.tenant_id != user.tenant_id:
        raise HTTPException(status_code=403, detail="Access denied to this job description")

    result = await db.execute(
        select(B2BVersion)
        .where(B2BVersion.jd_id == jd_id)
        .order_by(B2BVersion.version_number.desc())
    )
    versions = result.scalars().all()

    return [
        VersionResponse(
            id=v.id,
            version_number=v.version_number,
            content=v.content,
            created_at=v.created_at,
        )
        for v in versions
    ]


@router.post("/{jd_id}/restore/{version_id}")
async def restore_version(
    jd_id: uuid.UUID,
    version_id: uuid.UUID,
    user: AuthUser = Depends(get_current_b2b_user),
    db: AsyncSession = Depends(get_db),
):
    """Restore JD content from a previous version."""
    result = await db.execute(
        select(B2BVersion).where(
            B2BVersion.id == version_id,
            B2BVersion.jd_id == jd_id,
        )
    )
    version = result.scalar_one_or_none()
    if not version:
        raise HTTPException(status_code=404, detail="Version not found")

    jd_result = await db.execute(
        select(B2BJobDescription).where(B2BJobDescription.id == jd_id)
    )
    jd = jd_result.scalar_one_or_none()
    if not jd:
        raise HTTPException(status_code=404, detail="Job description not found")

    if jd.tenant_id != user.tenant_id:
        raise HTTPException(status_code=403, detail="Access denied to this job description")

    # Save current as a version first
    await save_version(jd_id, user, db)

    jd.content = version.content
    await db.commit()

    return {"status": "restored", "version_number": version.version_number}

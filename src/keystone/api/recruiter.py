"""Recruiter endpoints: share links, templates, ratings.

Covers:
- KY2.2: Share links (public JD viewing)
- KY2.3: Brand templates CRUD
- KY2.5: JD quality rating
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
    B2BJobDescription,
    B2BShareLink,
    B2BTemplate,
    B2BUser,
)
from keystone.services.clerk_auth import get_current_user, get_current_b2b_user, AuthUser

router = APIRouter(prefix="/recruiter", tags=["recruiter"])


# =============================================================================
# REQUEST/RESPONSE MODELS
# =============================================================================


class ShareLinkResponse(BaseModel):
    url: str
    token: str
    expires_at: datetime


class ShareLinkViewResponse(BaseModel):
    id: uuid.UUID
    title: str
    company: str
    content: str
    created_at: datetime


class TemplateCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    logo_s3_key: Optional[str] = None
    brand_primary_color: str = Field(default="#4F46E5", pattern="^#[0-9A-Fa-f]{6}$")
    brand_secondary_color: str = Field(default="#6B7280", pattern="^#[0-9A-Fa-f]{6}$")
    font_choice: str = Field(default="Inter", max_length=50)


class TemplateUpdateRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    logo_s3_key: Optional[str] = None
    brand_primary_color: Optional[str] = Field(None, pattern="^#[0-9A-Fa-f]{6}$")
    brand_secondary_color: Optional[str] = Field(None, pattern="^#[0-9A-Fa-f]{6}$")
    font_choice: Optional[str] = Field(None, max_length=50)


class TemplateResponse(BaseModel):
    id: uuid.UUID
    name: str
    logo_s3_key: Optional[str]
    brand_primary_color: str
    brand_secondary_color: str
    font_choice: str
    created_at: datetime


class RatingRequest(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    feedback: Optional[str] = Field(None, max_length=2000)


class RatingResponse(BaseModel):
    id: uuid.UUID
    rating: int
    feedback: Optional[str]
    created_at: datetime


# =============================================================================
# CONSTANTS
# =============================================================================

SHARE_LINK_EXPIRY_DAYS = 7
SHARE_TOKEN_LENGTH = 32


# =============================================================================
# SHARE LINKS (PUBLIC - NO AUTH REQUIRED)
# =============================================================================


@router.post("/jd/{jd_id}/share", response_model=ShareLinkResponse)
async def create_share_link(
    jd_id: uuid.UUID,
    user: AuthUser = Depends(get_current_b2b_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a shareable link for a job description (7-day expiry)."""
    result = await db.execute(
        select(B2BJobDescription).where(B2BJobDescription.id == jd_id)
    )
    jd = result.scalar_one_or_none()
    if not jd:
        raise HTTPException(status_code=404, detail="Job description not found")

    if jd.tenant_id != user.tenant_id:
        raise HTTPException(status_code=403, detail="Access denied")

    # Generate unique token
    token = secrets.token_urlsafe(SHARE_TOKEN_LENGTH)
    expires_at = datetime.utcnow() + timedelta(days=SHARE_LINK_EXPIRY_DAYS)

    share_link = B2BShareLink(
        id=uuid.uuid4(),
        jd_id=jd_id,
        token=token,
        expires_at=expires_at,
    )
    db.add(share_link)
    await db.commit()

    from keystone.core import get_settings
    settings = get_settings()
    base_url = getattr(settings, "app_base_url", "http://localhost:3000")
    url = f"{base_url}/share/{token}"

    return ShareLinkResponse(url=url, token=token, expires_at=expires_at)


@router.get("/share/{token}", response_model=ShareLinkViewResponse)
async def view_shared_jd(
    token: str,
    db: AsyncSession = Depends(get_db),
):
    """View a shared job description (public, no auth required)."""
    result = await db.execute(
        select(B2BShareLink).where(B2BShareLink.token == token)
    )
    share_link = result.scalar_one_or_none()

    if not share_link:
        raise HTTPException(status_code=404, detail="Share link not found")

    if share_link.expires_at < datetime.utcnow():
        raise HTTPException(status_code=410, detail="Share link has expired")

    # Increment view count
    share_link.view_count += 1
    await db.commit()

    # Get JD content
    jd_result = await db.execute(
        select(B2BJobDescription).where(B2BJobDescription.id == share_link.jd_id)
    )
    jd = jd_result.scalar_one_or_none()
    if not jd:
        raise HTTPException(status_code=404, detail="Job description not found")

    return ShareLinkViewResponse(
        id=jd.id,
        title=jd.title,
        company=jd.company,
        content=jd.content,
        created_at=jd.created_at,
    )


# =============================================================================
# BRAND TEMPLATES CRUD
# =============================================================================


@router.post("/templates", response_model=TemplateResponse)
async def create_template(
    request: TemplateCreateRequest,
    user: AuthUser = Depends(get_current_b2b_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a new brand template for job descriptions."""
    template = B2BTemplate(
        id=uuid.uuid4(),
        tenant_id=user.tenant_id,
        name=request.name,
        logo_s3_key=request.logo_s3_key,
        brand_primary_color=request.brand_primary_color,
        brand_secondary_color=request.brand_secondary_color,
        font_choice=request.font_choice,
    )
    db.add(template)
    await db.commit()
    await db.refresh(template)

    return TemplateResponse(
        id=template.id,
        name=template.name,
        logo_s3_key=template.logo_s3_key,
        brand_primary_color=template.brand_primary_color,
        brand_secondary_color=template.brand_secondary_color,
        font_choice=template.font_choice,
        created_at=template.created_at,
    )


@router.get("/templates")
async def list_templates(
    user: AuthUser = Depends(get_current_b2b_user),
    db: AsyncSession = Depends(get_db),
):
    """List all brand templates for the current tenant."""
    result = await db.execute(
        select(B2BTemplate)
        .where(B2BTemplate.tenant_id == user.tenant_id)
        .order_by(B2BTemplate.created_at.desc())
    )
    templates = result.scalars().all()

    return [
        TemplateResponse(
            id=t.id,
            name=t.name,
            logo_s3_key=t.logo_s3_key,
            brand_primary_color=t.brand_primary_color,
            brand_secondary_color=t.brand_secondary_color,
            font_choice=t.font_choice,
            created_at=t.created_at,
        )
        for t in templates
    ]


@router.put("/templates/{template_id}", response_model=TemplateResponse)
async def update_template(
    template_id: uuid.UUID,
    request: TemplateUpdateRequest,
    user: AuthUser = Depends(get_current_b2b_user),
    db: AsyncSession = Depends(get_db),
):
    """Update a brand template."""
    result = await db.execute(
        select(B2BTemplate).where(
            B2BTemplate.id == template_id,
            B2BTemplate.tenant_id == user.tenant_id,
        )
    )
    template = result.scalar_one_or_none()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")

    if request.name is not None:
        template.name = request.name
    if request.logo_s3_key is not None:
        template.logo_s3_key = request.logo_s3_key
    if request.brand_primary_color is not None:
        template.brand_primary_color = request.brand_primary_color
    if request.brand_secondary_color is not None:
        template.brand_secondary_color = request.brand_secondary_color
    if request.font_choice is not None:
        template.font_choice = request.font_choice

    await db.commit()
    await db.refresh(template)

    return TemplateResponse(
        id=template.id,
        name=template.name,
        logo_s3_key=template.logo_s3_key,
        brand_primary_color=template.brand_primary_color,
        brand_secondary_color=template.brand_secondary_color,
        font_choice=template.font_choice,
        created_at=template.created_at,
    )


@router.delete("/templates/{template_id}")
async def delete_template(
    template_id: uuid.UUID,
    user: AuthUser = Depends(get_current_b2b_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete a brand template."""
    result = await db.execute(
        select(B2BTemplate).where(
            B2BTemplate.id == template_id,
            B2BTemplate.tenant_id == user.tenant_id,
        )
    )
    template = result.scalar_one_or_none()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")

    await db.delete(template)
    await db.commit()

    return {"status": "deleted"}


# =============================================================================
# JD QUALITY RATING
# =============================================================================


@router.post("/jd/{jd_id}/rate", response_model=RatingResponse)
async def rate_jd(
    jd_id: uuid.UUID,
    request: RatingRequest,
    user: AuthUser = Depends(get_current_b2b_user),
    db: AsyncSession = Depends(get_db),
):
    """Rate a job description and provide optional feedback."""
    result = await db.execute(
        select(B2BJobDescription).where(
            B2BJobDescription.id == jd_id,
            B2BJobDescription.tenant_id == user.tenant_id,
        )
    )
    jd = result.scalar_one_or_none()
    if not jd:
        raise HTTPException(status_code=404, detail="Job description not found")

    jd.rating = request.rating
    jd.rating_feedback = request.feedback
    await db.commit()
    await db.refresh(jd)

    return RatingResponse(
        id=jd.id,
        rating=jd.rating,
        feedback=jd.rating_feedback,
        created_at=jd.created_at,
    )


@router.get("/jd/{jd_id}/rate")
async def get_jd_rating(
    jd_id: uuid.UUID,
    user: AuthUser = Depends(get_current_b2b_user),
    db: AsyncSession = Depends(get_db),
):
    """Get rating for a job description."""
    result = await db.execute(
        select(B2BJobDescription).where(
            B2BJobDescription.id == jd_id,
            B2BJobDescription.tenant_id == user.tenant_id,
        )
    )
    jd = result.scalar_one_or_none()
    if not jd:
        raise HTTPException(status_code=404, detail="Job description not found")

    if jd.rating is None:
        raise HTTPException(status_code=404, detail="No rating yet")

    return RatingResponse(
        id=jd.id,
        rating=jd.rating,
        feedback=jd.rating_feedback,
        created_at=jd.created_at,
    )


@router.get("/analytics/ratings")
async def get_ratings_analytics(
    user: AuthUser = Depends(get_current_b2b_user),
    db: AsyncSession = Depends(get_db),
):
    """Get aggregate rating analytics for the tenant."""
    result = await db.execute(
        select(B2BJobDescription).where(
            B2BJobDescription.tenant_id == user.tenant_id,
            B2BJobDescription.rating.isnot(None),
        )
    )
    jds = result.scalars().all()

    if not jds:
        return {
            "total_rated": 0,
            "average_rating": None,
            "rating_distribution": {},
        }

    ratings = [jd.rating for jd in jds]
    avg = sum(ratings) / len(ratings)
    dist = {str(i): ratings.count(i) for i in range(1, 6)}

    return {
        "total_rated": len(ratings),
        "average_rating": round(avg, 2),
        "rating_distribution": dist,
    }

"""JD Generation API for recruiters.

Supports skill-frequency-based JD generation with cold-start fallback.
Share links and ranking removed based on user feedback.
"""
import uuid
import logging
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_

from keystone.models.base import get_db
from keystone.models.entities import (
    B2BJobDescription,
    B2BVersion,
    RoleSkillFrequency,
    JDGenerationLog,
)
from keystone.core import get_settings
from keystone.services.claude_client import get_claude_client, ClaudeResponse
from keystone.services.circuit_breaker import CircuitBreakerError
from keystone.services.rate_limit import check_rate_limit
from keystone.services.clerk_auth import get_current_b2b_user, AuthUser

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/recruiter", tags=["recruiter"])

# =============================================================================
# REQUEST/RESPONSE MODELS
# =============================================================================


class SkillsLookupRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    industry: str = Field(..., pattern="^(fintech|technology|banking_finance|consulting|government_public|healthcare|retail_consumer|engineering|education|other)$")
    seniority: str = Field(..., pattern="^(junior|mid|senior|lead)$")
    company_type: Optional[str] = Field(None, pattern="^(glc|statutory_board|mnc|startup|banking|fintech|sme|other)$")


class SkillItem(BaseModel):
    skill: str
    weighted_freq: float
    required_count: int
    preferred_count: int
    total_jds: int


class SkillsLookupResponse(BaseModel):
    skills: list[SkillItem]
    total_jds_analyzed: int
    cold_start_warning: Optional[str] = None
    prompt_for_manual_input: bool = False
    min_required_skills: int = 5


class JDGenerateRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    company: str = Field(..., min_length=1, max_length=255)
    industry: str = Field(..., min_length=1, max_length=255)
    company_type: Optional[str] = Field(None, pattern="^(banking|fintech|startup|mnc|other)$")
    skills: Optional[list[str]] = Field(None, max_length=20)
    seniority: str = Field(..., pattern="^(junior|mid|senior|lead)$")
    use_skill_frequency: bool = Field(True, description="Query skill_frequency DB if no explicit skills provided")
    template_id: Optional[uuid.UUID] = None


class JDGenerateResponse(BaseModel):
    id: uuid.UUID
    title: str
    company: str
    content: str
    word_count: int
    generated_at: datetime
    generation_source: str
    skills_used: list[str]


class VersionResponse(BaseModel):
    id: uuid.UUID
    version_number: int
    content: str
    created_at: datetime


# =============================================================================
# CONSTANTS
# =============================================================================

# Cold start thresholds per architecture spec §4
COLD_START_WARNING_THRESHOLD = 30
MANUAL_INPUT_THRESHOLD = 5
MAX_SKILLS_RETURNED = 15

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
# SKILL LOOKUP LOGIC
# =============================================================================

async def query_skill_frequency(
    db: AsyncSession,
    title: str,
    industry: str,
    seniority: str,
    company_type: Optional[str] = None,
) -> tuple[list[SkillItem], int, bool, bool]:
    """Query skill_frequency DB with cold-start fallback.

    Returns:
        (skills, total_jds, cold_start_warning, prompt_for_manual_input)
    """
    # Normalize title for lookup
    from keystone.services.skill_normalizer import normalize_title
    normalized_title = normalize_title(title)

    # Try exact match first
    query = select(RoleSkillFrequency).where(
        and_(
            RoleSkillFrequency.title_normalized == normalized_title,
            RoleSkillFrequency.industry == industry,
            RoleSkillFrequency.seniority == seniority,
        )
    )
    if company_type:
        query = query.where(
            or_(
                RoleSkillFrequency.company_type == company_type,
                RoleSkillFrequency.company_type == "ANY",
            )
        )
    else:
        query = query.where(RoleSkillFrequency.company_type == "ANY")

    result = await db.execute(query)
    skill_freq_record = result.scalar_one_or_none()

    # Cold start fallback per architecture spec §4
    total_jds = 0
    skills: list[SkillItem] = []
    cold_start_warning: Optional[str] = None
    prompt_for_manual_input = False

    if skill_freq_record:
        skills_data = skill_freq_record.skills_json or []
        total_jds = skill_freq_record.total_jds_analyzed

        # Take top 15 skills by weighted frequency
        sorted_skills = sorted(
            skills_data,
            key=lambda x: x.get("raw_weighted_freq", 0),
            reverse=True
        )[:MAX_SKILLS_RETURNED]

        skills = [
            SkillItem(
                skill=s.get("skill", ""),
                weighted_freq=s.get("raw_weighted_freq", 0.0),
                required_count=s.get("required_count", 0),
                preferred_count=s.get("preferred_count", 0),
                total_jds=s.get("total_jds", total_jds),
            )
            for s in sorted_skills
        ]

    # Apply cold start thresholds per §4
    if total_jds > 0 and total_jds < MANUAL_INPUT_THRESHOLD:
        prompt_for_manual_input = True
        cold_start_warning = f"Only {total_jds} JDs found for this role. Please provide 3-5 required skills manually."
    elif total_jds > 0 and total_jds < COLD_START_WARNING_THRESHOLD:
        cold_start_warning = f"Based on {total_jds} JDs — results may vary. Consider providing additional skills."

    # If no exact match, try broadening
    if not skill_freq_record:
        # Try with "other" industry baseline (tech skills apply across industries)
        if industry != "other":
            query = select(RoleSkillFrequency).where(
                and_(
                    RoleSkillFrequency.title_normalized == normalized_title,
                    RoleSkillFrequency.industry == "other",
                    RoleSkillFrequency.seniority == seniority,
                )
            )
            if company_type:
                query = query.where(
                    or_(
                        RoleSkillFrequency.company_type == company_type,
                        RoleSkillFrequency.company_type == "ANY",
                    )
                )
            else:
                query = query.where(RoleSkillFrequency.company_type == "ANY")

            result = await db.execute(query)
            skill_freq_record = result.scalar_one_or_none()

            if skill_freq_record:
                skills_data = skill_freq_record.skills_json or []
                total_jds = skill_freq_record.total_jds_analyzed

                sorted_skills = sorted(
                    skills_data,
                    key=lambda x: x.get("raw_weighted_freq", 0),
                    reverse=True
                )[:MAX_SKILLS_RETURNED]

                skills = [
                    SkillItem(
                        skill=s.get("skill", ""),
                        weighted_freq=s.get("raw_weighted_freq", 0.0),
                        required_count=s.get("required_count", 0),
                        preferred_count=s.get("preferred_count", 0),
                        total_jds=s.get("total_jds", total_jds),
                    )
                    for s in sorted_skills
                ]

                if total_jds < MANUAL_INPUT_THRESHOLD:
                    prompt_for_manual_input = True
                    cold_start_warning = f"Only {total_jds} JDs found with broader criteria. Please provide 3-5 required skills manually."
                elif total_jds < COLD_START_WARNING_THRESHOLD:
                    cold_start_warning = f"Based on {total_jds} JDs — results may vary."

    return skills, total_jds, cold_start_warning, prompt_for_manual_input


# =============================================================================
# SKILL LOOKUP ENDPOINT
# =============================================================================

@router.get("/skills/lookup", response_model=SkillsLookupResponse)
async def lookup_skills(
    title: str = Query(..., min_length=1, max_length=255),
    industry: str = Query(..., pattern="^(fintech|technology|banking_finance|consulting|government_public|healthcare|retail_consumer|engineering|education|other)$"),
    seniority: str = Query(..., pattern="^(junior|mid|senior|lead)$"),
    company_type: Optional[str] = Query(None, pattern="^(glc|statutory_board|mnc|startup|banking|fintech|sme|other)$"),
    user: AuthUser = Depends(get_current_b2b_user),
    db: AsyncSession = Depends(get_db),
):
    """Look up top skills for a role from the skill_frequency DB.

    Returns top 15 skills with weighted frequency, plus cold-start warnings
    if insufficient data.
    """
    # Rate limit by user subscription tier
    tier_key = user.subscription_tier or "free"
    check_rate_limit(str(user.b2b_user_id), tier_key)

    logger.info(
        "skills_lookup.start",
        title=title,
        industry=industry,
        seniority=seniority,
        company_type=company_type,
        user_id=str(user.user_id),
    )

    skills, total_jds, cold_start_warning, prompt_for_manual_input = await query_skill_frequency(
        db, title, industry, seniority, company_type
    )

    logger.info(
        "skills_lookup.complete",
        title=title,
        total_skills=len(skills),
        total_jds=total_jds,
        cold_start_warning=cold_start_warning,
        prompt_for_manual_input=prompt_for_manual_input,
    )

    return SkillsLookupResponse(
        skills=skills,
        total_jds_analyzed=total_jds,
        cold_start_warning=cold_start_warning,
        prompt_for_manual_input=prompt_for_manual_input,
        min_required_skills=MANUAL_INPUT_THRESHOLD,
    )


# =============================================================================
# JD GENERATION
# =============================================================================

@router.post("/jd/generate", response_model=JDGenerateResponse)
async def generate_jd(
    request: JDGenerateRequest,
    user: AuthUser = Depends(get_current_b2b_user),
    db: AsyncSession = Depends(get_db),
):
    """Generate a job description using Claude Haiku.

    If use_skill_frequency=True and no explicit skills provided,
    queries skill_frequency DB for top skills.
    """
    # Rate limit JD generation (AI API calls are expensive)
    check_rate_limit(str(user.b2b_user_id), "jd_generate")

    client = get_claude_client()
    settings = get_settings()

    skills_to_use: list[str]
    generation_source: str
    skills_from_frequency_data: Optional[list[str]] = None

    # Determine skills source
    if request.skills and len(request.skills) > 0:
        # User provided explicit skills
        skills_to_use = request.skills
        generation_source = "user_provided"
        logger.info(
            "jd_generate.skills_source",
            source="user_provided",
            skill_count=len(skills_to_use),
        )
    elif request.use_skill_frequency:
        # Query skill_frequency DB
        from keystone.services.skill_normalizer import normalize_title
        normalized_title = normalize_title(request.title)

        # Use company_type mapping for query
        db_company_type = None
        if request.company_type:
            company_type_map = {
                "banking": "banking",
                "fintech": "fintech",
                "startup": "startup",
                "mnc": "mnc",
                "other": "other",
            }
            db_company_type = company_type_map.get(request.company_type)

        # Map frontend industry free-text to DB slug
        industry_map = {
            "Finance & Accounting": "banking_finance",
            "Technology & Software": "technology",
            "Healthcare & Medical": "healthcare",
            "Engineering & Manufacturing": "engineering",
            "Marketing & Communications": "other",
            "Sales & Business Development": "other",
            "Human Resources": "other",
            "Operations & Logistics": "other",
            "Legal & Compliance": "other",
            "Education & Training": "education",
            "Consulting": "consulting",
            "Other": "other",
        }
        db_industry = industry_map.get(request.industry, "other")

        skills, total_jds, cold_start_warning, prompt_for_manual_input = await query_skill_frequency(
            db,
            request.title,
            db_industry,
            request.seniority,
            db_company_type,
        )

        if skills and len(skills) > 0:
            skills_to_use = [s.skill for s in skills]
            skills_from_frequency_data = skills_to_use.copy()
            generation_source = "skill_frequency"
            logger.info(
                "jd_generate.skills_source",
                source="skill_frequency",
                skill_count=len(skills_to_use),
                total_jds=total_jds,
                cold_start_warning=cold_start_warning,
            )
        else:
            # No skills found, use fallback prompt
            skills_to_use = []
            generation_source = "fallback_prompt"
            logger.warning(
                "jd_generate.skills_source",
                source="fallback_prompt",
                reason="no_skills_found",
            )
    else:
        # use_skill_frequency=False and no explicit skills
        skills_to_use = []
        generation_source = "fallback_prompt"
        logger.info(
            "jd_generate.skills_source",
            source="fallback_prompt",
            reason="use_skill_frequency_disabled",
        )

    # Build user prompt
    if skills_to_use:
        skills_str = ", ".join(skills_to_use)
        user_prompt = f"""Write a job description for:
- Title: {request.title}
- Company: {request.company}
- Company Type: {request.company_type or 'Other'}
- Required Skills: {skills_str}
- Seniority: {request.seniority}

Format with these sections: Overview, Responsibilities, Requirements, Nice to Have"""
    else:
        user_prompt = f"""Write a job description for:
- Title: {request.title}
- Company: {request.company}
- Company Type: {request.company_type or 'Other'}
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

    # Save JD to database
    jd = B2BJobDescription(
        id=uuid.uuid4(),
        tenant_id=user.tenant_id,
        created_by_id=user.b2b_user_id,
        title=request.title,
        company=request.company,
        company_type=request.company_type,
        skills_json=skills_to_use,
        seniority=request.seniority,
        content=response.content,
        brand_template_id=request.template_id,
    )
    db.add(jd)

    # Log generation
    generation_log = JDGenerationLog(
        id=uuid.uuid4(),
        input_title=request.title,
        input_industry=request.industry,
        input_seniority=request.seniority,
        input_company_type=request.company_type,
        input_skills_user=request.skills,
        skills_from_frequency=skills_from_frequency_data,
        generation_source=generation_source,
    )
    db.add(generation_log)

    await db.commit()
    await db.refresh(jd)

    logger.info(
        "jd_generate.complete",
        jd_id=str(jd.id),
        generation_source=generation_source,
        skill_count=len(skills_to_use),
    )

    return JDGenerateResponse(
        id=jd.id,
        title=jd.title,
        company=jd.company,
        content=jd.content,
        word_count=len(response.content.split()),
        generated_at=jd.created_at,
        generation_source=generation_source,
        skills_used=skills_to_use,
    )


# =============================================================================
# VERSION HISTORY
# =============================================================================


@router.post("/jd/{jd_id}/versions", response_model=VersionResponse)
async def save_version(
    jd_id: uuid.UUID,
    user: AuthUser = Depends(get_current_b2b_user),
    db: AsyncSession = Depends(get_db),
):
    """Save current JD content as a new version."""
    # Rate limit by user subscription tier
    tier_key = user.subscription_tier or "free"
    check_rate_limit(str(user.b2b_user_id), tier_key)

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


@router.get("/jd/{jd_id}/versions")
async def list_versions(
    jd_id: uuid.UUID,
    user: AuthUser = Depends(get_current_b2b_user),
    db: AsyncSession = Depends(get_db),
):
    """List all versions for a job description."""
    # Rate limit by user subscription tier
    tier_key = user.subscription_tier or "free"
    check_rate_limit(str(user.b2b_user_id), tier_key)

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


@router.post("/jd/{jd_id}/restore/{version_id}")
async def restore_version(
    jd_id: uuid.UUID,
    version_id: uuid.UUID,
    user: AuthUser = Depends(get_current_b2b_user),
    db: AsyncSession = Depends(get_db),
):
    """Restore JD content from a previous version."""
    # Rate limit by user subscription tier
    tier_key = user.subscription_tier or "free"
    check_rate_limit(str(user.b2b_user_id), tier_key)

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

"""Job Seeker API - B2C resume optimization and application tracking.

Core workflow:
1. Upload resume → get analysis + SG flags
2. Submit JD (URL or text) → get match assessment
3. Get suggestions → accept/reject/modify
4. Track applications
"""
import hashlib
import uuid
from datetime import datetime, timedelta
from typing import Optional

import structlog
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Request
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from keystone.models.base import get_db
from keystone.models.entities import (
    Application,
    ApplicationStatus,
    ConsentType,
    JobAnalysis,
    Resume,
    Suggestion,
    SubscriptionTier,
    User,
    UserConsent,
)
from keystone.services.claude_client import get_claude_client
from keystone.services.clerk_auth import AuthUser, get_current_user
from keystone.services.content_sanitizer import sanitize_resume_content, validate_before_storage
from keystone.services.nric_detector import detect_nric
from keystone.services.rate_limit import check_rate_limit
from keystone.core import get_settings

logger = structlog.get_logger()

router = APIRouter(prefix="/job-seeker", tags=["job-seeker"])


# =============================================================================
# REQUEST/RESPONSE MODELS
# =============================================================================


class ResumeUploadResponse(BaseModel):
    id: uuid.UUID
    content_hash: str
    sg_flags: dict
    nric_detected: bool
    created_at: datetime


class ResumeListResponse(BaseModel):
    id: uuid.UUID
    filename: str
    uploaded_at: datetime
    page_count: Optional[int] = None
    word_count: Optional[int] = None
    analyses_count: int


class JobParseRequest(BaseModel):
    url: Optional[str] = None
    text: Optional[str] = None


class JobParseResponse(BaseModel):
    job_id: uuid.UUID
    title: Optional[str] = None
    company: Optional[str] = None
    company_type: Optional[str] = None
    skills: list[str]
    seniority: Optional[str] = None
    parsed_from: str  # "url" or "text"


class MatchAssessmentResponse(BaseModel):
    job_analysis_id: uuid.UUID
    match_levels: dict  # {requirement: "strong"|"transferable"|"addressable"|"fundamental"}
    overall_score: float
    created_at: datetime


class SuggestionRequest(BaseModel):
    job_analysis_id: uuid.UUID


class SuggestionResponse(BaseModel):
    id: uuid.UUID
    section: str
    original_text: str
    suggested_text: str
    rationale: Optional[str]
    match_level: str
    created_at: datetime


class SuggestionFeedbackRequest(BaseModel):
    suggestion_id: uuid.UUID
    action: str = Field(..., pattern="^(accept|reject|modify)$")
    modified_text: Optional[str] = None


class ApplicationCreateRequest(BaseModel):
    employer: str
    role: str
    job_analysis_id: Optional[uuid.UUID] = None


class ApplicationResponse(BaseModel):
    id: uuid.UUID
    employer: str
    role: str
    status: str
    stages: list
    created_at: datetime


class ApplicationUpdateRequest(BaseModel):
    status: Optional[str] = None
    final_outcome: Optional[str] = None
    notes: Optional[str] = None


# =============================================================================
# RESUME UPLOAD
# =============================================================================


@router.post("/resume/upload", response_model=ResumeUploadResponse)
async def upload_resume(
    request: Request,
    file: UploadFile = File(...),
    user: AuthUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Upload and analyze resume.

    Rate limited per user tier.
    """
    # Rate limit by user
    tier_key = user.subscription_tier or "free"
    check_rate_limit(str(user.job_seeker_id), tier_key)

    settings = get_settings()

    # Read file content
    content = await file.read()
    text_content = content.decode("utf-8", errors="ignore")

    # Validate before storage (NRIC check)
    is_safe, error_msg = validate_before_storage(text_content)
    if not is_safe:
        raise HTTPException(
            status_code=400,
            detail=f"Resume contains sensitive data that cannot be stored: {error_msg}"
        )

    # Sanitize content
    sanitized = sanitize_resume_content(text_content)
    if sanitized.warnings:
        logger.warning("resume_sanitization_warnings", warnings=sanitized.warnings)

    # Calculate content hash for caching
    content_hash = hashlib.sha256(content).hexdigest()

    # Check if resume with same hash already exists for this user
    existing = await db.execute(
        select(Resume).where(
            Resume.user_id == user.job_seeker_id,
            Resume.content_hash == content_hash,
        )
    )
    existing_resume = existing.scalar_one_or_none()
    if existing_resume:
        return ResumeUploadResponse(
            id=existing_resume.id,
            content_hash=existing_resume.content_hash,
            sg_flags=existing_resume.sg_flags or {},
            nric_detected=sanitized.warnings and any("NRIC" in w for w in sanitized.warnings),
            created_at=existing_resume.created_at,
        )

    # Detect SG-specific flags
    sg_flags = _extract_sg_flags(sanitized.sanitized_content)

    # Store resume
    resume = Resume(
        id=uuid.uuid4(),
        user_id=user.job_seeker_id,
        content_hash=content_hash,
        parsed_json={"filename": file.filename},
        sg_flags=sg_flags,
        s3_key=f"resumes/{user.id}/{content_hash}",  # TODO: actual S3 upload
        created_at=datetime.utcnow(),
    )
    db.add(resume)
    await db.commit()
    await db.refresh(resume)

    return ResumeUploadResponse(
        id=resume.id,
        content_hash=resume.content_hash,
        sg_flags=sg_flags,
        nric_detected=sanitized.warnings and any("NRIC" in w for w in sanitized.warnings),
        created_at=resume.created_at,
    )


@router.get("/resumes", response_model=list[ResumeListResponse])
async def list_resumes(
    user: AuthUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List all resumes for the current user."""
    from sqlalchemy import func

    # Get all resumes for user with analysis counts
    result = await db.execute(
        select(Resume, func.count(JobAnalysis.id).label("analyses_count"))
        .outerjoin(JobAnalysis, JobAnalysis.resume_id == Resume.id)
        .where(Resume.user_id == user.job_seeker_id)
        .group_by(Resume.id)
        .order_by(Resume.created_at.desc())
    )
    rows = result.all()

    return [
        ResumeListResponse(
            id=resume.id,
            filename=resume.parsed_json.get("filename", "resume.txt") if resume.parsed_json else "resume.txt",
            uploaded_at=resume.created_at,
            page_count=resume.parsed_json.get("page_count") if resume.parsed_json else None,
            word_count=resume.parsed_json.get("word_count") if resume.parsed_json else None,
            analyses_count=analyses_count,
        )
        for resume, analyses_count in rows
    ]


def _extract_sg_flags(content: str) -> dict:
    """Extract Singapore-specific flags from resume content."""
    flags = {
        "has_nric": False,
        "has_photo": False,
        "ns_quality": None,
        "education_format": None,
    }

    # Check for NRIC
    nric_result = detect_nric(content)
    flags["has_nric"] = nric_result.found

    # Check for photo mention (heuristic)
    photo_keywords = ["photo", "passport photo", "profile picture"]
    flags["has_photo"] = any(kw in content.lower() for kw in photo_keywords)

    # NS-related (for male Singaporeans)
    ns_keywords = ["national service", "ns", "saf", "scdf", "spf", "nsf"]
    if any(kw in content.lower() for kw in ns_keywords):
        flags["ns_mentioned"] = True

    return flags


# =============================================================================
# JOB PARSING
# =============================================================================


@router.post("/job/parse", response_model=JobParseResponse)
async def parse_job(
    request: JobParseRequest,
    http_request: Request,
    user: AuthUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Parse job posting from URL or text.

    Extracts: title, company, company_type, skills, seniority
    Rate limited per user tier.
    """
    # Rate limit by user
    tier_key = user.subscription_tier or "free"
    check_rate_limit(str(user.job_seeker_id), tier_key)

    if not request.url and not request.text:
        raise HTTPException(
            status_code=400,
            detail="Either url or text must be provided"
        )

    client = get_claude_client()
    settings = get_settings()

    if request.url:
        # Fetch URL content
        try:
            text_content = await _fetch_url_content(request.url)
        except Exception as e:
            logger.warning("job_url_fetch_failed", url=request.url, error=str(e))
            raise HTTPException(status_code=400, detail=f"Failed to fetch job posting URL: {e}")
        parsed = await _parse_job_with_ai(client, settings, text=text_content)
        parsed["parsed_from"] = "url"
    else:
        parsed = await _parse_job_with_ai(client, settings, text=request.text)
        parsed["parsed_from"] = "text"

    # Store job analysis
    analysis = JobAnalysis(
        id=uuid.uuid4(),
        user_id=user.job_seeker_id,
        job_url=request.url or None,
        job_parsed_json=parsed,
        company_type=parsed.get("company_type"),
        created_at=datetime.utcnow(),
    )
    db.add(analysis)
    await db.commit()
    await db.refresh(analysis)

    return JobParseResponse(
        job_id=analysis.id,
        title=parsed.get("title"),
        company=parsed.get("company"),
        company_type=parsed.get("company_type"),
        skills=parsed.get("skills", []),
        seniority=parsed.get("seniority"),
        parsed_from=parsed["parsed_from"],
    )


async def _fetch_url_content(url: str) -> str:
    """Fetch and extract text content from a job posting URL."""
    import re

    import httpx

    # Only allow http/https
    if not url.startswith(("http://", "https://")):
        raise ValueError("URL must start with http:// or https://")

    async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
        response = await client.get(url)
        response.raise_for_status()

        content_type = response.headers.get("content-type", "")
        if "text/html" in content_type:
            # Extract text from HTML (simple approach)
            html = response.text
            # Remove scripts and styles
            html = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL)
            html = re.sub(r"<style[^>]*>.*?</style>", "", html, flags=re.DOTALL)
            # Remove HTML tags
            text = re.sub(r"<[^>]+>", " ", html)
            # Collapse whitespace
            text = re.sub(r"\s+", " ", text).strip()
            return text[:10000]  # Limit to 10k chars
        else:
            # Return raw text
            return response.text[:10000]


async def _parse_job_with_ai(client, settings, text: str) -> dict:
    """Use Claude to extract job information from text."""
    import json
    from keystone.services.claude_client import ClaudeResponse
    from keystone.services.circuit_breaker import CircuitBreakerError

    prompt = f"""Extract job information from this job posting. Return ONLY valid JSON with no markdown:
{{"title": "job title", "company": "company name", "company_type": "banking|fintech|startup|mnc|other", "skills": ["skill1", "skill2"], "seniority": "junior|mid|senior|lead"}}

Job posting:
{text[:3000]}"""

    try:
        response: ClaudeResponse = await client.generate(
            model=settings.anthropic_model_haiku,
            system_prompt="You are a job posting analyst. Return ONLY valid JSON, no markdown or explanation.",
            user_prompt=prompt,
            max_tokens=1024,
        )
        # Parse JSON from response
        content = response.content.strip()
        # Remove markdown code blocks if present
        if content.startswith("```"):
            lines = content.split("\n")
            content = "\n".join(lines[1:-1])
        result = json.loads(content)
        # Validate and normalize
        return {
            "title": result.get("title", "Unknown Title"),
            "company": result.get("company", "Unknown Company"),
            "company_type": result.get("company_type", "other"),
            "skills": result.get("skills", []),
            "seniority": result.get("seniority", "mid"),
        }
    except json.JSONDecodeError:
        logger.warning("job_parse_json_decode_failed", content=response.content[:500])
        return {
            "title": "Unknown Title",
            "company": "Unknown Company",
            "company_type": "other",
            "skills": [],
            "seniority": "mid",
        }
    except CircuitBreakerError:
        raise HTTPException(status_code=503, detail="AI service temporarily unavailable")


# =============================================================================
# MATCH ASSESSMENT
# =============================================================================


@router.post("/job/{job_id}/analyze", response_model=MatchAssessmentResponse)
async def analyze_match(
    job_id: uuid.UUID,
    resume_id: uuid.UUID,
    http_request: Request,
    user: AuthUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Analyze resume against job posting - four-level match assessment.

    Rate limited per user tier.
    """
    from keystone.services.claude_client import ClaudeResponse
    from keystone.services.circuit_breaker import CircuitBreakerError

    # Rate limit by user
    tier_key = user.subscription_tier or "free"
    check_rate_limit(str(user.job_seeker_id), tier_key)

    client = get_claude_client()
    settings = get_settings()

    # Get resume and job analysis
    resume_result = await db.execute(
        select(Resume).where(Resume.id == resume_id, Resume.user_id == user.job_seeker_id)
    )
    resume = resume_result.scalar_one_or_none()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    job_result = await db.execute(
        select(JobAnalysis).where(JobAnalysis.id == job_id, JobAnalysis.user_id == user.job_seeker_id)
    )
    job = job_result.scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=404, detail="Job analysis not found")

    # Generate match assessment
    resume_content = resume.parsed_json if resume.parsed_json else {}
    resume_text = resume_content.get("text", resume_content.get("filename", ""))
    prompt = f"""Analyze this resume against the job requirements.
Classify each skill/requirement as:
- strong: user clearly has this
- transferable: user has adjacent experience
- addressable: user can claim this with reframing
- fundamental: user lacks this

Resume:
{resume_text}

Job requirements:
{job.job_parsed_json}"""

    try:
        response: ClaudeResponse = await client.generate(
            model=settings.anthropic_model_haiku,
            system_prompt="You are a job match analyst. Respond with JSON.",
            user_prompt=prompt,
            max_tokens=2048,
        )
    except CircuitBreakerError:
        raise HTTPException(status_code=503, detail="AI service temporarily unavailable")

    # Store match results
    job.match_results = {"assessment": response.content}
    await db.commit()

    # Calculate overall score
    overall_score = _calculate_match_score(job.match_results)

    return MatchAssessmentResponse(
        job_analysis_id=job.id,
        match_levels=job.match_results.get("levels", {}),
        overall_score=overall_score,
        created_at=job.created_at,
    )


def _calculate_match_score(match_results: dict) -> float:
    """Calculate overall match score 0-100."""
    levels = match_results.get("levels", {})
    if not levels:
        return 50.0

    scores = {"strong": 100, "transferable": 70, "addressable": 40, "fundamental": 0}
    total = sum(scores.get(l, 50) for l in levels.values())
    return round(total / len(levels), 1)


# =============================================================================
# SUGGESTIONS
# =============================================================================


@router.post("/suggestions", response_model=list[SuggestionResponse])
async def get_suggestions(
    request: SuggestionRequest,
    user: AuthUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Generate line-by-line revision suggestions."""
    from keystone.services.claude_client import ClaudeResponse
    from keystone.services.circuit_breaker import CircuitBreakerError

    client = get_claude_client()
    settings = get_settings()

    # Get job analysis
    result = await db.execute(
        select(JobAnalysis).where(
            JobAnalysis.id == request.job_analysis_id,
            JobAnalysis.user_id == user.job_seeker_id,
        )
    )
    job = result.scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=404, detail="Job analysis not found")

    # Generate suggestions using Claude Sonnet for better quality
    prompt = f"""Generate resume revision suggestions for this job application.
For each suggestion, provide:
- section: which part of resume (experience/education/skills)
- original_text: the original text to replace
- suggested_text: the improved version
- rationale: why this change helps for this job
- match_level: the match level of this suggestion

Job: {job.job_parsed_json}

Format each suggestion as JSON."""

    try:
        response: ClaudeResponse = await client.generate(
            model=settings.anthropic_model_sonnet,
            system_prompt="You are an expert resume writer. Generate specific, actionable suggestions.",
            user_prompt=prompt,
            max_tokens=4096,
        )
    except CircuitBreakerError:
        raise HTTPException(status_code=503, detail="AI service temporarily unavailable")

    # Parse suggestions (simplified - real implementation would parse JSON)
    suggestions = _parse_suggestions(response.content, request.job_analysis_id)

    # Store suggestions
    for sugg in suggestions:
        db.add(sugg)
    await db.commit()

    return [SuggestionResponse.model_validate(s) for s in suggestions]


def _parse_suggestions(content: str, job_analysis_id: uuid.UUID) -> list[Suggestion]:
    """Parse suggestions from AI response."""
    import json

    suggestions = []
    try:
        # Try to parse as JSON array
        content = content.strip()
        if content.startswith("```"):
            lines = content.split("\n")
            content = "\n".join(lines[1:-1])
        data = json.loads(content)
        if not isinstance(data, list):
            data = [data]
        for item in data:
            if not isinstance(item, dict):
                continue
            suggestion = Suggestion(
                id=uuid.uuid4(),
                job_analysis_id=job_analysis_id,
                section=item.get("section", "experience"),
                original_text=item.get("original_text", ""),
                suggested_text=item.get("suggested_text", ""),
                rationale=item.get("rationale"),
                match_level=item.get("match_level", "transferable"),
            )
            suggestions.append(suggestion)
    except json.JSONDecodeError:
        logger.warning("suggestions_parse_failed", content=content[:500])
    return suggestions


@router.post("/suggestions/{suggestion_id}/feedback")
async def submit_suggestion_feedback(
    suggestion_id: uuid.UUID,
    request: SuggestionFeedbackRequest,
    user: AuthUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Submit feedback on a suggestion (accept/reject/modify)."""
    result = await db.execute(
        select(Suggestion).where(Suggestion.id == suggestion_id)
    )
    suggestion = result.scalar_one_or_none()
    if not suggestion:
        raise HTTPException(status_code=404, detail="Suggestion not found")

    # Log the signal for learning
    from keystone.models.entities import SuggestionSignal

    signal = SuggestionSignal(
        id=uuid.uuid4(),
        anonymized_user_id=_hash_user_id(user.id),
        suggestion_id=suggestion_id,
        action=request.action.upper(),
        modified_text=request.modified_text,
        created_at=datetime.utcnow(),
    )
    db.add(signal)

    # If modified, update the suggestion
    if request.action == "modify" and request.modified_text:
        suggestion.suggested_text = request.modified_text

    await db.commit()

    return {"status": "recorded", "action": request.action}


def _hash_user_id(user_id: str) -> str:
    """Anonymize user ID for suggestion signals (PDPA compliance)."""
    import hashlib
    return hashlib.sha256(user_id.encode()).hexdigest()[:16]


# =============================================================================
# APPLICATION TRACKING
# =============================================================================


@router.post("/applications", response_model=ApplicationResponse)
async def create_application(
    request: ApplicationCreateRequest,
    user: AuthUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a new job application record."""
    application = Application(
        id=uuid.uuid4(),
        user_id=user.job_seeker_id,
        job_analysis_id=request.job_analysis_id,
        employer=request.employer,
        role=request.role,
        status="interested",
        stages=[],
        created_at=datetime.utcnow(),
    )
    db.add(application)
    await db.commit()
    await db.refresh(application)

    return ApplicationResponse(
        id=application.id,
        employer=application.employer,
        role=application.role,
        status=application.status,
        stages=application.stages or [],
        created_at=application.created_at,
    )


@router.get("/applications", response_model=list[ApplicationResponse])
async def list_applications(
    user: AuthUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List all applications for the current user."""
    result = await db.execute(
        select(Application).where(Application.user_id == user.job_seeker_id)
    )
    applications = result.scalars().all()

    return [
        ApplicationResponse(
            id=a.id,
            employer=a.employer,
            role=a.role,
            status=a.status,
            stages=a.stages or [],
            created_at=a.created_at,
        )
        for a in applications
    ]


@router.get("/applications/{application_id}", response_model=ApplicationResponse)
async def get_application(
    application_id: uuid.UUID,
    user: AuthUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get application details."""
    result = await db.execute(
        select(Application).where(
            Application.id == application_id,
            Application.user_id == user.job_seeker_id,
        )
    )
    application = result.scalar_one_or_none()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    return ApplicationResponse(
        id=application.id,
        employer=application.employer,
        role=application.role,
        status=application.status,
        stages=application.stages or [],
        created_at=application.created_at,
    )


@router.put("/applications/{application_id}", response_model=ApplicationResponse)
async def update_application(
    application_id: uuid.UUID,
    request: ApplicationUpdateRequest,
    user: AuthUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update application status/outcome."""
    result = await db.execute(
        select(Application).where(
            Application.id == application_id,
            Application.user_id == user.job_seeker_id,
        )
    )
    application = result.scalar_one_or_none()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    if request.status:
        application.status = request.status
    if request.final_outcome:
        application.final_outcome = request.final_outcome
    if request.notes:
        application.notes = request.notes

    application.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(application)

    return ApplicationResponse(
        id=application.id,
        employer=application.employer,
        role=application.role,
        status=application.status,
        stages=application.stages or [],
        created_at=application.created_at,
    )


# =============================================================================
# BATCH APPLICATION OPERATIONS (Nudge + No-News)
# =============================================================================


class BatchUpdateItem(BaseModel):
    id: uuid.UUID
    status: Optional[ApplicationStatus] = None
    final_outcome: Optional[str] = None


class BatchUpdateRequest(BaseModel):
    applications: list[BatchUpdateItem]


class BatchUpdateResponse(BaseModel):
    updated: int
    failed: int
    errors: list[str]


class NudgeEligibleApplicationResponse(BaseModel):
    id: uuid.UUID
    employer: str
    role: str
    status: ApplicationStatus
    last_activity_at: Optional[datetime]
    days_since_activity: int
    created_at: datetime


@router.get("/applications/nudge-eligible", response_model=list[NudgeEligibleApplicationResponse])
async def get_nudge_eligible(
    user: AuthUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    http_request: Request = None,
    days: int = 14,
    limit: int = 50,
):
    """Get applications eligible for nudge (no activity, still active)."""
    if http_request:
        check_rate_limit(get_client_identifier(http_request), "default")

    if not user.job_seeker_id:
        raise HTTPException(status_code=401, detail="User not found")

    cutoff = datetime.utcnow() - timedelta(days=days)

    result = await db.execute(
        select(Application).where(
            Application.user_id == user.job_seeker_id,
            Application.status.in_([ApplicationStatus.APPLIED, ApplicationStatus.SCREENING, ApplicationStatus.INTERVIEW]),
            Application.last_activity_at < cutoff,
            Application.auto_closed_at.is_(None),
        ).order_by(Application.last_activity_at.asc()).limit(limit)
    )
    apps = result.scalars().all()

    return [
        NudgeEligibleApplicationResponse(
            id=a.id,
            employer=a.employer,
            role=a.role,
            status=a.status,
            last_activity_at=a.last_activity_at,
            days_since_activity=(datetime.utcnow() - a.last_activity_at).days if a.last_activity_at else 999,
            created_at=a.created_at,
        )
        for a in apps
    ]


@router.post("/applications/batch-update", response_model=BatchUpdateResponse)
async def batch_update_applications(
    request: BatchUpdateRequest,
    user: AuthUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    http_request: Request = None,
):
    """Batch update application statuses and outcomes."""
    if http_request:
        check_rate_limit(get_client_identifier(http_request), "default")

    if not user.job_seeker_id:
        raise HTTPException(status_code=401, detail="User not found")

    updated = 0
    failed = 0
    errors: list[str] = []

    for item in request.applications:
        try:
            result = await db.execute(
                select(Application).where(
                    Application.id == item.id,
                    Application.user_id == user.job_seeker_id,
                )
            )
            app = result.scalar_one_or_none()
            if not app:
                failed += 1
                errors.append(f"Application {item.id} not found")
                continue

            if item.status is not None:
                app.status = item.status
                app.last_activity_at = datetime.utcnow()
            if item.final_outcome is not None:
                app.final_outcome = item.final_outcome
            app.updated_at = datetime.utcnow()
            updated += 1
        except Exception as e:
            failed += 1
            errors.append(f"Application {item.id}: {str(e)}")

    await db.commit()

    return BatchUpdateResponse(updated=updated, failed=failed, errors=errors)


@router.post("/applications/mark-all-no-news")
async def mark_all_no_news(
    user: AuthUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    http_request: Request = None,
):
    """Mark all nudge-eligible applications as 'no news' (keep active)."""
    if http_request:
        check_rate_limit(get_client_identifier(http_request), "default")

    if not user.job_seeker_id:
        raise HTTPException(status_code=401, detail="User not found")

    cutoff = datetime.utcnow() - timedelta(days=14)

    result = await db.execute(
        select(Application).where(
            Application.user_id == user.job_seeker_id,
            Application.status.in_([ApplicationStatus.APPLIED, ApplicationStatus.SCREENING, ApplicationStatus.INTERVIEW]),
            Application.last_activity_at < cutoff,
            Application.auto_closed_at.is_(None),
        )
    )
    apps = result.scalars().all()

    count = 0
    for app in apps:
        app.last_activity_at = datetime.utcnow()
        count += 1

    await db.commit()

    return {"marked": count}


# =============================================================================
# INTERNAL: AUTO-CLOSE STALE APPLICATIONS
# =============================================================================


@router.post("/internal/auto-close-applications")
async def auto_close_stale_applications(
    days_inactive: int = 30,
    db: AsyncSession = Depends(get_db),
):
    """Auto-close applications with no recent activity.

    Closes applications that are in terminal states (offer/rejected/withdrawn)
    and have had no activity for the specified number of days.
    Callable by AWS EventBridge cron or similar scheduler.
    """
    cutoff = datetime.utcnow() - timedelta(days=days_inactive)
    terminal_states = [ApplicationStatus.OFFER, ApplicationStatus.REJECTED, ApplicationStatus.WITHDRAWN]

    result = await db.execute(
        select(Application).where(
            Application.status.in_(terminal_states),
            Application.auto_closed_at.is_(None),
            Application.last_activity_at < cutoff,
        )
    )
    apps = result.scalars().all()

    closed = 0
    for app in apps:
        app.auto_closed_at = datetime.utcnow()
        closed += 1

    await db.commit()

    logger.info("auto_close.run", closed=closed, days_inactive=days_inactive)
    return {"closed": closed}


# =============================================================================
# ANALYTICS
# =============================================================================


class AnalyticsSummaryResponse(BaseModel):
    total_applications: int
    by_status: dict[str, int]
    nudge_eligible_count: int
    active_last_30d: int
    completed_last_30d: int


class ProfileCompletenessResponse(BaseModel):
    resume_uploaded: bool
    resume_parsed: bool
    phone_verified: bool
    stripe_customer: bool
    consent_complete: bool
    completeness_percent: int


@router.get("/analytics/summary", response_model=AnalyticsSummaryResponse)
async def get_analytics_summary(
    user: AuthUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    http_request: Request = None,
):
    """Get application analytics summary for the current user."""
    if http_request:
        check_rate_limit(get_client_identifier(http_request), "default")

    if not user.job_seeker_id:
        raise HTTPException(status_code=401, detail="User not found")

    # Total and by-status counts
    all_result = await db.execute(
        select(Application).where(Application.user_id == user.job_seeker_id)
    )
    all_apps = all_result.scalars().all()
    total = len(all_apps)
    by_status: dict[str, int] = {}
    for app in all_apps:
        key = app.status.value if hasattr(app.status, 'value') else str(app.status)
        by_status[key] = by_status.get(key, 0) + 1

    # Nudge-eligible (no activity 14+ days, still active)
    cutoff_14 = datetime.utcnow() - timedelta(days=14)
    nudge_result = await db.execute(
        select(Application).where(
            Application.user_id == user.job_seeker_id,
            Application.status.in_([ApplicationStatus.APPLIED, ApplicationStatus.SCREENING, ApplicationStatus.INTERVIEW]),
            Application.last_activity_at < cutoff_14,
            Application.auto_closed_at.is_(None),
        )
    )
    nudge_count = len(nudge_result.scalars().all())

    # Active last 30d (had activity)
    cutoff_30 = datetime.utcnow() - timedelta(days=30)
    active_30d = sum(1 for a in all_apps if a.last_activity_at and a.last_activity_at >= cutoff_30)

    # Completed last 30d (final outcome set)
    completed_30d = sum(1 for a in all_apps if a.final_outcome and a.created_at >= cutoff_30)

    return AnalyticsSummaryResponse(
        total_applications=total,
        by_status=by_status,
        nudge_eligible_count=nudge_count,
        active_last_30d=active_30d,
        completed_last_30d=completed_30d,
    )


@router.get("/analytics/completeness", response_model=ProfileCompletenessResponse)
async def get_profile_completeness(
    user: AuthUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    http_request: Request = None,
):
    """Get profile completeness score for the current user."""
    if http_request:
        check_rate_limit(get_client_identifier(http_request), "default")

    if not user.job_seeker_id:
        raise HTTPException(status_code=401, detail="User not found")

    # Fetch user record
    user_result = await db.execute(select(User).where(User.id == user.job_seeker_id))
    user_record = user_result.scalar_one_or_none()

    # Resume check
    resume_result = await db.execute(
        select(Resume).where(Resume.user_id == user.job_seeker_id).limit(1)
    )
    resume = resume_result.scalar_one_or_none()
    resume_uploaded = resume is not None
    resume_parsed = resume is not None and resume.parsed_json is not None

    # Phone verified
    phone_verified = user_record.phone_verified if user_record else False

    # Stripe customer
    stripe_customer = user_record.stripe_customer_id is not None if user_record else False

    # Consent complete (all 4 required consents granted)
    consent_result = await db.execute(
        select(UserConsent).where(
            UserConsent.user_id == user.job_seeker_id,
            UserConsent.granted_at.isnot(None),
            UserConsent.revoked_at.is_(None),
        )
    )
    granted_consents = {c.consent_type for c in consent_result.scalars().all()}
    required_consents = {ConsentType.REGISTRATION, ConsentType.STORAGE, ConsentType.AI_PROCESSING, ConsentType.OUTCOME_TRACKING}
    consent_complete = required_consents.issubset(granted_consents)

    # Compute percentage
    fields = [resume_uploaded, resume_parsed, phone_verified, stripe_customer, consent_complete]
    completeness_percent = int(sum(fields) / len(fields) * 100)

    return ProfileCompletenessResponse(
        resume_uploaded=resume_uploaded,
        resume_parsed=resume_parsed,
        phone_verified=phone_verified,
        stripe_customer=stripe_customer,
        consent_complete=consent_complete,
        completeness_percent=completeness_percent,
    )


# =============================================================================
# SUGGESTIONS

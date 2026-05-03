"""Job Seeker API - B2C resume optimization and application tracking.

Core workflow:
1. Upload resume → get analysis + SG flags
2. Submit JD (URL or text) → get match assessment
3. Get suggestions → accept/reject/modify
4. Track applications
"""
import uuid
import hashlib
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from keystone.models.base import get_db
from keystone.models.entities import (
    User,
    Resume,
    JobAnalysis,
    Suggestion,
    Application,
    SubscriptionTier,
)
from keystone.services.clerk_auth import get_current_user, AuthUser
from keystone.services.content_sanitizer import sanitize_resume_content, validate_before_storage
from keystone.services.nric_detector import detect_nric
from keystone.services.claude_client import get_claude_client
from keystone.core import get_settings

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
    file: UploadFile = File(...),
    user: AuthUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Upload and analyze resume.

    - Extracts text from PDF/DOCX/text
    - Runs NRIC detection (PDPA compliance)
    - Stores content hash for caching
    - Returns SG-specific flags
    """
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
    user: AuthUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Parse job posting from URL or text.

    Extracts: title, company, company_type, skills, seniority
    """
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


async def _fetch_url_content(url: str) -> str:
    """Fetch and extract text content from a job posting URL."""
    import httpx
    import re

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
            html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
            html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)
            # Remove HTML tags
            text = re.sub(r'<[^>]+>', ' ', html)
            # Collapse whitespace
            text = re.sub(r'\s+', ' ', text).strip()
            return text[:10000]  # Limit to 10k chars
        else:
            # Return raw text
            return response.text[:10000]

    # Store job analysis
    analysis = JobAnalysis(
        id=uuid.uuid4(),
        user_id=user.job_seeker_id,
        job_url=request.url,
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
    user: AuthUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Analyze resume against job posting - four-level match assessment."""
    from keystone.services.claude_client import ClaudeResponse
    from keystone.services.circuit_breaker import CircuitBreakerError

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
    prompt = f"""Analyze this resume against the job requirements.
Classify each skill/requirement as:
- strong: user clearly has this
- transferable: user has adjacent experience
- addressable: user can claim this with reframing
- fundamental: user lacks this

Resume:
[User resume content]

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


# Import logger at module level
import structlog
logger = structlog.get_logger()

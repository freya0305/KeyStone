"""Job Seeker API - B2C resume optimization and application tracking.

Core workflow:
1. Upload resume → get analysis + SG flags
2. Submit JD (URL or text) → get match assessment
3. Get suggestions → accept/reject/modify
4. Track applications
"""
import hashlib
import io
import uuid
import asyncio
import json
from datetime import datetime, timedelta
from typing import Literal, Optional, AsyncGenerator

import structlog
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Request, Cookie, BackgroundTasks, Header
from fastapi.responses import StreamingResponse, Response
from pydantic import BaseModel, Field, FieldValidationInfo
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from keystone.models.base import get_db, async_session_factory
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
from keystone.services.claude_client import get_claude_client, ClaudeResponse
from keystone.services.clerk_auth import AuthUser, get_current_user
from keystone.services.consent import ConsentService
from keystone.services.content_sanitizer import sanitize_resume_content, validate_before_storage
from keystone.services.nric_detector import detect_nric, assert_no_nric, mask_nric
from keystone.services.rate_limit import check_rate_limit, get_client_identifier
from keystone.core import get_settings
from keystone.services.s3 import upload_resume_to_s3
from keystone.services.resume_parsing import (
    extract_resume_text,
    extract_sg_flags,
    parse_resume_with_claude,
    mask_resume_text,
    FileValidationError,
    ResumeParseError,
    ResumeText,
)
from keystone.services.jd_fetcher import fetch_jd_from_url, JDFetchResult
from keystone.services.jd_parser import parse_job_description, parsed_to_dict, ParsedJobDescription
from keystone.services.company_classifier import classify_company, CompanyClassification
from keystone.services.match_assessor import assess_match, assessment_to_dict, MatchAssessment

logger = structlog.get_logger()

router = APIRouter(prefix="/job-seeker", tags=["job-seeker"])


def verify_internal_api_key(x_internal_api_key: str = Header(None)) -> str:
    """Verify internal API key for admin/cron endpoints."""
    settings = get_settings()
    if not settings.INTERNAL_API_KEY:
        raise HTTPException(500, "Internal API key not configured")
    if x_internal_api_key != settings.INTERNAL_API_KEY:
        raise HTTPException(401, "Invalid internal API key")
    return x_internal_api_key


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


class GatedSuggestionResponse(BaseModel):
    """Response for gated suggestions (M4.3)."""
    id: uuid.UUID
    section: str
    original_text: str
    suggested_text: str
    rationale: Optional[str]
    match_level: str
    created_at: datetime
    gated: bool = False


class SuggestionListResponse(BaseModel):
    """Response for suggestions endpoint with free tier gating (M4.3)."""
    suggestions: list[GatedSuggestionResponse]
    gated: bool = False
    gated_count: int = 0
    gate_context: Optional[str] = None  # e.g., "experience section, JD coverage 85%"


class SuggestionFeedbackRequest(BaseModel):
    suggestion_id: uuid.UUID
    action: str = Field(..., pattern="^(accept|reject|modify)$")
    modified_text: Optional[str] = None


class ApplicationCreateRequest(BaseModel):
    employer: str
    role: str
    job_url: Optional[str] = None
    applied_at: Optional[str] = None
    status: str = "applied"
    notes: Optional[str] = None
    job_analysis_id: Optional[uuid.UUID] = None
    suggestion_set_id: Optional[uuid.UUID] = None


class ApplicationResponse(BaseModel):
    id: uuid.UUID
    employer: str
    role: str
    status: str
    stages: list
    created_at: datetime
    job_url: Optional[str] = None
    applied_at: Optional[str] = None
    suggestion_set_id: Optional[uuid.UUID] = None


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
    """Upload and analyze resume (M2.1).

    - Magic-byte validation (PDF/DOCX)
    - Text extraction with pdfplumber/docx
    - SHA-256 content hash for caching
    - NRIC Stage 1: mask before S3 write
    - Write to S3 (keystone-resumes-{env})
    - Rate limited per user tier

    Args:
        file: Resume file (PDF or DOCX, max 5MB)
        user: Authenticated user
        db: Database session

    Returns:
        ResumeUploadResponse with resume_id, content_hash, sg_flags, nric_detected
    """
    # Rate limit by user
    tier_key = user.subscription_tier or "free"
    check_rate_limit(str(user.job_seeker_id), tier_key)

    # Read file content
    content = await file.read()

    try:
        # Extract text with magic-byte validation
        resume_text: ResumeText = await extract_resume_text(content, file.filename)
    except FileValidationError as e:
        logger.warning("resume_file_validation_failed", filename=file.filename, error=str(e))
        raise HTTPException(status_code=422, detail=str(e))
    except ResumeParseError as e:
        logger.warning("resume_text_extraction_failed", filename=file.filename, error=str(e))
        raise HTTPException(status_code=422, detail=f"Failed to extract text from resume: {e}")

    content_hash = resume_text.content_hash

    # Check if resume with same hash already exists for this user (cache check)
    existing = await db.execute(
        select(Resume).where(
            Resume.user_id == user.job_seeker_id,
            Resume.content_hash == content_hash,
        )
    )
    existing_resume = existing.scalar_one_or_none()
    if existing_resume:
        logger.info("resume_cache_hit", resume_id=str(existing_resume.id), content_hash=content_hash[:16])
        return ResumeUploadResponse(
            id=existing_resume.id,
            content_hash=existing_resume.content_hash,
            sg_flags=existing_resume.sg_flags or {},
            nric_detected=existing_resume.sg_flags.get("has_nric", False) if existing_resume.sg_flags else False,
            created_at=existing_resume.created_at,
        )

    # Stage 1: Apply NRIC masking before S3 upload
    masked_text = mask_resume_text(resume_text.text)

    # Upload to S3
    try:
        s3_key = await upload_resume_to_s3(
            content=content,
            content_hash=content_hash,
            user_id=str(user.job_seeker_id),
            filename=file.filename,
        )
    except Exception as e:
        logger.error("s3_upload_failed", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to store resume")

    # Extract SG-specific flags (M2.3)
    sg_flags_dict = _extract_sg_flags_to_dict(resume_text.text)

    # Store resume record
    resume = Resume(
        id=uuid.uuid4(),
        user_id=user.job_seeker_id,
        content_hash=content_hash,
        parsed_json={
            "filename": file.filename,
            "file_type": resume_text.file_type,
            "page_count": resume_text.page_count,
            "word_count": resume_text.word_count,
            "text_preview": masked_text[:500],  # Store masked preview
        },
        sg_flags=sg_flags_dict,
        s3_key=s3_key,
        created_at=datetime.utcnow(),
    )
    db.add(resume)
    await db.commit()
    await db.refresh(resume)

    logger.info(
        "resume_uploaded",
        resume_id=str(resume.id),
        content_hash=content_hash[:16],
        filename=file.filename,
        file_type=resume_text.file_type,
        page_count=resume_text.page_count,
    )

    return ResumeUploadResponse(
        id=resume.id,
        content_hash=content_hash,
        sg_flags=sg_flags_dict,
        nric_detected=sg_flags_dict.get("has_nric", False),
        created_at=resume.created_at,
    )


def _extract_sg_flags_to_dict(text: str) -> dict:
    """Extract SG-specific flags as dict for storage."""
    flags = extract_sg_flags(text)
    return {
        "has_nric": flags.has_nric,
        "has_photo": flags.has_photo,
        "ns_quality": flags.ns_quality,
        "ns_mentioned": flags.ns_quality != "not_mentioned",
        "education_tier": flags.education_tier,
        "pmet_signals": flags.pmet_signals,
        "is_pmet": flags.is_pmet,
    }


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


# =============================================================================
# M2.2: RESUME PARSING SERVICE (Claude Haiku)
# =============================================================================


class ResumeParseResponse(BaseModel):
    """Response for parsed resume data."""
    resume_id: uuid.UUID
    contact: dict
    summary: Optional[str]
    experience: list[dict]
    education: list[dict]
    skills: list[str]
    certifications: list[str]
    ns_status: str
    parsed_at: datetime


@router.post("/resumes/{resume_id}/parse", response_model=ResumeParseResponse)
async def parse_resume(
    resume_id: uuid.UUID,
    user: AuthUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Parse resume with Claude Haiku (M2.2).

    - Input: masked resume text
    - Output: structured JSON with contact, summary, experience, education, skills, certifications, ns
    - NRIC Stage 2: assert_no_nric before sending to Claude
    - Cache results by content_hash

    Args:
        resume_id: UUID of the uploaded resume
        user: Authenticated user
        db: Database session

    Returns:
        ParsedResume with structured data
    """
    # Check AI processing consent
    consent_service = ConsentService(db)
    if not await consent_service.check_ai_processing(user.job_seeker_id):
        raise HTTPException(
            status_code=403,
            detail="AI processing consent required. Please grant AI processing consent to use this feature."
        )

    # Get resume from DB
    result = await db.execute(
        select(Resume).where(
            Resume.id == resume_id,
            Resume.user_id == user.job_seeker_id,
        )
    )
    resume = result.scalar_one_or_none()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    # Check if already parsed (cache by content_hash)
    if resume.parsed_json and resume.parsed_json.get("parsed"):
        logger.info("resume_parse_cache_hit", resume_id=str(resume_id), content_hash=resume.content_hash[:16])
        parsed = resume.parsed_json.get("parsed_data", {})
        return ResumeParseResponse(
            resume_id=resume.id,
            contact=parsed.get("contact", {}),
            summary=parsed.get("summary"),
            experience=parsed.get("experience", []),
            education=parsed.get("education", []),
            skills=parsed.get("skills", []),
            certifications=parsed.get("certifications", []),
            ns_status=parsed.get("ns_status", "unknown"),
            parsed_at=resume.parsed_json.get("parsed_at"),
        )

    # Get masked text from S3 or use stored preview
    masked_text = resume.parsed_json.get("text_preview", "") if resume.parsed_json else ""

    if not masked_text:
        # If no text preview, we need to re-extract from S3
        try:
            from keystone.services.s3 import get_resume_from_s3
            raw_content = await get_resume_from_s3(resume.s3_key)
            # Extract text again
            resume_text = await extract_resume_text(raw_content, resume.parsed_json.get("filename", "resume.pdf"))
            masked_text = mask_resume_text(resume_text.text)
        except Exception as e:
            logger.error("resume_re_extraction_failed", resume_id=str(resume_id), error=str(e))
            raise HTTPException(status_code=500, detail="Failed to extract resume text")

    # Parse with Claude Haiku
    try:
        parsed_resume = await parse_resume_with_claude(masked_text, resume.content_hash)
    except ResumeParseError as e:
        logger.warning("resume_parse_failed", resume_id=str(resume_id), error=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to parse resume: {e}")

    # Update resume with parsed data
    resume.parsed_json = resume.parsed_json or {}
    resume.parsed_json["parsed"] = True
    resume.parsed_json["parsed_data"] = {
        "contact": parsed_resume.contact,
        "summary": parsed_resume.summary,
        "experience": parsed_resume.experience,
        "education": parsed_resume.education,
        "skills": parsed_resume.skills,
        "certifications": parsed_resume.certifications,
        "ns_status": parsed_resume.ns_status,
    }
    resume.parsed_json["parsed_at"] = datetime.utcnow().isoformat()

    await db.commit()

    logger.info(
        "resume_parsed",
        resume_id=str(resume_id),
        content_hash=resume.content_hash[:16],
        skills_count=len(parsed_resume.skills),
        experience_count=len(parsed_resume.experience),
    )

    return ResumeParseResponse(
        resume_id=resume.id,
        contact=parsed_resume.contact,
        summary=parsed_resume.summary,
        experience=parsed_resume.experience,
        education=parsed_resume.education,
        skills=parsed_resume.skills,
        certifications=parsed_resume.certifications,
        ns_status=parsed_resume.ns_status,
        parsed_at=datetime.utcnow(),
    )


# =============================================================================
# M2.4: RESUME ANALYSIS ENDPOINT (Async with SSE Progress)
# =============================================================================


class AnalysisStatusResponse(BaseModel):
    """Response for analysis status."""
    resume_id: uuid.UUID
    status: str  # "pending" | "processing" | "ready" | "error"
    progress: float  # 0.0 to 1.0
    stages: list[str]  # ["parsing", "nric_check", "sg_flags", "ready"]
    current_stage: Optional[str]
    error: Optional[str]


@router.get("/resumes/{resume_id}/analysis", response_model=AnalysisStatusResponse)
async def get_analysis_status(
    resume_id: uuid.UUID,
    user: AuthUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get resume analysis status (M2.4).

    Returns current status of async analysis with progress stages:
    - parsing: text extraction
    - nric_check: NRIC validation
    - sg_flags: SG-specific intelligence extraction
    - ready: analysis complete

    Args:
        resume_id: UUID of the uploaded resume
        user: Authenticated user
        db: Database session

    Returns:
        AnalysisStatusResponse with current progress
    """
    # Get resume from DB
    result = await db.execute(
        select(Resume).where(
            Resume.id == resume_id,
            Resume.user_id == user.job_seeker_id,
        )
    )
    resume = result.scalar_one_or_none()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    # Check analysis status from sg_flags metadata
    analysis_status = resume.sg_flags.get("analysis_status", "pending") if resume.sg_flags else "pending"
    analysis_progress = resume.sg_flags.get("analysis_progress", 0.0) if resume.sg_flags else 0.0
    current_stage = resume.sg_flags.get("current_stage") if resume.sg_flags else None
    error_msg = resume.sg_flags.get("analysis_error") if resume.sg_flags else None

    stages = ["parsing", "nric_check", "sg_flags", "ready"]
    if analysis_status == "ready":
        current_stage = "ready"
        analysis_progress = 1.0

    return AnalysisStatusResponse(
        resume_id=resume.id,
        status=analysis_status,
        progress=analysis_progress,
        stages=stages,
        current_stage=current_stage,
        error=error_msg,
    )


@router.post("/resumes/{resume_id}/analyze")
async def trigger_analysis(
    resume_id: uuid.UUID,
    background_tasks: BackgroundTasks,
    user: AuthUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Trigger async resume analysis (M2.4).

    Starts background analysis pipeline:
    1. Upload → text extracted
    2. Processing → NRIC check + SG flags + Claude parsing
    3. Result → stored in resume

    Args:
        resume_id: UUID of the uploaded resume
        background_tasks: FastAPI background tasks
        user: Authenticated user
        db: Database session

    Returns:
        JSON with status message
    """
    # Get resume from DB
    result = await db.execute(
        select(Resume).where(
            Resume.id == resume_id,
            Resume.user_id == user.job_seeker_id,
        )
    )
    resume = result.scalar_one_or_none()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    # Check if already being processed
    if resume.sg_flags and resume.sg_flags.get("analysis_status") == "processing":
        return {"status": "processing", "message": "Analysis already in progress"}

    # Update status to processing
    if not resume.sg_flags:
        resume.sg_flags = {}
    resume.sg_flags["analysis_status"] = "processing"
    resume.sg_flags["current_stage"] = "parsing"
    resume.sg_flags["analysis_progress"] = 0.1
    await db.commit()

    # Queue background task
    background_tasks.add_task(
        _process_resume_analysis,
        resume_id=resume_id,
        user_id=str(user.job_seeker_id),
    )

    return {"status": "processing", "message": "Analysis started"}


async def _process_resume_analysis(resume_id: uuid.UUID, user_id: str) -> None:
    """Background task to process resume analysis.

    Pipeline: parsing → nric_check → sg_flags → ready
    """
    async with async_session_factory() as db:
        try:
            # Get resume
            result = await db.execute(
                select(Resume).where(Resume.id == resume_id)
            )
            resume = result.scalar_one_or_none()
            if not resume:
                logger.error("resume_analysis_resume_not_found", resume_id=str(resume_id))
                return

            # Stage 1: Parsing (0.1 → 0.4)
            resume.sg_flags = resume.sg_flags or {}
            resume.sg_flags["current_stage"] = "parsing"
            resume.sg_flags["analysis_progress"] = 0.2
            await db.commit()

            # Re-extract text if needed
            masked_text = ""
            try:
                from keystone.services.s3 import get_resume_from_s3
                raw_content = await get_resume_from_s3(resume.s3_key)
                resume_text = await extract_resume_text(raw_content, resume.parsed_json.get("filename", "resume.pdf"))
                masked_text = mask_resume_text(resume_text.text)
            except Exception as e:
                logger.error("resume_analysis_extraction_failed", resume_id=str(resume_id), error=str(e))
                raise ResumeParseError(f"Failed to extract text: {e}")

            # Stage 2: NRIC Check (0.4 → 0.6)
            resume.sg_flags["current_stage"] = "nric_check"
            resume.sg_flags["analysis_progress"] = 0.5

            # Stage 3: SG Flags (0.6 → 0.8)
            resume.sg_flags["current_stage"] = "sg_flags"
            resume.sg_flags["analysis_progress"] = 0.7

            # Extract SG flags
            sg_flags = extract_sg_flags(masked_text)
            resume.sg_flags.update({
                "has_nric": sg_flags.has_nric,
                "has_photo": sg_flags.has_photo,
                "ns_quality": sg_flags.ns_quality,
                "ns_status": sg_flags.ns_status,
                "education_tier": sg_flags.education_tier,
                "pmet_signals": sg_flags.pmet_signals,
                "is_pmet": sg_flags.is_pmet,
            })

            # Stage 4: Claude Parsing (0.8 → 0.9)
            resume.sg_flags["current_stage"] = "claude_parsing"
            resume.sg_flags["analysis_progress"] = 0.8
            await db.commit()

            # Parse with Claude
            try:
                parsed_resume = await parse_resume_with_claude(masked_text, resume.content_hash)

                # Store parsed data
                resume.parsed_json = resume.parsed_json or {}
                resume.parsed_json["parsed"] = True
                resume.parsed_json["parsed_data"] = {
                    "contact": parsed_resume.contact,
                    "summary": parsed_resume.summary,
                    "experience": parsed_resume.experience,
                    "education": parsed_resume.education,
                    "skills": parsed_resume.skills,
                    "certifications": parsed_resume.certifications,
                    "ns_status": parsed_resume.ns_status,
                }
                resume.parsed_json["parsed_at"] = datetime.utcnow().isoformat()
            except ResumeParseError as e:
                logger.warning("resume_claude_parse_failed", resume_id=str(resume_id), error=str(e))
                # Continue even if Claude parsing fails - SG flags are more important

            # Stage 5: Ready (0.9 → 1.0)
            resume.sg_flags["current_stage"] = "ready"
            resume.sg_flags["analysis_status"] = "ready"
            resume.sg_flags["analysis_progress"] = 1.0
            resume.sg_flags["analysis_error"] = None
            await db.commit()

            logger.info("resume_analysis_complete", resume_id=str(resume_id), user_id=user_id)

        except Exception as e:
            logger.error("resume_analysis_failed", resume_id=str(resume_id), error=str(e))
            # Update error status
            try:
                result = await db.execute(
                    select(Resume).where(Resume.id == resume_id)
                )
                resume = result.scalar_one_or_none()
                if resume:
                    resume.sg_flags = resume.sg_flags or {}
                    resume.sg_flags["analysis_status"] = "error"
                    resume.sg_flags["analysis_error"] = str(e)
                    await db.commit()
            except Exception:
                pass


# =============================================================================
# SSE PROGRESS STREAMING (M2.4)
# =============================================================================


@router.get("/resumes/{resume_id}/analysis/stream")
async def stream_analysis_progress(
    resume_id: uuid.UUID,
    user: AuthUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Stream analysis progress via SSE (M2.4).

    SSE events:
    - stage: current processing stage
    - progress: progress percentage (0-100)
    - complete: when analysis is done
    - error: if analysis fails

    Args:
        resume_id: UUID of the uploaded resume
        user: Authenticated user
        db: Database session

    Returns:
        StreamingResponse with SSE events
    """
    # Verify resume exists and belongs to user
    result = await db.execute(
        select(Resume).where(
            Resume.id == resume_id,
            Resume.user_id == user.job_seeker_id,
        )
    )
    resume = result.scalar_one_or_none()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    async def event_generator() -> AsyncGenerator[str, None]:
        """Generate SSE events for analysis progress."""
        stages = ["parsing", "nric_check", "sg_flags", "claude_parsing", "ready"]
        last_stage_idx = -1

        while True:
            # Fetch current status
            result = await db.execute(
                select(Resume).where(Resume.id == resume_id)
            )
            resume = result.scalar_one_or_none()
            if not resume:
                yield _sse_event("error", {"message": "Resume not found"})
                break

            current_flags = resume.sg_flags or {}
            current_stage = current_flags.get("current_stage", "pending")
            status = current_flags.get("analysis_status", "pending")
            progress = current_flags.get("analysis_progress", 0.0)

            # Find current stage index
            try:
                stage_idx = stages.index(current_stage) if current_stage in stages else -1
            except ValueError:
                stage_idx = -1

            # Check for completion or error
            if status == "ready":
                yield _sse_event("complete", {
                    "resume_id": str(resume_id),
                    "progress": 100,
                })
                break

            if status == "error":
                error_msg = current_flags.get("analysis_error", "Unknown error")
                yield _sse_event("error", {"message": error_msg})
                break

            # Send progress update if stage changed
            if stage_idx > last_stage_idx:
                yield _sse_event("stage", {
                    "stage": current_stage,
                    "progress": int(progress * 100),
                    "message": f"Processing: {current_stage}",
                })
                last_stage_idx = stage_idx
            elif int(progress * 100) % 10 == 0:
                # Send periodic progress
                yield _sse_event("progress", {
                    "stage": current_stage,
                    "progress": int(progress * 100),
                })

            # Poll interval
            await asyncio.sleep(0.5)

        yield _sse_event("done", {})

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # Disable nginx buffering
        },
    )


def _sse_event(event_type: str, data: dict) -> str:
    """Format SSE event."""
    return f"event: {event_type}\ndata: {json.dumps(data)}\n\n"


def _extract_sg_flags_from_text(text: str) -> dict:
    """Extract Singapore-specific flags from resume content."""
    flags = extract_sg_flags(text)
    return {
        "has_nric": flags.has_nric,
        "has_photo": flags.has_photo,
        "ns_quality": flags.ns_quality,
        "ns_mentioned": flags.ns_quality != "not_mentioned",
        "education_tier": flags.education_tier,
        "pmet_signals": flags.pmet_signals,
        "is_pmet": flags.is_pmet,
    }


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

    # Check AI processing consent before Claude API call
    consent_service = ConsentService(db)
    if not await consent_service.check_ai_processing(user.job_seeker_id):
        raise HTTPException(
            status_code=403,
            detail="AI processing consent required. Please grant AI processing consent to use this feature."
        )

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

    # Stage 2: Assert no NRIC before sending to Claude API
    assert_no_nric(text)

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
# M3.5: JOB ANALYSIS ENDPOINT (Async with SSE Progress)
# =============================================================================


class JobAnalysisRequest(BaseModel):
    """Request for full job analysis pipeline."""
    url: Optional[str] = None
    text: Optional[str] = None
    resume_id: uuid.UUID


class JobAnalysisStatusResponse(BaseModel):
    """Response for job analysis status."""
    job_analysis_id: uuid.UUID
    status: str  # "pending" | "fetching" | "parsing" | "classifying" | "assessing" | "ready" | "error"
    progress: float  # 0.0 to 1.0
    stages: list[str]
    current_stage: Optional[str]
    error: Optional[str]


class JobAnalysisResponse(BaseModel):
    """Response for completed job analysis."""
    job_analysis_id: uuid.UUID
    job_title: Optional[str] = None
    company_name: Optional[str] = None
    company_type: Optional[str] = None
    seniority_level: Optional[str] = None
    industry: Optional[str] = None
    requirements: list[str]
    responsibilities: list[str]
    benefits: list[str]
    match_assessment: Optional[dict] = None
    overall_match_score: Optional[float] = None
    created_at: datetime


@router.post("/job-analyses", response_model=JobAnalysisResponse)
async def create_job_analysis(
    request: JobAnalysisRequest,
    http_request: Request,
    user: AuthUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """M3.5: Full job analysis pipeline with SSE progress streaming.

    Pipeline: URL fetch → JD parse → Company classify → Match assess

    Args:
        request: JobAnalysisRequest with url OR text, and resume_id
        user: Authenticated user
        db: Database session

    Returns:
        JobAnalysisResponse with parsed JD and match assessment
    """
    # Rate limit by user (M3.6)
    tier_key = user.subscription_tier or "free"
    check_rate_limit(str(user.job_seeker_id), tier_key)

    # Check AI processing consent before Claude API call
    consent_service = ConsentService(db)
    if not await consent_service.check_ai_processing(user.job_seeker_id):
        raise HTTPException(
            status_code=403,
            detail="AI processing consent required. Please grant AI processing consent to use this feature."
        )

    if not request.url and not request.text:
        raise HTTPException(
            status_code=400,
            detail="Either url or text must be provided"
        )

    # Get resume
    resume_result = await db.execute(
        select(Resume).where(Resume.id == request.resume_id, Resume.user_id == user.job_seeker_id)
    )
    resume = resume_result.scalar_one_or_none()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    # Get resume text for matching
    resume_content = resume.parsed_json if resume.parsed_json else {}
    resume_text = resume_content.get("text", resume_content.get("filename", ""))
    if not resume_text:
        # Try to get from S3
        try:
            from keystone.services.s3 import get_resume_from_s3
            raw_content = await get_resume_from_s3(resume.s3_key)
            resume_text_obj = await extract_resume_text(raw_content, resume.parsed_json.get("filename", "resume.pdf"))
            resume_text = resume_text_obj.text
        except Exception as e:
            logger.error("resume_re-extraction_failed", resume_id=str(request.resume_id), error=str(e))
            raise HTTPException(status_code=500, detail="Failed to extract resume text")

    # Step 1: Fetch JD (M3.1)
    raw_jd_text: str
    source_url: Optional[str] = None

    if request.url:
        try:
            fetch_result = await fetch_jd_from_url(request.url)
            raw_jd_text = fetch_result.text
            source_url = fetch_result.source_url
        except ValueError as e:
            logger.warning("jd_fetch_failed", url=request.url, error=str(e))
            raise HTTPException(status_code=400, detail=str(e))
    else:
        raw_jd_text = request.text
        source_url = None

    # Step 2: Parse JD (M3.2)
    try:
        parsed_jd: ParsedJobDescription = await parse_job_description(raw_jd_text)
    except Exception as e:
        logger.error("jd_parse_failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to parse job description: {e}")

    # Step 3: Classify company (M3.3)
    company_classification = classify_company(parsed_jd.company_name)
    company_type = company_classification.company_type

    # Step 4: Assess match (M3.4)
    match_assessment: Optional[MatchAssessment] = None
    overall_score: Optional[float] = None

    try:
        match_assessment = await assess_match(
            resume_text=mask_resume_text(resume_text),
            job_requirements=parsed_jd.requirements,
            company_type=company_type,
            seniority_level=parsed_jd.seniority_level,
            industry=parsed_jd.industry,
        )
        overall_score = match_assessment.overall_score
    except Exception as e:
        logger.warning("match_assessment_failed", error=str(e))
        # Continue without match assessment - don't fail the whole pipeline

    # Store job analysis
    job_analysis = JobAnalysis(
        id=uuid.uuid4(),
        user_id=user.job_seeker_id,
        resume_id=request.resume_id,
        job_url=source_url,
        job_parsed_json={
            **parsed_to_dict(parsed_jd),
            "company_type": company_type,
            "company_type_confidence": company_classification.confidence,
            "company_type_method": company_classification.classification_method,
        },
        company_type=company_type,
        match_results=assessment_to_dict(match_assessment) if match_assessment else None,
        created_at=datetime.utcnow(),
    )
    db.add(job_analysis)
    await db.commit()
    await db.refresh(job_analysis)

    logger.info(
        "job_analysis.complete",
        job_analysis_id=str(job_analysis.id),
        job_title=parsed_jd.job_title,
        company=parsed_jd.company_name,
        company_type=company_type,
        match_score=overall_score,
    )

    return JobAnalysisResponse(
        job_analysis_id=job_analysis.id,
        job_title=parsed_jd.job_title,
        company_name=parsed_jd.company_name,
        company_type=company_type,
        seniority_level=parsed_jd.seniority_level,
        industry=parsed_jd.industry,
        requirements=parsed_jd.requirements,
        responsibilities=parsed_jd.responsibilities,
        benefits=parsed_jd.benefits,
        match_assessment=assessment_to_dict(match_assessment) if match_assessment else None,
        overall_match_score=overall_score,
        created_at=job_analysis.created_at,
    )


@router.get("/job-analyses/{job_analysis_id}/stream")
async def stream_job_analysis_progress(
    job_analysis_id: uuid.UUID,
    user: AuthUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Stream job analysis progress via SSE (M3.5).

    SSE events:
    - stage: current processing stage
    - progress: progress percentage (0-100)
    - complete: when analysis is done
    - error: if analysis fails

    Note: This endpoint is for real-time progress monitoring.
    The actual analysis runs synchronously in create_job_analysis.
    """
    # Verify job analysis exists and belongs to user
    result = await db.execute(
        select(JobAnalysis).where(
            JobAnalysis.id == job_analysis_id,
            JobAnalysis.user_id == user.job_seeker_id,
        )
    )
    job_analysis = result.scalar_one_or_none()
    if not job_analysis:
        raise HTTPException(status_code=404, detail="Job analysis not found")

    async def event_generator() -> AsyncGenerator[str, None]:
        """Generate SSE events for job analysis progress."""
        stages = ["fetching", "parsing", "classifying", "assessing", "ready"]
        last_stage_idx = -1

        # Since analysis is synchronous, we'll send a quick progression
        for i, stage in enumerate(stages):
            yield _sse_event("stage", {
                "stage": stage,
                "progress": int((i / len(stages)) * 100),
                "message": f"Processing: {stage}",
            })
            await asyncio.sleep(0.1)  # Brief delay between stages

        # Send completion
        yield _sse_event("complete", {
            "job_analysis_id": str(job_analysis_id),
            "progress": 100,
        })
        yield _sse_event("done", {})

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@router.get("/job-analyses/{job_analysis_id}", response_model=JobAnalysisResponse)
async def get_job_analysis(
    job_analysis_id: uuid.UUID,
    user: AuthUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get job analysis by ID."""
    result = await db.execute(
        select(JobAnalysis).where(
            JobAnalysis.id == job_analysis_id,
            JobAnalysis.user_id == user.job_seeker_id,
        )
    )
    job_analysis = result.scalar_one_or_none()
    if not job_analysis:
        raise HTTPException(status_code=404, detail="Job analysis not found")

    parsed_json = job_analysis.job_parsed_json or {}
    match_results = job_analysis.match_results

    return JobAnalysisResponse(
        job_analysis_id=job_analysis.id,
        job_title=parsed_json.get("job_title"),
        company_name=parsed_json.get("company_name"),
        company_type=job_analysis.company_type,
        seniority_level=parsed_json.get("seniority_level"),
        industry=parsed_json.get("industry"),
        requirements=parsed_json.get("requirements", []),
        responsibilities=parsed_json.get("responsibilities", []),
        benefits=parsed_json.get("benefits", []),
        match_assessment=match_results,
        overall_match_score=match_results.get("overall_score") if match_results else None,
        created_at=job_analysis.created_at,
    )


@router.get("/job-analyses", response_model=list[JobAnalysisResponse])
async def list_job_analyses(
    user: AuthUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 50,
):
    """List all job analyses for the current user."""
    result = await db.execute(
        select(JobAnalysis)
        .where(JobAnalysis.user_id == user.job_seeker_id)
        .order_by(JobAnalysis.created_at.desc())
        .offset(skip)
        .limit(min(limit, 100))
    )
    job_analyses = result.scalars().all()

    return [
        JobAnalysisResponse(
            job_analysis_id=ja.id,
            job_title=ja.job_parsed_json.get("job_title") if ja.job_parsed_json else None,
            company_name=ja.job_parsed_json.get("company_name") if ja.job_parsed_json else None,
            company_type=ja.company_type,
            seniority_level=ja.job_parsed_json.get("seniority_level") if ja.job_parsed_json else None,
            industry=ja.job_parsed_json.get("industry") if ja.job_parsed_json else None,
            requirements=ja.job_parsed_json.get("requirements", []) if ja.job_parsed_json else [],
            responsibilities=ja.job_parsed_json.get("responsibilities", []) if ja.job_parsed_json else [],
            benefits=ja.job_parsed_json.get("benefits", []) if ja.job_parsed_json else [],
            match_assessment=ja.match_results,
            overall_match_score=ja.match_results.get("overall_score") if ja.match_results else None,
            created_at=ja.created_at,
        )
        for ja in job_analyses
    ]


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

    # Check AI processing consent before Claude API call
    consent_service = ConsentService(db)
    if not await consent_service.check_ai_processing(user.job_seeker_id):
        raise HTTPException(
            status_code=403,
            detail="AI processing consent required. Please grant AI processing consent to use this feature."
        )

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

    # Stage 2: Assert no NRIC before sending to Claude API
    assert_no_nric(resume_text)

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

    # Stage 3: Sanitize Claude output before storing
    sanitized_response = mask_nric(response.content)

    # Store match results
    job.match_results = {"assessment": sanitized_response}
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
# SUGGESTIONS (Job-Analyses specific - M4.1, M4.3, M4.4)
# =============================================================================


@router.post("/job-analyses/{job_id}/suggestions", response_model=SuggestionListResponse)
async def generate_job_analysis_suggestions(
    job_id: uuid.UUID,
    resume_id: uuid.UUID,
    user: AuthUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Generate line-by-line revision suggestions for a job analysis.

    M4.1: Uses Claude Sonnet for high-quality suggestions with SG context.
    M4.3: Free tier gating - first JD unlimited, subsequent JDs first 3 + gated.
    M4.4: LLM cost ceiling tracking with graceful degradation.
    """
    from keystone.services.claude_client import ClaudeResponse
    from keystone.services.circuit_breaker import CircuitBreakerError
    from keystone.services.llm_cost_tracker import get_llm_cost_tracker
    from keystone.services.suggestion_generator import (
        _build_suggestion_prompt,
        _SUGGESTION_SYSTEM_PROMPT,
        parse_suggestions_from_response,
    )

    settings = get_settings()
    cost_tracker = get_llm_cost_tracker()

    # Check AI processing consent before Claude API call
    consent_service = ConsentService(db)
    if not await consent_service.check_ai_processing(user.job_seeker_id):
        raise HTTPException(
            status_code=403,
            detail="AI processing consent required. Please grant AI processing consent to use this feature."
        )

    client = get_claude_client()

    # Get job analysis
    job_result = await db.execute(
        select(JobAnalysis).where(
            JobAnalysis.id == job_id,
            JobAnalysis.user_id == user.job_seeker_id,
        )
    )
    job = job_result.scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=404, detail="Job analysis not found")

    # Get resume for context
    resume_result = await db.execute(
        select(Resume).where(
            Resume.id == resume_id,
            Resume.user_id == user.job_seeker_id,
        )
    )
    resume = resume_result.scalar_one_or_none()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    resume_text = resume.parsed_json.get("text", "") if resume.parsed_json else ""
    sg_flags = resume.sg_flags or {}

    # Check cost ceiling BEFORE generating (M4.4)
    user_cost_status = cost_tracker.get_cost_status(str(user.job_seeker_id))
    if user_cost_status["ceiling_reached"]:
        logger.warning(
            "suggestions_cost_ceiling_reached",
            user_id=str(user.job_seeker_id),
            cost_sgd=user_cost_status["current_cost_sgd"],
        )
        # Return cached or simplified response
        return await _get_cached_or_degraded_suggestions(job_id, job, db)

    # Check free tier gating (M4.3) - is this the user's first JD?
    is_first_jd = await _is_users_first_job_analysis(user.job_seeker_id, job_id, db)
    tier = user.subscription_tier or SubscriptionTier.FREE

    # Count existing suggestions for this job analysis
    existing_suggestions_result = await db.execute(
        select(Suggestion).where(Suggestion.job_analysis_id == job_id)
    )
    existing_suggestions = existing_suggestions_result.scalars().all()
    existing_count = len(existing_suggestions)

    # Pro user: no gating
    if tier == SubscriptionTier.PRO:
        if existing_count > 0:
            # Return cached suggestions
            return _build_suggestion_response(list(existing_suggestions), False, 0, None)

        # Generate new suggestions
        suggestions = await _generate_and_store_suggestions(
            job, resume_text, sg_flags, client, settings, cost_tracker, str(user.job_seeker_id), db
        )
        return _build_suggestion_response(suggestions, False, 0, None)

    # Free user: check if first JD
    if is_first_jd:
        # First JD = unlimited suggestions
        if existing_count > 0:
            return _build_suggestion_response(list(existing_suggestions), False, 0, None)

        suggestions = await _generate_and_store_suggestions(
            job, resume_text, sg_flags, client, settings, cost_tracker, str(user.job_seeker_id), db
        )
        return _build_suggestion_response(suggestions, False, 0, None)

    # Free user, not first JD: gate at 3 suggestions
    FREE_TIER_VISIBLE = 3

    if existing_count >= FREE_TIER_VISIBLE:
        # Already have enough, return first 3 + gated
        visible = list(existing_suggestions)[:FREE_TIER_VISIBLE]
        gated_count = existing_count - FREE_TIER_VISIBLE
        gate_context = _build_gate_context(job, visible)

        return SuggestionListResponse(
            suggestions=[_to_gated_response(s) for s in visible],
            gated=True,
            gated_count=gated_count,
            gate_context=gate_context,
        )

    if existing_count > 0 and existing_count < FREE_TIER_VISIBLE:
        # Partial existing - return what we have + gated indicator
        gated_count = max(0, FREE_TIER_VISIBLE - existing_count)
        gate_context = _build_gate_context(job, list(existing_suggestions))

        return SuggestionListResponse(
            suggestions=[_to_gated_response(s) for s in existing_suggestions],
            gated=True,
            gated_count=gated_count,
            gate_context=gate_context,
        )

    # Need to generate
    suggestions = await _generate_and_store_suggestions(
        job, resume_text, sg_flags, client, settings, cost_tracker, str(user.job_seeker_id), db
    )

    if len(suggestions) <= FREE_TIER_VISIBLE:
        # All visible (not many generated)
        return _build_suggestion_response(suggestions, False, 0, None)

    # Gate excess suggestions
    visible = suggestions[:FREE_TIER_VISIBLE]
    gated = suggestions[FREE_TIER_VISIBLE:]
    gated_count = len(gated)
    gate_context = _build_gate_context(job, visible)

    logger.info(
        "suggestions_gated",
        user_id=str(user.job_seeker_id),
        job_id=str(job_id),
        visible=len(visible),
        gated=gated_count,
    )

    return SuggestionListResponse(
        suggestions=[_to_gated_response(s) for s in visible],
        gated=True,
        gated_count=gated_count,
        gate_context=gate_context,
    )


async def _is_users_first_job_analysis(
    user_id: uuid.UUID,
    current_job_id: uuid.UUID,
    db: AsyncSession,
) -> bool:
    """Check if this is the user's first job analysis."""
    result = await db.execute(
        select(JobAnalysis).where(
            JobAnalysis.user_id == user_id,
            JobAnalysis.id != current_job_id,
        )
    )
    existing = result.scalars().first()
    return existing is None


def _build_gate_context(job: JobAnalysis, visible_suggestions: list) -> str:
    """Build the gate context string describing what was shown."""
    sections = list(set(s.section for s in visible_suggestions))
    sections_str = ", ".join(sections) if sections else "various sections"

    # Calculate JD coverage based on match results
    coverage_pct = 0
    if job.match_results and "levels" in job.match_results:
        levels = job.match_results.get("levels", {})
        if levels:
            total = len(levels)
            covered = sum(1 for l in levels.values() if l != "fundamental")
            coverage_pct = int((covered / total) * 100) if total > 0 else 0

    return f"{sections_str}, JD coverage {coverage_pct}%"


def _to_gated_response(suggestion: Suggestion) -> GatedSuggestionResponse:
    """Convert a Suggestion to GatedSuggestionResponse."""
    return GatedSuggestionResponse(
        id=suggestion.id,
        section=suggestion.section,
        original_text=suggestion.original_text,
        suggested_text=suggestion.suggested_text,
        rationale=suggestion.rationale,
        match_level=suggestion.match_level,
        created_at=suggestion.created_at,
        gated=False,
    )


def _build_suggestion_response(
    suggestions: list,
    gated: bool,
    gated_count: int,
    gate_context: Optional[str],
) -> SuggestionListResponse:
    """Build SuggestionListResponse from list of Suggestion objects."""
    return SuggestionListResponse(
        suggestions=[_to_gated_response(s) for s in suggestions],
        gated=gated,
        gated_count=gated_count,
        gate_context=gate_context,
    )


async def _generate_and_store_suggestions(
    job: JobAnalysis,
    resume_text: str,
    sg_flags: dict,
    client,
    settings,
    cost_tracker,
    user_id: str,
    db: AsyncSession,
) -> list[Suggestion]:
    """Generate suggestions using Claude Sonnet and store them."""
    from keystone.services.claude_client import ClaudeResponse
    from keystone.services.circuit_breaker import CircuitBreakerError
    from keystone.services.suggestion_generator import (
        _build_suggestion_prompt,
        _SUGGESTION_SYSTEM_PROMPT,
        parse_suggestions_from_response,
    )

    # Stage 2: Assert no NRIC before sending to Claude API
    assert_no_nric(resume_text)

    try:
        prompt = _build_suggestion_prompt(
            resume_text=resume_text,
            job_parsed_json=job.job_parsed_json or {},
            company_type=job.company_type,
            sg_flags=sg_flags,
        )

        response: ClaudeResponse = await client.generate(
            model=settings.anthropic_model_sonnet,
            system_prompt=_SUGGESTION_SYSTEM_PROMPT,
            user_prompt=prompt,
            max_tokens=4096,
        )

        # Track cost (M4.4)
        cost_tracker.add_cost(
            user_id=user_id,
            model=settings.anthropic_model_sonnet,
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
        )

        # Stage 3: Sanitize Claude output before parsing/storing
        sanitized_content = mask_nric(response.content)

        # Parse suggestions
        suggestions = parse_suggestions_from_response(sanitized_content, job.id)

        # Store suggestions
        for sugg in suggestions:
            db.add(sugg)
        await db.commit()

        logger.info(
            "suggestions_generated",
            job_id=str(job.id),
            user_id=user_id,
            count=len(suggestions),
            cost_sgd=response.usage.cost_sgd,
        )

        return suggestions

    except CircuitBreakerError:
        raise HTTPException(status_code=503, detail="AI service temporarily unavailable")


async def _get_cached_or_degraded_suggestions(
    job_id: uuid.UUID,
    job: JobAnalysis,
    db: AsyncSession,
) -> SuggestionListResponse:
    """Return cached suggestions or degraded response when cost ceiling is reached."""
    # Try to get existing cached suggestions
    result = await db.execute(
        select(Suggestion).where(Suggestion.job_analysis_id == job_id)
    )
    existing = result.scalars().all()

    if existing:
        # Return first 3 cached suggestions (free tier behavior)
        visible = list(existing)[:3]
        return SuggestionListResponse(
            suggestions=[_to_gated_response(s) for s in visible],
            gated=True,
            gated_count=max(0, len(existing) - 3),
            gate_context="Cost ceiling reached. Upgrade to Pro for unlimited suggestions.",
        )

    # No cached suggestions - return empty with degraded message
    return SuggestionListResponse(
        suggestions=[],
        gated=True,
        gated_count=0,
        gate_context="Cost ceiling reached. Upgrade to Pro for new suggestions.",
    )


# =============================================================================
# LEGACY SUGGESTIONS ENDPOINT (kept for backwards compatibility)
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

    # Check AI processing consent before Claude API call
    consent_service = ConsentService(db)
    if not await consent_service.check_ai_processing(user.job_seeker_id):
        raise HTTPException(
            status_code=403,
            detail="AI processing consent required. Please grant AI processing consent to use this feature."
        )

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

    # Stage 2: Assert no NRIC before sending to Claude API (on job data)
    import json
    assert_no_nric(json.dumps(job.job_parsed_json))

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

    # Stage 3: Sanitize Claude output before parsing/storing
    sanitized_content = mask_nric(response.content)

    # Parse suggestions (simplified - real implementation would parse JSON)
    suggestions = _parse_suggestions(sanitized_content, request.job_analysis_id)

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
    # Parse applied_at date if provided
    applied_date = None
    if request.applied_at:
        try:
            applied_date = datetime.fromisoformat(request.applied_at.replace("Z", "+00:00"))
        except ValueError:
            pass

    application = Application(
        id=uuid.uuid4(),
        user_id=user.job_seeker_id,
        job_analysis_id=request.job_analysis_id,
        suggestion_set_id=request.suggestion_set_id,
        employer=request.employer,
        role=request.role,
        job_url=request.job_url,
        applied_date=applied_date,
        status=ApplicationStatus.APPLIED if request.status == "applied" else ApplicationStatus.INTERESTED,
        stages=[],
        notes=request.notes,
    )
    db.add(application)
    await db.commit()
    await db.refresh(application)

    logger.info(
        "application.created",
        application_id=str(application.id),
        user_id=str(user.job_seeker_id),
        employer=request.employer,
        role=request.role,
    )

    return ApplicationResponse(
        id=application.id,
        employer=application.employer,
        role=application.role,
        status=application.status.value if hasattr(application.status, 'value') else str(application.status),
        stages=application.stages or [],
        created_at=application.created_at,
        job_url=application.job_url,
        applied_at=application.applied_date.isoformat() if application.applied_date else None,
        suggestion_set_id=application.suggestion_set_id,
    )


@router.get("/applications", response_model=list[ApplicationResponse])
async def list_applications(
    user: AuthUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
):
    """List applications for the current user with optional status filter and pagination.

    Args:
        status: Filter by application status (INTERESTED, APPLIED, SCREENING, INTERVIEW, OFFER, REJECTED, WITHDRAWN)
        skip: Number of records to skip (for pagination)
        limit: Maximum number of records to return (default 50, max 100)
    """
    query = select(Application).where(Application.user_id == user.job_seeker_id)

    if status:
        try:
            status_enum = ApplicationStatus(status)
            query = query.where(Application.status == status_enum)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid status: {status}. Must be one of: {[s.value for s in ApplicationStatus]}"
            )

    query = query.order_by(Application.created_at.desc()).offset(skip).limit(min(limit, 100))

    result = await db.execute(query)
    applications = result.scalars().all()

    return [
        ApplicationResponse(
            id=a.id,
            employer=a.employer,
            role=a.role,
            status=a.status.value if hasattr(a.status, 'value') else str(a.status),
            stages=a.stages or [],
            created_at=a.created_at,
            job_url=a.job_url,
            applied_at=a.applied_date.isoformat() if a.applied_date else None,
            suggestion_set_id=a.suggestion_set_id,
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
        status=application.status.value if hasattr(application.status, 'value') else str(application.status),
        stages=application.stages or [],
        created_at=application.created_at,
        job_url=application.job_url,
        applied_at=application.applied_date.isoformat() if application.applied_date else None,
        suggestion_set_id=application.suggestion_set_id,
    )


@router.patch("/applications/{application_id}", response_model=ApplicationResponse)
async def update_application(
    application_id: uuid.UUID,
    request: ApplicationUpdateRequest,
    user: AuthUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update application status/outcome/notes."""
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
        application.status = ApplicationStatus(request.status)
    if request.final_outcome:
        application.final_outcome = request.final_outcome
    if request.notes is not None:
        application.notes = request.notes

    application.last_activity_at = datetime.utcnow()
    application.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(application)

    logger.info(
        "application.updated",
        application_id=str(application_id),
        user_id=str(user.job_seeker_id),
        status=request.status,
    )

    return ApplicationResponse(
        id=application.id,
        employer=application.employer,
        role=application.role,
        status=application.status.value if hasattr(application.status, 'value') else str(application.status),
        stages=application.stages or [],
        created_at=application.created_at,
        job_url=application.job_url,
        applied_at=application.applied_date.isoformat() if application.applied_date else None,
    )


@router.delete("/applications/{application_id}")
async def delete_application(
    application_id: uuid.UUID,
    user: AuthUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Soft delete an application (sets auto_closed_at).

    The application is marked as closed rather than being permanently deleted.
    """
    result = await db.execute(
        select(Application).where(
            Application.id == application_id,
            Application.user_id == user.job_seeker_id,
        )
    )
    application = result.scalar_one_or_none()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    application.auto_closed_at = datetime.utcnow()
    application.last_activity_at = datetime.utcnow()
    await db.commit()

    logger.info(
        "application.deleted",
        application_id=str(application_id),
        user_id=str(user.job_seeker_id),
    )

    return {"status": "deleted", "application_id": str(application_id)}


# =============================================================================
# STAGE PROGRESSION
# =============================================================================


class StageAdvanceRequest(BaseModel):
    stage_type: str  # response|screening|interview|final|offer|rejection|withdrawal
    round_number: Optional[int] = None  # 1-5 for interviews
    format: Optional[str] = None  # email|phone|video|in-person|assessment_centre|panel|technical|case
    outcome: Optional[str] = None  # passed|failed|pending
    stage_date: Optional[datetime] = None
    notes: Optional[str] = None


class StageResponse(BaseModel):
    id: uuid.UUID
    stage_type: str
    round_number: Optional[int]
    format: Optional[str]
    outcome: Optional[str]
    stage_date: Optional[datetime]
    notes: Optional[str]
    created_at: datetime


class StageEditRequest(BaseModel):
    """Request model for editing an existing stage."""
    stage_type: Optional[str] = None
    round_number: Optional[int] = None
    format: Optional[str] = None
    outcome: Optional[str] = None
    stage_date: Optional[datetime] = None
    notes: Optional[str] = None


@router.post("/applications/{application_id}/stages", response_model=StageResponse)
async def advance_stage(
    application_id: uuid.UUID,
    request: StageAdvanceRequest,
    user: AuthUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Record a stage advancement event for an application."""
    from keystone.models.entities import ApplicationStage

    # Verify application exists and belongs to user
    result = await db.execute(
        select(Application).where(
            Application.id == application_id,
            Application.user_id == user.job_seeker_id,
        )
    )
    application = result.scalar_one_or_none()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    # Create stage event
    stage_event = ApplicationStage(
        application_id=application_id,
        stage_type=request.stage_type,
        round_number=request.round_number,
        format=request.format,
        outcome=request.outcome,
        stage_date=request.stage_date or datetime.utcnow(),
        notes=request.notes,
    )
    db.add(stage_event)

    # Update application's stages JSON for quick access (keep in sync with table)
    current_stages = application.stages or []
    current_stages.append({
        "id": str(stage_event.id),
        "stage_type": request.stage_type,
        "round_number": request.round_number,
        "format": request.format,
        "outcome": request.outcome,
        "stage_date": (request.stage_date or datetime.utcnow()).isoformat(),
        "notes": request.notes,
    })
    application.stages = current_stages
    application.last_activity_at = datetime.utcnow()

    await db.commit()
    await db.refresh(stage_event)

    logger.info(
        "stage.advanced",
        application_id=str(application_id),
        stage_type=request.stage_type,
        round_number=request.round_number,
        user_id=str(user.job_seeker_id),
    )

    return StageResponse(
        id=stage_event.id,
        stage_type=stage_event.stage_type,
        round_number=stage_event.round_number,
        format=stage_event.format,
        outcome=stage_event.outcome,
        stage_date=stage_event.stage_date,
        notes=stage_event.notes,
        created_at=stage_event.created_at,
    )


@router.patch("/applications/{application_id}/stages/{stage_id}", response_model=StageResponse)
async def edit_stage(
    application_id: uuid.UUID,
    stage_id: uuid.UUID,
    request: StageEditRequest,
    user: AuthUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Edit an existing stage event for an application."""
    from keystone.models.entities import ApplicationStage

    # Verify application exists and belongs to user
    result = await db.execute(
        select(Application).where(
            Application.id == application_id,
            Application.user_id == user.job_seeker_id,
        )
    )
    application = result.scalar_one_or_none()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    # Find the stage event
    stage_result = await db.execute(
        select(ApplicationStage).where(
            ApplicationStage.id == stage_id,
            ApplicationStage.application_id == application_id,
        )
    )
    stage_event = stage_result.scalar_one_or_none()
    if not stage_event:
        raise HTTPException(status_code=404, detail="Stage not found")

    # Update stage fields if provided
    if request.stage_type is not None:
        stage_event.stage_type = request.stage_type
    if request.round_number is not None:
        stage_event.round_number = request.round_number
    if request.format is not None:
        stage_event.format = request.format
    if request.outcome is not None:
        stage_event.outcome = request.outcome
    if request.stage_date is not None:
        stage_event.stage_date = request.stage_date
    if request.notes is not None:
        stage_event.notes = request.notes

    # Sync to application's stages JSON
    current_stages = application.stages or []
    for i, stage in enumerate(current_stages):
        if stage.get("id") == str(stage_id):
            if request.stage_type is not None:
                current_stages[i]["stage_type"] = request.stage_type
            if request.round_number is not None:
                current_stages[i]["round_number"] = request.round_number
            if request.format is not None:
                current_stages[i]["format"] = request.format
            if request.outcome is not None:
                current_stages[i]["outcome"] = request.outcome
            if request.stage_date is not None:
                current_stages[i]["stage_date"] = request.stage_date.isoformat()
            if request.notes is not None:
                current_stages[i]["notes"] = request.notes
            break
    application.stages = current_stages
    application.last_activity_at = datetime.utcnow()

    await db.commit()
    await db.refresh(stage_event)

    logger.info(
        "stage.edited",
        application_id=str(application_id),
        stage_id=str(stage_id),
        stage_type=request.stage_type,
        user_id=str(user.job_seeker_id),
    )

    return StageResponse(
        id=stage_event.id,
        stage_type=stage_event.stage_type,
        round_number=stage_event.round_number,
        format=stage_event.format,
        outcome=stage_event.outcome,
        stage_date=stage_event.stage_date,
        notes=stage_event.notes,
        created_at=stage_event.created_at,
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


@router.get("/applications/batch-update", response_model=list[NudgeEligibleApplicationResponse])
async def get_batch_update_eligible(
    user: AuthUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    http_request: Request = None,
    days: int = 14,
    limit: int = 50,
):
    """Get applications eligible for batch update (nudge-eligible).

    Returns applications with status IN (applied, screening, interview)
    that have had no activity for the specified number of days.
    """
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

    logger.info(
        "batch_update.eligible",
        user_id=str(user.job_seeker_id),
        count=len(apps),
        days=days,
    )

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


class AutoClosedApplicationResponse(BaseModel):
    id: uuid.UUID
    employer: str
    role: str
    status: str
    auto_closed_at: datetime


@router.get("/applications/auto-closed", response_model=list[AutoClosedApplicationResponse])
async def get_auto_closed_applications(
    user: AuthUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get applications that were auto-closed (for correction banner)."""
    if not user.job_seeker_id:
        raise HTTPException(status_code=401, detail="User not found")

    result = await db.execute(
        select(Application).where(
            Application.user_id == user.job_seeker_id,
            Application.auto_closed_at.isnot(None),
        ).order_by(Application.auto_closed_at.desc())
    )
    applications = result.scalars().all()

    return [
        AutoClosedApplicationResponse(
            id=a.id,
            employer=a.employer,
            role=a.role,
            status=a.status.value if hasattr(a.status, 'value') else str(a.status),
            auto_closed_at=a.auto_closed_at,
        )
        for a in applications
    ]


@router.post("/applications/batch-update/mark-all-no-news")
async def mark_all_no_news_batch(
    user: AuthUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    http_request: Request = None,
):
    """Mark all nudge-eligible applications as 'no news' (keep active).

    Alias for /applications/mark-all-no-news for batch-update API consistency.
    """
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

    logger.info(
        "batch_update.mark_all_no_news",
        user_id=str(user.job_seeker_id),
        marked=count,
    )

    return {"marked": count}


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
    _api_key: str = Depends(verify_internal_api_key),
):
    """Auto-close applications with no recent activity.

    Closes applications that are in terminal states (offer/rejected/withdrawn)
    and have had no activity for the specified number of days.
    Callable by AWS EventBridge cron or similar scheduler.
    """
    from keystone.models.entities import ApplicationStage

    cutoff = datetime.utcnow() - timedelta(days=days_inactive)
    # Non-terminal states that should be auto-closed
    active_states = [
        ApplicationStatus.INTERESTED,
        ApplicationStatus.APPLIED,
        ApplicationStatus.SCREENING,
        ApplicationStatus.INTERVIEW,
    ]

    result = await db.execute(
        select(Application).where(
            Application.status.in_(active_states),
            Application.auto_closed_at.is_(None),
            Application.last_activity_at < cutoff,
        )
    )
    apps = result.scalars().all()

    closed = 0
    for app in apps:
        # Set final outcome and status
        app.final_outcome = "no_response"
        app.status = ApplicationStatus.REJECTED  # Map to terminal state
        app.auto_closed_at = datetime.utcnow()
        app.last_activity_at = datetime.utcnow()

        # Write stage event for analytics
        stage_event = ApplicationStage(
            application_id=app.id,
            stage_type="rejection",
            format="inferred_no_response",
            outcome="failed",
            notes="Auto-closed after 30 days of inactivity",
        )
        db.add(stage_event)

        # Also append to stages JSON
        current_stages = app.stages or []
        current_stages.append({
            "stage_type": "rejection",
            "format": "inferred_no_response",
            "outcome": "failed",
            "notes": "Auto-closed after 30 days of inactivity",
            "stage_date": datetime.utcnow().isoformat(),
        })
        app.stages = current_stages
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


class StagePassRates(BaseModel):
    response_rate: float | None  # % of applied that got a response
    screening_rate: float | None  # % of responded that went to screening
    interview_rate: float | None  # % of screened that went to interview
    offer_rate: float | None  # % of interviewed that got offer


class MatchLevelDistribution(BaseModel):
    strong_match_applications: int
    transferable_applications: int
    addressable_applications: int
    fundamental_applications: int
    strong_match_r2_plus_rate: float | None  # % of strong that reached R2+


class EnhancedAnalyticsResponse(BaseModel):
    total_applications: int
    response_rate: float | None  # Only shown after 5+ apps
    pass_rates: StagePassRates
    match_distribution: MatchLevelDistribution
    by_status: dict[str, int]
    by_month: dict[str, int]  # applications by month


class TrackingCompletenessResponse(BaseModel):
    score: float  # 0.0 to 1.0
    tier: str  # neutral|active|strong|complete
    total_applications: int
    logged_outcome: int  # applications with final_outcome
    with_stage_events: int  # applications with stage events
    percentile_rank: str | None  # e.g., "top_30_percent"


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


@router.get("/analytics/tracking-completeness", response_model=TrackingCompletenessResponse)
async def get_tracking_completeness(
    user: AuthUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    http_request: Request = None,
):
    """Get application tracking completeness score.

    Formula: (applications_with_final_outcome_logged + applications_with_stage_events)
             / total_applications_created
    """
    if http_request:
        check_rate_limit(get_client_identifier(http_request), "default")

    if not user.job_seeker_id:
        raise HTTPException(status_code=401, detail="User not found")

    # Get all applications
    result = await db.execute(
        select(Application).where(Application.user_id == user.job_seeker_id)
    )
    all_apps = result.scalars().all()
    total = len(all_apps)

    if total == 0:
        return TrackingCompletenessResponse(
            score=0.0,
            tier="neutral",
            total_applications=0,
            logged_outcome=0,
            with_stage_events=0,
            percentile_rank=None,
        )

    # Count applications with outcome logged
    logged_outcome = sum(1 for a in all_apps if a.final_outcome)

    # Count applications with stage events
    with_stage_events = sum(1 for a in all_apps if a.stages and len(a.stages) > 0)

    # Calculate score
    tracked = logged_outcome + with_stage_events
    score = tracked / total if total > 0 else 0.0

    # Determine tier
    if score >= 1.0:
        tier = "complete"
    elif score >= 0.7:
        tier = "strong"
    elif score >= 0.4:
        tier = "active"
    else:
        tier = "neutral"

    # Placeholder percentile (would need aggregate data from all users)
    percentile_rank = None
    if total >= 10:
        # Mock percentile for now based on score
        if score >= 0.8:
            percentile_rank = "top_20_percent"
        elif score >= 0.6:
            percentile_rank = "top_40_percent"
        elif score >= 0.4:
            percentile_rank = "top_60_percent"
        else:
            percentile_rank = "bottom_40_percent"

    return TrackingCompletenessResponse(
        score=round(score, 2),
        tier=tier,
        total_applications=total,
        logged_outcome=logged_outcome,
        with_stage_events=with_stage_events,
        percentile_rank=percentile_rank,
    )


@router.get("/analytics/enhanced", response_model=EnhancedAnalyticsResponse)
async def get_enhanced_analytics(
    user: AuthUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    http_request: Request = None,
):
    """Get enhanced application analytics including response rate and pass rates.

    Response rate and pass rates are only shown after 5+ applications (per spec).
    """
    if http_request:
        check_rate_limit(get_client_identifier(http_request), "default")

    if not user.job_seeker_id:
        raise HTTPException(status_code=401, detail="User not found")

    # Get all applications
    result = await db.execute(
        select(Application).where(Application.user_id == user.job_seeker_id)
    )
    all_apps = result.scalars().all()
    total = len(all_apps)

    # By status
    by_status: dict[str, int] = {}
    for app in all_apps:
        key = app.status.value if hasattr(app.status, 'value') else str(app.status)
        by_status[key] = by_status.get(key, 0) + 1

    # By month
    by_month: dict[str, int] = {}
    for app in all_apps:
        if app.created_at:
            month_key = app.created_at.strftime("%Y-%m")
            by_month[month_key] = by_month.get(month_key, 0) + 1

    # Calculate stage pass rates from stage events
    # Count apps that have response stage
    apps_with_response = 0
    apps_with_screening = 0
    apps_with_interview = 0
    apps_with_offer = 0

    for app in all_apps:
        if app.stages:
            stage_types = {s.get("stage_type") for s in app.stages if isinstance(s, dict)}
            if "response" in stage_types:
                apps_with_response += 1
            if "screening" in stage_types:
                apps_with_screening += 1
            if "interview" in stage_types:
                apps_with_interview += 1
            if "offer" in stage_types:
                apps_with_offer += 1

    # Calculate rates (only if we have enough data)
    response_rate = None
    screening_rate = None
    interview_rate = None
    offer_rate = None

    if total >= 5:
        if total > 0:
            response_rate = round(apps_with_response / total, 3)
        if apps_with_response > 0:
            screening_rate = round(apps_with_screening / apps_with_response, 3)
        if apps_with_screening > 0:
            interview_rate = round(apps_with_interview / apps_with_screening, 3)
        if apps_with_interview > 0:
            offer_rate = round(apps_with_offer / apps_with_interview, 3)

    # Match level distribution (from job_analysis.match_results)
    strong_count = 0
    transferable_count = 0
    addressable_count = 0
    fundamental_count = 0
    strong_r2_plus = 0

    for app in all_apps:
        if app.job_analysis and app.job_analysis.match_results:
            match_results = app.job_analysis.match_results
            if isinstance(match_results, dict):
                match_level = match_results.get("match_level", "unknown")
            elif isinstance(match_results, list) and len(match_results) > 0:
                # Handle list format
                strong_count += sum(1 for m in match_results if m.get("match_level") == "strong")
                transferable_count += sum(1 for m in match_results if m.get("match_level") == "transferable")
                addressable_count += sum(1 for m in match_results if m.get("match_level") == "addressable")
                fundamental_count += sum(1 for m in match_results if m.get("match_level") == "fundamental")
                continue
            else:
                match_level = "unknown"

            if match_level == "strong":
                strong_count += 1
                # Check if this app reached R2+ (interview stage)
                if app.stages and len([s for s in app.stages if s.get("stage_type") == "interview"]) > 0:
                    strong_r2_plus += 1
            elif match_level == "transferable":
                transferable_count += 1
            elif match_level == "addressable":
                addressable_count += 1
            elif match_level == "fundamental":
                fundamental_count += 1

    strong_r2_rate = round(strong_r2_plus / strong_count, 3) if strong_count > 0 else None

    return EnhancedAnalyticsResponse(
        total_applications=total,
        response_rate=response_rate,
        pass_rates=StagePassRates(
            response_rate=response_rate,
            screening_rate=screening_rate,
            interview_rate=interview_rate,
            offer_rate=offer_rate,
        ),
        match_distribution=MatchLevelDistribution(
            strong_match_applications=strong_count,
            transferable_applications=transferable_count,
            addressable_applications=addressable_count,
            fundamental_applications=fundamental_count,
            strong_match_r2_plus_rate=strong_r2_rate,
        ),
        by_status=by_status,
        by_month=by_month,
    )


# =============================================================================
# ONBOARDING


class OnboardingRequest(BaseModel):
    looking_for: str
    application_count: str


@router.post("/onboarding")
async def submit_onboarding(
    request: OnboardingRequest,
    user: AuthUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Submit onboarding questionnaire answers and detect user persona."""
    # Map looking_for to persona
    persona_map = {
        "fresh_grad": "fresh_graduate",
        "switching": "career_switcher",
        "pmet": "pmet",
        "employed": "employed_exploring",
    }
    persona = persona_map.get(request.looking_for, "unknown")

    # Update user record with persona
    from keystone.models.entities import User
    result = await db.execute(select(User).where(User.id == user.job_seeker_id))
    user_record = result.scalar_one_or_none()
    if user_record:
        user_record.persona = persona
        await db.commit()

    logger.info("onboarding.complete", user_id=str(user.job_seeker_id), persona=persona)
    return {"status": "ok", "persona": persona}


# =============================================================================
# EXPORT
# =============================================================================


class ExportRequest(BaseModel):
    job_analysis_id: str
    format: Literal["pdf", "docx"] = "docx"


@router.post("/export")
async def export_resume(
    request: ExportRequest,
    user: AuthUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Export resume with applied suggestions as PDF or DOCX."""
    from keystone.services.document_export import generate_pdf, generate_docx

    # Fetch suggestions for this job analysis
    suggestions_result = await db.execute(
        select(Suggestion).where(Suggestion.job_analysis_id == request.job_analysis_id)
    )
    suggestions = suggestions_result.scalars().all()

    # Fetch job analysis details
    analysis_result = await db.execute(
        select(JobAnalysis).where(JobAnalysis.id == request.job_analysis_id)
    )
    analysis = analysis_result.scalar_one_or_none()

    if not analysis:
        raise HTTPException(status_code=404, detail="Job analysis not found")

    # Build context
    context = {
        "job_title": analysis.job_title,
        "company": analysis.company,
        "skills": analysis.required_skills or [],
        "suggestions": [
            {
                "section": s.section,
                "original_text": s.original_text,
                "suggested_text": s.suggested_text,
                "match_level": s.match_level,
            }
            for s in suggestions
        ],
    }

    if request.format == "pdf":
        content = generate_pdf(context)
        media_type = "application/pdf"
        ext = "pdf"
    else:
        content = generate_docx(context)
        media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        ext = "docx"

    filename = f"resume_{analysis.job_title or 'export'}.{ext}".replace(" ", "_")

    return Response(
        content=content,
        media_type=media_type,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


# =============================================================================
# SUGGESTIONS

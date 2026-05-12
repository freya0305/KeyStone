"""All SQLAlchemy models for KeyStone.

Includes both Job Seeker and Recruiter (B2B) entities.
RLS (Row-Level Security) must be enforced at database level for B2B tables.
"""
import uuid
from datetime import datetime, date
from enum import Enum as PyEnum
from typing import Optional

from sqlalchemy import (
    Column,
    String,
    Text,
    DateTime,
    Date,
    ForeignKey,
    Integer,
    Boolean,
    Numeric,
    JSON,
    Enum,
    Index,
    CheckConstraint,
    Float,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from keystone.models.base import Base


class SubscriptionTier(str, PyEnum):
    FREE = "free"
    PRO = "pro"


class ApplicationStatus(str, PyEnum):
    INTERESTED = "interested"
    APPLIED = "applied"
    SCREENING = "screening"
    INTERVIEW = "interview"
    OFFER = "offer"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"
    CLOSED = "closed"  # Auto-closed after 60 days of inactivity


class AccessLevel(str, PyEnum):
    ADMIN = "admin"
    MEMBER = "member"


# =============================================================================
# JOB SEEKER MODELS
# =============================================================================


class User(Base):
    """Job seeker user."""

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    clerk_id = Column(String(255), unique=True, nullable=False, index=True)  # Clerk user ID (clerk_xxx)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=True)  # Nullable for OAuth-only
    name = Column(String(255), nullable=False)
    subscription_tier = Column(
        Enum(SubscriptionTier),
        default=SubscriptionTier.FREE,
        nullable=False,
    )
    stripe_customer_id = Column(String(255), unique=True, nullable=True)
    stripe_subscription_id = Column(String(255), nullable=True)
    # Legacy consent flags (superseded by user_consents table)
    consent_pdpa = Column(Boolean, default=False)
    consent_marketing = Column(Boolean, default=False)
    consent_ai_training = Column(Boolean, default=False)
    # Phone verification (for SMS OTP anti-abuse)
    phone_hash = Column(String(64), unique=True, nullable=True)  # SHA256 of phone, for deduplication
    phone_verified = Column(Boolean, default=False)
    phone_verified_at = Column(DateTime, nullable=True)
    # User persona from onboarding questionnaire
    persona = Column(String(50), nullable=True)  # fresh_graduate, career_switcher, pmet, employed_exploring
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login_at = Column(DateTime, nullable=True)  # for weekly digest tracking

    # Gamification fields (P2: engagement flywheel)
    current_streak = Column(Integer, default=0, nullable=False)  # consecutive days with activity
    longest_streak = Column(Integer, default=0, nullable=False)  # all-time best
    last_activity_date = Column(Date, nullable=True)  # last date with application activity
    earned_badges = Column(JSON, default=list, nullable=False)  # list of earned badge IDs

    # Relationships
    resumes = relationship("Resume", back_populates="user", lazy="selectin")
    job_analyses = relationship("JobAnalysis", back_populates="user", lazy="selectin")
    applications = relationship("Application", back_populates="user", lazy="selectin")
    consents = relationship("UserConsent", back_populates="user", lazy="selectin")


class ConsentType(str, PyEnum):
    """Six-type consent architecture."""
    REGISTRATION = "registration"  # mandatory for account creation
    STORAGE = "storage"  # storing resume + application data
    AI_PROCESSING = "ai_processing"  # sending data to Claude API
    B2B_SHARING = "b2b_sharing"  # aggregate data with institutional clients
    OUTCOME_TRACKING = "outcome_tracking"  # storing application outcomes
    MARKETING = "marketing"  # newsletters + promotional emails
    AI_TRAINING = "ai_training"  # B2C only: feedback used for model improvement


class UserConsent(Base):
    """Per-user per-type consent state — six-type consent architecture."""

    __tablename__ = "user_consents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    consent_type = Column(Enum(ConsentType), nullable=False)
    granted_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    revoked_at = Column(DateTime, nullable=True)  # NULL means currently granted

    # Relationships
    user = relationship("User", back_populates="consents")

    __table_args__ = (
        Index("ix_user_consents_user_id", "user_id"),
        Index("ix_user_consents_user_type", "user_id", "consent_type", unique=True),
    )


class Resume(Base):
    """Uploaded resume."""

    __tablename__ = "resumes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    content_hash = Column(String(64), nullable=False, index=True)  # SHA256 of content
    parsed_json = Column(JSON, nullable=True)  # Structured resume data
    sg_flags = Column(JSON, nullable=True)  # SG-specific flags (NS-related, etc.)
    s3_key = Column(String(512), nullable=True)  # S3 path to original file
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="resumes")
    job_analyses = relationship("JobAnalysis", back_populates="resume", lazy="selectin")

    __table_args__ = (
        Index("ix_resumes_user_id", "user_id"),
        Index("ix_resumes_content_hash", "content_hash"),
    )


class AnalyzedJob(Base):
    """Track which JDs a user has already analyzed (for free tier gating).

    Uses job_url_hash to identify unique job postings - the same job URL
    analyzed multiple times counts as a single analyzed job.
    """

    __tablename__ = "analyzed_jobs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    job_url_hash = Column(String(64), nullable=False, index=True)  # SHA256 of normalized job URL
    job_title = Column(String(500), nullable=True)
    analyzed_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (
        UniqueConstraint("user_id", "job_url_hash", name="uq_analyzed_jobs_user_url"),
        Index("ix_analyzed_jobs_user_id", "user_id"),
        Index("ix_analyzed_jobs_job_url_hash", "job_url_hash"),
    )


class JobAnalysis(Base):
    """Analysis of resume against a job posting."""

    __tablename__ = "job_analyses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    resume_id = Column(UUID(as_uuid=True), ForeignKey("resumes.id"), nullable=True)
    job_url = Column(Text, nullable=True)
    job_parsed_json = Column(JSON, nullable=True)  # Parsed job requirements
    company_type = Column(String(50), nullable=True)  # banking/fintech/startup/mnc/other
    match_results = Column(JSON, nullable=True)  # Match analysis results
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="job_analyses")
    resume = relationship("Resume", back_populates="job_analyses")
    suggestions = relationship("Suggestion", back_populates="job_analysis", lazy="selectin")

    __table_args__ = (
        Index("ix_job_analyses_user_id", "user_id"),
        Index("ix_job_analyses_resume_id", "resume_id"),
    )


class Suggestion(Base):
    """Line-by-line revision suggestion."""

    __tablename__ = "suggestions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_analysis_id = Column(UUID(as_uuid=True), ForeignKey("job_analyses.id"), nullable=False)
    section = Column(String(100), nullable=False)  # experience/education/skills/etc
    original_text = Column(Text, nullable=False)
    suggested_text = Column(Text, nullable=False)
    rationale = Column(Text, nullable=True)
    sg_context = Column(JSON, nullable=True)  # SG-specific context
    match_level = Column(String(20), nullable=True)  # strong/transferable/addressable/fundamental
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    job_analysis = relationship("JobAnalysis", back_populates="suggestions")
    signals = relationship("SuggestionSignal", back_populates="suggestion", lazy="selectin")


class SuggestionSignal(Base):
    """Learning loop: user feedback on suggestions."""

    __tablename__ = "suggestion_signals"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # NOTE: user_id is anonymized - not linked to PII in this table per PDPA
    anonymized_user_id = Column(String(64), nullable=False)  # Hashed user_id
    suggestion_id = Column(UUID(as_uuid=True), ForeignKey("suggestions.id"), nullable=False)
    action = Column(String(20), nullable=False)  # ACCEPTED/REJECTED/MODIFIED
    modified_text = Column(Text, nullable=True)
    context_company_type = Column(String(50), nullable=True)  # GLC/MNC/SME/STARTUP/GOVERNMENT
    context_role_level = Column(String(20), nullable=True)  # ENTRY/MID/SENIOR/MANAGEMENT
    context_industry = Column(String(100), nullable=True)
    context_ns_related = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    suggestion = relationship("Suggestion", back_populates="signals")

    __table_args__ = (
        Index("ix_suggestion_signals_created_at", "created_at"),
    )


class ApplicationStage(Base):
    """Stage events for application tracking — normalized child table."""

    __tablename__ = "application_stages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    application_id = Column(UUID(as_uuid=True), ForeignKey("applications.id"), nullable=False)
    stage_type = Column(String(20), nullable=False)  # response|screening|interview|final|offer|rejection|withdrawal
    round_number = Column(Integer, nullable=True)  # 1-5 for interviews
    format = Column(String(50), nullable=True)  # email|phone|video|in-person|assessment_centre|panel|technical|case
    outcome = Column(String(20), nullable=True)  # passed|failed|pending|withdrawn
    stage_date = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    application = relationship("Application", back_populates="stage_events")

    __table_args__ = (
        Index("ix_application_stages_application_id", "application_id"),
    )


class Application(Base):
    """Job application tracking."""

    __tablename__ = "applications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    job_analysis_id = Column(UUID(as_uuid=True), ForeignKey("job_analyses.id"), nullable=True)
    suggestion_set_id = Column(UUID(as_uuid=True), ForeignKey("job_analyses.id"), nullable=True)  # links to which suggestions were applied
    employer = Column(String(255), nullable=False)
    role = Column(String(255), nullable=False)
    job_url = Column(Text, nullable=True)  # URL of the job posting
    applied_date = Column(DateTime, nullable=True)  # when user applied to this job
    status = Column(Enum(ApplicationStatus), default=ApplicationStatus.INTERESTED)
    is_confirmed = Column(Boolean, default=False, nullable=False)  # user confirmed they submitted
    stages = Column(JSON, default=list)  # kept in sync with application_stages table
    final_outcome = Column(String(50), nullable=True)
    source = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)
    last_activity_at = Column(DateTime, nullable=True)  # for nudge-eligibility
    auto_closed_at = Column(DateTime, nullable=True)  # set by auto-close job
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="applications")
    job_analysis = relationship("JobAnalysis", foreign_keys=[job_analysis_id])
    suggestion_set = relationship("JobAnalysis", foreign_keys=[suggestion_set_id])
    stage_events = relationship("ApplicationStage", back_populates="application", lazy="selectin")

    __table_args__ = (
        Index("ix_applications_user_id", "user_id"),
        Index("ix_applications_created_at", "created_at"),
    )


# =============================================================================
# RECRUITER (B2B) MODELS
# =============================================================================


class B2BTenant(Base):
    """B2B organization (recruitment agency)."""

    __tablename__ = "b2b_tenants"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    tenant_type = Column(String(50), nullable=True)  # UNIVERSITY/WSG/AGENCY
    contract_value = Column(Numeric(10, 2), nullable=True)
    seat_count = Column(Integer, default=1)
    # Stripe subscription fields
    stripe_subscription_id = Column(String(255), nullable=True, unique=True)
    tier = Column(String(20), nullable=False, default="free")  # free/basic/pro/team
    jd_generation_count = Column(Integer, default=0)
    jd_limit = Column(Integer, default=-1)  # -1 = unlimited, 50 for basic
    jd_limit_reset_at = Column(DateTime, nullable=True)  # Monthly reset timestamp
    is_suspended = Column(Boolean, default=False)  # Suspended when subscription cancelled
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    users = relationship("B2BUser", back_populates="tenant", lazy="selectin")
    job_descriptions = relationship("B2BJobDescription", back_populates="tenant", lazy="selectin")
    templates = relationship("B2BTemplate", back_populates="tenant", lazy="selectin")
    aggregate_reports = relationship("B2BAggregateReport", back_populates="tenant", lazy="selectin")


class B2BUser(Base):
    """B2B user (recruiter within an agency)."""

    __tablename__ = "b2b_users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, unique=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("b2b_tenants.id"), nullable=False)
    access_level = Column(Enum(AccessLevel), default=AccessLevel.MEMBER)
    invited_at = Column(DateTime, nullable=True)  # When invite was sent
    joined_at = Column(DateTime, nullable=True)  # When user accepted invite
    provisioned_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User")
    tenant = relationship("B2BTenant", back_populates="users")
    job_descriptions = relationship("B2BJobDescription", back_populates="created_by_user", lazy="selectin")


class B2BJobDescription(Base):
    """Job description created by recruiter."""

    __tablename__ = "b2b_job_descriptions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("b2b_tenants.id"), nullable=False)
    created_by_id = Column(UUID(as_uuid=True), ForeignKey("b2b_users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    company = Column(String(255), nullable=False)
    company_type = Column(String(50), nullable=True)  # banking/fintech/startup/mnc/other
    skills_json = Column(JSON, nullable=False)  # List of skills
    seniority = Column(String(20), nullable=True)  # junior/mid/senior/lead
    content = Column(Text, nullable=False)  # Generated JD content
    brand_template_id = Column(UUID(as_uuid=True), ForeignKey("b2b_templates.id"), nullable=True)
    rating = Column(Integer, nullable=True)  # 1-5, from JD quality rating
    rating_feedback = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    tenant = relationship("B2BTenant", back_populates="job_descriptions")
    created_by_user = relationship("B2BUser", back_populates="job_descriptions")
    brand_template = relationship("B2BTemplate", foreign_keys=[brand_template_id])
    share_links = relationship("B2BShareLink", back_populates="job_description", lazy="selectin")
    versions = relationship("B2BVersion", back_populates="job_description", lazy="selectin")

    __table_args__ = (
        Index("ix_b2b_jd_tenant_id", "tenant_id"),
        Index("ix_b2b_jd_created_by_id", "created_by_id"),
    )


class B2BShareLink(Base):
    """Shareable link for a job description."""

    __tablename__ = "b2b_share_links"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    jd_id = Column(UUID(as_uuid=True), ForeignKey("b2b_job_descriptions.id"), nullable=False)
    token = Column(String(64), unique=True, nullable=False, index=True)
    expires_at = Column(DateTime, nullable=False)
    view_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    job_description = relationship("B2BJobDescription", back_populates="share_links")


class InviteLink(Base):
    """Invite link for B2B team onboarding."""

    __tablename__ = "invite_links"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("b2b_tenants.id"), nullable=False)
    token = Column(String(64), unique=True, nullable=False, index=True)
    email = Column(String(255), nullable=False)  # Invited email
    access_level = Column(Enum(AccessLevel), default=AccessLevel.MEMBER)
    expires_at = Column(DateTime, nullable=False)
    used_at = Column(DateTime, nullable=True)  # When invite was accepted
    created_by_id = Column(UUID(as_uuid=True), ForeignKey("b2b_users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    tenant = relationship("B2BTenant")

    __table_args__ = (
        Index("ix_invite_links_token", "token"),
        Index("ix_invite_links_tenant_id", "tenant_id"),
    )


class B2BVersion(Base):
    """Version history for a job description."""

    __tablename__ = "b2b_versions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    jd_id = Column(UUID(as_uuid=True), ForeignKey("b2b_job_descriptions.id"), nullable=False)
    content = Column(Text, nullable=False)
    version_number = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    job_description = relationship("B2BJobDescription", back_populates="versions")


class B2BTemplate(Base):
    """Brand template for job descriptions."""

    __tablename__ = "b2b_templates"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("b2b_tenants.id"), nullable=False)
    name = Column(String(255), nullable=False)
    logo_s3_key = Column(String(512), nullable=True)
    brand_primary_color = Column(String(7), default="#4F46E5")  # Hex color
    brand_secondary_color = Column(String(7), default="#6B7280")
    font_choice = Column(String(50), default="Inter")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    tenant = relationship("B2BTenant", back_populates="templates")


class B2BAggregateReport(Base):
    """Aggregate analytics reports for B2B tenants.

    Stores pre-computed cohort-level statistics for dashboard display.
    """

    __tablename__ = "b2b_aggregate_reports"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("b2b_tenants.id"), nullable=False)
    cohort_period = Column(String(50), nullable=False)  # e.g., "2025-S1", "2025-Q1", "2025"
    aggregate_stats_json = Column(JSON, nullable=False)  # pre-computed statistics
    generated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    tenant = relationship("B2BTenant")


# =============================================================================
# SKILL FREQUENCY ANALYSIS MODELS (JD Generator v2)
# =============================================================================


class RawJD(Base):
    """Raw job description from all sources.

    Architecture: specs/jd-generator-architecture.md §10
    """

    __tablename__ = "raw_jds"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_url = Column(Text, nullable=True)
    source_platform = Column(String(50), nullable=True)  # mcf, jobstreet, linkedin, direct
    data_source = Column(String(50), nullable=False)  # scraped, user_submitted, partner
    job_title_raw = Column(Text, nullable=True)
    company = Column(Text, nullable=True)
    company_type = Column(
        String(50), nullable=False
    )  # glc, statutory_board, mnc, startup, banking, fintech, sme, other
    industry = Column(
        String(50), nullable=False
    )  # fintech, technology, banking_finance, consulting, government_public, healthcare, retail_consumer, engineering, education, other
    seniority = Column(String(50), nullable=False)  # junior, mid, senior, lead
    raw_text = Column(Text, nullable=True)
    posted_at = Column(DateTime, nullable=True)
    scraped_at = Column(DateTime, default=datetime.utcnow)
    submitted_at = Column(DateTime, nullable=True)
    consent_given = Column(Boolean, default=False)
    is_duplicate = Column(Boolean, default=False)
    is_spam = Column(Boolean, default=False)
    is_stale = Column(Boolean, default=False)

    __table_args__ = (
        Index("ix_raw_jds_company_title_posted", "company", "job_title_raw", "posted_at"),
        Index("ix_raw_jds_data_source", "data_source"),
        Index("ix_raw_jds_industry_seniority", "industry", "seniority"),
    )


class NormalizedRole(Base):
    """Normalized job title with variants.

    Architecture: specs/jd-generator-architecture.md §10
    """

    __tablename__ = "normalized_roles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title_normalized = Column(Text, nullable=False)
    title_variants = Column(JSON, nullable=True)  # ["Software Engineer", "SWE", "Software Dev"]
    industry = Column(String(50), nullable=False)
    seniority = Column(String(50), nullable=False)
    total_jds = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("title_normalized", "industry", "seniority", name="uq_normalized_role_lookup"),
        Index("ix_normalized_roles_title", "title_normalized"),
    )


class RoleSkillFrequency(Base):
    """Denormalized skill frequency read table.

    Architecture: specs/jd-generator-architecture.md §10
    Updated nightly via ETL.
    """

    __tablename__ = "role_skill_frequency"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    normalized_role_id = Column(UUID(as_uuid=True), ForeignKey("normalized_roles.id"), nullable=True)
    title_normalized = Column(Text, nullable=False)
    industry = Column(String(50), nullable=False)
    seniority = Column(String(50), nullable=False)
    company_type = Column(String(50), nullable=False)  # glc, statutory_board, mnc, startup, banking, fintech, sme, other, ANY
    skills_json = Column(
        JSON, nullable=False
    )  # [{"skill": "Python", "raw_weighted_freq": 0.811, "required_count": 73, "preferred_count": 27, "total_jds": 100}]
    total_jds_analyzed = Column(Integer, nullable=False)
    recency_weight = Column(Float, default=1.0)
    last_updated = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("title_normalized", "industry", "seniority", "company_type", name="uq_role_skill_freq_lookup"),
        Index("ix_role_skill_freq_title", "title_normalized"),
    )


class JDGenerationLog(Base):
    """JD generation feedback log.

    Tracks skill sources and generation outcomes per architecture spec §8.
    """

    __tablename__ = "jd_generation_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    input_title = Column(Text, nullable=True)
    input_industry = Column(String(50), nullable=True)
    input_seniority = Column(String(50), nullable=True)
    input_company_type = Column(String(50), nullable=True)
    input_skills_user = Column(JSON, nullable=True)  # user-provided skills
    skills_from_frequency = Column(JSON, nullable=True)  # AI-selected from skill_frequency DB
    generation_source = Column(String(50), nullable=False)  # "skill_frequency", "fallback_prompt", "user_provided"
    adopted = Column(Boolean, nullable=True)  # saved by recruiter
    edited = Column(Boolean, nullable=True)  # recruiter changed AI skills
    used_in_posting = Column(Boolean, nullable=True)  # actually posted
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index("ix_jd_generation_logs_created_at", "created_at"),
    )

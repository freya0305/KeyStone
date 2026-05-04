"""All SQLAlchemy models for KeyStone.

Includes both Job Seeker and Recruiter (B2B) entities.
RLS (Row-Level Security) must be enforced at database level for B2B tables.
"""
import uuid
from datetime import datetime
from enum import Enum as PyEnum
from typing import Optional

from sqlalchemy import (
    Column,
    String,
    Text,
    DateTime,
    ForeignKey,
    Integer,
    Boolean,
    Numeric,
    JSON,
    Enum,
    Index,
    CheckConstraint,
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
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

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
    applied_date = Column(DateTime, nullable=True)
    status = Column(Enum(ApplicationStatus), default=ApplicationStatus.INTERESTED)
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
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

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

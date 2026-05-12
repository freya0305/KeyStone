"""Analysis cache service for tracking analyzed jobs per user.

Used for free tier suggestion gating: first analysis of a unique job URL
gets unlimited suggestions, subsequent analyses of the same URL are gated.
"""
import hashlib
from uuid import UUID

import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from keystone.models.entities import AnalyzedJob

logger = structlog.get_logger()


def normalize_job_url(url: str) -> str:
    """Normalize a job URL for hashing.

    Strips tracking parameters and normalizes the URL structure
    so that the same job posting with different tracking params
    hashes to the same value.
    """
    if not url:
        return ""

    url = url.strip().lower()

    # Remove common tracking parameters
    # (these don't change the actual job posting)
    tracking_params = {
        "utm_source",
        "utm_medium",
        "utm_campaign",
        "utm_term",
        "utm_content",
        "ref",
        "ref_src",
        "ref_url",
        "source",
        "fbclid",
        "gclid",
        "msclkid",
    }

    try:
        from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

        parsed = urlparse(url)

        # Only normalize if we have a valid scheme and netloc
        if parsed.scheme and parsed.netloc:
            # Parse and filter query parameters
            params = parse_qs(parsed.query)
            filtered_params = {
                k: v
                for k, v in params.items()
                if k.lower() not in tracking_params
            }
            # Re-encode with filtered params (sorted for consistency)
            new_query = urlencode(sorted(filtered_params.items()), doseq=True)
            normalized = urlunparse(
                (
                    parsed.scheme,
                    parsed.netloc.lower(),
                    parsed.path,
                    parsed.params,
                    new_query,
                    "",  # Remove fragment
                )
            )
            return normalized
    except Exception:
        # If URL parsing fails, just return the stripped lowercase URL
        pass

    return url


def hash_job_url(url: str) -> str:
    """Create a SHA256 hash of a normalized job URL."""
    normalized = normalize_job_url(url)
    return hashlib.sha256(normalized.encode()).hexdigest()


async def mark_job_analyzed(
    user_id: UUID,
    job_url: str,
    job_title: str | None,
    db: AsyncSession,
) -> AnalyzedJob:
    """Mark a job URL as analyzed for a user.

    Creates a new AnalyzedJob record if this is the first time
    analyzing this URL. If already analyzed, returns the existing record.
    Uses upsert logic to handle concurrent requests.
    """
    url_hash = hash_job_url(job_url) if job_url else ""

    # Check if already exists
    existing = await db.execute(
        select(AnalyzedJob).where(
            AnalyzedJob.user_id == user_id,
            AnalyzedJob.job_url_hash == url_hash,
        )
    )
    existing_job = existing.scalar_one_or_none()

    if existing_job:
        logger.debug(
            "job_already_analyzed",
            user_id=str(user_id),
            url_hash=url_hash,
        )
        return existing_job

    # Create new record
    analyzed_job = AnalyzedJob(
        user_id=user_id,
        job_url_hash=url_hash,
        job_title=job_title,
    )
    db.add(analyzed_job)

    try:
        await db.commit()
        await db.refresh(analyzed_job)
        logger.info(
            "job_marked_analyzed",
            user_id=str(user_id),
            url_hash=url_hash,
            job_title=job_title,
        )
    except Exception:
        # Handle race condition: another request may have inserted between
        # our check and our insert. In that case, fetch and return existing.
        await db.rollback()
        existing = await db.execute(
            select(AnalyzedJob).where(
                AnalyzedJob.user_id == user_id,
                AnalyzedJob.job_url_hash == url_hash,
            )
        )
        analyzed_job = existing.scalar_one_or_none()
        if analyzed_job:
            return analyzed_job
        # If still not found, re-raise the original exception
        raise

    return analyzed_job


async def is_job_previously_analyzed(
    user_id: UUID,
    job_url: str,
    db: AsyncSession,
) -> bool:
    """Check if a user has previously analyzed this job URL.

    Returns True if an AnalyzedJob record exists for this user and URL hash.
    """
    url_hash = hash_job_url(job_url) if job_url else ""

    result = await db.execute(
        select(AnalyzedJob).where(
            AnalyzedJob.user_id == user_id,
            AnalyzedJob.job_url_hash == url_hash,
        )
    )
    return result.scalar_one_or_none() is not None


async def get_user_analyzed_job_count(
    user_id: UUID,
    db: AsyncSession,
) -> int:
    """Get the total count of unique jobs analyzed by a user."""
    from sqlalchemy import func

    result = await db.execute(
        select(func.count(AnalyzedJob.id)).where(
            AnalyzedJob.user_id == user_id,
        )
    )
    return result.scalar() or 0

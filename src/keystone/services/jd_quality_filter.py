"""JD quality filtering per architecture spec §3.

Spam detection, deduplication, and staleness detection for raw JDs.
"""
import re
from datetime import datetime, timedelta
from typing import Optional

import structlog

from keystone.models.entities import RawJD

logger = structlog.get_logger()

# Architecture spec §3: word count threshold
MIN_JD_WORDS = 50

# Architecture spec §3: spam patterns
SPAM_PATTERNS = [
    re.compile(r"work\s+from\s+home", re.IGNORECASE),
    re.compile(r"no\s+experience\s+needed", re.IGNORECASE),
    re.compile(r"earn\s+sgd\s*\d+", re.IGNORECASE),
    re.compile(r"earn\s*\$?\s*5000", re.IGNORECASE),
    re.compile(r"guaranteed\s+income", re.IGNORECASE),
    re.compile(r"immediate\s+start\s+today", re.IGNORECASE),
    re.compile(r"work\s+at\s+home", re.IGNORECASE),
]

# Staleness thresholds per architecture spec §3
STALE_AGE_DAYS = 180  # weight = 0.5
EXCLUDED_AGE_DAYS = 365  # excluded from skill_frequency

# Deduplication window per architecture spec §3
DEDUP_WINDOW_DAYS = 7


def count_words(text: str) -> int:
    """Count words in text."""
    if not text:
        return 0
    return len(text.split())


def is_spam(jd_text: str) -> bool:
    """Check if JD appears to be spam per architecture spec §3.

    Reject if:
    - Word count < 50 (likely not a real JD)
    - Contains obvious spam patterns

    Args:
        jd_text: Raw job description text

    Returns:
        True if JD appears to be spam
    """
    if not jd_text:
        logger.info("jd_quality.spam", reason="empty_text")
        return True

    # Word count check
    word_count = count_words(jd_text)
    if word_count < MIN_JD_WORDS:
        logger.info("jd_quality.spam", reason="too_short", word_count=word_count)
        return True

    # Pattern matching for obvious spam
    for pattern in SPAM_PATTERNS:
        if pattern.search(jd_text):
            logger.info("jd_quality.spam", reason="spam_pattern", pattern=pattern.pattern)
            return True

    return False


def is_duplicate(
    jd: RawJD,
    existing_jds: list[RawJD],
) -> bool:
    """Check if JD is a duplicate per architecture spec §3.

    Duplicate if: same company + same job_title_raw + posted within 7 days.
    Keep the most recent.

    Args:
        jd: New JD to check
        existing_jds: List of existing JDs to compare against

    Returns:
        True if JD is a duplicate
    """
    if not jd.company or not jd.job_title_raw:
        return False

    jd_posted = jd.posted_at
    if jd_posted is None:
        jd_posted = datetime.utcnow()

    cutoff = jd_posted - timedelta(days=DEDUP_WINDOW_DAYS)

    for existing in existing_jds:
        # Skip self
        if existing.id == jd.id:
            continue

        # Same company
        if existing.company and existing.company.lower() != jd.company.lower():
            continue

        # Same job title
        if existing.job_title_raw and existing.job_title_raw.lower() != jd.job_title_raw.lower():
            continue

        # Posted within 7 days
        if existing.posted_at and existing.posted_at >= cutoff:
            logger.info(
                "jd_quality.duplicate",
                company=jd.company,
                title=jd.job_title_raw,
                posted_at=jd.posted_at,
                existing_posted_at=existing.posted_at,
            )
            return True

    return False


def get_staleness_weight(posted_at: Optional[datetime]) -> tuple[str, float]:
    """Determine staleness weight based on posting age per architecture spec §3.

    Args:
        posted_at: When the job was posted

    Returns:
        Tuple of (staleness_category, weight)
        - "fresh": weight 1.0 (posted < 180 days)
        - "stale": weight 0.5 (posted 180-365 days)
        - "excluded": weight 0.0 (posted > 365 days, excluded from skill_frequency)
    """
    if posted_at is None:
        # Assume fresh if unknown
        return ("fresh", 1.0)

    now = datetime.utcnow()
    age_days = (now - posted_at).days

    if age_days <= STALE_AGE_DAYS:
        return ("fresh", 1.0)
    elif age_days <= EXCLUDED_AGE_DAYS:
        return ("stale", 0.5)
    else:
        return ("excluded", 0.0)


def apply_staleness_flags(jd: RawJD) -> bool:
    """Mark JD as stale based on age per architecture spec §3.

    > 180 days: weight = 0.5 (still counted, but half weight)
    > 365 days: excluded from skill_frequency, kept in raw_jds for historical analysis

    Args:
        jd: RawJD to check and update

    Returns:
        True if JD is stale (weight < 1.0)
    """
    staleness, weight = get_staleness_weight(jd.posted_at)

    if staleness == "excluded":
        jd.is_stale = True
        logger.info(
            "jd_quality.staleness",
            jd_id=str(jd.id),
            category=staleness,
            weight=weight,
            posted_at=jd.posted_at,
        )
    elif staleness == "stale":
        jd.is_stale = True
        logger.info(
            "jd_quality.staleness",
            jd_id=str(jd.id),
            category=staleness,
            weight=weight,
            posted_at=jd.posted_at,
        )
    else:
        jd.is_stale = False

    return jd.is_stale


def filter_jd_batch(jds: list[RawJD]) -> list[RawJD]:
    """Filter a batch of JDs for spam, duplicates, and staleness.

    Applies all quality filters to a batch of JDs and returns
    the filtered list. Updates is_spam, is_duplicate, and is_stale
    flags on each JD.

    Args:
        jds: List of RawJD objects to filter

    Returns:
        List of JDs that pass all filters (is_spam=False, is_duplicate=False)
    """
    filtered: list[RawJD] = []

    for jd in jds:
        # Apply spam check
        if is_spam(jd.raw_text or ""):
            jd.is_spam = True
            continue

        # Apply staleness flags
        apply_staleness_flags(jd)

        # Check duplicates against already-accepted JDs
        if is_duplicate(jd, filtered):
            jd.is_duplicate = True
            continue

        # Also check against previously stored JDs (would need DB access in production)
        # For now, just check against this batch
        filtered.append(jd)

    logger.info(
        "jd_quality.batch_filtered",
        total=len(jds),
        passed=len(filtered),
        spam_count=sum(1 for jd in jds if jd.is_spam),
        duplicate_count=sum(1 for jd in jds if jd.is_duplicate),
    )

    return filtered

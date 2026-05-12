"""Rate limiting middleware.

Simple in-memory rate limiter for MVP.
Production should use Redis-based rate limiting.
"""
import time
from collections import deque, defaultdict
from typing import Callable
import uuid

import structlog
from fastapi import Request, HTTPException

logger = structlog.get_logger()

# Simple in-memory rate limiter
# Key: identifier (IP or user_id)
# Value: deque of request timestamps, max 1000 per identifier to bound memory
_rate_limit_store: dict[str, deque[float]] = defaultdict(lambda: deque(maxlen=1000))

# Rate limits per tier
RATE_LIMITS = {
    "free": {"requests": 60, "window": 60},      # 60/min (guest/unauthenticated)
    "pro": {"requests": 600, "window": 60},      # 600/min
    "jd_generate": {"requests": 10, "window": 60}, # 10 JD generations/min
    "job_analysis": {"requests": 20, "window": 60}, # 20 job analyses/hour per user/IP
}

# Cleanup interval (seconds)
CLEANUP_INTERVAL = 300
_last_cleanup = time.time()


def _cleanup_old_entries() -> None:
    """Remove expired entries from rate limit store."""
    global _last_cleanup
    now = time.time()

    if now - _last_cleanup < CLEANUP_INTERVAL:
        return

    _last_cleanup = now
    for key in list(_rate_limit_store.keys()):
        # Remove entries older than the window
        cutoff = now - 60  # 1 minute
        _rate_limit_store[key] = [t for t in _rate_limit_store[key] if t > cutoff]
        if not _rate_limit_store[key]:
            del _rate_limit_store[key]


def check_rate_limit(identifier: str, limit_type: str = "default") -> None:
    """Check if request is within rate limit.

    Args:
        identifier: Unique identifier (IP or user_id)
        limit_type: Type of limit to apply

    Raises:
        HTTPException: If rate limit exceeded
    """
    _cleanup_old_entries()

    now = time.time()
    entries = _rate_limit_store[identifier]

    # Get limit config - use tier from RATE_LIMITS if available, else fall back to "free"
    if limit_type in RATE_LIMITS:
        limit_config = RATE_LIMITS[limit_type]
    else:
        limit_config = RATE_LIMITS["free"]  # Default for unknown tiers

    max_requests = limit_config["requests"]
    window = limit_config["window"]
    cutoff = now - window

    # Remove old entries
    entries = [t for t in entries if t > cutoff]
    _rate_limit_store[identifier] = entries

    if len(entries) >= max_requests:
        logger.warning("rate_limit_exceeded", identifier=identifier[:8], limit_type=limit_type)
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded. Try again in {window} seconds."
        )

    # Add current request
    entries.append(now)


def get_client_identifier(request: Request) -> str:
    """Get unique identifier for a request.

    Uses X-Forwarded-For if behind proxy, otherwise client IP.
    Falls back to a generated UUID for convenience during development.
    """
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()

    # Fallback for local development
    if request.client:
        return request.client.host

    # Last resort - generate a stable identifier
    return str(uuid.uuid4())

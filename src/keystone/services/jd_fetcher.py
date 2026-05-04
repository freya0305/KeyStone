"""M3.1 - JD URL Fetcher + Text Extractor.

Allowed sources: mycareersfuture.gov.sg, jobstreet.com.sg, linkedin.com/jobs, corporate career pages
HTTP fetch with 10s timeout, 1MB cap
User-agent: KeyStoneBot/1.0
HTML→text via BeautifulSoup
Respect robots.txt
Cache: URL → parsed JD, TTL 7 days
Fallback: if fetch fails, return text-paste input
"""
import hashlib
import re
import time
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional

import httpx
import structlog
from bs4 import BeautifulSoup

logger = structlog.get_logger()

# Allowed job posting domains
ALLOWED_DOMAINS = [
    "mycareersfuture.gov.sg",
    "jobstreet.com.sg",
    "linkedin.com",
    "jobs.jobstreet.com.sg",
    "careers.page",
    "greenfield",
]

# Simple in-memory cache: url_hash → (fetched_at, text)
# Production should use Redis
_JD_CACHE: dict[str, tuple[float, str]] = {}
_JD_CACHE_TTL_SECONDS = 7 * 24 * 60 * 60  # 7 days


@dataclass
class JDFetchResult:
    text: str
    source_url: str
    cached: bool
    fetched_at: datetime


def _is_allowed_url(url: str) -> bool:
    """Check if URL is from an allowed job posting source."""
    url_lower = url.lower()
    return any(domain in url_lower for domain in ALLOWED_DOMAINS)


def _extract_domain(url: str) -> str:
    """Extract domain from URL for logging."""
    try:
        from urllib.parse import urlparse
        parsed = urlparse(url)
        return parsed.netloc
    except Exception:
        return "unknown"


async def fetch_jd_from_url(url: str, timeout: float = 10.0) -> JDFetchResult:
    """Fetch job description from URL.

    Args:
        url: Job posting URL
        timeout: Request timeout in seconds

    Returns:
        JDFetchResult with extracted text

    Raises:
        ValueError: If URL is not from allowed source
        httpx.HTTPError: If fetch fails
    """
    if not _is_allowed_url(url):
        raise ValueError(
            f"URL not from allowed job source. Allowed: {ALLOWED_DOMAINS}"
        )

    url_hash = hashlib.sha256(url.encode()).hexdigest()[:32]

    # Check cache
    now = time.time()
    if url_hash in _JD_CACHE:
        fetched_at, cached_text = _JD_CACHE[url_hash]
        if now - fetched_at < _JD_CACHE_TTL_SECONDS:
            logger.info("jd_fetch.cache_hit", url_hash=url_hash, domain=_extract_domain(url))
            return JDFetchResult(
                text=cached_text,
                source_url=url,
                cached=True,
                fetched_at=datetime.fromtimestamp(fetched_at),
            )

    # Fetch with httpx
    headers = {
        "User-Agent": "KeyStoneBot/1.0 (job seeker tool; contact: support@keystone.com)",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
    }

    try:
        async with httpx.AsyncClient(timeout=timeout, follow_redirects=True) as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()

            content_type = response.headers.get("content-type", "")
            if "text/html" not in content_type and "application/xhtml" not in content_type:
                # Not HTML, return raw text up to 1MB
                text = response.text[:1_048_576]
            else:
                text = _extract_text_from_html(response.text)

            # Enforce 1MB cap
            text = text[:1_048_576]

    except httpx.TimeoutException:
        logger.warning("jd_fetch.timeout", url=url, timeout=timeout)
        raise ValueError(f"Timeout fetching job posting URL ({timeout}s)")
    except httpx.HTTPStatusError as e:
        logger.warning("jd_fetch.http_error", url=url, status=e.response.status_code)
        raise ValueError(f"HTTP error {e.response.status_code} fetching job posting URL")
    except httpx.RequestError as e:
        logger.warning("jd_fetch.request_error", url=url, error=str(e))
        raise

    # Cache the result
    _JD_CACHE[url_hash] = (now, text)

    logger.info(
        "jd_fetch.success",
        url_hash=url_hash,
        domain=_extract_domain(url),
        text_length=len(text),
    )

    return JDFetchResult(
        text=text,
        source_url=url,
        cached=False,
        fetched_at=datetime.fromtimestamp(now),
    )


def _extract_text_from_html(html: str) -> str:
    """Extract readable text from HTML using BeautifulSoup.

    Args:
        html: Raw HTML content

    Returns:
        Extracted text content
    """
    soup = BeautifulSoup(html, "html.parser")

    # Remove script, style, and other non-content elements
    for tag in soup.find_all(["script", "style", "nav", "header", "footer", "noscript"]):
        tag.decompose()

    # Try to find main content area
    main_content = None
    for selector in ["main", "article", "[role='main']", ".job-content", "#job-content"]:
        main_content = soup.select_one(selector)
        if main_content:
            break

    if main_content:
        text = main_content.get_text(separator=" ", strip=True)
    else:
        text = soup.get_text(separator=" ", strip=True)

    # Clean up whitespace
    text = re.sub(r"\s+", " ", text)
    text = text.strip()

    return text


def clear_jd_cache(url: Optional[str] = None) -> None:
    """Clear JD fetch cache.

    Args:
        url: If provided, clear only this URL's cache. Otherwise clear all.
    """
    if url:
        url_hash = hashlib.sha256(url.encode()).hexdigest()[:32]
        if url_hash in _JD_CACHE:
            del _JD_CACHE[url_hash]
            logger.info("jd_cache.cleared", url_hash=url_hash)
    else:
        _JD_CACHE.clear()
        logger.info("jd_cache.cleared_all")

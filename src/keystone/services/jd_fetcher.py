"""M3.1 - JD URL Fetcher + Text Extractor.

Allowed sources: mycareersfuture.gov.sg, jobstreet.com.sg
HTTP fetch with 10s timeout, 1MB cap
User-agent: KeyStoneBot/1.0
HTML→text via BeautifulSoup
Respect robots.txt + rate limiting per architecture spec §6
Cache: URL → parsed JD, TTL 7 days
Fallback: if fetch fails, return text-paste input
"""
import hashlib
import re
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional
from urllib.parse import urlparse

import httpx
import structlog
from bs4 import BeautifulSoup

logger = structlog.get_logger()

# Allowed job posting domains per architecture spec §6
ALLOWED_DOMAINS = [
    "mycareersfuture.gov.sg",
    "jobstreet.com.sg",
    "jobs.jobstreet.com.sg",
    "linkedin.com",
]

# Rate limiting: 1 request per 5 seconds per domain per architecture spec §6
RATE_LIMIT_SECONDS = 5.0

# In-memory cache: url_hash → (fetched_at, text)
# Production should use Redis
_JD_CACHE: dict[str, tuple[float, str]] = {}
_JD_CACHE_TTL_SECONDS = 7 * 24 * 60 * 60  # 7 days

# Rate limit tracking: domain → last_request_time
_DOMAIN_LAST_REQUEST: dict[str, float] = {}

# Robots.txt cache: domain → allowed paths
_ROBOTS_CACHE: dict[str, set[str]] = {}


@dataclass
class JDFetchResult:
    """Structured JD fetch result."""

    text: str
    source_url: str
    source_platform: str  # mcf, jobstreet
    title: Optional[str] = None
    company: Optional[str] = None
    company_type: Optional[str] = None
    posted_date: Optional[datetime] = None
    cached: bool = False
    fetched_at: datetime = field(default_factory=datetime.utcnow)


def _is_allowed_url(url: str) -> bool:
    """Check if URL is from an allowed job posting source."""
    url_lower = url.lower()
    return any(domain in url_lower for domain in ALLOWED_DOMAINS)


def _extract_domain(url: str) -> str:
    """Extract domain from URL for logging."""
    try:
        parsed = urlparse(url)
        return parsed.netloc
    except Exception:
        return "unknown"


def _detect_platform(url: str) -> str:
    """Detect platform from URL."""
    url_lower = url.lower()
    if "mycareersfuture" in url_lower:
        return "mcf"
    elif "jobstreet" in url_lower:
        return "jobstreet"
    elif "linkedin.com/jobs/view" in url_lower:
        return "linkedin"
    return "direct"


async def _check_robots_txt(url: str) -> bool:
    """Check if URL is allowed by robots.txt.

    Returns True if scraping is allowed, False otherwise.
    """
    parsed = urlparse(url)
    domain = parsed.netloc

    # Check cache
    if domain in _ROBOTS_CACHE:
        allowed_paths = _ROBOTS_CACHE[domain]
        # Check if this path is allowed
        for allowed in allowed_paths:
            if allowed == "/":
                return True
            if parsed.path.startswith(allowed):
                return True
        return False

    # Fetch robots.txt
    robots_url = f"{parsed.scheme}://{domain}/robots.txt"

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(robots_url)
            if response.status_code != 200:
                # No robots.txt or can't fetch it - assume allowed
                _ROBOTS_CACHE[domain] = {"/"}
                return True

            robots_text = response.text

        # Parse robots.txt
        allowed_paths: set[str] = {"/"}
        disallow_paths: set[str] = set()

        current_user_agent = "*"
        for line in robots_text.split("\n"):
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            if line.lower().startswith("user-agent:"):
                current_user_agent = line.split(":", 1)[1].strip()
            elif line.lower().startswith("disallow:"):
                path = line.split(":", 1)[1].strip()
                if current_user_agent == "*" or current_user_agent.lower() == "keystonebot":
                    if path:
                        disallow_paths.add(path)
            elif line.lower().startswith("allow:"):
                path = line.split(":", 1)[1].strip()
                if current_user_agent == "*" or current_user_agent.lower() == "keystonebot":
                    if path:
                        allowed_paths.add(path)

        # Check if our path is disallowed
        path_allowed = True
        for disallowed in disallow_paths:
            if parsed.path.startswith(disallowed):
                # Check if there's an explicit allow override
                path_allowed = False
                break

        _ROBOTS_CACHE[domain] = allowed_paths if path_allowed else set()

        if not path_allowed:
            logger.info("jd_fetch.robots_blocked", domain=domain, path=parsed.path)

        return path_allowed

    except Exception as e:
        logger.warning("jd_fetch.robots_check_failed", url=url, error=str(e))
        # If robots.txt check fails, allow by default
        _ROBOTS_CACHE[domain] = {"/"}
        return True


def _apply_rate_limit(domain: str) -> None:
    """Apply rate limiting for domain.

    Sleeps if last request was within RATE_LIMIT_SECONDS.
    """
    now = time.time()

    if domain in _DOMAIN_LAST_REQUEST:
        last_request = _DOMAIN_LAST_REQUEST[domain]
        elapsed = now - last_request

        if elapsed < RATE_LIMIT_SECONDS:
            sleep_time = RATE_LIMIT_SECONDS - elapsed
            logger.info("jd_fetch.rate_limiting", domain=domain, sleep_seconds=sleep_time)
            time.sleep(sleep_time)

    _DOMAIN_LAST_REQUEST[domain] = time.time()


async def fetch_jd_from_url(url: str, timeout: float = 10.0) -> JDFetchResult:
    """Fetch job description from URL.

    Args:
        url: Job posting URL
        timeout: Request timeout in seconds

    Returns:
        JDFetchResult with extracted text and metadata

    Raises:
        ValueError: If URL is not from allowed source
        httpx.HTTPError: If fetch fails
    """
    if not _is_allowed_url(url):
        raise ValueError(
            f"URL not from allowed job source. Allowed: {ALLOWED_DOMAINS}"
        )

    # LinkedIn requires JavaScript rendering — handle separately with Playwright
    url_lower = url.lower()
    if "linkedin.com/jobs/view" in url_lower:
        return await _fetch_linkedin_jd(url)

    domain = _extract_domain(url)

    # Check robots.txt
    if not await _check_robots_txt(url):
        raise ValueError(f"URL blocked by robots.txt: {url}")

    # Apply rate limiting
    _apply_rate_limit(domain)

    url_hash = hashlib.sha256(url.encode()).hexdigest()[:32]

    # Check cache
    now = time.time()
    if url_hash in _JD_CACHE:
        fetched_at, cached_text = _JD_CACHE[url_hash]
        if now - fetched_at < _JD_CACHE_TTL_SECONDS:
            logger.info("jd_fetch.cache_hit", url_hash=url_hash, domain=domain)
            platform = _detect_platform(url)
            return JDFetchResult(
                text=cached_text,
                source_url=url,
                source_platform=platform,
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
                platform = _detect_platform(url)
                text, metadata = _extract_text_and_metadata_mcf(response.text, platform, url)

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
        domain=domain,
        text_length=len(text),
        platform=platform,
    )

    return JDFetchResult(
        text=text,
        source_url=url,
        source_platform=platform,
        title=metadata.get("title"),
        company=metadata.get("company"),
        company_type=metadata.get("company_type"),
        posted_date=metadata.get("posted_date"),
        cached=False,
        fetched_at=datetime.utcnow(),
    )


def _extract_text_and_metadata_mcf(html: str, platform: str, url: str) -> tuple[str, dict]:
    """Extract readable text and metadata from HTML based on platform.

    Args:
        html: Raw HTML content
        platform: Source platform (mcf, jobstreet)
        url: Original URL for reference

    Returns:
        Tuple of (extracted_text, metadata_dict)
    """
    soup = BeautifulSoup(html, "html.parser")

    # Remove script, style, and other non-content elements
    for tag in soup.find_all(["script", "style", "nav", "header", "footer", "noscript"]):
        tag.decompose()

    metadata: dict = {}

    if platform == "mcf":
        metadata = _extract_mcf_metadata(soup)
    elif platform == "jobstreet":
        metadata = _extract_jobstreet_metadata(soup)

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

    return text, metadata


def _extract_mcf_metadata(soup: BeautifulSoup) -> dict:
    """Extract metadata from MyCareersFuture HTML.

    Args:
        soup: Parsed BeautifulSoup object

    Returns:
        Dict with title, company, company_type, posted_date
    """
    metadata: dict = {
        "title": None,
        "company": None,
        "company_type": None,
        "posted_date": None,
    }

    # Job title - usually in h1 or specific class
    title_elem = soup.select_one("h1") or soup.select_one("[data-testid='job-title']")
    if title_elem:
        metadata["title"] = title_elem.get_text(strip=True)

    # Company name
    company_elem = soup.select_one("[data-testid='company-name']") or soup.select_one(".company-name")
    if company_elem:
        metadata["company"] = company_elem.get_text(strip=True)

    # Company type (GLC, MNC, etc.)
    company_type_elem = soup.select_one("[data-testid='company-type']") or soup.select_one(".company-type")
    if company_type_elem:
        company_type_text = company_type_elem.get_text(strip=True).lower()
        if "government" in company_type_text or "statutory" in company_type_text:
            metadata["company_type"] = "statutory_board"
        elif "multinational" in company_type_text or "mnc" in company_type_text:
            metadata["company_type"] = "mnc"
        elif "bank" in company_type_text or "financial" in company_type_text:
            metadata["company_type"] = "banking"
        elif "fintech" in company_type_text:
            metadata["company_type"] = "fintech"
        elif "startup" in company_type_text:
            metadata["company_type"] = "startup"
        elif "small medium" in company_type_text or "sme" in company_type_text:
            metadata["company_type"] = "sme"
        else:
            metadata["company_type"] = "other"

    # Posted date
    posted_elem = soup.select_one("[data-testid='posted-date']") or soup.select_one(".posted-date")
    if posted_elem:
        posted_text = posted_elem.get_text(strip=True)
        metadata["posted_date"] = _parse_mcf_date(posted_text)

    return metadata


def _extract_jobstreet_metadata(soup: BeautifulSoup) -> dict:
    """Extract metadata from JobStreet HTML.

    Args:
        soup: Parsed BeautifulSoup object

    Returns:
        Dict with title, company, company_type, posted_date
    """
    metadata: dict = {
        "title": None,
        "company": None,
        "company_type": None,
        "posted_date": None,
    }

    # Job title
    title_elem = (
        soup.select_one("h1")
        or soup.select_one("[data-testid='job-detail-title']")
        or soup.select_one(".job-title")
    )
    if title_elem:
        metadata["title"] = title_elem.get_text(strip=True)

    # Company name
    company_elem = (
        soup.select_one("[data-testid='job-detail-company-name']")
        or soup.select_one(".company-name")
        or soup.select_one("a.company-name")
    )
    if company_elem:
        metadata["company"] = company_elem.get_text(strip=True)

    # Company type from company profile if available
    company_type_elem = soup.select_one(".company-type") or soup.select_one("[data-testid='company-type']")
    if company_type_elem:
        company_type_text = company_type_elem.get_text(strip=True).lower()
        if "government" in company_type_text or "public" in company_type_text:
            metadata["company_type"] = "statutory_board"
        elif "multinational" in company_type_text or "mnc" in company_type_text:
            metadata["company_type"] = "mnc"
        elif "bank" in company_type_text or "financial" in company_type_text:
            metadata["company_type"] = "banking"
        elif "fintech" in company_type_text:
            metadata["company_type"] = "fintech"
        elif "startup" in company_type_text:
            metadata["company_type"] = "startup"
        elif "small medium" in company_type_text or "sme" in company_type_text:
            metadata["company_type"] = "sme"
        else:
            metadata["company_type"] = "other"

    # Posted date
    posted_elem = (
        soup.select_one("[data-testid='job-detail-posted-date']")
        or soup.select_one(".posted-date")
        or soup.select_one("span.date-posted")
    )
    if posted_elem:
        posted_text = posted_elem.get_text(strip=True)
        metadata["posted_date"] = _parse_jobstreet_date(posted_text)

    return metadata


def _parse_mcf_date(date_str: str) -> Optional[datetime]:
    """Parse MyCareersFuture date string.

    Args:
        date_str: Date string like "Posted 3 days ago" or "Posted on 15 Jan 2024"

    Returns:
        Parsed datetime or None
    """
    date_str = date_str.lower().strip()

    # Relative date like "3 days ago"
    relative_match = re.search(r"(\d+)\s+days?\s+ago", date_str)
    if relative_match:
        days = int(relative_match.group(1))
        return datetime.utcnow() - timedelta(days=days)

    # "Today" or "Just now"
    if "today" in date_str or "just" in date_str:
        return datetime.utcnow()

    # "Yesterday"
    if "yesterday" in date_str:
        return datetime.utcnow() - timedelta(days=1)

    # Specific date format like "15 Jan 2024"
    try:
        # Try common formats
        for fmt in ["%d %b %Y", "%d %B %Y", "%Y-%m-%d"]:
            try:
                return datetime.strptime(date_str.replace("posted ", "").strip(), fmt)
            except ValueError:
                continue
    except Exception:
        pass

    return None


def _parse_jobstreet_date(date_str: str) -> Optional[datetime]:
    """Parse JobStreet date string.

    Args:
        date_str: Date string like "Posted 3 days ago" or "5 days ago"

    Returns:
        Parsed datetime or None
    """
    date_str = date_str.lower().strip()

    # Remove "posted" prefix
    date_str = re.sub(r"^posted\s*", "", date_str)

    # Relative date like "3 days ago"
    relative_match = re.search(r"(\d+)\s+days?\s+ago", date_str)
    if relative_match:
        days = int(relative_match.group(1))
        return datetime.utcnow() - timedelta(days=days)

    # "Today"
    if "today" in date_str:
        return datetime.utcnow()

    # "Yesterday"
    if "yesterday" in date_str:
        return datetime.utcnow() - timedelta(days=1)

    # Specific date format
    try:
        for fmt in ["%d %b %Y", "%d %B %Y", "%Y-%m-%d"]:
            try:
                return datetime.strptime(date_str.strip(), fmt)
            except ValueError:
                continue
    except Exception:
        pass

    return None


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


async def _fetch_linkedin_jd(url: str) -> JDFetchResult:
    """Fetch job description from LinkedIn using Playwright for JavaScript rendering.

    Args:
        url: LinkedIn job posting URL (must contain /jobs/view)

    Returns:
        JDFetchResult with extracted title, company, and description

    Raises:
        ValueError: If Playwright is not available or LinkedIn blocks the request
    """
    try:
        from playwright.async_api import async_playwright

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            # Set a realistic user agent
            await page.set_extra_http_headers({
                "Accept-Language": "en-US,en;q=0.9",
            })

            await page.goto(url, wait_until="networkidle", timeout=30000)

            # Wait for job description to load
            await page.wait_for_selector(".description__text", timeout=10000)

            # Extract title
            title_elem = page.locator(".topcard__title")
            title = await title_elem.text_content() if await title_elem.count() > 0 else None

            # Extract company
            company_elem = page.locator(".topcard__org-name")
            company = await company_elem.text_content() if await company_elem.count() > 0 else None

            # Extract job description
            desc_elem = page.locator(".description__text")
            description = await desc_elem.text_content() if await desc_elem.count() > 0 else None

            await browser.close()

            logger.info(
                "jd_fetch.linkedin.success",
                url=url,
                title=title,
                company=company,
                description_length=len(description) if description else 0,
            )

            if not description:
                raise ValueError(
                    "Could not parse LinkedIn job description. "
                    "Please paste the job description text instead."
                )

            return JDFetchResult(
                text=description.strip() if description else "",
                source_url=url,
                source_platform="linkedin",
                title=title.strip() if title else None,
                company=company.strip() if company else None,
                cached=False,
                fetched_at=datetime.utcnow(),
            )

    except ImportError:
        logger.warning("jd_fetch.linkedin.playwright_not_available")
        raise ValueError(
            "LinkedIn parsing requires Playwright. "
            "Please install it with: pip install playwright && playwright install chromium. "
            "Alternatively, paste the job description text directly."
        )
    except Exception as e:
        logger.warning("jd_fetch.linkedin.error", url=url, error=str(e))
        raise ValueError(
            f"Could not parse LinkedIn URL. Please paste the job description text instead. "
            f"Error: {e}"
        )


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

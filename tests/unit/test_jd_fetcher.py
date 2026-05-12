"""Tests for JD Fetcher service - URL validation, HTML extraction, caching."""
import pytest
from keystone.services.jd_fetcher import (
    _is_allowed_url,
    _extract_domain,
    JDFetchResult,
    clear_jd_cache,
)


class TestIsAllowedUrl:
    """URL validation tests."""

    def test_mycareersfuture_allowed(self):
        """mycareersfuture.gov.sg should be allowed."""
        assert _is_allowed_url("https://www.mycareersfuture.gov.sg/job/software-engineer") is True

    def test_jobstreet_allowed(self):
        """jobstreet.com.sg should be allowed."""
        assert _is_allowed_url("https://www.jobstreet.com.sg/job/software-engineer") is True

    def test_linkedin_allowed(self):
        """linkedin.com should be allowed."""
        assert _is_allowed_url("https://www.linkedin.com/jobs/software-engineer") is True

    def test_arbitrary_url_rejected(self):
        """Random URLs should be rejected."""
        assert _is_allowed_url("https://www.example.com/job") is False
        assert _is_allowed_url("https://www.google.com") is False

    def test_case_insensitive(self):
        """URL check should be case insensitive."""
        assert _is_allowed_url("https://WWW.JOBSTREET.COM.SG/JOB") is True

    def test_subdomain_allowed(self):
        """Subdomains of allowed domains should be allowed."""
        assert _is_allowed_url("https://jobs.jobstreet.com.sg/job/123") is True


class TestExtractDomain:
    """Domain extraction tests."""

    def test_extracts_netloc(self):
        """Should extract domain from URL."""
        result = _extract_domain("https://www.mycareersfuture.gov.sg/job/123")
        assert result == "www.mycareersfuture.gov.sg"

    def test_handles_invalid_url(self):
        """Should return empty string for invalid URLs that don't parse properly."""
        result = _extract_domain("not a url")
        # urlparse returns empty netloc for malformed URLs, not an exception
        assert result == ""


class TestJDFetchResult:
    """JDFetchResult dataclass tests."""

    def test_has_required_fields(self):
        """JDFetchResult should have all required fields."""
        result = JDFetchResult(
            text="Job description text",
            source_url="https://example.com",
            source_platform="mcf",
            cached=False,
            fetched_at=None,
        )
        assert hasattr(result, 'text')
        assert hasattr(result, 'source_url')
        assert hasattr(result, 'source_platform')
        assert hasattr(result, 'cached')
        assert hasattr(result, 'fetched_at')


class TestJDCaching:
    """JD fetch caching tests."""

    def test_clear_jd_cache_all(self):
        """clear_jd_cache with no args should clear all."""
        clear_jd_cache()  # Should not raise

    def test_clear_jd_cache_specific_url(self):
        """clear_jd_cache with URL should clear that URL's cache."""
        # Just verify it doesn't raise - URL not in cache is fine
        clear_jd_cache("https://www.mycareersfuture.gov.sg/job/test")

"""Tests for S3 service - resume storage."""
import pytest
from keystone.services.s3 import (
    get_resume_bucket,
    _get_content_type,
)


class TestGetResumeBucket:
    """Resume bucket name tests."""

    def test_bucket_name_format(self):
        """Bucket name should follow keystone-resumes-{env} format."""
        bucket = get_resume_bucket()
        assert bucket.startswith("keystone-resumes-")
        assert "dev" in bucket or "staging" in bucket or "prod" in bucket


class TestGetContentType:
    """Content type detection tests."""

    def test_pdf_content_type(self):
        """PDF extension should return pdf content type."""
        assert _get_content_type("resume.pdf") == "application/pdf"

    def test_docx_content_type(self):
        """DOCX extension should return word processing content type."""
        result = _get_content_type("resume.docx")
        assert result == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

    def test_doc_content_type(self):
        """DOC extension should return msword content type."""
        assert _get_content_type("resume.doc") == "application/msword"

    def test_unknown_extension_returns_octet_stream(self):
        """Unknown extension should return octet-stream."""
        assert _get_content_type("resume.txt") == "application/octet-stream"
        assert _get_content_type("resume.unknown") == "application/octet-stream"

    def test_case_insensitive(self):
        """Extension check should be case insensitive."""
        assert _get_content_type("resume.PDF") == "application/pdf"
        assert _get_content_type("resume.DOCX") == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

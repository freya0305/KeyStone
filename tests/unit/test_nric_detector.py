"""Tests for NRIC detector - PDPA compliance critical."""
import pytest
from keystone.services.nric_detector import (
    detect_nric,
    mask_nric,
    assert_no_nric,
    NRICDetectedError,
)


class TestDetectNRIC:
    """NRIC detection tests."""

    def test_detect_valid_nric_s_prefix(self):
        """S1234567A should be detected."""
        result = detect_nric("My NRIC is S1234567A")
        assert result.found is True
        assert result.count == 1

    def test_detect_valid_nric_t_prefix(self):
        """T9876543B should be detected."""
        result = detect_nric("NRIC: T9876543B")
        assert result.found is True
        assert result.count == 1

    def test_detect_valid_nric_f_prefix(self):
        """F5555555C should be detected."""
        result = detect_nric("IC: F5555555C")
        assert result.found is True

    def test_detect_valid_nric_g_prefix(self):
        """G4444444D should be detected."""
        result = detect_nric("G4444444D")
        assert result.found is True

    def test_detect_multiple_nric(self):
        """Multiple NRICs in text should all be detected."""
        text = "Father S1234567A, Mother T9876543B"
        result = detect_nric(text)
        assert result.count == 2

    def test_no_nric_found(self):
        """Normal text without NRIC should return found=False."""
        text = "I am a software engineer with 5 years experience."
        result = detect_nric(text)
        assert result.found is False
        assert result.count == 0
        assert result.redacted_content == text


class TestMaskNRIC:
    """NRIC masking tests."""

    def test_mask_replaces_nric(self):
        """NRIC should be replaced with [NRIC REDACTED]."""
        text = "My NRIC is S1234567A"
        result = detect_nric(text)
        assert "[NRIC REDACTED]" in result.redacted_content
        assert "S1234567A" not in result.redacted_content

    def test_mask_preserves_rest_of_text(self):
        """Text around NRIC should be preserved."""
        text = "Name: John, NRIC: S1234567A, Email: john@example.com"
        result = detect_nric(text)
        assert "Name: John" in result.redacted_content
        assert "Email: john@example.com" in result.redacted_content


class TestAssertNRIC:
    """NRIC assertion tests."""

    def test_assert_raises_on_nric(self):
        """assert_no_nric should raise NRICDetectedError when NRIC found."""
        with pytest.raises(NRICDetectedError):
            assert_no_nric("My NRIC is S1234567A")

    def test_assert_passes_without_nric(self):
        """assert_no_nric should pass when no NRIC found."""
        text = "No NRIC here"
        assert_no_nric(text)  # Should not raise


class TestNRICPatternsEdgeCases:
    """Edge cases for NRIC detection."""

    def test_nric_with_spaces(self):
        """NRIC with spaces should be detected."""
        result = detect_nric("IC: S 1234567 A")
        assert result.found is True

    def test_lowercase_prefix(self):
        """Lowercase prefix should still be detected."""
        result = detect_nric("s1234567a")
        assert result.found is True

    def test_nric_in_sentence(self):
        """NRIC embedded in sentence should be detected."""
        text = "Please use my IC S1234567A for verification."
        result = detect_nric(text)
        assert result.found is True

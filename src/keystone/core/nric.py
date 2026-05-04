"""NRIC detection and masking utilities.

Three-stage pipeline for PDPA-compliant NRIC handling:
- Stage 1: mask at S3 upload (before storage)
- Stage 2: assert before Claude API call (before sending to external AI)
- Stage 3: sanitize Claude output (before storing AI-generated suggestions)

NRIC regex pattern: [STFGstfg]\d{7}[A-Za-z]
Singapore NRIC format: S1234567A or T1234567A (old), F1234567A or G1234567A (new)
"""
import re
from typing import List

import structlog

logger = structlog.get_logger()

# NRIC/FIN regex: S/T/F/G followed by 7 digits followed by a letter
_NRIC_PATTERN = re.compile(r"[STFGstfg]\d{7}[A-Za-z]")
_NRIC_REPLACEMENT = "[NRIC_REDACTED]"


class NRICDetectedError(ValueError):
    """Raised when NRIC is detected and must be masked."""
    pass


def detect_nric(text: str) -> List[str]:
    """Find all NRIC/FIN patterns in text.

    Args:
        text: Input text to search

    Returns:
        List of all NRIC matches found (original case as-is)

    Example:
        >>> detect_nric("My NRIC is S1234567A and T9876543B")
        ['S1234567A', 'T9876543B']
    """
    return _NRIC_PATTERN.findall(text)


def mask_nric(text: str) -> str:
    """Replace all NRIC/FIN patterns with redaction marker.

    Preserves surrounding text. Use this at Stage 1 (S3 upload)
    and Stage 3 (Claude output sanitization).

    Args:
        text: Input text with potential NRICs

    Returns:
        Text with all NRIC patterns replaced

    Example:
        >>> mask_nric("My NRIC is S1234567A")
        'My NRIC is [NRIC_REDACTED]'
    """
    return _NRIC_PATTERN.sub(_NRIC_REPLACEMENT, text)


def assert_no_nric(text: str) -> None:
    """Assert that text contains no NRIC patterns.

    Use this at Stage 2 (before Claude API call) to prevent
    accidental NRIC leakage to external AI services.

    Raises:
        NRICDetectedError: If any NRIC pattern is found in text

    Example:
        >>> assert_no_nric("Normal text with no NRIC")  # passes
        >>> assert_no_nric("My NRIC is S1234567A")
        NRICDetectedError: Detected 1 NRIC(s) in text
    """
    matches = detect_nric(text)
    if matches:
        logger.warning("nric.detected", count=len(matches), samples=matches[:3])
        raise NRICDetectedError(f"Detected {len(matches)} NRIC(s) in text")


def detect_nric_count(text: str) -> int:
    """Return count of NRIC patterns in text.

    Useful for logging detection events without storing the actual NRIC.
    """
    return len(detect_nric(text))

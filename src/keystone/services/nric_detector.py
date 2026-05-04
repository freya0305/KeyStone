"""NRIC detection for PDPA compliance.

Red team finding: NRIC detection gap.
NRIC patterns must be flagged/redacted, never stored.
"""
import re
from dataclasses import dataclass

import structlog

logger = structlog.get_logger()

# Singapore NRIC pattern: S/F/G + 7 digits + letter
NRIC_PATTERN = re.compile(
    r'\b([SFTGstftg])\s*(\d{7})\s*([A-Za-z])\b',
    re.IGNORECASE,
)

# Alternative: NRIC in format like S1234567A
NRIC_PATTERN_ALT = re.compile(
    r'\b([SFTG])\d{7}([A-Za-z])\b',
)


@dataclass
class NRICDetectionResult:
    found: bool
    count: int
    redacted_content: str


def detect_nric(content: str) -> NRICDetectionResult:
    """Detect NRIC numbers in text.

    Returns:
        NRICDetectionResult with count and redacted version.
        The redacted version replaces NRIC with [NRIC REDACTED].
    """
    matches = NRIC_PATTERN.findall(content)
    if not matches:
        matches = NRIC_PATTERN_ALT.findall(content)

    count = len(matches)

    if count == 0:
        return NRICDetectionResult(
            found=False,
            count=0,
            redacted_content=content,
        )

    # Redact all found NRICs
    redacted = content
    for match in matches:
        if isinstance(match, tuple):
            # Format: S 1234567 A -> S1234567A
            redacted_nric = f"{match[0].upper()}{match[1]}{match[2].upper()}"
        else:
            # Already formatted
            redacted_nric = match
        redacted = redacted.replace(redacted_nric, "[NRIC REDACTED]")

    logger.warning("nric_detected", count=count)

    return NRICDetectionResult(
        found=True,
        count=count,
        redacted_content=redacted,
    )


def validate_content(content: str) -> tuple[bool, str]:
    """Validate content for NRIC and other sensitive data.

    Returns:
        (is_safe, redacted_content)
    """
    result = detect_nric(content)
    return (not result.found, result.redacted_content)


class NRICDetectedError(ValueError):
    """Raised when NRIC is detected and must be masked before processing."""

    pass


def assert_no_nric(content: str) -> None:
    """Assert that content contains no NRIC patterns.

    Use at Stage 2 (before Claude API call) to prevent accidental
    NRIC leakage to external AI services.

    Raises:
        NRICDetectedError: If any NRIC pattern is found

    Example:
        >>> assert_no_nric("Normal text with no NRIC")  # passes
        >>> assert_no_nric("My NRIC is S1234567A")  # raises NRICDetectedError
    """
    result = detect_nric(content)
    if result.found:
        logger.warning("nric.detected_before_claude", count=result.count)
        raise NRICDetectedError(
            f"Detected {result.count} NRIC(s) in content. "
            "Content must be masked before sending to external AI services."
        )


def mask_nric(content: str) -> str:
    """Replace all NRIC patterns with redaction marker.

    Use at Stage 1 (before S3 upload) and Stage 3 (sanitize Claude output).

    Args:
        content: Input text with potential NRICs

    Returns:
        Text with all NRIC patterns replaced with [NRIC_REDACTED]

    Example:
        >>> mask_nric("My NRIC is S1234567A")
        'My NRIC is [NRIC_REDACTED]'
    """
    result = detect_nric(content)
    return result.redacted_content

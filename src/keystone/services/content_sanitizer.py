"""Content sanitization for PDPA compliance.

Handles:
- NRIC detection and redaction
- General sensitive data detection
- Safe content storage

All content stored must be sanitized. NRIC numbers are NEVER stored.
"""
import re
from dataclasses import dataclass
from typing import Optional

import structlog

from keystone.services.nric_detector import detect_nric, NRIC_PATTERN

logger = structlog.get_logger()


@dataclass
class SanitizationResult:
    """Result of content sanitization."""
    is_safe: bool
    sanitized_content: str
    warnings: list[str]


def sanitize_resume_content(content: str) -> SanitizationResult:
    """Sanitize resume content for storage.

    - Detects and redacts NRIC numbers
    - Flags other potential sensitive data
    - Returns sanitized content safe for storage

    Args:
        content: Raw resume text content

    Returns:
        SanitizationResult with sanitized content and any warnings
    """
    warnings = []

    # Check for NRIC
    nric_result = detect_nric(content)
    if nric_result.found:
        warnings.append(f"NRIC detected ({nric_result.count}x) - redacted")
        logger.warning("nric_in_resume", count=nric_result.count)

    # Additional patterns to check
    patterns_to_check = [
        (" passport", r'\b[A-Z]{1,2}\d{6,9}\b', "Passport number"),
        ("bank account", r'\b\d{8,16}\b', "Bank account number"),
    ]

    for pattern_name, regex, label in patterns_to_check:
        if pattern_name.lower() in content.lower():
            matches = re.findall(regex, content)
            if matches:
                # Just warn, don't auto-redact without confirmation
                warnings.append(f"Potential {label} detected - manual review recommended")

    return SanitizationResult(
        is_safe=not nric_result.found,
        sanitized_content=nric_result.redacted_content,
        warnings=warnings,
    )


def validate_before_storage(content: str) -> tuple[bool, str]:
    """Validate content is safe for storage.

    This should be called BEFORE any content is stored to DB or S3.

    Args:
        content: Content to validate

    Returns:
        (is_valid, error_message)
    """
    nric_result = detect_nric(content)

    if nric_result.found:
        return False, f"Content contains {nric_result.count} NRIC number(s) which cannot be stored. Content has been redacted but NOT stored."

    return True, ""


def mask_sensitive_fields(data: dict) -> dict:
    """Mask potentially sensitive fields in a dict.

    Used for logging and display purposes.

    Args:
        data: Dictionary with potentially sensitive fields

    Returns:
        Dictionary with sensitive fields masked
    """
    sensitive_fields = {"nric", "passport", "bank_account", "credit_card", "password"}

    masked = data.copy()
    for key in masked:
        if any(sf in key.lower() for sf in sensitive_fields):
            masked[key] = "***REDACTED***"

    return masked

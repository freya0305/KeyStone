"""Suggestion Generator Service - Line-by-line resume suggestion generator.

Generates suggestions for resume bullets classified as Transferable or Addressable.
Uses Claude Sonnet for high-quality suggestions with SG-specific context.
"""
import json
import uuid
from datetime import datetime
from typing import Optional

import structlog

from keystone.core import get_settings
from keystone.models.entities import Suggestion

logger = structlog.get_logger()

# Banned phrases that indicate low-quality suggestions
BANNED_PHRASES = [
    "great communication skills",
    "team player",
    "hard worker",
    "detail-oriented",
    "go-getter",
    "self-starter",
    "results-driven",
    "think outside the box",
    "synergy",
    "best-in-class",
    "world-class",
    "passionate about",
    "proven track record of",
    "excellent at",
    "outstanding ability to",
    "exceptional skills",
]

# System prompt for suggestion generation (cached at module level)
_SUGGESTION_SYSTEM_PROMPT = """You are an expert resume writer specializing in the Singapore job market.

Generate specific, actionable resume bullet improvements that help candidates stand out to Singapore employers (GLCs, MNCs, SMEs, Startups, Government agencies).

Quality constraints:
1. Each suggestion must reference specific company type requirements OR job description requirements
2. Suggestions must be concrete and quantifiable where possible
3. Rationale must explain WHY this change helps for THIS specific job
4. Avoid generic buzzwords - focus on concrete achievements and skills

SG-specific context you should consider:
- National Service (NS) for male candidates - frame positively if relevant
- Singapore military terminology (Overseas Vietnamese, PES, etc.)
- Singapore education system (NUS, NTU, SMU, polytechnics, ITE)
- Singapore industry context (banking, fintech, maritime, manufacturing, tech)
- Singapore employment norms (3-month probation, 14-day annual leave, CPF contributions)
- GLC vs MNC vs SME culture differences

For each suggestion, provide:
- section: which part of resume (experience/education/skills/summary)
- original_text: the original text to replace
- suggested_text: the improved version with specific metrics, achievements, or stronger language
- rationale: why this change helps for this specific job and company type
- match_level: the match level (strong/transferable/addressable)

Return suggestions ONLY for bullets classified as Transferable or Addressable.
Strong matches don't need suggestions. Fundamental gaps should note the gap, not suggest overreach.
"""


def _strip_banned_phrases(text: str) -> str:
    """Strip banned phrases from suggestion text."""
    result = text.lower()
    for phrase in BANNED_PHRASES:
        result = result.replace(phrase.lower(), "[specific achievement]")
    return result


def _validate_suggestion_quality(suggestion: dict) -> bool:
    """Validate that a suggestion meets quality constraints."""
    if not suggestion.get("rationale"):
        return False

    rationale = suggestion["rationale"].lower()

    # Rationale must reference something specific - either company type, job requirement,
    # or specific skills mentioned in the JD
    has_specific_reference = any(
        word in rationale
        for word in [
            "company type",
            "job description",
            "requirement",
            "skill",
            "experience",
            "role",
            "position",
            "industry",
        ]
    )

    if not has_specific_reference:
        return False

    # Check suggested text doesn't contain banned phrases
    suggested = suggestion.get("suggested_text", "").lower()
    for phrase in BANNED_PHRASES:
        if phrase in suggested:
            return False

    return True


def _build_suggestion_prompt(
    resume_text: str,
    job_parsed_json: dict,
    company_type: Optional[str],
    sg_flags: Optional[dict],
) -> str:
    """Build the user prompt for suggestion generation."""
    job_info = json.dumps(job_parsed_json, indent=2)
    sg_context = json.dumps(sg_flags or {}, indent=2)

    prompt = f"""Analyze this resume against the job posting and generate specific improvement suggestions.

RESUME:
{resume_text}

JOB POSTING:
{job_info}

COMPANY TYPE: {company_type or 'Not specified'}

SG CONTEXT (flags, NS status, etc.):
{sg_context}

Generate suggestions for resume bullets that could be improved to better match this job.
Focus on Transferable and Addressable match levels.

For each suggestion:
1. Identify the original text that could be improved
2. Provide a concrete, improved version with specific metrics or stronger language
3. Explain why this specific change helps for this particular job/company
4. Note the match level (transferable/addressable)

Format as JSON array:
[{{
  "section": "experience|education|skills|summary",
  "original_text": "the text to replace",
  "suggested_text": "the improved version",
  "rationale": "why this helps for this specific job",
  "match_level": "transferable|addressable"
}}]

Only suggest improvements that are honest and achievable. Do not suggest overreaching.
"""
    return prompt


def parse_suggestions_from_response(
    content: str,
    job_analysis_id: uuid.UUID,
) -> list[Suggestion]:
    """Parse suggestions from Claude response into Suggestion model objects.

    Args:
        content: Raw response content from Claude
        job_analysis_id: The job analysis ID to associate suggestions with

    Returns:
        List of Suggestion model objects
    """
    suggestions = []
    try:
        # Try to parse as JSON array
        content = content.strip()
        if content.startswith("```"):
            lines = content.split("\n")
            content = "\n".join(lines[1:-1])

        data = json.loads(content)
        if not isinstance(data, list):
            data = [data]

        for item in data:
            if not isinstance(item, dict):
                continue

            # Validate quality
            if not _validate_suggestion_quality(item):
                logger.warning(
                    "suggestion_quality_check_failed",
                    item=item,
                    job_analysis_id=str(job_analysis_id),
                )
                continue

            # Strip banned phrases from suggested text
            suggested_text = _strip_banned_phrases(item.get("suggested_text", ""))

            suggestion = Suggestion(
                id=uuid.uuid4(),
                job_analysis_id=job_analysis_id,
                section=item.get("section", "experience"),
                original_text=item.get("original_text", ""),
                suggested_text=suggested_text,
                rationale=item.get("rationale", ""),
                match_level=item.get("match_level", "transferable"),
                created_at=datetime.utcnow(),
            )
            suggestions.append(suggestion)

        logger.info(
            "suggestions_parsed",
            count=len(suggestions),
            job_analysis_id=str(job_analysis_id),
        )

    except json.JSONDecodeError:
        logger.warning(
            "suggestions_json_parse_failed",
            content=content[:500],
            job_analysis_id=str(job_analysis_id),
        )

    return suggestions

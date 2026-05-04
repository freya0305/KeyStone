"""M3.2 - JD Parsing Service (Claude Haiku).

Input: raw JD text
Output: job_title, company_name, requirements, responsibilities, benefits, seniority_level, industry
Uses Claude Haiku
NRIC Stage 2: assert_no_nric before Claude call
"""
import json
from dataclasses import dataclass
from typing import Optional

import structlog

from keystone.core import get_settings
from keystone.services.claude_client import get_claude_client, ClaudeResponse
from keystone.services.nric_detector import assert_no_nric, NRICDetectedError

logger = structlog.get_logger()


@dataclass
class ParsedJobDescription:
    """Structured job description from parsing."""
    job_title: str
    company_name: str
    requirements: list[str]
    responsibilities: list[str]
    benefits: list[str]
    seniority_level: str  # junior|mid|senior|lead|manager|director
    industry: str
    raw_skills: list[str]  # Extracted skills list for convenience


_JD_PARSE_SYSTEM_PROMPT = """You are a job posting analyst specializing in Singapore job market.

Extract structured information from the job posting text below.
Return ONLY valid JSON with these exact fields:
- job_title: The job title (e.g., "Software Engineer")
- company_name: Company name (or "Not Specified")
- requirements: Array of requirement strings (skills, qualifications, experience)
- responsibilities: Array of responsibility strings (day-to-day duties)
- benefits: Array of benefit strings (what the company offers)
- seniority_level: One of: junior|mid|senior|lead|manager|director|not_specified
- industry: Industry sector (e.g., "Banking", "Technology", "Healthcare") or "Not Specified"
- raw_skills: Array of skill keywords extracted from the posting

Be thorough but concise. Focus on actionable information."""


async def parse_job_description(raw_text: str) -> ParsedJobDescription:
    """Parse raw job description text into structured format.

    Args:
        raw_text: Raw job description text (from URL fetch or paste)

    Returns:
        ParsedJobDescription with structured fields

    Raises:
        NRICDetectedError: If NRIC is detected before sending to Claude
        ValueError: If parsing fails
    """
    # Stage 2: Assert no NRIC before Claude API call
    assert_no_nric(raw_text)

    settings = get_settings()
    client = get_claude_client()

    # Truncate to avoid excessive tokens (first 4000 chars should have most info)
    truncated_text = raw_text[:4000]

    prompt = f"""Extract structured job information from this posting:

{truncated_text}

Return ONLY valid JSON, no markdown or explanation."""

    try:
        response: ClaudeResponse = await client.generate(
            model=settings.anthropic_model_haiku,
            system_prompt=_JD_PARSE_SYSTEM_PROMPT,
            user_prompt=prompt,
            max_tokens=1024,
        )

        # Parse JSON from response
        content = response.content.strip()
        # Remove markdown code blocks if present
        if content.startswith("```"):
            lines = content.split("\n")
            content = "\n".join(lines[1:-1])

        result = json.loads(content)

        parsed = ParsedJobDescription(
            job_title=result.get("job_title", "Unknown Title"),
            company_name=result.get("company_name", "Not Specified"),
            requirements=result.get("requirements", []),
            responsibilities=result.get("responsibilities", []),
            benefits=result.get("benefits", []),
            seniority_level=result.get("seniority_level", "not_specified"),
            industry=result.get("industry", "Not Specified"),
            raw_skills=result.get("raw_skills", []),
        )

        logger.info(
            "jd_parse.success",
            job_title=parsed.job_title,
            company=parsed.company_name,
            requirements_count=len(parsed.requirements),
        )

        return parsed

    except json.JSONDecodeError as e:
        logger.warning("jd_parse.json_decode_failed", error=str(e), content=response.content[:500])
        raise ValueError(f"Failed to parse job description JSON: {e}")
    except NRICDetectedError:
        raise
    except Exception as e:
        logger.error("jd_parse.error", error=str(e))
        raise ValueError(f"Failed to parse job description: {e}")


def parsed_to_dict(parsed: ParsedJobDescription) -> dict:
    """Convert ParsedJobDescription to dict for storage.

    Args:
        parsed: Parsed job description

    Returns:
        Dictionary suitable for JSON storage
    """
    return {
        "job_title": parsed.job_title,
        "company_name": parsed.company_name,
        "requirements": parsed.requirements,
        "responsibilities": parsed.responsibilities,
        "benefits": parsed.benefits,
        "seniority_level": parsed.seniority_level,
        "industry": parsed.industry,
        "raw_skills": parsed.raw_skills,
    }

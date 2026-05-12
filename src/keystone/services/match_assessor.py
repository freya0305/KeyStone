"""M3.4 - Four-Level Match Assessment (Claude Sonnet).

Assess each JD requirement against resume
Output: strong/transferable/addressable/fundamental
SG system prompt (cached)
Rationale must reference company type OR JD requirement
"""
import json
from dataclasses import dataclass
from typing import Optional

import structlog

from keystone.core import get_settings
from keystone.services.claude_client import get_claude_client, ClaudeResponse
from keystone.services.nric_detector import assert_no_nric, NRICDetectedError

logger = structlog.get_logger()


# Match level definitions
MATCH_LEVELS = {
    "strong": "Candidate clearly has this skill/requirement",
    "transferable": "Candidate has adjacent experience that applies",
    "addressable": "Candidate can claim this with some reframing",
    "fundamental": "Candidate lacks this skill/requirement",
}

# SG-specific context for match assessment
_SG_MATCH_CONTEXT = """
You are assessing resumes for the Singapore job market.
Consider:
- Singapore employers value local qualifications (NUS, NTU, SMU, SIT, SUSS)
- Singapore diplomas from polytechnics are valued for mid-level roles
- Professional certifications (CFA, CPA, ACCA) are highly valued in finance
- Tech certifications (AWS, GCP, Azure) valued in tech roles
- Singapore-specific skills: handling IRAS, CPF, MOM regulations are valuable for finance/HR/admin
- SGX-listed company experience is valued in finance
- Government sector experience valued for compliance roles
- GLC (Government-Linked Company) experience valued for stability and structured environment
- Startup experience valued for adaptability and broad exposure
"""


@dataclass
class RequirementMatch:
    """Match result for a single requirement."""
    requirement: str
    match_level: str  # strong|transferable|addressable|fundamental
    rationale: str
    company_type_reference: Optional[str] = None
    jd_requirement_reference: Optional[str] = None


@dataclass
class MatchAssessment:
    """Complete match assessment result."""
    requirement_matches: list[RequirementMatch]
    overall_score: float  # 0.0 to 100.0
    summary: str
    recommendations: list[str]


_MATCH_ASSESSMENT_SYSTEM_PROMPT = """You are an expert resume-job match analyst for the Singapore market.

For each requirement from the job posting, assess the candidate's resume against it.
Classify each into ONE of four levels:
- strong: The candidate clearly has this skill/experience as demonstrated in their resume
- transferable: The candidate has adjacent experience that directly applies (e.g., similar domain, related tools)
- addressable: The candidate could claim this with some reframing of their existing experience
- fundamental: The candidate does not have this skill/experience

IMPORTANT:
1. Each rationale MUST reference either the company type (e.g., "particularly valued at GLCs") OR a specific JD requirement
2. For Singapore market: consider local qualifications, professional certifications, and relevant experience
3. Be specific about what the resume shows vs what the job requires

Return your assessment as a JSON array of objects with this structure:
[{
  "requirement": "the specific requirement being assessed",
  "match_level": "strong|transferable|addressable|fundamental",
  "rationale": "Detailed explanation referencing company type or JD requirement",
  "match_evidence": "Specific resume evidence supporting this level"
}]

Also provide:
- overall_score: A number from 0-100 representing overall fit
- summary: Brief summary of overall fit
- recommendations: Array of 2-3 actionable suggestions for the candidate
"""


async def assess_match(
    resume_text: str,
    job_requirements: list[str],
    company_type: str,
    seniority_level: str,
    industry: str,
) -> MatchAssessment:
    """Assess resume against job requirements.

    Args:
        resume_text: Resume text (already masked for NRIC)
        job_requirements: List of job requirements to assess
        company_type: Classified company type (e.g., "banking_glc", "startup")
        seniority_level: Job seniority level
        industry: Industry sector

    Returns:
        MatchAssessment with per-requirement matches and overall score

    Raises:
        NRICDetectedError: If NRIC detected in resume before sending to Claude
    """
    # Stage 2: Assert no NRIC before Claude API call
    assert_no_nric(resume_text)

    if not job_requirements:
        return MatchAssessment(
            requirement_matches=[],
            overall_score=50.0,
            summary="No specific requirements to assess",
            recommendations=[],
        )

    settings = get_settings()
    client = get_claude_client()

    # Build the prompt with all context
    requirements_text = "\n".join(f"- {req}" for req in job_requirements)

    prompt = f"""Assess this resume against the job requirements.

Company context:
- Company type: {company_type}
- Seniority level: {seniority_level}
- Industry: {industry}

{_SG_MATCH_CONTEXT}

Job Requirements to assess:
{requirements_text}

Resume:
{resume_text[:3000]}

Return your assessment as a JSON object with this structure:
{{
  "assessments": [
    {{
      "requirement": "the requirement being assessed",
      "match_level": "strong|transferable|addressable|fundamental",
      "rationale": "Detailed explanation referencing company type or JD requirement",
      "match_evidence": "Specific resume evidence"
    }}
  ],
  "overall_score": 0-100,
  "summary": "Brief overall assessment",
  "recommendations": ["suggestion 1", "suggestion 2", "suggestion 3"]
}}

Return ONLY valid JSON, no markdown or explanation."""

    try:
        response: ClaudeResponse = await client.generate(
            model=settings.anthropic_model_sonnet,
            system_prompt=_MATCH_ASSESSMENT_SYSTEM_PROMPT,
            user_prompt=prompt,
            timeout=10.0,  # Analysis ≤10s per spec
            max_tokens=2048,
        )

        content = response.content.strip()
        if content.startswith("```"):
            lines = content.split("\n")
            content = "\n".join(lines[1:-1])

        result = json.loads(content)

        # Parse requirement matches
        requirement_matches = []
        for item in result.get("assessments", []):
            requirement_matches.append(RequirementMatch(
                requirement=item.get("requirement", ""),
                match_level=item.get("match_level", "fundamental"),
                rationale=item.get("rationale", ""),
                company_type_reference=company_type,
                jd_requirement_reference=item.get("requirement"),
            ))

        assessment = MatchAssessment(
            requirement_matches=requirement_matches,
            overall_score=float(result.get("overall_score", 50.0)),
            summary=result.get("summary", ""),
            recommendations=result.get("recommendations", []),
        )

        logger.info(
            "match_assessment.success",
            overall_score=assessment.overall_score,
            requirements_count=len(requirement_matches),
            company_type=company_type,
        )

        return assessment

    except json.JSONDecodeError as e:
        logger.warning("match_assessment.json_decode_failed", error=str(e), content=response.content[:500])
        raise ValueError(f"Failed to parse match assessment JSON: {e}")
    except NRICDetectedError:
        raise
    except Exception as e:
        logger.error("match_assessment.error", error=str(e))
        raise ValueError(f"Failed to assess match: {e}")


def assessment_to_dict(assessment: MatchAssessment) -> dict:
    """Convert MatchAssessment to dict for storage.

    Args:
        assessment: Match assessment result

    Returns:
        Dictionary suitable for JSON storage
    """
    return {
        "requirement_matches": [
            {
                "requirement": m.requirement,
                "match_level": m.match_level,
                "rationale": m.rationale,
                "company_type_reference": m.company_type_reference,
                "jd_requirement_reference": m.jd_requirement_reference,
            }
            for m in assessment.requirement_matches
        ],
        "overall_score": assessment.overall_score,
        "summary": assessment.summary,
        "recommendations": assessment.recommendations,
    }


def calculate_overall_score(requirement_matches: list[RequirementMatch]) -> float:
    """Calculate overall score from requirement matches.

    Args:
        requirement_matches: List of requirement match results

    Returns:
        Overall score 0-100
    """
    if not requirement_matches:
        return 50.0

    scores = {
        "strong": 100,
        "transferable": 70,
        "addressable": 40,
        "fundamental": 0,
    }

    total = sum(scores.get(m.match_level, 50) for m in requirement_matches)
    return round(total / len(requirement_matches), 1)

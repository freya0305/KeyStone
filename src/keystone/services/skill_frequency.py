"""Section-weighted skill frequency calculation per architecture spec §2.

Section weights:
- Requirements / Must Have: 1.0
- Responsibilities: 0.5
- Nice to Have / Plus: 0.3
- About the Role / Overview: 0.2
- Benefits / Perks: 0.05
"""
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional

# Section weights from architecture spec §2
SECTION_WEIGHTS: dict[str, float] = {
    "requirements": 1.0,
    "must_have": 1.0,
    "required": 1.0,
    "nice_to_have": 0.3,
    "preferred": 0.3,
    "plus": 0.3,
    "overview": 0.2,
    "about": 0.2,
    "about_role": 0.2,
    "role_overview": 0.2,
    "responsibilities": 0.5,
    "role": 0.5,
    "duties": 0.5,
    "what_youll_do": 0.5,
    "benefits": 0.05,
    "perks": 0.05,
    "what_we_offer": 0.05,
    "compensation": 0.05,
}

# Recency weights from architecture spec §5
RECENCY_WEIGHTS: dict[str, float] = {
    "fresh": 1.0,  # posted < 90 days ago
    "stale": 0.7,  # posted 90-180 days ago
    "old": 0.5,  # posted 180-365 days ago
    "excluded": 0.0,  # posted > 365 days ago
}


@dataclass
class SkillFrequency:
    """Skill frequency data."""

    skill: str
    raw_weighted_freq: float
    required_count: int
    preferred_count: int
    total_jds: int


def get_section_weight(section_name: str) -> float:
    """Get weight for a section name."""
    return SECTION_WEIGHTS.get(section_name.lower().strip(), 0.3)


def get_recency_weight(posted_at: Optional[datetime]) -> float:
    """Calculate recency weight based on posting date."""
    if posted_at is None:
        return 1.0  # assume fresh if unknown

    now = datetime.utcnow()
    age_days = (now - posted_at).days

    if age_days <= 90:
        return RECENCY_WEIGHTS["fresh"]
    elif age_days <= 180:
        return RECENCY_WEIGHTS["stale"]
    elif age_days <= 365:
        return RECENCY_WEIGHTS["old"]
    else:
        return RECENCY_WEIGHTS["excluded"]


def calculate_weighted_frequency(
    required_count: int,
    preferred_count: int,
    total_jds: int,
) -> float:
    """Calculate section-weighted frequency.

    Formula: (required_count × 1.0 + preferred_count × 0.3) / total_jds

    Architecture spec §2 example:
    - Python: Requirements 73 times, Nice to Have 27 times
      = (73 × 1.0 + 27 × 0.3) / 100 = 0.811

    Args:
        required_count: Number of JDs where skill is in requirements section
        preferred_count: Number of JDs where skill is in nice-to-have section
        total_jds: Total number of JDs analyzed

    Returns:
        Weighted frequency score (0.0 to ~1.0+)
    """
    if total_jds == 0:
        return 0.0
    return (required_count * 1.0 + preferred_count * 0.3) / total_jds


def detect_section(text: str) -> str:
    """Detect which section this text belongs to based on surrounding context.

    Args:
        text: Job description text chunk

    Returns:
        Section name (requirements, nice_to_have, overview, responsibilities, benefits)
    """
    text_lower = text.lower()

    # Section header patterns
    if any(kw in text_lower for kw in ["requirement", "must have", "what you need", "skills required"]):
        return "requirements"
    elif any(kw in text_lower for kw in ["nice to have", "preferred", "plus", "bonus", "advantage"]):
        return "nice_to_have"
    elif any(kw in text_lower for kw in ["overview", "about the role", "about this role", "role overview"]):
        return "overview"
    elif any(kw in text_lower for kw in ["responsibility", "what you'll do", "duties", "role and resp"]):
        return "responsibilities"
    elif any(kw in text_lower for kw in ["benefit", "perk", "what we offer", "compensation"]):
        return "benefits"
    else:
        return "overview"  # default


@dataclass
class JDStructured:
    """Structured JD data for skill extraction."""

    title: str
    company: str
    company_type: str
    industry: str
    seniority: str
    text: str
    posted_at: Optional[datetime] = None


def extract_skills_from_jd(
    jd: JDStructured,
    skill_patterns: list[str],
) -> dict[str, dict[str, int]]:
    """Extract skills and their section counts from a JD.

    Args:
        jd: Structured JD data
        skill_patterns: List of skill names to look for (already normalized)

    Returns:
        Dict: {skill: {"required": N, "preferred": N, "total": N}}
    """
    results: dict[str, dict[str, int]] = {skill: {"required": 0, "preferred": 0, "total": 0} for skill in skill_patterns}

    text_lower = jd.text.lower()

    # Split into sections
    section_keywords = {
        "requirements": ["requirement", "must have", "what you need", "skills required"],
        "nice_to_have": ["nice to have", "preferred", "plus", "bonus", "advantage"],
        "overview": ["overview", "about the role", "about this role", "role overview"],
        "responsibilities": ["responsibility", "what you'll do", "duties", "role and resp"],
        "benefits": ["benefit", "perk", "what we offer", "compensation"],
    }

    current_section = "overview"  # default

    lines = jd.text.split("\n")
    for line in lines:
        line_lower = line.lower()

        # Detect section change
        for section, keywords in section_keywords.items():
            if any(kw in line_lower for kw in keywords):
                current_section = section
                break

        # Count skills in this line
        for skill in skill_patterns:
            skill_lower = skill.lower()
            if skill_lower in line_lower:
                if current_section in ("requirements", "responsibilities"):
                    results[skill]["required"] += 1
                elif current_section in ("nice_to_have", "benefits"):
                    results[skill]["preferred"] += 1
                else:
                    # overview defaults to 0.2 weight
                    pass
                results[skill]["total"] += 1

    return results

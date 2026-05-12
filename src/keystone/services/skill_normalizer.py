"""Skill normalization pipeline per architecture spec §1.

3-step normalization:
1. Clean: lowercase, strip, remove trailing programming/development/skills, fix typos
2. Map to LinkedIn Skills Taxonomy (manual mapping table)
3. Expand abbreviations (ML → Machine Learning, etc.)
"""
import re
from typing import Optional

# Hard-coded abbreviation expansions (architecture spec §1 step 3)
# Only expand if the skill IS the abbreviation, not a substring
ABBREVIATION_MAP: dict[str, str] = {
    "ML": "Machine Learning",
    "DL": "Deep Learning",
    "AI": "Artificial Intelligence",
    "PM": "Project Management",  # context-dependent, recruiter intent
    "FS": "Financial Services",  # context-dependent
    "JS": "JavaScript",
    "TS": "TypeScript",
    "ReactJS": "React",
    "NodeJS": "Node.js",
    "VueJS": "Vue.js",
    "Vue": "Vue.js",  # normalize Vue → Vue.js
    "AWS": "Amazon Web Services",
    "GCP": "Google Cloud Platform",
    "Azure": "Microsoft Azure",
    "K8s": "Kubernetes",
    "Kubernetes": "Kubernetes",
    " Postgres": "PostgreSQL",
    "Py": "Python",
    "Python": "Python",
    "React": "React",
    "Java": "Java",
    "JavaScript": "JavaScript",
    "TypeScript": "TypeScript",
    "Go": "Go",
    "Golang": "Go",
    "SQL": "SQL",
    "NoSQL": "NoSQL",
    "API": "API",
    "REST": "REST",
    "RESTful": "REST",
    "CI": "CI/CD",
    "CD": "CI/CD",
    "DevOps": "DevOps",
    "Agile": "Agile",
    "Scrum": "Scrum",
    "TDD": "TDD",
    "BDD": "BDD",
    "UX": "UX",
    "UI": "UI",
    "Figma": "Figma",
    "Sketch": "Sketch",
    "Docker": "Docker",
    "K8": "Kubernetes",
    "GKE": "Google Kubernetes Engine",
    "EKS": "Amazon EKS",
    "AKS": "Azure Kubernetes Service",
    "Lambda": "AWS Lambda",
    "S3": "AWS S3",
    "EC2": "AWS EC2",
    "RDS": "Amazon RDS",
    "DynamoDB": "Amazon DynamoDB",
    "PostgreSQL": "PostgreSQL",
    "MongoDB": "MongoDB",
    "Redis": "Redis",
    "Kafka": "Apache Kafka",
    "Spark": "Apache Spark",
    "Hadoop": "Hadoop",
    "TensorFlow": "TensorFlow",
    "PyTorch": "PyTorch",
    "Scikit-learn": "scikit-learn",
    "Pandas": "Pandas",
    "NumPy": "NumPy",
    "NLP": "Natural Language Processing",
    "CV": "Computer Vision",
    "MLOps": "MLOps",
    "Blockchain": "Blockchain",
    "QA": "Quality Assurance",
    "UAT": "User Acceptance Testing",
}

# Common typos (architecture spec §1 step 1)
TYPO_MAP: dict[str, str] = {
    "Sython": "Python",
    "Javscript": "JavaScript",
    "Typescrypt": "TypeScript",
    "Reactjs": "React",
    "Vuejs": "Vue.js",
    "Nodejs": "Node.js",
    "Postgress": "PostgreSQL",
    "Postres": "PostgreSQL",
    "Mongodb": "MongoDB",
    "Reddis": "Redis",
    "Kuberneties": "Kubernetes",
    "Kubernets": "Kubernetes",
    "Jav": "Java",
    "Javscript": "JavaScript",
    "Typescript": "TypeScript",
    "Pythong": "Python",
    "PYTHON": "Python",
    "Javascript": "JavaScript",
    "Typescripe": "TypeScript",
    "Reacts": "React",
    "C++": "C++",
    "C#": "C#",
    ".NET": ".NET",
    "Dotnet": ".NET",
    "Node": "Node.js",
    "NextJS": "Next.js",
    "Nextjs": "Next.js",
    "Next": "Next.js",
}

# Trailing words to strip (architecture spec §1 step 1)
TRAILING_WORDS_TO_STRIP = ["programming", "development", "skills", "skill", "engineer", "developer"]

# Skills that are too generic to be useful
SKILLS_BLOCKLIST: set[str] = {
    "experience",
    "work",
    "team",
    "ability",
    "skills",
    "knowledge",
    "understanding",
    "strong",
    "excellent",
    "good",
    "exposure",
    "working",
    "including",
    "etc",
    "various",
    "multiple",
    "new",
    "good communication",
    "communication",
    "communication skills",
}


def normalize_skill(skill: str) -> Optional[str]:
    """3-step normalization: clean → fix typos → expand abbreviations.

    Args:
        skill: Raw skill string

    Returns:
        Normalized skill string, or None if invalid
    """
    if not skill or not isinstance(skill, str):
        return None

    # Step 1: Clean
    s = skill.lower().strip()
    s = re.sub(r"\s+", " ", s)  # collapse whitespace

    # Remove trailing programming/development/skills
    for word in TRAILING_WORDS_TO_STRIP:
        if s.endswith(f" {word}"):
            s = s[: -len(word) - 1]
        if s == word:
            s = ""

    # Remove common suffixes that don't add meaning
    s = re.sub(r"\s*\(.*\)\s*$", "", s)  # Remove parenthetical

    if not s or len(s) < 2:
        return None

    # Step 2: Fix typos
    for typo, correction in TYPO_MAP.items():
        if s == typo.lower():
            s = correction.lower()
            break

    # Step 3: Expand abbreviations (only if skill IS the abbreviation)
    s_lower = s.lower().strip()
    for abbr, full in ABBREVIATION_MAP.items():
        if s_lower == abbr.lower():
            s = full
            break

    # Check blocklist
    if s_lower in SKILLS_BLOCKLIST:
        return None

    # Filter single characters and numbers
    if len(s) < 2:
        return None

    return s.strip()


def normalize_skill_list(skills: list[str]) -> list[str]:
    """Deduplicate + normalize a list of skills.

    Args:
        skills: List of raw skill strings

    Returns:
        Deduplicated, normalized, sorted list of skills
    """
    normalized: set[str] = set()
    for skill in skills:
        n = normalize_skill(skill)
        if n:
            normalized.add(n)
    return sorted(normalized)


def normalize_title(title: str) -> str:
    """Normalize a job title for matching.

    Args:
        title: Raw job title

    Returns:
        Normalized title
    """
    if not title:
        return ""

    t = title.lower().strip()
    t = re.sub(r"\s+", " ", t)

    # Common title simplifications
    title_normalizations = {
        "software engineer": "software engineer",
        "software developer": "software engineer",
        "swe": "software engineer",
        "senior software engineer": "senior software engineer",
        "staff software engineer": "staff engineer",
        "principal engineer": "principal engineer",
        "engineering manager": "engineering manager",
        "product manager": "product manager",
        "pm": "product manager",
        "data scientist": "data scientist",
        "data analyst": "data analyst",
        "machine learning engineer": "machine learning engineer",
        "mle": "machine learning engineer",
        "devops engineer": "devops engineer",
        "sre": "sre",
        "site reliability engineer": "sre",
        "frontend engineer": "frontend engineer",
        "front-end engineer": "frontend engineer",
        "frontend developer": "frontend developer",
        "back-end engineer": "backend engineer",
        "backend engineer": "backend engineer",
        "full stack engineer": "full stack engineer",
        "fullstack engineer": "full stack engineer",
        "full stack developer": "full stack developer",
        "ui engineer": "ui engineer",
        "ux designer": "ux designer",
        "product designer": "product designer",
    }

    for variant, standard in title_normalizations.items():
        if variant in t:
            return standard

    return t.strip()

"""ETL pipeline for skill frequency computation.

Performs nightly batch ETL to rebuild role_skill_frequency table.
Architecture: specs/jd-generator-architecture.md §5

Cadence:
- Real-time: New user_submitted JDs go into raw queue
- Nightly batch: ETL runs overnight, rebuilds skill_frequency
- Full rebuild: Every 7 days
"""
import structlog
from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID

from sqlalchemy import select, func, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession

from keystone.models.base import async_session_factory
from keystone.models.entities import RawJD, NormalizedRole, RoleSkillFrequency
from keystone.services.skill_normalizer import normalize_skill_list, normalize_title
from keystone.services.skill_frequency import (
    calculate_weighted_frequency,
    get_recency_weight,
    detect_section,
    JDStructured,
    extract_skills_from_jd,
)

logger = structlog.get_logger()

# Common technical skills to look for (MVP list)
# In production, this would be derived from LinkedIn Skills Taxonomy
SKILL_PATTERNS = [
    # Programming Languages
    "Python", "Java", "JavaScript", "TypeScript", "Go", "Rust", "C++", "C#", "Ruby", "PHP", "Swift", "Kotlin",
    # Web
    "React", "Vue.js", "Angular", "Next.js", "Node.js", "Django", "FastAPI", "Flask", "Spring", "Express",
    # Data
    "SQL", "PostgreSQL", "MySQL", "MongoDB", "Redis", "Elasticsearch", "Kafka", "Apache Spark", "Hadoop",
    # Cloud
    "AWS", "Amazon Web Services", "Google Cloud Platform", "Azure", "Microsoft Azure", "Kubernetes", "Docker",
    # AI/ML
    "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "scikit-learn", "Pandas", "NumPy", "NLP",
    "Computer Vision", "MLOps", "Natural Language Processing",
    # Practice
    "Agile", "Scrum", "TDD", "BDD", "CI/CD", "DevOps", "REST", "GraphQL", "Microservices",
    # Domain
    "Fintech", "Blockchain", "Cybersecurity", "Product Management", "Project Management",
    # Soft (excluded per architecture spec §1)
]


class SkillETL:
    """ETL pipeline for skill frequency computation."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def run_nightly_etl(
        self,
        title: Optional[str] = None,
        industry: Optional[str] = None,
        seniority: Optional[str] = None,
    ) -> dict:
        """Run nightly ETL for affected (title, industry, seniority) tuples.

        Args:
            title: Specific title to process (None = all)
            industry: Specific industry to process (None = all)
            seniority: Specific seniority to process (None = all)

        Returns:
            Stats dict with processing counts
        """
        logger.info("skill_etl.start", title=title, industry=industry, seniority=seniority)

        start_time = datetime.utcnow()
        stats = {
            "raw_jds_processed": 0,
            "roles_updated": 0,
            "skill_frequencies_computed": 0,
            "duration_seconds": 0,
        }

        try:
            # Step 1: Get eligible raw JDs
            # PDPA compliance: exclude B2B/university data — training pipeline only for B2C
            query = select(RawJD).where(
                and_(
                    RawJD.is_duplicate == False,
                    RawJD.is_spam == False,
                    RawJD.consent_given == True,
                    RawJD.data_source.not_in(["b2b", "university"]),
                )
            )

            # Apply filters
            if title:
                query = query.where(RawJD.job_title_raw.ilike(f"%{title}%"))
            if industry:
                query = query.where(RawJD.industry == industry)
            if seniority:
                query = query.where(RawJD.seniority == seniority)

            result = await self.session.execute(query)
            raw_jds = result.scalars().all()
            stats["raw_jds_processed"] = len(raw_jds)

            # Step 2: Group by (title_normalized, industry, seniority, company_type)
            jd_groups: dict[tuple, list[RawJD]] = {}
            for jd in raw_jds:
                normalized_title = normalize_title(jd.job_title_raw or "")
                key = (normalized_title, jd.industry, jd.seniority, jd.company_type)
                if normalized_title:
                    jd_groups.setdefault(key, []).append(jd)

            # Step 3: For each group, compute skill frequencies
            for (title_norm, industry, seniority, company_type), jds in jd_groups.items():
                await self._process_group(title_norm, industry, seniority, company_type, jds)
                stats["roles_updated"] += 1

            await self.session.commit()

            duration = (datetime.utcnow() - start_time).total_seconds()
            stats["duration_seconds"] = duration

            logger.info("skill_etl.complete", stats=stats)
            return stats

        except Exception as e:
            logger.error("skill_etl.failed", error=str(e))
            await self.session.rollback()
            raise

    async def _process_group(
        self,
        title_normalized: str,
        industry: str,
        seniority: str,
        company_type: str,
        jds: list[RawJD],
    ):
        """Process a group of JDs and compute skill frequencies."""
        # Get or create NormalizedRole
        role = await self._get_or_create_normalized_role(
            title_normalized, industry, seniority
        )

        # Aggregate skills across all JDs in group
        skill_counts: dict[str, dict[str, int]] = {}
        total_jds = len(jds)

        for jd in jds:
            if not jd.raw_text:
                continue

            # Apply recency weight
            recency_weight = get_recency_weight(jd.posted_at)
            if recency_weight == 0.0:
                continue

            # Extract skills from this JD
            jd_structured = JDStructured(
                title=jd.job_title_raw or "",
                company=jd.company or "",
                company_type=jd.company_type,
                industry=jd.industry,
                seniority=jd.seniority,
                text=jd.raw_text,
                posted_at=jd.posted_at,
            )

            skill_results = extract_skills_from_jd(jd_structured, SKILL_PATTERNS)

            for skill, counts in skill_results.items():
                if skill not in skill_counts:
                    skill_counts[skill] = {"required": 0, "preferred": 0}
                skill_counts[skill]["required"] += counts["required"]
                skill_counts[skill]["preferred"] += counts["preferred"]

        # Compute weighted frequencies
        skills_json = []
        for skill, counts in skill_counts.items():
            weighted_freq = calculate_weighted_frequency(
                counts["required"], counts["preferred"], total_jds
            )
            if weighted_freq > 0:
                skills_json.append({
                    "skill": skill,
                    "raw_weighted_freq": round(weighted_freq, 4),
                    "required_count": counts["required"],
                    "preferred_count": counts["preferred"],
                    "total_jds": total_jds,
                })

        # Sort by frequency descending
        skills_json.sort(key=lambda x: x["raw_weighted_freq"], reverse=True)

        # Upsert RoleSkillFrequency
        await self._upsert_skill_frequency(
            role.id if role else None,
            title_normalized,
            industry,
            seniority,
            company_type,
            skills_json,
            total_jds,
        )

    async def _get_or_create_normalized_role(
        self,
        title_normalized: str,
        industry: str,
        seniority: str,
    ) -> Optional[NormalizedRole]:
        """Get or create a NormalizedRole record."""
        result = await self.session.execute(
            select(NormalizedRole).where(
                and_(
                    NormalizedRole.title_normalized == title_normalized,
                    NormalizedRole.industry == industry,
                    NormalizedRole.seniority == seniority,
                )
            )
        )
        role = result.scalar_one_or_none()

        if not role:
            role = NormalizedRole(
                title_normalized=title_normalized,
                industry=industry,
                seniority=seniority,
                total_jds=0,
            )
            self.session.add(role)
            await self.session.flush()

        return role

    async def _upsert_skill_frequency(
        self,
        normalized_role_id: Optional[UUID],
        title_normalized: str,
        industry: str,
        seniority: str,
        company_type: str,
        skills_json: list[dict],
        total_jds: int,
    ):
        """Upsert a RoleSkillFrequency record."""
        result = await self.session.execute(
            select(RoleSkillFrequency).where(
                and_(
                    RoleSkillFrequency.title_normalized == title_normalized,
                    RoleSkillFrequency.industry == industry,
                    RoleSkillFrequency.seniority == seniority,
                    RoleSkillFrequency.company_type == company_type,
                )
            )
        )
        existing = result.scalar_one_or_none()

        if existing:
            existing.normalized_role_id = normalized_role_id
            existing.skills_json = skills_json
            existing.total_jds_analyzed = total_jds
            existing.last_updated = datetime.utcnow()
        else:
            freq = RoleSkillFrequency(
                normalized_role_id=normalized_role_id,
                title_normalized=title_normalized,
                industry=industry,
                seniority=seniority,
                company_type=company_type,
                skills_json=skills_json,
                total_jds_analyzed=total_jds,
                last_updated=datetime.utcnow(),
            )
            self.session.add(freq)


async def run_etl_for_tuple(
    title: str,
    industry: str,
    seniority: str,
) -> dict:
    """Convenience function to run ETL for a specific tuple.

    Called when new JDs are submitted for a specific role.
    """
    async with async_session_factory() as session:
        etl = SkillETL(session)
        return await etl.run_nightly_etl(title=title, industry=industry, seniority=seniority)


# ---------------------------------------------------------------------------
# Celery task registration
# ---------------------------------------------------------------------------
from celery import Task


class _SkillETLTask(Task):
    """Celery-bound wrapper for SkillETL.run_nightly_etl."""

    name = "keystone.services.skill_etl.run_nightly_etl"

    def run(self, title: Optional[str] = None, industry: Optional[str] = None, seniority: Optional[str] = None) -> dict:
        """Synchronous entry point required by Celery executor.

        Runs the ETL inside an async session and returns the stats dict.
        """
        # Import here to avoid circular imports at module load time
        from keystone.models.base import async_session_factory

        async def _inner() -> dict:
            async with async_session_factory() as session:
                etl = SkillETL(session)
                return await etl.run_nightly_etl(
                    title=title, industry=industry, seniority=seniority
                )

        # Celery tasks are sync by default; bridge to async via asyncio.run
        import asyncio
        return asyncio.run(_inner())


run_nightly_etl_task = _SkillETLTask()

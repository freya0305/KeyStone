"""Tests for Skill ETL pipeline.

Tests:
1. run_nightly_etl function
2. Skill frequency computation
3. Task registration (Celery task wrapper)
"""
import pytest
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

from keystone.services.skill_etl import (
    SkillETL,
    SKILL_PATTERNS,
    run_nightly_etl_task,
    _SkillETLTask,
)
from keystone.services.skill_normalizer import normalize_skill_list, normalize_title
from keystone.services.skill_frequency import (
    calculate_weighted_frequency,
    get_recency_weight,
    extract_skills_from_jd,
    JDStructured,
    get_section_weight,
    detect_section,
)


class TestSkillNormalization:
    """Tests for skill normalization."""

    def test_normalize_skill_list_deduplicates(self):
        """normalize_skill_list should deduplicate skills."""
        skills = ["Python", "python", "JavaScript", "JS"]
        result = normalize_skill_list(skills)
        # normalize_skill normalizes case but normalize_skill_list preserves first-seen case
        assert "Python" in result
        assert "JavaScript" in result
        # JS -> JavaScript via abbreviation expansion
        assert len(result) < len(skills)

    def test_normalize_skill_list_removes_invalid(self):
        """normalize_skill_list should filter out invalid/too-short skills."""
        skills = ["x", "", "React"]
        result = normalize_skill_list(skills)
        assert "x" not in result
        assert "" not in result
        assert "React" in result

    def test_normalize_skill_list_handles_empty_input(self):
        """normalize_skill_list should handle empty list."""
        result = normalize_skill_list([])
        assert result == []

    def test_normalize_title_software_engineer(self):
        """normalize_title should standardize software engineer variants."""
        assert normalize_title("Software Engineer") == "software engineer"
        assert normalize_title("software developer") == "software engineer"
        assert normalize_title("SWE") == "software engineer"

    def test_normalize_title_data_scientist(self):
        """normalize_title should standardize data scientist variants."""
        assert normalize_title("Data Scientist") == "data scientist"
        assert normalize_title("Data Analyst") == "data analyst"

    def test_normalize_title_ml_engineer(self):
        """normalize_title should standardize ML engineer variants."""
        assert normalize_title("Machine Learning Engineer") == "machine learning engineer"
        assert normalize_title("MLE") == "machine learning engineer"

    def test_normalize_title_empty(self):
        """normalize_title should return empty string for empty input."""
        assert normalize_title("") == ""
        assert normalize_title(None) == ""


class TestFrequencyWeighting:
    """Tests for skill frequency calculation."""

    def test_calculate_weighted_frequency_basic(self):
        """calculate_weighted_frequency should compute weighted average."""
        # (73 * 1.0 + 27 * 0.3) / 100 = 0.811
        freq = calculate_weighted_frequency(required_count=73, preferred_count=27, total_jds=100)
        assert freq == pytest.approx(0.811, rel=1e-3)

    def test_calculate_weighted_frequency_all_required(self):
        """All required should give 1.0."""
        freq = calculate_weighted_frequency(required_count=100, preferred_count=0, total_jds=100)
        assert freq == 1.0

    def test_calculate_weighted_frequency_all_preferred(self):
        """All preferred should give 0.3."""
        freq = calculate_weighted_frequency(required_count=0, preferred_count=100, total_jds=100)
        assert freq == pytest.approx(0.3, rel=1e-3)

    def test_calculate_weighted_frequency_zero_total(self):
        """Zero total JDs should return 0.0."""
        freq = calculate_weighted_frequency(required_count=0, preferred_count=0, total_jds=0)
        assert freq == 0.0

    def test_calculate_weighted_frequency_empty(self):
        """No skills should give 0.0."""
        freq = calculate_weighted_frequency(required_count=0, preferred_count=0, total_jds=50)
        assert freq == 0.0

    def test_get_recency_weight_fresh(self):
        """Recent postings (<90 days) should get weight 1.0."""
        recent = datetime.utcnow() - timedelta(days=30)
        assert get_recency_weight(recent) == 1.0

    def test_get_recency_weight_stale(self):
        """Postings 90-180 days old should get weight 0.7."""
        stale = datetime.utcnow() - timedelta(days=120)
        assert get_recency_weight(stale) == 0.7

    def test_get_recency_weight_old(self):
        """Postings 180-365 days old should get weight 0.5."""
        old = datetime.utcnow() - timedelta(days=270)
        assert get_recency_weight(old) == 0.5

    def test_get_recency_weight_excluded(self):
        """Postings >365 days old should get weight 0.0."""
        very_old = datetime.utcnow() - timedelta(days=400)
        assert get_recency_weight(very_old) == 0.0

    def test_get_recency_weight_none(self):
        """None posted_at should default to 1.0 (assume fresh)."""
        assert get_recency_weight(None) == 1.0

    def test_get_section_weight_requirements(self):
        """Requirements section should have weight 1.0."""
        assert get_section_weight("requirements") == 1.0
        assert get_section_weight("required") == 1.0

    def test_get_section_weight_nice_to_have(self):
        """Nice to have section should have weight 0.3."""
        assert get_section_weight("nice_to_have") == 0.3
        assert get_section_weight("preferred") == 0.3
        assert get_section_weight("plus") == 0.3

    def test_get_section_weight_responsibilities(self):
        """Responsibilities section should have weight 0.5."""
        assert get_section_weight("responsibilities") == 0.5
        assert get_section_weight("role") == 0.5

    def test_get_section_weight_benefits(self):
        """Benefits section should have weight 0.05."""
        assert get_section_weight("benefits") == 0.05
        assert get_section_weight("perks") == 0.05

    def test_get_section_weight_unknown(self):
        """Unknown sections should default to 0.3."""
        assert get_section_weight("unknown_section") == 0.3


class TestDetectSection:
    """Tests for section detection."""

    def test_detect_section_requirements(self):
        """Should detect requirements section."""
        assert detect_section("Requirements: Python, SQL") == "requirements"
        assert detect_section("Must have: React") == "requirements"
        assert detect_section("Skills required: Java") == "requirements"

    def test_detect_section_nice_to_have(self):
        """Should detect nice to have section."""
        assert detect_section("Nice to have: Docker") == "nice_to_have"
        assert detect_section("Preferred: Kubernetes") == "nice_to_have"
        assert detect_section("Plus: AWS experience") == "nice_to_have"

    def test_detect_section_benefits(self):
        """Should detect benefits section."""
        assert detect_section("Benefits: Health insurance") == "benefits"
        assert detect_section("Perks: gym membership") == "benefits"

    def test_detect_section_default(self):
        """Unknown context should default to overview."""
        assert detect_section("About the role:") == "overview"
        assert detect_section("Role overview") == "overview"


class TestExtractSkillsFromJD:
    """Tests for skill extraction from job descriptions."""

    def test_extract_skills_basic(self):
        """Should extract skills from JD text."""
        jd = JDStructured(
            title="Software Engineer",
            company="TechCorp",
            company_type="startup",
            industry="technology",
            seniority="mid",
            text="Requirements: Python, SQL\nNice to have: React",
        )
        results = extract_skills_from_jd(jd, SKILL_PATTERNS)

        assert "Python" in results
        assert "SQL" in results
        assert results["Python"]["required"] >= 1
        assert results["React"]["preferred"] >= 1

    def test_extract_skills_empty_jd(self):
        """Should handle empty JD text."""
        jd = JDStructured(
            title="Engineer",
            company="Corp",
            company_type="other",
            industry="technology",
            seniority="mid",
            text="",
        )
        results = extract_skills_from_jd(jd, SKILL_PATTERNS)
        # All skills should have zero counts
        for skill_data in results.values():
            assert skill_data["required"] == 0
            assert skill_data["preferred"] == 0

    def test_extract_skills_case_insensitive(self):
        """Should extract skills case-insensitively."""
        jd = JDStructured(
            title="Engineer",
            company="Corp",
            company_type="other",
            industry="technology",
            seniority="mid",
            text="requirements: python, JAVASCRIPT",
        )
        results = extract_skills_from_jd(jd, SKILL_PATTERNS)

        assert "Python" in results
        assert "JavaScript" in results

    def test_extract_skills_no_matches(self):
        """Should return zero counts when no skills match."""
        # Use text that cannot possibly match any skill pattern
        jd = JDStructured(
            title="Engineer",
            company="Corp",
            company_type="other",
            industry="technology",
            seniority="mid",
            text="This job involves managing people and communication",
        )
        results = extract_skills_from_jd(jd, SKILL_PATTERNS)

        # At least verify that "Communication" and "Management" skills have zero counts
        # These are not in SKILL_PATTERNS but exist in real taxonomy
        for skill_data in results.values():
            assert skill_data["total"] == 0


class TestSkillETLRunNightly:
    """Tests for SkillETL.run_nightly_etl method."""

    @pytest.fixture
    def mock_session(self):
        """Create a mock AsyncSession."""
        session = AsyncMock()
        session.execute = AsyncMock()
        session.commit = AsyncMock()
        session.rollback = AsyncMock()
        session.add = MagicMock()
        session.flush = AsyncMock()
        return session

    @pytest.fixture
    def mock_raw_jd(self):
        """Create a mock RawJD object."""
        jd = MagicMock()
        jd.id = uuid4()
        jd.job_title_raw = "Software Engineer"
        jd.company = "TechCorp"
        jd.company_type = "startup"
        jd.industry = "technology"
        jd.seniority = "mid"
        jd.raw_text = "Requirements: Python, SQL\nNice to have: React"
        jd.posted_at = datetime.utcnow() - timedelta(days=30)
        return jd

    @pytest.mark.asyncio
    async def test_run_nightly_etl_no_filters(self, mock_session, mock_raw_jd):
        """run_nightly_etl should process all eligible JDs when no filters."""
        # Setup: return one mock JD
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [mock_raw_jd]
        mock_session.execute.return_value = mock_result

        # Setup: NormalizedRole lookup returns None (create new)
        mock_role_result = MagicMock()
        mock_role_result.scalar_one_or_none.return_value = None
        mock_session.execute.return_value = mock_role_result

        # Setup: RoleSkillFrequency lookup returns None (create new)
        mock_freq_result = MagicMock()
        mock_freq_result.scalar_one_or_none.return_value = None

        # Configure execute to return different results in sequence
        call_count = [0]
        def execute_side_effect(*args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 1:
                return mock_result
            elif call_count[0] == 2:
                return mock_role_result
            else:
                return mock_freq_result
        mock_session.execute.side_effect = execute_side_effect

        etl = SkillETL(mock_session)
        stats = await etl.run_nightly_etl()

        assert stats["raw_jds_processed"] == 1
        assert stats["roles_updated"] >= 0
        assert stats["duration_seconds"] >= 0
        mock_session.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_run_nightly_etl_with_title_filter(self, mock_session, mock_raw_jd):
        """run_nightly_etl should filter by title when provided."""
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [mock_raw_jd]
        mock_session.execute.return_value = mock_result

        mock_role_result = MagicMock()
        mock_role_result.scalar_one_or_none.return_value = None
        mock_freq_result = MagicMock()
        mock_freq_result.scalar_one_or_none.return_value = None

        call_count = [0]
        def execute_side_effect(*args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 1:
                return mock_result
            elif call_count[0] == 2:
                return mock_role_result
            else:
                return mock_freq_result
        mock_session.execute.side_effect = execute_side_effect

        etl = SkillETL(mock_session)
        stats = await etl.run_nightly_etl(title="Software Engineer")

        assert stats["raw_jds_processed"] == 1

    @pytest.mark.asyncio
    async def test_run_nightly_etl_empty_result(self, mock_session):
        """run_nightly_etl should handle empty JD list."""
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_session.execute.return_value = mock_result

        etl = SkillETL(mock_session)
        stats = await etl.run_nightly_etl()

        assert stats["raw_jds_processed"] == 0
        assert stats["roles_updated"] == 0

    @pytest.mark.asyncio
    async def test_run_nightly_etl_rollback_on_error(self, mock_session):
        """run_nightly_etl should rollback on exception."""
        mock_session.execute.side_effect = Exception("Database error")

        etl = SkillETL(mock_session)
        with pytest.raises(Exception, match="Database error"):
            await etl.run_nightly_etl()

        mock_session.rollback.assert_called_once()


class TestSkillETLTask:
    """Tests for Celery task wrapper."""

    def test_skill_etl_task_name(self):
        """Task should have correct name."""
        assert run_nightly_etl_task.name == "keystone.services.skill_etl.run_nightly_etl"

    def test_skill_etl_task_is_task_instance(self):
        """run_nightly_etl_task should be a Celery Task instance."""
        assert isinstance(run_nightly_etl_task, _SkillETLTask)

    def test_skill_etl_task_has_run_method(self):
        """Task should have run method."""
        assert hasattr(run_nightly_etl_task, "run")
        assert callable(run_nightly_etl_task.run)

    def test_skill_etl_task_accepts_optional_params(self):
        """Task run method should accept optional title, industry, seniority params."""
        import inspect
        sig = inspect.signature(run_nightly_etl_task.run)
        params = list(sig.parameters.keys())
        assert "title" in params
        assert "industry" in params
        assert "seniority" in params


class TestSKILLPATTERNS:
    """Tests for SKILL_PATTERNS constant."""

    def test_skill_patterns_is_list(self):
        """SKILL_PATTERNS should be a list."""
        assert isinstance(SKILL_PATTERNS, list)

    def test_skill_patterns_not_empty(self):
        """SKILL_PATTERNS should not be empty."""
        assert len(SKILL_PATTERNS) > 0

    def test_skill_patterns_contains_programming_languages(self):
        """SKILL_PATTERNS should contain programming languages."""
        assert "Python" in SKILL_PATTERNS
        assert "Java" in SKILL_PATTERNS
        assert "JavaScript" in SKILL_PATTERNS
        assert "Go" in SKILL_PATTERNS

    def test_skill_patterns_contains_web_frameworks(self):
        """SKILL_PATTERNS should contain web frameworks."""
        assert "React" in SKILL_PATTERNS
        assert "Django" in SKILL_PATTERNS
        assert "FastAPI" in SKILL_PATTERNS
        assert "Node.js" in SKILL_PATTERNS

    def test_skill_patterns_contains_cloud_aws(self):
        """SKILL_PATTERNS should contain AWS."""
        assert "AWS" in SKILL_PATTERNS
        assert "Amazon Web Services" in SKILL_PATTERNS

    def test_skill_patterns_contains_ml_tools(self):
        """SKILL_PATTERNS should contain ML tools."""
        assert "Machine Learning" in SKILL_PATTERNS
        assert "TensorFlow" in SKILL_PATTERNS
        assert "PyTorch" in SKILL_PATTERNS
        assert "scikit-learn" in SKILL_PATTERNS

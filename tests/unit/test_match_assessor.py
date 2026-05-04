"""Tests for Match Assessor service - four-level match assessment."""
import pytest
from keystone.services.match_assessor import (
    RequirementMatch,
    MatchAssessment,
    MATCH_LEVELS,
    calculate_overall_score,
    assessment_to_dict,
)


class TestMATCHLEVELS:
    """Match level definitions tests."""

    def test_all_four_levels_defined(self):
        """All four match levels should be defined."""
        assert "strong" in MATCH_LEVELS
        assert "transferable" in MATCH_LEVELS
        assert "addressable" in MATCH_LEVELS
        assert "fundamental" in MATCH_LEVELS

    def test_strong_level_description(self):
        """Strong level should indicate clear skill match."""
        assert "clearly has" in MATCH_LEVELS["strong"]

    def test_transferable_level_description(self):
        """Transferable level should indicate adjacent experience."""
        assert "adjacent" in MATCH_LEVELS["transferable"]


class TestRequirementMatch:
    """RequirementMatch dataclass tests."""

    def test_has_required_fields(self):
        """RequirementMatch should have all required fields."""
        match = RequirementMatch(
            requirement="Python programming",
            match_level="strong",
            rationale="5 years Python experience",
        )
        assert match.requirement == "Python programming"
        assert match.match_level == "strong"
        assert match.rationale == "5 years Python experience"

    def test_optional_fields_default_none(self):
        """Optional fields should default to None."""
        match = RequirementMatch(
            requirement="SQL",
            match_level="transferable",
            rationale="Used MySQL in past",
        )
        assert match.company_type_reference is None
        assert match.jd_requirement_reference is None


class TestMatchAssessment:
    """MatchAssessment dataclass tests."""

    def test_has_required_fields(self):
        """MatchAssessment should have all required fields."""
        assessment = MatchAssessment(
            requirement_matches=[],
            overall_score=75.0,
            summary="Good fit",
            recommendations=["Get AWS certification"],
        )
        assert assessment.overall_score == 75.0
        assert assessment.summary == "Good fit"
        assert assessment.recommendations == ["Get AWS certification"]


class TestCalculateOverallScore:
    """Overall score calculation tests."""

    def test_all_strong_returns_100(self):
        """All strong matches should return 100."""
        matches = [
            RequirementMatch("req1", "strong", "rationale"),
            RequirementMatch("req2", "strong", "rationale"),
        ]
        assert calculate_overall_score(matches) == 100.0

    def test_all_fundamental_returns_0(self):
        """All fundamental matches should return 0."""
        matches = [
            RequirementMatch("req1", "fundamental", "rationale"),
            RequirementMatch("req2", "fundamental", "rationale"),
        ]
        assert calculate_overall_score(matches) == 0.0

    def test_mixed_matches(self):
        """Mixed matches should return weighted average."""
        matches = [
            RequirementMatch("req1", "strong", "rationale"),      # 100
            RequirementMatch("req2", "transferable", "rationale"), # 70
            RequirementMatch("req3", "addressable", "rationale"),  # 40
            RequirementMatch("req4", "fundamental", "rationale"),  # 0
        ]
        # (100 + 70 + 40 + 0) / 4 = 52.5
        assert calculate_overall_score(matches) == 52.5

    def test_empty_matches_returns_50(self):
        """Empty matches should return default 50."""
        assert calculate_overall_score([]) == 50.0

    def test_single_strong(self):
        """Single strong match should return 100."""
        matches = [RequirementMatch("req1", "strong", "rationale")]
        assert calculate_overall_score(matches) == 100.0

    def test_unknown_level_defaults_to_50(self):
        """Unknown match level should default to 50."""
        match = RequirementMatch("req", "unknown_level", "rationale")
        assert calculate_overall_score([match]) == 50.0


class TestAssessmentToDict:
    """assessment_to_dict conversion tests."""

    def test_converts_all_fields(self):
        """Should convert all assessment fields to dict."""
        matches = [
            RequirementMatch("Python", "strong", "5 years experience"),
        ]
        assessment = MatchAssessment(
            requirement_matches=matches,
            overall_score=100.0,
            summary="Excellent fit",
            recommendations=["Continue applying"],
        )
        result = assessment_to_dict(assessment)

        assert result["overall_score"] == 100.0
        assert result["summary"] == "Excellent fit"
        assert result["recommendations"] == ["Continue applying"]
        assert len(result["requirement_matches"]) == 1

    def test_requirement_matches_preserved(self):
        """Requirement matches should be preserved in conversion."""
        matches = [
            RequirementMatch("SQL", "transferable", "Used MySQL"),
            RequirementMatch("Python", "strong", "5 years"),
        ]
        assessment = MatchAssessment(
            requirement_matches=matches,
            overall_score=85.0,
            summary="Good",
            recommendations=[],
        )
        result = assessment_to_dict(assessment)

        assert len(result["requirement_matches"]) == 2
        assert result["requirement_matches"][0]["requirement"] == "SQL"
        assert result["requirement_matches"][0]["match_level"] == "transferable"

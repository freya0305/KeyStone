"""Tests for JD Parser service - job description parsing."""
import pytest
from keystone.services.jd_parser import (
    ParsedJobDescription,
    parsed_to_dict,
)


class TestParsedJobDescription:
    """ParsedJobDescription dataclass tests."""

    def test_has_required_fields(self):
        """ParsedJobDescription should have all required fields."""
        parsed = ParsedJobDescription(
            job_title="Software Engineer",
            company_name="DBS Bank",
            requirements=["Python", "SQL"],
            responsibilities=["Build software"],
            benefits=["Health insurance"],
            seniority_level="mid",
            industry="Banking",
            raw_skills=["Python", "Django"],
        )
        assert parsed.job_title == "Software Engineer"
        assert parsed.company_name == "DBS Bank"
        assert parsed.requirements == ["Python", "SQL"]
        assert parsed.responsibilities == ["Build software"]
        assert parsed.benefits == ["Health insurance"]
        assert parsed.seniority_level == "mid"
        assert parsed.industry == "Banking"
        assert parsed.raw_skills == ["Python", "Django"]

    def test_default_seniority_level(self):
        """Default seniority should be not_specified."""
        parsed = ParsedJobDescription(
            job_title="Engineer",
            company_name="Co",
            requirements=[],
            responsibilities=[],
            benefits=[],
            seniority_level="not_specified",
            industry="Tech",
            raw_skills=[],
        )
        assert parsed.seniority_level == "not_specified"


class TestParsedToDict:
    """parsed_to_dict conversion tests."""

    def test_converts_all_fields(self):
        """Should convert all fields to dict."""
        parsed = ParsedJobDescription(
            job_title="Data Engineer",
            company_name="OCBC",
            requirements=["Python", "Spark"],
            responsibilities=["Build pipelines"],
            benefits=["Bonus"],
            seniority_level="senior",
            industry="Finance",
            raw_skills=["Python", "AWS"],
        )
        result = parsed_to_dict(parsed)

        assert result["job_title"] == "Data Engineer"
        assert result["company_name"] == "OCBC"
        assert result["requirements"] == ["Python", "Spark"]
        assert result["responsibilities"] == ["Build pipelines"]
        assert result["benefits"] == ["Bonus"]
        assert result["seniority_level"] == "senior"
        assert result["industry"] == "Finance"
        assert result["raw_skills"] == ["Python", "AWS"]

    def test_parsed_to_dict_keys_complete(self):
        """Dict should have all expected keys."""
        parsed = ParsedJobDescription(
            job_title="T",
            company_name="C",
            requirements=[],
            responsibilities=[],
            benefits=[],
            seniority_level="junior",
            industry="I",
            raw_skills=[],
        )
        result = parsed_to_dict(parsed)
        expected_keys = {"job_title", "company_name", "requirements", "responsibilities",
                        "benefits", "seniority_level", "industry", "raw_skills"}
        assert set(result.keys()) == expected_keys

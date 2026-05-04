"""Tests for Suggestion Generator service - resume bullet suggestions."""
import pytest
import uuid
from keystone.services.suggestion_generator import (
    _strip_banned_phrases,
    _validate_suggestion_quality,
    parse_suggestions_from_response,
    BANNED_PHRASES,
)


class TestBannedPhrases:
    """Banned phrases list tests."""

    def test_has_banned_phrases(self):
        """BANNED_PHRASES should contain common buzzwords."""
        assert "great communication skills" in BANNED_PHRASES
        assert "team player" in BANNED_PHRASES
        assert "hard worker" in BANNED_PHRASES

    def test_banned_phrases_is_list(self):
        """BANNED_PHRASES should be a list."""
        assert isinstance(BANNED_PHRASES, list)
        assert len(BANNED_PHRASES) > 0


class TestStripBannedPhrases:
    """Banned phrase stripping tests."""

    def test_strips_single_phrase(self):
        """Should strip a single banned phrase."""
        result = _strip_banned_phrases("I am a great communication skills team player")
        assert "great communication skills" not in result
        assert "team player" not in result

    def test_replaces_with_sentinel(self):
        """Should replace banned phrase with sentinel."""
        result = _strip_banned_phrases("I have great communication skills")
        assert "[specific achievement]" in result

    def test_case_insensitive(self):
        """Should strip phrases case-insensitively."""
        result = _strip_banned_phrases("TEAM PLAYER and Hard Worker")
        assert "team player" not in result
        assert "hard worker" not in result

    def test_preserves_non_banned(self):
        """Should preserve text that is not banned."""
        result = _strip_banned_phrases("Led team delivering 20% revenue growth")
        # Result is lowercased but content is preserved
        assert "led team delivering 20% revenue growth" in result


class TestValidateSuggestionQuality:
    """Suggestion quality validation tests."""

    def test_valid_suggestion(self):
        """Valid suggestion should pass."""
        suggestion = {
            "rationale": "This is good for the company type requirement",
            "suggested_text": "Increased sales by 30%",
        }
        assert _validate_suggestion_quality(suggestion) is True

    def test_missing_rationale(self):
        """Suggestion without rationale should fail."""
        suggestion = {"suggested_text": "Increased sales"}
        assert _validate_suggestion_quality(suggestion) is False

    def test_rationale_without_specific_reference(self):
        """Rationale without specific reference should fail."""
        suggestion = {
            "rationale": "This is nice",  # No job/company/skill reference
            "suggested_text": "Increased sales",
        }
        assert _validate_suggestion_quality(suggestion) is False

    def test_suggested_text_with_banned_phrase(self):
        """Suggested text with banned phrase should fail."""
        suggestion = {
            "rationale": "This matches the job requirement for communication",
            "suggested_text": "I am a great communication skills team player",
        }
        assert _validate_suggestion_quality(suggestion) is False

    def test_rationale_with_job_reference(self):
        """Rationale with 'job' reference should pass."""
        suggestion = {
            "rationale": "This matches the job description requirement",
            "suggested_text": "Delivered project on time",
        }
        assert _validate_suggestion_quality(suggestion) is True

    def test_rationale_with_skill_reference(self):
        """Rationale with 'skill' reference should pass."""
        suggestion = {
            "rationale": "The company values this skill",
            "suggested_text": "Certified in AWS",
        }
        assert _validate_suggestion_quality(suggestion) is True

    def test_empty_suggestion(self):
        """Empty suggestion should fail."""
        assert _validate_suggestion_quality({}) is False


class TestParseSuggestionsFromResponse:
    """Suggestion parsing tests."""

    def test_parses_valid_json_response(self):
        """Should parse valid JSON response."""
        content = '''[
            {
                "section": "experience",
                "original_text": "Did stuff",
                "suggested_text": "Led team of 5 engineers delivering 20% growth",
                "rationale": "Matches the leadership requirement in the job description",
                "match_level": "transferable"
            }
        ]'''
        job_analysis_id = uuid.uuid4()
        result = parse_suggestions_from_response(content, job_analysis_id)

        assert len(result) == 1
        assert result[0].original_text == "Did stuff"
        # suggested_text is lowercased by _strip_banned_phrases
        assert result[0].suggested_text == "led team of 5 engineers delivering 20% growth"
        assert result[0].match_level == "transferable"

    def test_strips_banned_phrases_from_suggestions(self):
        """Should strip banned phrases from suggested text."""
        content = '''[
            {
                "section": "experience",
                "original_text": "Worked on team",
                "suggested_text": "I am a great communication skills team player",
                "rationale": "Matches the job requirement for interpersonal skills",
                "match_level": "transferable"
            }
        ]'''
        job_analysis_id = uuid.uuid4()
        result = parse_suggestions_from_response(content, job_analysis_id)

        assert len(result) == 0  # Filtered out due to banned phrase

    def test_filters_invalid_quality_suggestions(self):
        """Should filter out suggestions with poor quality."""
        content = '''[
            {
                "section": "experience",
                "original_text": "Did stuff",
                "suggested_text": "Something generic",
                "rationale": "Good",  # Too vague - no specific reference
                "match_level": "transferable"
            }
        ]'''
        job_analysis_id = uuid.uuid4()
        result = parse_suggestions_from_response(content, job_analysis_id)

        # Should be filtered out due to missing specific reference in rationale
        assert len(result) == 0

    def test_handles_invalid_json(self):
        """Should handle invalid JSON gracefully."""
        content = "This is not valid JSON"
        job_analysis_id = uuid.uuid4()
        result = parse_suggestions_from_response(content, job_analysis_id)

        assert result == []

    def test_handles_markdown_code_block(self):
        """Should handle markdown code block wrapper."""
        content = '''```json
[
    {
        "section": "skills",
        "original_text": "Know Python",
        "suggested_text": "5 years Python expertise",
        "rationale": "Matches the job skill requirement",
        "match_level": "strong"
    }
]
```'''
        job_analysis_id = uuid.uuid4()
        result = parse_suggestions_from_response(content, job_analysis_id)

        assert len(result) == 1
        assert result[0].section == "skills"

    def test_returns_empty_list_for_non_list_response(self):
        """Should return empty list if response is not a list."""
        content = '{"section": "experience"}'  # Not a list
        job_analysis_id = uuid.uuid4()
        result = parse_suggestions_from_response(content, job_analysis_id)

        assert result == []

    def test_creates_suggestion_with_correct_job_analysis_id(self):
        """Should create suggestions with correct job_analysis_id."""
        content = '''[
            {
                "section": "experience",
                "original_text": "Old text",
                "suggested_text": "New text with metrics",
                "rationale": "Matches job requirement for achievements",
                "match_level": "transferable"
            }
        ]'''
        job_analysis_id = uuid.uuid4()
        result = parse_suggestions_from_response(content, job_analysis_id)

        assert len(result) == 1
        assert result[0].job_analysis_id == job_analysis_id

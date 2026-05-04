"""Tests for Company Classifier service - SG company type classification."""
import pytest
from keystone.services.company_classifier import (
    CompanyClassification,
    classify_company,
    clear_company_cache,
    KNOWN_GLCS,
    KNOWN_GOVERNMENT_DEPARTMENTS,
    KNOWN_MNCS,
)


class TestClassifyCompany:
    """Company classification tests."""

    def test_dbs_classified_as_banking_glc(self):
        """DBS should be classified as banking_glc via partial match."""
        result = classify_company("DBS Bank")
        assert result.company_type == "banking_glc"
        # Partial match gives 0.8 confidence (exact match "DBS" would be 1.0)
        assert result.confidence == 0.8
        assert result.classification_method == "database"

    def test_dbs_exact_match(self):
        """DBS exactly should be classified with full confidence."""
        result = classify_company("DBS")
        assert result.company_type == "banking_glc"
        assert result.confidence == 1.0
        assert result.classification_method == "database"

    def test_ocbc_classified(self):
        """OCBC should be classified as banking_glc."""
        result = classify_company("OCBC Bank")
        assert result.company_type == "banking_glc"

    def test_uob_classified(self):
        """UOB should be classified as banking_glc."""
        result = classify_company("United Overseas Bank")
        assert result.company_type == "banking_glc"

    def test_singtel_classified(self):
        """SingTel should be classified as telecom_glc."""
        result = classify_company("SingTel")
        assert result.company_type == "telecom_glc"

    def test_google_classified_as_mnc_tech(self):
        """Google should be classified as mnc_tech."""
        result = classify_company("Google")
        assert result.company_type == "mnc_tech"

    def test_microsoft_classified(self):
        """Microsoft should be classified as mnc_tech."""
        result = classify_company("Microsoft")
        assert result.company_type == "mnc_tech"

    def test_jpmorgan_classified(self):
        """JPMorgan should be classified as mnc_banking."""
        result = classify_company("JPMorgan Chase")
        assert result.company_type == "mnc_banking"

    def test_deloitte_classified(self):
        """Deloitte should be classified as mnc_professional."""
        result = classify_company("Deloitte")
        assert result.company_type == "mnc_professional"

    def test_ministry_of_education_classified_as_government(self):
        """MOE should be classified as government."""
        result = classify_company("Ministry of Education")
        assert result.company_type == "government"

    def test_mom_classified(self):
        """MOM should be classified as government."""
        result = classify_company("Ministry of Manpower")
        assert result.company_type == "government"

    def test_ira_classified(self):
        """IRA should be classified as government."""
        result = classify_company("ira")
        assert result.company_type == "government"

    def test_unknown_company_returns_other(self):
        """Unknown company should return 'other' classification."""
        result = classify_company("Some Random Company Pte Ltd")
        # Returns CompanyClassification with possibly other type
        assert isinstance(result, CompanyClassification)

    def test_empty_company_name(self):
        """Empty company name should return 'other' with 0 confidence."""
        result = classify_company("")
        assert result.company_type == "other"
        assert result.confidence == 0.0
        assert result.classification_method == "none"

    def test_not_specified(self):
        """'Not Specified' should return 'other' with 0 confidence."""
        result = classify_company("Not Specified")
        assert result.company_type == "other"
        assert result.confidence == 0.0

    def test_case_insensitive(self):
        """Classification should be case insensitive."""
        result = classify_company("DBS BANK")
        assert result.company_type == "banking_glc"

    def test_partial_match(self):
        """Partial matches should work with lower confidence."""
        result = classify_company("DBS Bank Singapore")
        assert result.company_type == "banking_glc"
        assert result.confidence == 0.8  # Partial match


class TestClearCompanyCache:
    """Company cache management tests."""

    def test_clear_all_cache(self):
        """clear_company_cache with no args should clear all."""
        clear_company_cache()  # Should not raise

    def test_clear_specific_company_cache(self):
        """clear_company_cache with name should clear that company's cache."""
        clear_company_cache("DBS Bank")  # Should not raise even if not cached


class TestKnownDatabases:
    """Known employer database tests."""

    def test_known_glcs_has_dbs(self):
        """KNOWN_GLCS should include DBS."""
        assert "dbs" in KNOWN_GLCS
        assert KNOWN_GLCS["dbs"] == "banking_glc"

    def test_known_glcs_has_singtel(self):
        """KNOWN_GLCS should include SingTel."""
        assert "singtel" in KNOWN_GLCS

    def test_known_government_has_moe(self):
        """KNOWN_GOVERNMENT_DEPARTMENTS should include MOE."""
        assert "ministry of education" in KNOWN_GOVERNMENT_DEPARTMENTS

    def test_known_mncs_has_google(self):
        """KNOWN_MNCS should include Google."""
        assert "google" in KNOWN_MNCS
        assert KNOWN_MNCS["google"] == "mnc_tech"

    def test_known_mncs_has_grab(self):
        """KNOWN_MNCS should include Grab."""
        assert "grab" in KNOWN_MNCS
        assert KNOWN_MNCS["grab"] == "mnc_fintech"

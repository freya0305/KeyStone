"""Tests for resume parsing service - file validation and SG flags."""
import pytest
from keystone.services.resume_parsing import (
    validate_file_magic_bytes,
    extract_sg_flags,
    FileValidationError,
    SGFlags,
)


class TestValidateFileMagicBytes:
    """File magic byte validation tests."""

    def test_valid_pdf_magic_bytes(self):
        """PDF files starting with %PDF should be detected."""
        content = b"%PDF-1.4\nfake pdf content"
        result = validate_file_magic_bytes(content, "resume.pdf")
        assert result == "pdf"

    def test_valid_docx_magic_bytes(self):
        """DOCX files (ZIP with word/document.xml) should be detected."""
        content = b"PK\x03\x04word/document.xml" + b"\x00" * 100
        result = validate_file_magic_bytes(content, "resume.docx")
        assert result == "docx"

    def test_invalid_file_rejected(self):
        """Non-PDF/DOCX files should raise FileValidationError."""
        content = b"This is not a valid file"
        with pytest.raises(FileValidationError) as exc_info:
            validate_file_magic_bytes(content, "resume.txt")
        assert "Unable to validate file type" in str(exc_info.value)

    def test_pdf_fallback_by_extension(self):
        """If magic bytes fail, extension fallback should work for .pdf."""
        content = b"Random bytes not matching PDF"
        result = validate_file_magic_bytes(content, "resume.pdf")
        assert result == "pdf"

    def test_docx_fallback_by_extension(self):
        """If magic bytes fail, extension fallback should work for .docx."""
        content = b"Random bytes not matching DOCX"
        result = validate_file_magic_bytes(content, "resume.docx")
        assert result == "docx"

    def test_doc_fallback_by_extension(self):
        """Extension .doc should also map to docx."""
        content = b"Random bytes"
        result = validate_file_magic_bytes(content, "resume.doc")
        assert result == "docx"

    def test_zip_but_not_docx_rejected(self):
        """ZIP files without word/document.xml should be rejected."""
        content = b"PK\x03\x04other/file.xml" + b"\x00" * 100
        with pytest.raises(FileValidationError) as exc_info:
            validate_file_magic_bytes(content, "archive.zip")
        assert "not a valid DOCX" in str(exc_info.value)


class TestExtractSGFlags:
    """Singapore-specific intelligence flags tests."""

    def test_nric_detected_flags_true(self):
        """NRIC in text should set has_nric=True."""
        text = "My NRIC is S1234567A and I worked at DBS."
        flags = extract_sg_flags(text)
        assert flags.has_nric is True

    def test_nric_not_detected(self):
        """Normal text without NRIC should set has_nric=False."""
        text = "I am a software engineer with 5 years experience at a tech company."
        flags = extract_sg_flags(text)
        assert flags.has_nric is False

    def test_photo_keywords_detected(self):
        """Photo-related keywords should set has_photo=True."""
        text = "Please see attached resume with photo included."
        flags = extract_sg_flags(text)
        assert flags.has_photo is True

    def test_no_photo_keyword(self):
        """Text without photo keywords should set has_photo=False."""
        text = "Experienced software engineer seeking new opportunities."
        flags = extract_sg_flags(text)
        assert flags.has_photo is False

    def test_ns_completed_status(self):
        """NS completed keywords should set ns_status='completed'."""
        text = "NS completed in 2019. Worked at Singtel from 2020."
        flags = extract_sg_flags(text)
        assert flags.ns_status == "completed"

    def test_ns_ongoing_status(self):
        """NS ongoing keywords should set ns_status='ongoing'."""
        text = "Currently serving NS, will be available from Jan 2025."
        flags = extract_sg_flags(text)
        assert flags.ns_status == "ongoing"

    def test_ns_not_mentioned(self):
        """Text without NS keywords should set ns_status='not_applicable'."""
        text = "I am a fresh graduate from NUS."
        flags = extract_sg_flags(text)
        assert flags.ns_status == "not_applicable"

    def test_nus_education_tier(self):
        """NUS should be detected as local_university."""
        text = "Bachelor of Computing, National University of Singapore, 2023."
        flags = extract_sg_flags(text)
        assert flags.education_tier == "local_university"

    def test_ntu_education_tier(self):
        """NTU should be detected as local_university."""
        text = "BE in Electrical Engineering, Nanyang Technological University."
        flags = extract_sg_flags(text)
        assert flags.education_tier == "local_university"

    def test_smu_education_tier(self):
        """SMU should be detected as local_university."""
        text = "BBA, Singapore Management University, 2022."
        flags = extract_sg_flags(text)
        assert flags.education_tier == "local_university"

    def test_polytechnic_education_tier(self):
        """Polytechnic should be detected."""
        text = "Diploma in Information Technology, Ngee Ann Polytechnic."
        flags = extract_sg_flags(text)
        assert flags.education_tier == "polytechnic"

    def test_ite_education_tier(self):
        """ITE should be detected."""
        text = "NITEC in Electronics, Institute of Technical Education."
        flags = extract_sg_flags(text)
        assert flags.education_tier == "ite"

    def test_pmet_signals_management(self):
        """Management experience should trigger PMET signals."""
        text = "Led a team of 10 engineers. Managed budgets exceeding $1M."
        flags = extract_sg_flags(text)
        assert "management_experience" in flags.pmet_signals
        assert flags.is_pmet is True

    def test_pmet_signals_professional_title(self):
        """Professional titles should trigger PMET signals."""
        text = "Senior Software Engineer with 8 years experience."
        flags = extract_sg_flags(text)
        assert "professional_title" in flags.pmet_signals

    def test_pmet_multiple_signals(self):
        """Multiple PMET signals should set is_pmet=True."""
        text = "Director of Engineering. Overseeing team of 50. Salary expectations: $15K/month."
        flags = extract_sg_flags(text)
        assert len(flags.pmet_signals) >= 2
        assert flags.is_pmet is True

    def test_non_pmet_text(self):
        """Text without PMET signals should set is_pmet=False."""
        text = "I am a fresh graduate looking for my first job."
        flags = extract_sg_flags(text)
        assert flags.is_pmet is False


class TestSGFlagsDataclass:
    """SGFlags dataclass structure tests."""

    def test_sgflags_has_all_fields(self):
        """SGFlags should have all required fields."""
        text = "Test resume text"
        flags = extract_sg_flags(text)

        assert hasattr(flags, 'has_nric')
        assert hasattr(flags, 'has_photo')
        assert hasattr(flags, 'ns_quality')
        assert hasattr(flags, 'education_tier')
        assert hasattr(flags, 'pmet_signals')
        assert hasattr(flags, 'is_pmet')

    def test_sgflags_is_dataclass(self):
        """SGFlags should be a dataclass."""
        assert hasattr(SGFlags, '__dataclass_fields__')

    def test_pmet_signals_is_list(self):
        """pmet_signals should be a list."""
        text = "Test"
        flags = extract_sg_flags(text)
        assert isinstance(flags.pmet_signals, list)

# DECISION: M1 + M2 + M3 Implementation

**Date**: 2026-05-04
**Phase**: /implement

## M1 - Auth + PDPA ✅

### Completed
- M1.3 SMS OTP - already existed in `auth_phone.py`
- M1.4 NRIC Pipeline - `assert_no_nric()`, `mask_nric()` added to `nric_detector.py`
- M1.5 Consent checks - added before all Claude API calls in 4 endpoints
- M1.6 Privacy/Terms - pages already existed

### Files Modified
- `nric_detector.py` - Added `assert_no_nric()`, `mask_nric()`, `NRICDetectedError`
- `job_seeker.py` - Consent + NRIC checks in all Claude paths

---

## M2 - Resume Processing ✅

### Completed
- M2.1 Upload with magic-byte validation, S3, NRIC masking, cache by hash
- M2.2 Resume parsing with Claude Haiku
- M2.3 SG flags (NS, PMET, education tier)
- M2.4 SSE progress streaming

### Files Created
- `services/s3.py` - S3 upload service
- `services/resume_parsing.py` - Text extraction + SG flags

### Files Modified
- `job_seeker.py` - Added M2 endpoints

---

## M3 - Job Analysis Engine ✅

### Completed
- M3.1 JD URL fetcher with robots.txt, BeautifulSoup extraction, 7-day cache
- M3.2 JD parser with Claude Haiku
- M3.3 Company classifier with SG employer database + Haiku fallback
- M3.4 Four-level match assessor with Claude Sonnet
- M3.5 Job analysis endpoint with SSE streaming
- M3.6 Rate limiting (20/hour for job analysis)

### Files Created
- `services/jd_fetcher.py` - URL fetch + extraction
- `services/jd_parser.py` - JD parsing
- `services/company_classifier.py` - Company type detection
- `services/match_assessor.py` - Four-level match assessment

### Dependencies Added
- `beautifulsoup4>=4.12.0`

---

## Remaining Active Todos
- 00-ky0-summary.md
- 01-ky1-platform-foundation.md
- M0-foundation.md
- M6-payments-auth.md
- M7-frontend-design-system.md

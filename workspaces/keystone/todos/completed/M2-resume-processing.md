# M2 — Resume Processing Engine

> Depends on: M0.1, M0.2, M1.1 (NRIC pipeline), M1.5 (consent middleware)
> The resume pipeline is the entry point to ALL AI value. NRIC masking must be 100% in place before any resume reaches Claude.
> Implements: specs/product.md §Feature 1, specs/compliance.md §NRIC Handling

---

## M2.1 — Resume file upload endpoint

**What**: `POST /api/resumes/upload` — accepts PDF, DOCX, or plain text, validates, stores to S3.

**Deliverables**:
- Multipart upload endpoint (max 5MB per specs/mvp-scope.md)
- Magic-byte validation (NOT extension-only — PDF magic bytes `%PDF`, DOCX is ZIP with `word/document.xml`)
- File content extracted to plaintext:
  - PDF: pdfplumber (handles most professional resume PDFs); fallback to pypdf
  - DOCX: python-docx (preserves section structure)
  - Plain text: direct
- Malformed file returns friendly error (logged for debugging, not exposed to user): `"We couldn't read this file. Try exporting from Word as PDF, or paste the text directly."`
- Content hash (SHA-256) computed on extracted text
- **Check cache**: if content_hash exists in `resumes` table → return existing resume_id immediately (no re-processing)
- NRIC Stage 1: call `mask_nric()` on extracted text BEFORE writing to S3
- Write masked text to S3 (bucket: `keystone-resumes-{env}`, key: `{user_id}/{resume_id}`)
- Write `resumes` record with s3_key, content_hash, sg_flags.nric_detected

**Anonymous user support**: allow upload without auth (guest mode). Store with `user_id = null` + `anon_session_id` (signed JWT cookie valid 24h). When user signs up/in, backfill `user_id` on all anon records from that session.

**Acceptance criteria**:
- PDF with NRIC: NRIC masked before S3 write, `sg_flags.nric_detected = true`
- Same resume uploaded twice: second request returns cached `resume_id`, no S3 write
- Malformed PDF: returns 422 with user-friendly message (not 500)
- File >5MB: returns 413 with message: "This file is over 5MB. Try exporting from Word as PDF, or paste the text directly."

**Implements**: specs/product.md §Feature 1, specs/compliance.md §NRIC Stage 1

---

## M2.2 — Resume parsing service (Claude Haiku)

**What**: Extract structured resume data from plaintext. Runs after Stage 1 NRIC masking.

**Input**: masked resume text (from S3)
**Output** (stored as `parsed_json` on resume record):
```json
{
  "contact": { "name": "...", "email": "...", "phone": "...", "linkedin": "..." },
  "summary": "...",
  "experience": [{ "company": "...", "role": "...", "period": "...", "bullets": ["..."] }],
  "education": [{ "institution": "...", "degree": "...", "year": "...", "gpa": "..." }],
  "skills": ["..."],
  "certifications": ["..."],
  "ns": { "present": true, "unit": "...", "vocation": "...", "description": "..." }
}
```

**Model**: Claude Haiku (extraction task, low reasoning complexity)
**NRIC Stage 2**: `assert_no_nric(text)` called on masked text before sending to Claude
**Prompt caching**: system prompt is a static extraction schema — cache it
**Fallback**: if Haiku parsing fails (malformed resume), return `{ "parse_error": true, "raw_text": "..." }` — do NOT fail the whole flow

**Acceptance criteria**:
- Structured JSON output for 95% of SG professional resume formats
- Zero NRIC values in `parsed_json` output
- Haiku call logged with token counts
- Content hash + cached result: same resume returns cached JSON (no Haiku call)

**Implements**: specs/technical.md §AI Architecture (two-tier routing), specs/compliance.md §NRIC Stage 2

---

## M2.3 — SG-specific intelligence flags (Claude Haiku + rule engine)

**What**: Detect and assess SG-specific resume elements. Combined rule-based detection + Haiku assessment.

**Rule-based detections** (no LLM needed):
- NRIC: already done in Stage 1 — copy flag from resume record
- Professional photo: detect common photo-presence signals in PDF metadata or text cues (word "photo", JPG/PNG embedded object)
- NS section: presence of NS-related keywords (national service, SAF, RSAF, RSN, SPF, SCDF, platoon, NSF, NSman)
- Education institutions: check against SG university list for hierarchy context

**Haiku assessment for**:
- NS description quality: is current NS description vague ("did NS") or has civilian-equivalent framing? → output: `{quality: "poor|fair|good", suggested_reframe: "..."}`
- PMET signals detection: career gap, seniority indicators, industry tenure signals → categorize as `{persona: "fresh_grad|mid_career|pmet"}`
- Career pivot narrative: if PMET persona, is current resume language career-destination specific or origin-industry specific?

**Output** (stored as `sg_flags` on resume record):
```json
{
  "nric_detected": false,
  "photo_present": false,
  "ns_present": true,
  "ns_quality": "fair",
  "ns_suggested_reframe": "...",
  "persona": "pmet",
  "pmet_age_signals": ["graduation year visible", "early-career descriptions"],
  "career_pivot_needed": true,
  "education_tier": "NUS/NTU/SMU"
}
```

**Acceptance criteria**:
- NS detection tested against 20 SG resume samples (male graduates)
- PMET persona detection: accuracy tested against labeled test set of 50 resumes
- Photo detection: tested for common PDF formats
- All flags visible in resume detail API response

**Implements**: specs/product.md §Feature 1 (SG intelligence rules, PMET intelligence)

---

## M2.4 — Resume analysis endpoint (wire M2.1 + M2.2 + M2.3)

**What**: `GET /api/resumes/{resume_id}/analysis` — returns full resume analysis combining parsed JSON + SG flags + streaming status.

**Important**: analysis is async (upload → async job → result). Endpoint design:
- `POST /api/resumes/upload` → returns `{resume_id, status: "processing"}` immediately
- `GET /api/resumes/{resume_id}` → returns status: `processing|ready|failed` + result when ready
- Frontend polls every 2s OR uses SSE (Server-Sent Events) for progress updates

**Streaming progress events** (SSE endpoint `GET /api/resumes/{resume_id}/progress`):
```
data: {"step": "parsing", "message": "Reading your resume..."}
data: {"step": "nric_check", "message": "Scanning for sensitive data..."}
data: {"step": "sg_flags", "message": "Checking SG-specific elements..."}
data: {"step": "ready", "resume_id": "..."}
```

**Acceptance criteria**:
- Full analysis completes in ≤10 seconds (p95) — matching specs/mvp-scope.md done criteria
- SSE sends progress events at each stage
- Frontend shows: "✓ Parsed your resume" then "⟳ Checking SG-specific elements..."
- Resume result cached — re-requesting same resume_id returns instantly

**Wire todo**: this endpoint wires M2.1 (upload) → M2.2 (parser) → M2.3 (SG flags) → result

**Implements**: specs/product.md §Feature 1, specs/mvp-scope.md §Technical done criteria

---

## M2.5 — Resume export (PDF + DOCX with accepted suggestions)

**What**: Generate downloadable modified resume incorporating accepted suggestions.

**Input**: `resume_id` + `job_analysis_id` (identifies which suggestions to apply) → list of accepted suggestion_ids + modified texts
**Output**: PDF and/or DOCX with accepted suggestion texts replacing original bullets

**Approach**:
- Parse original resume structure from `parsed_json`
- For each accepted suggestion: replace original bullet text with `suggestion.suggested_text` (or `modified_text` if user edited)
- Regenerate document using:
  - PDF: WeasyPrint or ReportLab (from template) — NOT relying on LLM for formatting
  - DOCX: python-docx with template
- File name: `{employer}-{role}-resume.pdf` (derived from JD)
- Store to S3 temporarily (24h TTL), return signed URL

**Download triggers application creation** (per product spec):
- After download is initiated (non-blocking), show modal: "Submitting this to [Company]? [Yes — track this application] [Just downloading]"
- If "Yes": create application record with `suggestion_set_id` linkage (CRITICAL for outcome→suggestion causality)

**Acceptance criteria**:
- Exported PDF looks professional (not plaintext dump)
- Accepted suggestion text appears in output (integration test: accept suggestion → export → extract text from PDF → assert suggestion text present)
- DOCX export works and opens in Word without errors
- Download + "Yes" creates application record linked to `job_analysis_id`

**Implements**: specs/product.md §Feature 3 (output: modified resume as PDF/DOCX), specs/mvp-scope.md §Feature 3


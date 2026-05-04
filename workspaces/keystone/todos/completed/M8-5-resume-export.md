# M8.5 — Frontend: Resume Export (PDF/DOCX Download)

> Completed: 2026-05-04

## Implementation Summary

### Backend (`src/keystone/api/job_seeker.py`)
- Added `POST /job-seeker/export` endpoint
- Accepts `{ job_analysis_id: string, format: "pdf" | "docx" }`
- Returns binary file download with appropriate Content-Disposition header

### Export Service (`src/keystone/services/document_export.py`)
- `generate_pdf()` — creates formatted PDF using reportlab
  - Title, company, skills section
  - Suggestions with color-coded match levels (strong/transferable/addressable/fundamental)
  - Original and suggested text for each suggestion
- `generate_docx()` — creates formatted DOCX using python-docx
  - Same structure as PDF with proper formatting

### Dependencies
- Added `reportlab>=4.0.0` to `pyproject.toml` (was already had `python-docx>=1.1.0`)

### Frontend (`apps/web/src/app/(guest)/analyse/page.tsx`)
- Added `apiDownload()` function in `lib/api.ts` for binary file downloads
- Added `handleExport(format)` function
- Added download buttons (DOCX and PDF) on the results screen

---

## Verification

- Backend endpoint: `POST /job-seeker/export` with `job_analysis_id` and `format`
- PDF generation: reportlab renders colored match levels and suggestion text
- DOCX generation: python-docx with proper formatting and colors
- Frontend: Download buttons call export API and trigger browser download

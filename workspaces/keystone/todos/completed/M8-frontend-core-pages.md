# M8 — Frontend Core Pages — COMPLETED ✅

> All subtasks completed: M8.1, M8.2, M8.3, M8.4, M8.5, M8.6, M8.7
> Date: 2026-05-04

## Completion Summary

### M8.1 — Landing page (build) ✅
- `apps/web/src/app/page.tsx` (246+ lines)
- Full hero section with headline + CTA
- Features section (Resume Tailoring, Four-Level Match, Outcome Tracking)
- Singapore-specific section (NS & GLC Context, PDPA Compliant)
- Pricing preview (Free / Pro)
- Footer with Privacy / Terms / Trust links

### M8.2 — Landing page wire ✅
- `"use client"` directive added
- `useAuth` from `@clerk/nextjs` integrated
- Logged-in users see "Continue to dashboard →" CTA
- Non-logged-in users see "Try for free"
- Nav conditionally shows Dashboard/Sign out or Try free/Sign in/Get started

### M8.3 — Onboarding/activation flow (build) ✅
- JD-first input at `/analyse` (URL mode + text mode toggle)
- DropZone for resume upload (PDF, DOCX)
- Progressive loading states with cycling messages (4 progressive messages)
- Results page with match summary (Strong/Transferable/Addressable/Fundamental)
- Fundamental gaps section collapsed by default (`<details>` element)
- Registration prompt via `trackSignupTriggered` AFTER first accept (not before)

### M8.4 — Onboarding flow wire ✅
- `POST /job-seeker/job/parse` → parses JD (URL or text)
- `POST /job-seeker/job/{job_id}/analyze` → match assessment
- `POST /job-seeker/suggestions` → gets suggestions
- `POST /job-seeker/suggestions/{id}/feedback` → accept/reject signals
- Real API calls throughout — no mock data

### M8.5 — Suggestion export flow (build + wire) ✅
- `POST /job-seeker/export` endpoint (job_seeker.py:1312)
- `document_export.py` service: `generate_pdf()` (reportlab) + `generate_docx()` (python-docx)
- `apiDownload()` in `lib/api.ts` for binary responses
- Download DOCX + PDF buttons on results page
- `reportlab>=4.0.0` added to pyproject.toml

### M8.6 — My Resumes page (build + wire) ✅
- `apps/web/src/app/(app)/app/resumes/page.tsx`
- Lists user resumes with filename, upload date
- DropZone for new uploads
- API: `GET /job-seeker/resumes` + `GET /job-seeker/resumes/{id}/analyses`

### M8.7 — PostHog analytics instrumentation ✅
- `src/lib/analytics.ts` — PostHog client initialization
- `src/components/PostHogProvider.tsx` — user identification on auth change
- All key events wired:
  - `resume_uploaded` — DropZone onUploadSuccess
  - `jd_analysed` — analyse page after parse
  - `suggestion_accepted/rejected` — analyse page handleAccept/handleReject
  - `resume_downloaded` — handleExport
  - `signup_triggered` — first_accept/third_view/download
  - `application_created` — new/page.tsx
  - `signed_up` — onboarding/page.tsx
  - `pro_subscribed` — pricing/page.tsx
  - `paywall_seen` — ProGate component
  - `batch_update` — BatchUpdateModal
- Environment vars: `NEXT_PUBLIC_POSTHOG_KEY`, `NEXT_PUBLIC_POSTHOG_HOST`

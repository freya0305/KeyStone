# M9 — Frontend: Application Tracking + Dashboard + Settings

> Completed subtasks: M9.2, M9.3, M9.4, M9.5, M9.6, M9.7, M9.8
> Date: 2026-05-04

## Completion Summary

### M9.8 — Onboarding questionnaire ✅
- Created `/app/onboarding` page
- Two-step onboarding flow:
  - Step 1: "What brings you to KeyStone?" (persona selection)
  - Step 2: "How many jobs applied?" (count selection)
- Saves to `/onboarding` endpoint
- Stores `onboardingCompleted` in localStorage
- Redirects to dashboard after completion
- Back button on step 2 to return to step 1

### M9.7 — Settings page ✅
- Dark mode toggle (persisted in localStorage)
- Data export: "Export all my data" button (downloads JSON)
- Delete account: confirmation flow with two-step confirmation
- PDPA footer text added
- Consent management section with toggle switches
- Billing/subscription management with Stripe Portal link

### M9.5 — Stage progression celebration ✅
- `POST /job-seeker/applications/{id}/stages` endpoint added to backend
- StageCelebrationModal component created with:
  - Advancement form (response/screening/interview/final options)
  - Offer celebration with reflection form (checkboxes + free text)
  - Confetti animation (12 pieces, brand colors, 1.2s for advancement, 2.4s for offer)
  - Stage type, format, and date recording
- Celebration screen shows after stage advancement

### M9.3 — Batch update modal (build) ✅
- Keyboard shortcuts: Space/Enter = no news, R = response, X = rejected, Esc = close
- Card animation (200ms slide-out) when advancing
- Undo toast for "Mark all remaining as no news" with 8-second window
- Progress dots showing completion status
- Keyboard hint displayed below header
- Refs used for mutable values to avoid stale closure issues

### M9.2 — Applications dashboard wire ✅
- Dashboard page (`app/page.tsx`) now fetches real data from:
  - `GET /job-seeker/applications` → recent applications list
  - `GET /job-seeker/analytics/summary` → stats cards (total, active 30d, completed 30d, nudge eligible)
- Stats cards display with real numbers
- Nudge-eligible banner appears when `nudge_eligible_count > 0`
- Recent applications list shows real data with employer, role, status badges

### M9.4 — Batch update modal wire ✅
- Fixed API endpoint: `/job-seeker/applications/batch-update` (was incorrectly calling `/${id}/batch-update`)
- Fixed request body format: `{ applications: [{ id, status, final_outcome }] }`
- `mark-all-no-news` button correctly calls `/job-seeker/applications/mark-all-no-news`
- Field name fixed: `company` → `employer` to match backend response

### M9.6 — Auto-close correction banner ✅
- AutoCloseBanner component integrated into Dashboard
- Fetches from `GET /job-seeker/applications/auto-closed`
- Banner displays count and employer names
- "Correct" navigates to applications page
- "Looks right" dismisses banner
- Field names updated: `company` → `employer`, added `role`, `status`, `auto_closed_at`

---

## Remaining

All M9 subtasks completed ✅

---

Original M9 file preserved below:

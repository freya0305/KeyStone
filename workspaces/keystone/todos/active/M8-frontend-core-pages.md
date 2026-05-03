# M8 — Frontend Core Pages (Landing + Analysis Workspace)

> Depends on: M7 (design system), M2 (resume backend), M3 (job analysis backend), M4 (suggestions backend)
> Build todos below create static/mock UI. Wire todos connect to real backend APIs.
> Implements: workspaces/keystone/03-user-flows/01-site-map.md through 04-ai-interaction-patterns.md

---

## M8.1 — Landing page (build)

**What**: Marketing landing page at `/`. Gate-free CTA — user enters the product from here without signing up.

**Sections**:
1. **Hero** (above fold):
   - Headline: "The resume tailoring tool built for the Singapore job market." (H1, Inter 600 or Fraunces)
   - Subhead: "Paste a job. Get a resume tuned for that role, that company, this market. In under a minute."
   - CTA: `[Try it on one job — free]` → `/analyse` (NO sign-up required)
   - Sub-CTA: `[See how it works]` → scroll to features
   - Hero visual: NOT a product screenshot (too hard to keep current). Use a before/after text comparison: original vague bullet → specific rewrite with attribution "This GLC values quantified leadership — your phrase reads as ambiguous ownership."

2. **Social proof strip**: 3 one-line quotes from design partners (to be added before launch)

3. **How it works** (3 steps):
   - "Paste your resume + a job link (30s)"
   - "See where you match and where you don't (10s)"
   - "Review specific rewrites — accept the ones you want (60s)"

4. **Singapore-specific section**: "Built for how Singapore companies actually hire" — NRIC advice, NS framing, GLC vs MNC conventions, education hierarchy. This is the trust section — earns credibility, especially for PMET users.

5. **Pricing preview**: Simple 2-column (Free / Pro), SGD 19/month price visible. CTA: "Start free — no credit card."

6. **Footer**: Privacy / Terms / PDPA Compliant · Your data stays in Singapore · You can delete everything anytime

**Performance**: Hero section must load in <2s on mobile (3G simulation). Fonts: Inter loaded via `next/font`. No third-party scripts in `<head>`.

**Acceptance criteria**:
- CTA click goes to `/analyse` — no sign-up modal
- Page loads in <2s on mobile network
- Mobile responsive (test at 375px, 768px, 1280px)

**Implements**: specs/product.md §Core Value Proposition (landing page copy), Analysis 24 §Decision 2

---

## M8.2 — Landing page wire (connect to real state)

**What**: Wire landing page to live signup/auth state and real pricing data.

**Changes from build**:
- CTA changes to "Continue to dashboard →" if user is already logged in
- Pricing section fetches current prices from Stripe (not hardcoded)
- Social proof quotes loaded from CMS or config file (not hardcoded in JSX)

**Acceptance criteria**:
- Logged-in users see "Continue to dashboard" CTA
- Pricing correct in SGD

---

## M8.3 — Onboarding / activation flow (build)

**What**: The first-time user experience. Steps: resume upload → JD input → analysis wait → see suggestions.

**Flow implementation** (from Analysis 21 §Part 2):

**Step 1 — Entry** (`/analyse`, no auth required):
- JD input first (URL or text paste) — per Analysis 24 Decision 1: JD-first
- Or resume upload first — let A/B test determine winner, ship JD-first as default
- `<JDInput>` component (from M7.2)

**Step 2 — Resume upload** (shown after JD input, or combined on one screen):
- `<DropZone>` component
- Accept: PDF, DOCX, plain text
- If user has previous resume: "Use your previous resume [filename]" → skip upload

**Step 3 — Analysis loading** (10-30 seconds):
- Progressive disclosure (from Analysis 21 §Stage 4):
  - 0-3s: skeleton shimmer
  - 3-8s: "✓ Parsed JD · Identified GLC employer type · ⟳ Comparing with your experience..."
  - 8-12s: Match summary counts appear (before suggestions load)
  - 12s+: Suggestions stream in one by one
- `<LoadingInsight>` component rotates SG hiring insights

**Step 4 — Results page** (`/analyse/{job_analysis_id}`):
Three-column layout (desktop) / single column (mobile):
- **Left**: Resume outline with sections highlighted by match level (clickable to jump to suggestion)
- **Center**: `<SuggestionCard>` stack — Transferable + Addressable first
- **Right sidebar**: Match summary card showing Strong count + "What's already working" list

**Fundamental gaps** (bottom of page, collapsed by default):
- Section title: "Worth knowing (not a blocker)"
- Opener: "X of 12 requirements are strong matches. These 3 are longer-term — most candidates at this level face the same gaps."
- Uses `<MatchChip level="fundamental">` — PLUM, NOT RED

**Registration prompt** (NOT at start — shown after):
- First Accept: toast "Save your work — sign in to keep this analysis." + slide-in auth prompt (not modal blocking the flow)
- Third suggestion viewed: inline prompt
- Download click: required gate (must sign in to download)

**Acceptance criteria**:
- First-time user can see all suggestions without signing in
- Loading screen shows at least 3 progressive disclosure events
- First suggestion appears within 5 seconds of analysis completing
- Fundamental gap section collapsed by default, titled "Worth knowing"
- Registration prompt fires AFTER first accept — not before

**Implements**: Analysis 21 (full activation flow), Analysis 26 §3.1 (SuggestionCard), Analysis 28 §Risk 2 (Fundamental gap anxiety)

---

## M8.4 — Onboarding flow wire (connect to backend APIs)

**What**: Wire the activation flow to real backend APIs (M2, M3, M4).

**API calls to wire**:
- Resume upload: `POST /api/resumes/upload` (M2.1)
- JD analysis: `POST /api/job-analyses` (M3.5)
- Progress updates: SSE from `/api/resumes/{id}/progress` and `/api/job-analyses/{id}/progress`
- Suggestions: `GET /api/job-analyses/{id}/suggestions` (M4.5)
- Accept: `POST /api/suggestions/{id}/accept` (M4.2)
- Reject: `POST /api/suggestions/{id}/reject` (M4.2)
- Modify: `POST /api/suggestions/{id}/modify` (M4.2)

**Error states** (all must be user-friendly, per Analysis 26 §4.3):
- URL parse failure → silent switch to text paste
- Resume parse failure → silent switch to text area
- Analysis timeout (>30s) → "Taking a little longer than usual — here are your match results while suggestions finish loading"

**Free tier gate**: wire `<ProGate>` component to real API response `gated: true`

**Acceptance criteria**:
- Full flow works end-to-end: paste JD + upload resume → see real suggestions
- Progress SSE events display correctly
- Accept/Reject/Modify trigger real signal writes (verify in DB)
- Free tier gate shows with correct section name from real API response

---

## M8.5 — Suggestion export flow (build + wire)

**What**: "Download Resume" button and the application creation modal that follows.

**Build**:
- "Download tailored resume" button at top of suggestions page
- Download format picker: PDF / DOCX (two buttons or a toggle)
- Post-download modal: "Submitting this to [Company]? [Yes — track this application] [Just downloading]"
  - Company name pre-filled from JD extraction
  - "Yes" creates application record
  - "Just downloading" logs `opted_out` event
  
**Wire**:
- Download: `GET /api/job-analyses/{id}/export?format=pdf` → signed S3 URL → browser download
- Yes: `POST /api/applications` with `{job_analysis_id, suggestion_set_id, employer, role}` (M5.1)

**Acceptance criteria**:
- PDF download initiates immediately (non-blocking modal)
- Accepted suggestions appear in exported PDF
- Modal fires after download initiation (not before)
- "Yes" creates application record with `suggestion_set_id` linked

**Implements**: Analysis 05 §1.1 (auto-creation at download), specs/product.md §Feature 3 (export)

---

## M8.6 — My Resumes page (build + wire)

**What**: Page listing user's uploaded resumes with access to previous analyses.

**Build** (`/resumes`):
- List of resumes with: filename, upload date, number of analyses run
- For each resume: "See analyses" → list of job analyses run against it
- "Upload new resume" → `<DropZone>`

**Wire**: `GET /api/resumes` + `GET /api/resumes/{id}/analyses`

**Accepts criteria**: 
- User can view all previous resumes
- Each previous analysis is accessible (click → return to suggestion view)
- "Use this resume" for a new analysis pre-fills the resume step

**Implements**: workspaces/keystone/03-user-flows/01-site-map.md §My Resumes

---

## M8.7 — PostHog analytics instrumentation (wire)

**What**: Wire all key user actions to PostHog for the activation funnel monitoring. Required before design partner launch.

**Key events to instrument** (from Analysis 22 §Product Metrics):
- `page_view` (automatic via PostHog)
- `resume_uploaded` `{user_id, file_type, nric_detected, ns_present, persona}`
- `jd_analysed` `{job_analysis_id, company_type, source: 'url'|'text'}`
- `suggestion_accepted` `{suggestion_id, company_type, match_level, position_in_list}`
- `suggestion_rejected` `{suggestion_id, rejection_reason?}`
- `suggestion_modified` `{suggestion_id}`
- `resume_downloaded` `{job_analysis_id, format}`
- `application_created` `{from_download: bool, employer}`
- `signup_triggered` `{trigger: 'first_accept'|'third_view'|'download'}`
- `signed_up` `{method: 'google'|'email'}`
- `pro_subscribed` `{plan: 'monthly'|'annual'}`
- `paywall_seen` `{section, gated_count}`

**Funnel setup in PostHog**: landing → upload → analyse → suggestion_seen → suggestion_accepted → signed_up → pro_subscribed

**Acceptance criteria**:
- All events fire in correct order for a complete flow (verify in PostHog live view)
- `suggestion_accepted` fires only when real accept happens (not on load)
- Funnel visible in PostHog dashboard

**Implements**: Analysis 22 §Product Metrics Framework, specs/mvp-scope.md §Commercial done criteria


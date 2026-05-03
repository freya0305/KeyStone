# KeyStone — Core Workflow Screens

**Status**: Design specification — MVP v1.0
**Date**: 2026-04-29
**Coverage**: All authenticated screens after onboarding (and the deeper layers of guest screens)

---

## 1. Screen Inventory

| ID | Screen | Path | Used by |
|---|---|---|---|
| S1 | Dashboard | `/app` | Authenticated returning user |
| S2 | New Application — JD entry | `/app/new` | Auth + Guest (`/try`) |
| S2.5 | JD analysis (in-flight) | `/app/new/analyzing` | Both |
| S3 | New Application — Resume upload | `/app/new/resume` | Both |
| S3.5 | Resume parsing | `/app/new/parsing` | Both |
| S4 | Match assessment + Suggestions | `/app/applications/:id/suggestions` | Both |
| S5 | Tailored resume preview | `/app/applications/:id/preview` | Both |
| S6 | Export / download | `/app/applications/:id/export` | Both |
| S7 | Outcome tracking | `/app/applications/:id/outcome` | Auth only |
| S8 | Applications list | `/app/applications` | Auth only |
| S9 | Insights | `/app/insights` | Auth only |
| S10 | Settings — Consent | `/app/settings/consent` | Auth only |

---

## 2. S1 — Dashboard (`/app`)

**Purpose**: Returning-user landing. Surface the next action; track outcomes; gently surface the upgrade path.

**State variants**:
- New user (0 apps)
- Active user (1–9 apps)
- Power user (10+ apps)

### Layout — Active user (1–9 apps)

```
┌─────────────┬─────────────────────────────────────────────────────────────┐
│ KeyStone    │  Dashboard                                                  │
│             │  ────────                                                   │
│ ◉ Dashboard │                                                             │
│   New       │  ┌──────────────────────────────────────────┐               │
│   Apps (4)  │  │  Tailor a new application                │               │
│   Resumes   │  │  Paste a job posting to begin            │               │
│   Insights  │  │  ┌─────────────────────────────────┐    │               │
│             │  │  │ Paste JD URL or text…           │    │               │
│ ─────────   │  │  └─────────────────────────────────┘    │               │
│   Settings  │  │            [  Analyze →  ]               │               │
│   Help      │  └──────────────────────────────────────────┘               │
│             │                                                             │
│ Free tier   │  Recent applications                              View all → │
│ 2 / 3 used  │  ──────────────────────                                     │
│ [Upgrade]   │  ┌──────────────────────────────────────────┐               │
│             │  │ DBS — Operations Manager        ●Applied │               │
│             │  │ 71% match · 5/8 suggestions accepted     │               │
│             │  │ Applied 12 Mar · No update yet           │               │
│             │  │ [Update status]  [Open]                  │               │
│             │  └──────────────────────────────────────────┘               │
│             │  ┌──────────────────────────────────────────┐               │
│             │  │ GovTech — Senior PM      ●Phone screen   │               │
│             │  │ 84% match · 12/14 accepted               │               │
│             │  │ Phone screen on 18 Mar                   │               │
│             │  │ [Log outcome]  [Open]                    │               │
│             │  └──────────────────────────────────────────┘               │
│             │                                                             │
│             │  Your activity                                              │
│             │  ──────────                                                 │
│             │  ┌─────────────────┬─────────────────┐                      │
│             │  │ Response rate   │ Suggestion      │                      │
│             │  │     25%         │ accept rate     │                      │
│             │  │ 1 / 4 applied   │     78%         │                      │
│             │  └─────────────────┴─────────────────┘                      │
│             │                                                             │
└─────────────┴─────────────────────────────────────────────────────────────┘
```

**Component details**:

- **"Tailor a new application" hero card** (top, full content width):
  - This is the primary action — visually the largest interactive element
  - 16px input + 48px button — same as guest flow (consistency)
  - Background: subtle gradient from #F0FDFA → white (avoids AI-slop purple gradient, brand teal at low saturation)

- **Recent applications** (max 3 cards shown, "View all" link):
  - Each card: 88px tall, full width
  - Title row: `Employer — Role` (16px weight 600) + status pill on right
  - Stats row: match score, suggestions accepted (14px, color #6B7280)
  - Activity row: when applied, last update or "no update yet"
  - Two action buttons: primary action depends on state ([Update status] when no recent activity; [Log outcome] when stage transition pending)

- **Status pills** (right of title row):
  - ● Draft (grey)
  - ● Applied (blue)
  - ● Response (amber — "they wrote back")
  - ● Phone screen / Interview R1, R2, R3 (teal, the brand color — progress is good)
  - ● Final / Offer (green)
  - ● No response (light grey)
  - ● Rejected (light red)
  - The pills use SHAPE+COLOR redundancy for accessibility (filled circle + color)

- **"Your activity" widget pair**:
  - Shown only if user has ≥3 applications AND ≥1 outcome logged (else "Track your first outcome to see your stats")
  - Response rate (the SG-correct term, not "callback rate")
  - Suggestion accept rate — implicitly normalizes the user; high accept = high engagement
  - Both are absolute and personal; no comparison to "other users" until corpus is mature (M6+)

**Data events on dashboard render**:
```
dashboard.shown
  - app_count, applications_with_outcomes_count, applications_pending_update
  - days_since_last_action
```

Dashboard fires `applications_pending_update` because that drives the **batch outcome update banner** (a critical data collection surface):

### Banner — Outcome update prompt

```
┌──────────────────────────────────────────────────────────────────────┐
│ ⓘ  4 applications haven't been updated in over a week.               │
│    Spend 2 minutes to record what happened — it improves your        │
│    suggestions and the data we use to help others.                   │
│    [ Update all 4  →  ]   [ Not now ]                                │
└──────────────────────────────────────────────────────────────────────┘
```

- Appears at top of dashboard ONLY when there's an outcome backlog
- "improves your suggestions and the data we use to help others" — frames data sharing as reciprocal, not extractive
- "Update all 4" opens the batch quick-update UI (card swipe: 30 apps in <3 min — see project memory)

### Empty state — New user (0 apps)

```
┌─────────────────────────────────────────────────────┐
│  You haven't tailored a resume yet.                 │
│  Start with a job you're actually applying to —     │
│  the suggestions get more specific the more         │
│  context we have.                                   │
│                                                     │
│  ┌─────────────────────────────────────────┐        │
│  │ Paste a job URL or full job description │        │
│  │                                         │        │
│  └─────────────────────────────────────────┘        │
│         [   Analyze this job  →   ]                 │
│                                                     │
└─────────────────────────────────────────────────────┘
```

- Single screen-tall card. No sidebar widgets, no insights placeholders, no "tour" overlays.
- Microcopy is calm and explanatory, not enthusiastic.

---

## 3. S2 / S2.5 — JD Entry & Analysis

Covered in detail in `02-onboarding-activation.md` Steps 0–1. Authenticated variant is identical except:
- No anonymous session_id
- Pre-fills last-used resume option ("Use your master resume? [yes / pick different]")
- Skips to S4 if user already has a master resume on file

---

## 4. S3 / S3.5 — Resume Upload & Parsing

Covered in detail in `02-onboarding-activation.md` Steps 2–3. Authenticated variant adds:
- "Use my master resume" pre-checked option (eliminates a step for return users)
- Resume version picker: "Or pick a previous version" (for users iterating across many JDs)

---

## 5. S4 — Match Assessment + Suggestions (THE PRIMARY SCREEN)

This is where users spend 80% of their time. Designed for both first-time density-phobic users and power-users tailoring their 50th resume.

### Layout — Desktop (≥1280px)

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│ Applications / DBS — Operations Manager / Suggestions               [💾 Saved]  │
├─────────────────────────────────────────────────────────────────────────────────┤
│ DBS Bank Ltd — Operations Manager                                               │
│ 71% match · 5 of 8 suggestions accepted · GLC, banking domain                   │
│                                                                                 │
│ [Match]  [Suggestions]  [Preview]  [Outcome]                                    │
│ ─────────────────────────────────────────────────────────────────────────────── │
│                                                                                 │
│ ┌──────────────────────────┬────────────────────────────────────────────────┐  │
│ │ MATCH (left, 320px)      │ SUGGESTIONS (right, fluid)                     │  │
│ │                          │                                                │  │
│ │ ● Strong (5)         ▾   │ Filter: [All] [To do (3)] [Accepted (5)]       │  │
│ │   ✓ Stakeholder mgmt     │ ─────────────────────────────────────────────  │  │
│ │   ✓ Process improvement  │                                                │  │
│ │   ✓ Cross-team coord.    │ Suggestion 4 of 8                              │  │
│ │   ✓ Data analysis        │ ⚡ Reframe — addresses "regulatory exposure"   │  │
│ │   ✓ Vendor management    │                                                │  │
│ │                          │ Your resume says:                              │  │
│ │ ◐ Transferable (4)   ▾   │ ┌─────────────────────────────────────────┐    │  │
│ │   → Risk frameworks      │ │ "Worked with audit team on quarterly    │    │  │
│ │   → Regulatory exposure  │ │  compliance reviews."                   │    │  │
│ │   → Banking domain       │ └─────────────────────────────────────────┘    │  │
│ │   → SAP exposure         │                                                │  │
│ │                          │ We'd say:                                      │  │
│ │ ◑ Addressable (3)    ▾   │ ┌─────────────────────────────────────────┐    │  │
│ │   ⚡ Agile certs         │ │ "Partnered with Internal Audit on MAS    │    │  │
│ │   ⚡ Stakeholder seniority│ │  632-aligned compliance reviews,        │    │  │
│ │   ⚡ Quantified outcomes │ │  covering 12 banking entities quarterly."│    │  │
│ │                          │ └─────────────────────────────────────────┘    │  │
│ │ ⚠ Fundamental (2)    ▾   │                                                │  │
│ │   ⚠ 7+ yrs banking exp   │ Why: DBS expects familiarity with MAS         │  │
│ │   ⚠ MAS reg licensing    │ regulatory frameworks. Naming "MAS 632"        │  │
│ │                          │ shows domain literacy that "compliance         │  │
│ │ ─────────────            │ reviews" alone doesn't convey.                 │  │
│ │ [✏ Edit resume manually] │                                                │  │
│ │ [⤓ Download draft]       │                                                │  │
│ │                          │ ┌──────────┐  ┌──────────┐  ┌──────────┐      │  │
│ │                          │ │ ✓ Accept │  │ ✗ Skip   │  │ ✎ Edit   │      │  │
│ │                          │ │   [A]    │  │   [S]    │  │   [E]    │      │  │
│ │                          │ └──────────┘  └──────────┘  └──────────┘      │  │
│ │                          │                                                │  │
│ │                          │ [↑ Prev]               4 / 8       [↓ Next]   │  │
│ └──────────────────────────┴────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

**Component details — left pane (Match)**:

- Width: 320px fixed (collapsible to 64px icon strip via toggle)
- Each requirement section is collapsible; header shows count + chevron
- Tap a specific requirement → right pane filters to suggestions tied to that requirement (data linkage made navigable)
- Color discipline:
  - ● Strong = #059669 (green-600 — readable, not neon)
  - ◐ Transferable = #D97706 (amber-600 — warm, not alarming)
  - ◑ Addressable = #EA580C (orange-600 — urgent but actionable)
  - ⚠ Fundamental = #DC2626 (red-600) — used SPARINGLY, only on this small section, never in suggestion cards
- Critical: Fundamental section is **collapsed by default** — informational only. User can expand to see "what isn't fixable here" but doesn't get hit with red on first render.

**Component details — right pane (Suggestion card)**:

- Card: 720px max width, centered in the pane
- Header chip: `[Suggestion type] — addresses "[exact requirement text]"`
  - Suggestion types: Reframe, Strengthen, Quantify, Reorder, Add, Remove
  - Each type has a single-character icon (no emoji on cards — emoji is for the side panel categories only)
- "Your resume says:" / "We'd say:" — both in monospace-ish (not actual monospace, but a slightly distinct font weight/family) to evoke the typography of an editor reviewing your text
- "Why:" rationale — 2–3 sentences max, hard cap. Anything longer goes behind a "Show more" disclosure.
- Action buttons: Accept (primary teal), Skip (outlined neutral), Edit (outlined neutral)
  - All three buttons same width (96px), same height (40px) — equal visual weight
  - Keyboard shortcuts shown below each button: [A] [S] [E]
  - Power-user: down-arrow advances; up-arrow goes back; numeric keys jump to suggestion N

### Edit interaction

When user clicks [✎ Edit]:

```
┌─────────────────────────────────────────────────────────────┐
│ Suggestion 4 of 8 — Editing                                 │
│                                                             │
│ Your resume says:                                           │
│ ┌─────────────────────────────────────────────────────┐     │
│ │ "Worked with audit team on quarterly compliance     │     │
│ │  reviews."                                          │     │
│ └─────────────────────────────────────────────────────┘     │
│                                                             │
│ Edit our suggestion:                                        │
│ ┌─────────────────────────────────────────────────────┐     │
│ │ Partnered with Internal Audit on MAS 632-aligned    │     │
│ │ compliance reviews, covering 12 banking entities    │     │
│ │ quarterly.|                                         │     │
│ │                                                     │     │
│ └─────────────────────────────────────────────────────┘     │
│                                                             │
│ [✓ Save edit]   [Reset to suggestion]   [Cancel]            │
└─────────────────────────────────────────────────────────────┘
```

**Why edit is so important**:
- The edit IS the highest-value training signal — the user is correcting the model
- Anti-pattern is to make it a tiny popup; we give it the full card real estate
- "Reset to suggestion" — easy escape if they want our text back
- Captures the diff: what we suggested vs what user shipped

**Data event on save**:
```
suggestion.edited
  - suggestion_id, original_text, suggested_text, user_text
  - edit_distance (computed)
  - employer_id, role_level, industry, etc.
```

The edit distance feeds an explicit signal: low edit distance = our suggestion was almost right; high edit distance = our suggestion was directionally wrong but inspired the user. Both are valuable.

### State variants for the Suggestion card

**Already-accepted state** (when user navigates back to a suggestion they accepted):
```
┌─────────────────────────────────────────────┐
│ Suggestion 4 of 8                           │
│ ✓ Accepted                                  │
│                                             │
│ Your resume now says:                       │
│ ┌─────────────────────────────────────┐     │
│ │ "Partnered with Internal Audit..."  │     │
│ └─────────────────────────────────────┘     │
│                                             │
│ [Undo accept]   [See original]              │
└─────────────────────────────────────────────┘
```

**Already-skipped state**:
```
┌─────────────────────────────────────────────┐
│ Suggestion 4 of 8                           │
│ ✗ Skipped — your resume is unchanged here   │
│                                             │
│ [Try again]                                 │
└─────────────────────────────────────────────┘
```

**Loading state** (suggestions still being generated):
- 3 skeleton cards with shimmer
- Top bar shows "Generating suggestions… 4 of 8 ready"
- Once first suggestion is ready, show it (don't wait for all 8)

**Empty state** (rare — perfect resume?):
- "We couldn't find lines to improve for this role. Your resume is already well-aligned."
- Show match score + match breakdown only, no suggestion list
- Single CTA: "Tailor for another job →"
- Note: This state is suspicious — log a `suggestions.empty` event for monitoring (likely a parser failure, not a perfect resume)

**Error state** (suggestion generation failed):
- "Something interrupted the analysis. Your resume and JD are saved."
- [Try again] button — retries the suggestion engine without re-uploading
- Email-me-when-fixed if retry also fails

### Mobile layout (≤768px)

```
┌────────────────────────────────────┐
│ ☰  DBS — Ops Manager       [💾]   │
├────────────────────────────────────┤
│ 71% match · 5/8 accepted           │
├────────────────────────────────────┤
│ [Match] [Suggest] [Preview] [Out]  │  ← Tab bar
├────────────────────────────────────┤
│                                    │
│ Suggestion 4 of 8                  │
│ ⚡ Reframe                          │
│                                    │
│ Your resume says:                  │
│ "Worked with audit team..."        │
│                                    │
│ We'd say:                          │
│ "Partnered with Internal Audit     │
│  on MAS 632-aligned reviews..."    │
│                                    │
│ Why:                               │
│ DBS expects MAS familiarity...     │
│                                    │
│ ┌──────┐ ┌──────┐ ┌──────┐         │
│ │  ✓   │ │  ✗   │ │  ✎   │         │
│ └──────┘ └──────┘ └──────┘         │
│                                    │
│ ← swipe → for next                 │
└────────────────────────────────────┘
```

- Match panel becomes a separate tab (not a side rail)
- Swipe left = skip, swipe right = accept (mobile gesture)
- Tap-and-hold = edit (deliberate, not accidental)
- Card height takes ~80% of viewport — focuses attention

---

## 6. S5 — Tailored Resume Preview

```
┌─────────────────────────────────────────────────────────────────────────┐
│ Applications / DBS — Operations Manager / Preview            [💾 Saved] │
├─────────────────────────────────────────────────────────────────────────┤
│ Tailored for: DBS Bank — Operations Manager                             │
│ 5 of 8 suggestions applied                                              │
│                                                                         │
│ [Match] [Suggestions] [▶ Preview] [Outcome]                             │
│ ─────────────────────────────────────────────────────────────────────── │
│                                                                         │
│ ┌──────────────────────────┬────────────────────────────────────────┐  │
│ │ JANE TAN                 │ Show: [● Tailored] [○ Original] [○ Diff]│ │
│ │ Operations Lead          │                                        │  │
│ │ jane.tan@email.com       │ ┌────────────────────────────────────┐ │  │
│ │ +65 9XXX XXXX            │ │  EXPERIENCE                         │ │  │
│ │ Singapore                │ │                                     │ │  │
│ │                          │ │  DBS Bank — Operations Analyst      │ │  │
│ │ EXPERIENCE               │ │  Jan 2022 – Present                 │ │  │
│ │                          │ │                                     │ │  │
│ │ DBS Bank                 │ │  • Led cross-functional delivery of │ │  │
│ │ Jan 2022 – Present       │ │    $2M operations programme...      │ │  │
│ │  ● 3 lines tailored      │ │    [tailored] ✓                     │ │  │
│ │                          │ │                                     │ │  │
│ │ Standard Chartered       │ │  • Partnered with Internal Audit on │ │  │
│ │ 2019 – 2021              │ │    MAS 632-aligned compliance...    │ │  │
│ │  ● 2 lines tailored      │ │    [tailored] ✓                     │ │  │
│ │                          │ │                                     │ │  │
│ │ EDUCATION                │ │  • Quarterly review of vendor SLAs  │ │  │
│ │ NUS, Business            │ │    across 8 partner organizations.  │ │  │
│ │                          │ │    [unchanged]                       │ │  │
│ │                          │ └────────────────────────────────────┘ │  │
│ │                          │                                        │  │
│ │                          │ ┌──────────────────────────────────┐   │  │
│ │                          │ │  Looks good? Download as PDF.    │   │  │
│ │                          │ │  [⤓ Download PDF]  [⤓ DOCX]      │   │  │
│ │                          │ └──────────────────────────────────┘   │  │
│ └──────────────────────────┴────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
```

**Component details**:

- Left pane (240px): Resume outline / table of contents
  - Each section shows count of tailored lines
  - Click jumps to that section in the preview
- Right pane: Live preview of the tailored resume
- View toggle: Tailored | Original | Diff (red strikethrough + green addition)
- "[tailored] ✓" inline annotation on each line that was changed (subtle, color #6B7280, click to see the original)

**Diff view** — important for trust:
```
DBS Bank — Operations Analyst                       Jan 2022 – Present

  • ~~Managed projects across multiple teams.~~
    Led cross-functional delivery of $2M operations programme spanning
    Treasury, Tech and Ops.

  • ~~Worked with audit team on quarterly compliance reviews.~~
    Partnered with Internal Audit on MAS 632-aligned compliance
    reviews, covering 12 banking entities quarterly.

  • Quarterly review of vendor SLAs across 8 partner organizations.
```

- Strikethrough = removed (original)
- Below = new (tailored)
- Unchanged lines render normally
- This is the "show your work" view — builds trust by making the AI's edits fully visible and reversible

---

## 7. S6 — Export / Download

```
┌─────────────────────────────────────────────────────────────────┐
│ Export your tailored resume                                     │
│ ────────────────────────────                                    │
│                                                                 │
│ DBS — Operations Manager  ·  5 suggestions applied              │
│                                                                 │
│ ┌─────────────────────────────────────────────────────────┐    │
│ │ Format                                                  │    │
│ │ ● PDF — recommended for online applications             │    │
│ │ ○ DOCX — recommended if employer uses Workday/Taleo     │    │
│ │ ○ Plain text — for ATS systems that strip formatting    │    │
│ │                                                         │    │
│ │ Filename                                                │    │
│ │ ┌─────────────────────────────────────────────┐         │    │
│ │ │ Jane_Tan_Resume_DBS_Operations_Manager.pdf  │         │    │
│ │ └─────────────────────────────────────────────┘         │    │
│ │                                                         │    │
│ │ Filename includes the role — recruiters appreciate it   │    │
│ │                                                         │    │
│ └─────────────────────────────────────────────────────────┘    │
│                                                                 │
│              [   Download as PDF   →   ]                        │
│                                                                 │
│ ────────────────────────────────────────────────                │
│                                                                 │
│ ✓ Did you submit this to DBS?                                   │
│   Knowing helps us measure whether tailoring works —            │
│   and tells us when to follow up.                               │
│   [Yes, I applied]   [Not yet]                                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Critical design moment — the post-download outcome capture**:

This is the **download-triggered capture** moment from the project memory's pull-based outcome strategy. The user is at peak value-realization. Even a single click here delivers an `application.submitted` outcome event that anchors the entire downstream tracking.

- "Yes, I applied" → opens an application stage modal preset to "Applied" with date = today
- "Not yet" → fires `application.intent.no` with timestamp; will retry next session (digest email or in-product banner)
- NEVER block download on this question — it's a follow-up, not a gate

**Filename suggestion logic**:
- Default: `[FirstName]_[LastName]_Resume_[Employer]_[Role].pdf`
- Recruiter-friendly framing — explicit microcopy explains why
- Editable inline; user can override

**Export-watermark logic for guest users**:
- Anonymous user CAN export, but with a footer watermark: "Generated free with KeyStone — sign up to remove this line"
- Watermark is small, in resume footer, NOT a giant overlay (doesn't damage their actual application)
- Sign-up to remove watermark = the effective second gate

---

## 8. S7 — Outcome Tracking

```
┌─────────────────────────────────────────────────────────────────────────┐
│ DBS — Operations Manager                                                │
│ Outcome tracking                                                        │
│ ─────────────────────                                                   │
│                                                                         │
│ Where are you in this process?                                          │
│                                                                         │
│ ●─────●─────○─────○─────○─────○                                         │
│ Applied  Response  Phone  Onsite R1  Onsite R2  Decision                │
│ 12 Mar   18 Mar    —      —         —         —                         │
│                                                                         │
│ ┌──────────────────────────────────────────────────────────────────┐   │
│ │ Latest update: 18 Mar — Got an email response                    │   │
│ │                                                                  │   │
│ │ What happened?                                                   │   │
│ │ ○ Phone screen scheduled                                         │   │
│ │ ○ Asked for more information                                     │   │
│ │ ○ Rejected (politely)                                            │   │
│ │ ● Generic auto-response only                                     │   │
│ │ ○ Something else                                                 │   │
│ │                                                                  │   │
│ │ When?                                                            │   │
│ │ [📅 18 Mar 2026 ]                                                │   │
│ │                                                                  │   │
│ │ Anything you'd like to remember about this?                      │   │
│ │ ┌──────────────────────────────────────────────────────────┐    │   │
│ │ │ Optional notes — only you see these                      │    │   │
│ │ └──────────────────────────────────────────────────────────┘    │   │
│ │                                                                  │   │
│ │             [  Save outcome  ]                                   │   │
│ └──────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│ ────────────────────────────────────────────────                        │
│                                                                         │
│ Bigger picture                                                          │
│ Of your last 4 applications:                                            │
│   2 still waiting · 1 phone screen · 1 no response after 30 days        │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Component details**:

- **Stage timeline at top** — visual horizontal stepper. Filled dots = past, current open dot = where they are. Dates under each stage.
- **Stage selector** — radio list of common outcomes for that stage. Pre-set options drive structured data; "Something else" opens free-text but reduces ambiguity.
- **Calendar input** — defaults to today, easy to backdate
- **Optional notes** — the freetext is GENUINELY optional and "only you see these" framing reduces over-thinking
- **"Bigger picture" panel** — aggregate context from user's other applications, gentle social-proof-of-self

**Stage model** (from project memory):
- Applied → Response → Screening (phone screen) → Interview R1..RN → Final → Decision
- Multi-round support is non-optional (memory says: "Multi-round interview tracking is a data-model requirement — not optional")

**Auto-close logic**:
- After 30 days of silence at "Applied" stage → auto-marks as "No response (inferred)" with a correction toast next time user opens the app
- Toast: "We marked DBS as 'no response' since it's been 30 days. [Update if needed]"
- Correction is one-click — preserves data quality without forcing users to manually close stale apps

**Data events**:
```
outcome.logged
  - application_id, employer_id
  - stage_from, stage_to
  - outcome_type
  - days_since_application
  - logged_via: dashboard | email_link | post_download_modal | digest_link

application.auto_closed
  - reason: silence_30d
```

---

## 9. S8 — Applications List

```
┌─────────────────────────────────────────────────────────────────────────┐
│ Applications                                            [+ New]         │
│ ────────────                                                            │
│                                                                         │
│ Filter:  [All]  [Active]  [Awaiting]  [Outcomes pending]  [Closed]      │
│ Sort:    [Recent ▾]                                                     │
│                                                                         │
│ ┌─────────────────────────────────────────────────────────────────┐    │
│ │ ● Phone screen   · 18 Mar       GovTech — Senior PM             │    │
│ │ 84% match  ·  12/14 accepted    [Log next stage]  [Open]        │    │
│ │ ─────                                                           │    │
│ │ ● Applied        · 12 Mar       DBS — Ops Manager               │    │
│ │ 71% match  ·  5/8 accepted      [Update status]  [Open]         │    │
│ │ ─────                                                           │    │
│ │ ● No response    · 1 Feb        UOB — Risk Analyst              │    │
│ │ 58% match  ·  3/9 accepted      [Open]                          │    │
│ │ ─────                                                           │    │
│ │ ● Draft          · 28 Mar       Shopee — Operations Lead        │    │
│ │ Started, not applied yet        [Continue]  [Delete]            │    │
│ └─────────────────────────────────────────────────────────────────┘    │
│                                                                         │
│  4 applications  ·  1 awaiting outcome  ·  Avg match 78%               │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Component details**:

- Each row: 64px tall, status pill + date on left, employer + role center, match + accept count below, actions right
- Filter chips at top — driven by URL query params (shareable, browser-back-friendly)
- Footer summary line — instant aggregate
- Bulk action row appears when ≥2 selected (multi-select via checkbox on hover):
  - "Update all 4 outcomes" — opens batch update flow
  - "Archive selected"
  - "Export list (CSV)"

---

## 10. S9 — Insights

Surfaces only when ≥3 applications with ≥1 outcome each. Otherwise a placeholder:

```
┌──────────────────────────────────────────────────────┐
│ Your insights show up after a few applications.      │
│ Right now we have 2 applications and 0 outcomes      │
│ logged.                                              │
│                                                      │
│ When you start hearing back, this page tells you:    │
│   · Your response rate vs the SG market              │
│   · Which suggestions actually correlate with        │
│     callbacks                                        │
│   · Which employers respond to your profile          │
│                                                      │
│ [Update an outcome →]                                │
└──────────────────────────────────────────────────────┘
```

**Active state — once data exists**:

```
┌─────────────────────────────────────────────────────────────────────────┐
│ Insights                                                                │
│ ────────                                                                │
│                                                                         │
│ ┌─────────────────────┬─────────────────────┬─────────────────────┐    │
│ │ Response rate       │ Per-stage pass rate │ Suggestions         │    │
│ │     31%             │   Resp → Phone 67%  │ accepted: 78%       │    │
│ │ 5 / 16 applications │   Phone → Onsite 50%│ edited: 12%         │    │
│ │ ▲ vs SG avg ~22%    │   Onsite → Offer—   │ skipped: 10%        │    │
│ └─────────────────────┴─────────────────────┴─────────────────────┘    │
│                                                                         │
│ Where you're winning                                                    │
│ ────────────────────                                                    │
│ Banking sector applications:        45% response rate (5 / 11)          │
│ MNC applications:                   25% response rate (1 / 4)           │
│                                                                         │
│ Where to focus                                                          │
│ ──────────────                                                          │
│ You skip "Quantify outcomes" suggestions 60% of the time, but           │
│ accepted ones correlate with 2.3× higher response rates. Worth          │
│ revisiting.                                                             │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

- Comparison to SG avg shown only when corpus has ≥100 logged outcomes for that segment
- "Where to focus" — actionable insight derived from suggestion-type-to-outcome correlation. Heart of the data moat surfaced as user value.
- Privacy: never show comparison numbers smaller than N=20 (employer fingerprint reveal threshold)

---

## 11. S10 — Settings: Consent

```
┌─────────────────────────────────────────────────────────────────────────┐
│ Settings / Consent                                                      │
│ ─────────────────                                                       │
│                                                                         │
│ Singapore PDPA — what we collect and how it's used                      │
│                                                                         │
│ Each setting below is independent. You can change them any time.        │
│                                                                         │
│ 1. Service operation                                          [Required]│
│    Storing your resume + JDs to give you suggestions. This is how       │
│    KeyStone works — it can't be turned off without deleting your        │
│    account.                                                             │
│                                                                         │
│ 2. AI improvement (anonymous)                                  [✓ On]   │
│    Lets us learn from which suggestions you accept and skip.            │
│    Your name, NRIC, and personal details are stripped first.            │
│    Helps make suggestions better for everyone.                          │
│                                                                         │
│ 3. Outcome correlation                                         [✓ On]   │
│    When you log application outcomes, we pair them with the             │
│    suggestions you used. This is how we measure whether tailoring       │
│    actually helps. You can see your own results in Insights.            │
│                                                                         │
│ 4. Email reminders                                             [✓ On]   │
│    We email you on Day 3 / 10 / 21 after an application to nudge        │
│    you to log outcomes. Off = no emails about specific applications.    │
│                                                                         │
│ 5. Aggregate research                                          [○ Off]  │
│    Allow KeyStone to use your fully anonymized data in published        │
│    reports about Singapore hiring trends. Your individual data is       │
│    never identifiable.                                                  │
│                                                                         │
│ 6. University / employer sharing                               [○ Off]  │
│    If you joined via NUS / SMU / WSG, allow them to see                 │
│    aggregate stats about students in their cohort. Never your           │
│    individual data.                                                     │
│                                                                         │
│ ────────────────────────                                                │
│                                                                         │
│ [⤓ Download all my data]   [⚠ Delete my account]                        │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Component details**:

- Six independent toggles (PDPA: 6-type independent consent — see project memory)
- Each toggle has a HUMAN-LANGUAGE explanation, not legal jargon
- Defaults reflect the implicit choices made at signup (toggles 1–4 on by default; 5–6 off)
- Toggle off → confirmation modal explaining the trade-off ("If you turn off AI improvement, your suggestions won't get better over time. Your account still works.")

**Why this granular consent IS the trust signal**:
- Most products bundle "Accept all" or "Reject all" — users learn to assume the worst
- Granular consent with plain-language explanations + visible defaults makes data collection feel collaborative
- The user who reads this and leaves toggle 2 ON has explicitly opted in — making the moat data legally and ethically defensible

**Data event**:
```
consent.changed
  - consent_type: ai_improvement | outcome_correlation | reminders | research | sharing
  - new_value: true | false
  - trigger: settings_page | onboarding | privacy_policy_link
```

---

## 12. Cross-Screen Components

### Status pill (used everywhere)
- Filled dot + label, padding 4px 10px, border-radius 12px, font-size 12px
- Color paired with shape for accessibility

### Suggestion card chip
- Always shape: `[icon] [Type] — addresses "[requirement]"`
- Type icons (single character, not emoji): R / S / Q / O / + / −

### Action button hierarchy
- Primary: solid teal #0F766E, white text, 40px tall
- Secondary: outlined neutral, 40px tall
- Tertiary: text only, no border
- Destructive: text-red-600, no background until hover

### Empty / loading / error states (universal)
- Empty: descriptive text + single CTA, no illustration (illustrations age fast and are AI-slop fingerprints)
- Loading: skeleton elements, never indeterminate spinner alone
- Error: explanation + retry button + "email us" fallback

---

## 13. Keyboard Map (Power-User Surface)

| Key | Action | Where |
|---|---|---|
| `A` | Accept current suggestion | S4 |
| `S` | Skip current suggestion | S4 |
| `E` | Edit current suggestion | S4 |
| `↓` / `j` | Next suggestion | S4 |
| `↑` / `k` | Previous suggestion | S4 |
| `1`–`9` | Jump to suggestion N | S4 |
| `⌘+S` | Save (no-op — already auto-saved; shows "Saved" toast) | All |
| `⌘+E` | Export tailored resume | S4, S5 |
| `⌘+/` | Show keyboard shortcuts | All |
| `⌘+K` | Quick switch application (command palette) | All |
| `Esc` | Close modal / back to list | All |

A small `?` button bottom-right opens the shortcuts cheat sheet. Power users (mid-career persona, applies to many roles) discover this within 2–3 sessions.

---

## 14. Accessibility Guarantees

- All interactive elements ≥44×44px tap target (mobile)
- All color-coded states paired with shape or text label
- Tab order matches visual order
- All actions reachable via keyboard
- Live regions for AI streaming (announces "Suggestion 4 ready" to screen readers)
- WCAG AA contrast on all text — 4.5:1 minimum
- Focus rings visible (NOT removed for aesthetics — that's an AI-slop tell)

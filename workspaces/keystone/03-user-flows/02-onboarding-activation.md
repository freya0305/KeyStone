# KeyStone — Onboarding & Activation Storyboard

**Status**: Design specification — MVP v1.0
**Date**: 2026-04-29
**Goal**: First Suggestion Accepted in ≤5 minutes, ≥40% conversion to register

---

## 1. The Activation Funnel (Target Math)

```
Landing visit                        100%
  ↓ click "Try it now"               45%
Paste JD                             40%
  ↓ JD parsed                        38%
Upload resume                        32%
  ↓ resume parsed                    30%
Match assessment shown               29%
  ↓ scroll to first suggestion       28%
Accept first suggestion              18%   ← AHA MOMENT
  ↓ register prompt
Register                              9%   ← 50% post-aha conversion
```

Every step before "Accept first suggestion" is a leak point. Design discipline: **remove anything not strictly required to render the first suggestion**.

---

## 2. Step-by-Step Storyboard

### STEP 0 — Landing page (`/`)

**What user sees** (above the fold, desktop):

```
┌──────────────────────────────────────────────────────────────────────┐
│ [KeyStone]                                              [Log in →]   │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│                                                                      │
│       Get a resume tuned for the job you actually want.              │
│       ────────────────────────────────────────────────              │
│       Paste a Singapore job posting. We'll show you the              │
│       lines that need rewriting — and exactly how.                   │
│                                                                      │
│       ┌────────────────────────────────────────────────────┐        │
│       │ Paste a job URL or full job description here       │        │
│       │                                                    │        │
│       │ Try MyCareersFuture, JobStreet or LinkedIn         │        │
│       │                                                    │        │
│       └────────────────────────────────────────────────────┘        │
│                                                                      │
│                  [   Analyze this job  →   ]                         │
│                                                                      │
│         No signup. First analysis is free, unlimited.                │
│                                                                      │
│       ─────────────────────────────────────────────────              │
│       Calibrated on Singapore hiring. NRIC stays private.            │
│       Used by ▮▮▮ students at [University logo strip].              │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

**Component details**:

- **Headline** (48px, weight 600, line-height 1.1): "Get a resume tuned for the job you actually want."
  - NOT "AI-powered resume builder" (generic, AI-slop fingerprint)
  - NOT "Optimize your resume" (Jobscan-coded, low specificity)
  - "tuned for the job you actually want" — emotional hook on user's specific aspiration
- **Sub-headline** (18px, weight 400, color #4B5563): "Paste a Singapore job posting. We'll show you the lines that need rewriting — and exactly how."
  - "Singapore" anchors the SG-specific intelligence claim
  - "exactly how" promises specificity (the differentiator vs ChatGPT)
- **JD input box** (full width up to 720px, 5 rows tall, monospace placeholder text)
  - Placeholder: "Try MyCareersFuture, JobStreet or LinkedIn"
  - Auto-detects URL vs pasted text on first keystroke
- **CTA button**: "Analyze this job →"
  - Color: primary brand (deep teal #0F766E — NOT purple, NOT blue gradient — see anti-AI-slop note)
  - Size: 56px tall, 240px wide, weight 500
  - State: disabled until input has ≥40 characters
- **Trust line below CTA** (14px, weight 400, color #6B7280): "No signup. First analysis is free, unlimited."
- **Social proof strip** (96px below CTA): University logos in greyscale (NUS / SMU / NTU once piloted)

**Microcopy decisions**:
- "Paste a job URL or full job description here" — both inputs accepted, lowers friction
- "First analysis is free, unlimited" — emphasizes "unlimited" because returning users are gated; first-timers are NOT
- No mention of price on landing — pricing page is one click away, but not shoved at first-time visitors

**What user feels**: "Oh — I don't have to sign up. I'll just try it."

**Data event fired on CTA click**:
```
session.created
  - session_id: <uuid>
  - source: organic | paid | referral | direct
  - landing_variant: control | <variant>
  - jd_input_method: url | paste
  - jd_input_length: <chars>
```

---

### STEP 1 — JD Analysis (`/try/analyzing`, takes ≤8s)

**Decision: JD-first, not resume-first.**

Rationale:
1. User's intent is "I'm applying to X" — JD is the active anchor
2. JD parsing is faster than resume parsing (10–15s saved if we start it sooner)
3. "Job analyzed" before "upload resume" frames the resume request as **personalized to the job they care about**, not as a generic onboarding step
4. If user abandons here, we still have a JD signal (employer + role-level), useful for understanding demand

**What user sees during the 8-second JD analysis**:

```
┌──────────────────────────────────────────────────────────────────────┐
│                                                                      │
│       Reading the job posting…                                       │
│                                                                      │
│       ✓ Identified employer:    DBS Bank Ltd                         │
│       ✓ Role level:             Senior individual contributor         │
│       ✓ Industry:               Banking & Financial Services         │
│       ⏳ Extracting requirements…  (12 found so far)                  │
│       ◯ Detecting company type…                                      │
│                                                                      │
│       ────────────────────────────────────────                       │
│                                                                      │
│       Did you know?                                                  │
│       DBS hires 60% of its Operations roles internally.              │
│       External candidates win on demonstrated banking domain         │
│       knowledge — not generic project management language.           │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

**Component details**:

- **Streaming checklist** (checkmarks resolve as analysis completes):
  - Each item appears as Haiku finishes that field
  - ✓ resolved (green), ⏳ in-progress (animated), ◯ pending (grey)
  - Visible activity makes the wait feel productive, not stuck
- **"Did you know?" panel** (the genius slot):
  - Pulled from the SG market rules / employer fingerprint corpus (Layer 1 + Layer 2)
  - Different content for different employers / industries
  - **This is the moment KeyStone establishes "we know things ChatGPT doesn't"**
  - Falls back to a generic SG market insight if employer is unknown

**Empty / error states**:

- **JD URL fetch fails**: "We couldn't fetch the job posting. Paste the description here instead." — text area appears in place. Don't break the flow.
- **JD too short (<200 chars)**: "This looks short. Paste the full job description for the best analysis." — keep the user in flow, don't error.
- **Non-SG job detected**: Continue analysis but show a small banner: "Looks like this role isn't Singapore-based. Some of our SG-specific insights won't apply." — transparent about scope, doesn't block.

**Data event fired**:
```
jd.parsed
  - session_id
  - employer_id (or null)
  - employer_company_type: GLC | MNC | local_sme | government | startup | unknown
  - role_level: graduate | individual_contributor | senior_ic | manager | senior_manager | director
  - industry
  - requirements_count
  - parse_latency_ms
  - input_method: url | paste
```

---

### STEP 2 — Resume Upload (`/try/resume`)

**What user sees** (after JD analysis completes, auto-advance):

```
┌──────────────────────────────────────────────────────────────────────┐
│                                                                      │
│       Now show us your resume.                                       │
│       ────────────────────────                                       │
│       We'll match it against the DBS Operations Manager role         │
│       and tell you what to change.                                   │
│                                                                      │
│       ┌────────────────────────────────────────────────────┐        │
│       │                                                    │        │
│       │              📄                                    │        │
│       │       Drag your resume here                        │        │
│       │       or click to upload                           │        │
│       │                                                    │        │
│       │       PDF or Word.   Stays on your device          │        │
│       │       until you accept a suggestion.               │        │
│       │                                                    │        │
│       └────────────────────────────────────────────────────┘        │
│                                                                      │
│       Don't have a resume file?                                      │
│       [ Paste resume text instead ]                                  │
│                                                                      │
│       ────────────────────────────────────────────────────           │
│       NRIC numbers are detected and masked before analysis.          │
│       Your resume is never used to train AI without consent.         │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

**Component details**:

- **Headline** (32px, weight 600): "Now show us your resume."
- **Sub-headline** (16px, color #4B5563): References the SPECIFIC employer + role from Step 1 — this is the personalization payoff
- **Drop zone**: 480px wide, 240px tall, dashed border #D1D5DB → solid #0F766E on hover/dragover
  - File icon (48px) centered, label below
  - Microcopy "Stays on your device until you accept a suggestion" — privacy claim that's also literally accurate (we process server-side but don't persist until accept event)
- **Fallback link** (small, below drop zone): "Paste resume text instead" — opens textarea, never blocks
- **Trust line at bottom**:
  - "NRIC numbers are detected and masked before analysis."
  - "Your resume is never used to train AI without consent."
  - These are critical PDPA-aligned trust signals; fresh grad persona is highly sensitive to NRIC handling

**Mobile variation**: Camera capture as additional upload option ("Snap a photo of a printed resume" — not common but PMET persona reality).

**Data event fired**:
```
resume.upload.started
  - session_id
  - upload_method: drag | click | paste | camera
  - file_type: pdf | docx | txt | image
  - file_size_bytes
```

---

### STEP 3 — Resume Parsing (`/try/parsing`, takes ≤10s)

**What user sees**:

```
┌──────────────────────────────────────────────────────────────────────┐
│                                                                      │
│       Reading your resume…                                           │
│                                                                      │
│       ✓ Detected and masked:  1 NRIC (last 4 digits hidden)         │
│       ✓ Found:                3 roles, 2 education entries           │
│       ✓ Extracted:            41 skills and experiences              │
│       ⏳ Cross-referencing with the DBS role…                        │
│                                                                      │
│       ────────────────────────────────────────                       │
│                                                                      │
│       Quick read:                                                    │
│       Your strongest signals for this role are                       │
│       process improvement and stakeholder management.                │
│       Hold tight — we're checking 12 more requirements.              │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

**Component details**:

- The NRIC line is intentional — surfaces the SG-specific protection without making a big deal of it
- "Quick read" panel — preview of the analysis (the suggestion engine has already started; this is a teaser to keep engagement high during the wait)
- Total wait at this point: ~8s JD + 10s resume = ~18s. The inline "did you know" + "quick read" panels make it feel like 2 short stages, not 1 long one.

**Error states**:

- **NRIC found**: Always silent-mask, show count. Never display the NRIC. Never warn aggressively (PMET sensitivity).
- **Resume parse failure** (corrupt PDF, image-only PDF, scanned doc): "We can't read this format clearly. Try Word format, or paste the text below." Falls back to textarea — never dead-ends.
- **Resume too short (<200 words)**: Continue, but at suggestion stage say "Add more detail to your resume to get richer suggestions" rather than blocking.
- **Resume looks like a different person's** (e.g., uploaded JD by mistake): Heuristic check — if no first-person language detected, prompt: "This looks like a job posting, not a resume. Did you mean to upload your CV?"

**Data event**:
```
resume.parsed
  - session_id
  - role_count, education_count, skill_count
  - nric_found: boolean
  - photo_found: boolean
  - parse_latency_ms
```

---

### STEP 4 — The Aha Moment (`/try/match`)

**This is the screen that decides whether the user converts.** The user's first impression of the product's intelligence.

**What user sees** (full screen, 1280px desktop):

```
┌──────────────────────────────────────────────────────────────────────┐
│ Your resume vs DBS — Operations Manager                              │
│                                                                      │
│  ████████████░░░░░░  71% match                                       │
│                                                                      │
│  5 strong signals   •   4 transferable   •   3 to reframe   •   2 gaps │
│                                                                      │
│  Below: 8 specific lines we'd rewrite.                               │
│  ────────────────────────────────────────────────                    │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────┐     │
│  │  Suggestion 1 of 8                                         │     │
│  │  ⚡ Reframe — addresses "drive cross-team initiatives"      │     │
│  │                                                            │     │
│  │  Your resume says:                                         │     │
│  │  ┌────────────────────────────────────────────────────┐   │     │
│  │  │ "Managed projects across multiple teams."          │   │     │
│  │  └────────────────────────────────────────────────────┘   │     │
│  │                                                            │     │
│  │  We'd say:                                                 │     │
│  │  ┌────────────────────────────────────────────────────┐   │     │
│  │  │ "Led cross-functional delivery of $2M operations   │   │     │
│  │  │  programme spanning Treasury, Tech and Ops."       │   │     │
│  │  └────────────────────────────────────────────────────┘   │     │
│  │                                                            │     │
│  │  Why: DBS Operations roles are programme-led, not          │     │
│  │  project-led. The phrasing "cross-functional delivery"     │     │
│  │  matches how DBS hiring managers describe the work in      │     │
│  │  this requirement.                                         │     │
│  │                                                            │     │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐                 │     │
│  │  │ ✓ Accept │  │ ✗ Skip   │  │ ✎ Edit   │                 │     │
│  │  └──────────┘  └──────────┘  └──────────┘                 │     │
│  └────────────────────────────────────────────────────────────┘     │
│                                                                      │
│   Press ↓ for the next suggestion                                    │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

**Why this layout for the first suggestion (NOT the two-pane view yet)**:
- The two-pane match-breakdown view is dense; first impression must be ONE thing
- Show the diagnosis (top bar with %) + the prescription (one suggestion card)
- After Accept on this first suggestion, transition to the full two-pane view (deferred density)

**Component details**:

- **Match bar** (top): Solid filled portion = strong+transferable. Lighter portion = total. Single number "71%" — simple, intelligible.
- **Match summary line**: Counts only, no color-coded badges yet. Color enters in the suggestion cards.
- **Suggestion card** (centered, 720px wide):
  - Header chip: "⚡ Reframe — addresses [requirement]" — labels the SUGGESTION TYPE (Reframe / Strengthen / Quantify / Reorder) AND its tie-back to a specific JD requirement
  - "Your resume says:" / "We'd say:" — first person inclusive language, NOT "Original / Suggested" (clinical, AI-coded)
  - Quotation boxes around both versions (visual parity — the user's text is given the same weight as the AI's)
  - "Why:" rationale (NOT "Because" — softer, conversational)
  - Three action buttons, equal visual weight (this is critical — see § 4 of the AI Interaction Patterns doc)
- **Keyboard hint**: "Press ↓ for the next suggestion" — power-user accelerator surfaced from the start

**Why "We'd say" instead of "Suggested"**:
- "Suggested" is AI-output framing
- "We'd say" is colleague-giving-you-feedback framing
- Same information, different emotional register

**Data event fires on render**:
```
match.shown
  - session_id
  - match_score: 0.71
  - strong_count, transferable_count, addressable_count, fundamental_count
  - suggestion_count
  - render_latency_ms
```

---

### STEP 5 — First Accept (`/try/match` continued)

**What user sees on click [✓ Accept]**:

```
┌────────────────────────────────────────────────────────────┐
│  Suggestion 1 of 8                                         │
│  ✓ Accepted — your resume now reads:                       │
│                                                            │
│  ┌────────────────────────────────────────────────────┐   │
│  │ "Led cross-functional delivery of $2M operations   │   │
│  │  programme spanning Treasury, Tech and Ops."       │   │
│  └────────────────────────────────────────────────────┘   │
│                                                            │
│   [Undo] · [See full resume]                              │
└────────────────────────────────────────────────────────────┘
                       ↓ (300ms later)
┌────────────────────────────────────────────────────────────┐
│  Save your progress?                                       │
│  ────────────────────────                                  │
│  We'll keep your tailored resume and let you come back     │
│  to it later. 7 more suggestions ready.                    │
│                                                            │
│  [ Continue with email ]   [ Continue with Google ]        │
│                                                            │
│  Skip for now — finish all 8 suggestions first  →          │
└────────────────────────────────────────────────────────────┘
```

**Component details — the Accept confirmation**:
- Card transforms in place (NOT a modal popup — preserves context)
- Accepted text shown in a green-tinted block (#ECFDF5 background)
- Undo button — first 30 seconds (covers misclick anxiety)
- "See full resume" — secondary text link (not a button); rare action at this point

**Component details — the registration prompt** (300ms after accept):
- Appears as an inline panel BELOW the accepted suggestion (NOT a modal blocking the screen)
- Modal blocking is BLOCKED (the rule, not the dialog) because:
  - Interrupts momentum from the accept
  - Frames registration as a wall, not an offer
- Inline placement positions registration as "save your progress" not "pay the toll"

**Microcopy on registration prompt**:
- "Save your progress?" — frames registration as a benefit (your work is at risk if you don't)
- "We'll keep your tailored resume and let you come back to it later. 7 more suggestions ready." — quantifies what's preserved (7 more) which is itself a re-engagement hook
- "Continue with email" / "Continue with Google" — equal weight; Google is faster but email is for users who don't want SSO
- "Skip for now — finish all 8 suggestions first" — text link, NOT a hidden dismiss; lets user finish the flow without registering

**Critical rule — Skip is not punished**:
The skip path does NOT downgrade the experience. User can finish all 8 suggestions, see the preview, and only THEN hit a hard gate at "Download tailored resume" — by which point they've experienced the full value.

**Data events fired**:
```
suggestion.accepted              ← THIS is the moat-building event
  - session_id
  - suggestion_id
  - suggestion_type: reframe | strengthen | quantify | reorder | add | remove
  - jd_requirement_id
  - employer_id
  - employer_company_type
  - role_level
  - industry
  - user_segment: anonymous | fresh_grad | mid_career | pmet  (inferred)
  - latency_to_accept_ms (time from suggestion shown → accept)
  - position_in_session: 1 (first ever)

registration.prompt.shown
  - session_id
  - trigger: first_accept
  - prompt_variant: <variant>
```

---

### STEP 6 — Continued Suggestions (Skip-path users)

If user clicks "Skip for now":

```
┌────────────────────────────────────────────────────────────┐
│  Suggestion 2 of 8                                         │
│  ◐ Strengthen — addresses "data analysis and reporting"    │
│  ...                                                       │
└────────────────────────────────────────────────────────────┘
```

**Note**: Subsequent JDs (after the first) will gate at suggestion #4. But the FIRST JD is unlimited — this is the moat-priming guarantee. Every accept logged, every signal banked.

After all 8 suggestions reviewed:

```
┌────────────────────────────────────────────────────────────┐
│  All 8 suggestions reviewed.                               │
│  You accepted 5 · skipped 2 · edited 1.                    │
│                                                            │
│  Your tailored resume is ready.                            │
│                                                            │
│  [  Download your tailored resume  ]                       │
│                                                            │
│  Free download includes a watermark.                       │
│  Sign up free to download without watermark.               │
└────────────────────────────────────────────────────────────┘
```

**This is the second gate** — the watermark trick. Anonymous users CAN download (don't break the trust we built), but the watermarked PDF feels visibly second-class and the prompt to sign up is at the moment of highest perceived value (a real artifact).

---

## 3. The Five-Minute Budget — Allocation

| Stage | Target time | Cumulative | Notes |
|---|---|---|---|
| Land + read headline + click CTA | 0:30 | 0:30 | Or paste JD on landing |
| Paste / fetch JD | 0:30 | 1:00 | Most users paste a URL |
| JD analysis + "did you know" | 0:08 | 1:08 | Background — feels short |
| Upload resume | 0:30 | 1:38 | Drag-drop is fastest |
| Resume parsing | 0:10 | 1:48 | Background |
| Read first suggestion | 0:30 | 2:18 | THE READ that justifies the product |
| Click Accept | 0:02 | 2:20 | **AHA MOMENT** |
| Read registration prompt | 0:15 | 2:35 | |
| Click Continue with Google | 0:20 | 2:55 | OR skip |

**Total to first Accept: 2:20**. Below the 5-minute budget with 2:40 of buffer for hesitation, distraction, and reading time.

---

## 4. Persona-Specific Onboarding Variations

### Fresh Graduate (university pilot funnel — `/try?ref=university`)

- Landing variant: "Get your first interview, not your hundredth rejection."
- Suggested employers in JD input placeholder: GovTech, DBS, Accenture, Shopee, ByteDance (aspirational SG grad employers)
- Insights tier on Step 4: "Among graduates from your university, 62% accepted this kind of suggestion." (when corpus is mature)

### Mid-Career Switcher (`/try?ref=industry-switch`)

- Landing variant: "Translate your experience for the role you want next."
- Quick-add option above resume upload: "Paste a current job title + 3 bullets" — for users who want to test without uploading their full resume
- Tone in suggestions: peer-level, not coaching ("Here's how Operations leaders at fintechs frame this experience")

### PMET / Retrenched (`/try?ref=wsg`)

- Landing variant: "Bring your experience back to the front."
- No emoji icons in the flow (research signal: emoji feels infantilizing to this segment)
- Suggestions framed as recovery, not improvement: "This experience is valuable — let's make sure it lands." not "Your resume needs work."
- Pricing: WSG / e2i partner code surfaced at registration step ("Your training credit may cover this")

---

## 5. The Anti-Patterns (What This Onboarding Refuses to Do)

| Anti-pattern | Why we don't do it |
|---|---|
| Email signup before any value shown | First-use must be gate-free. Sign-up post-aha only. |
| Multi-step wizard ("Tell us about yourself!") | Every step before suggestion = lost user. Profile data is collected over time, not upfront. |
| AI chatbot as the entry point | Chat is a wayfinding crutch; we have a clear, structured workflow. Use chat where structure fails (it doesn't here). |
| Confetti / celebration animation on first accept | Anti-AI-slop; feels unserious for PMET segment; user's reward is the suggestion itself, not theatrics. |
| "AI is thinking…" generic spinner | Show what's actually happening (streaming checklist + did-you-know). |
| Forced tour / tutorial overlays | Onboarding IS the tour. The product teaches itself by being used. |
| "Welcome [name]!" personalization on registration | We don't have their name yet at the aha moment. Cheap personalization is anti-trust. |

---

## 6. Tracking the Funnel — Events Map

| Event | Phase | Used for |
|---|---|---|
| `session.created` | Landing | Acquisition channel attribution |
| `jd.parsed` | Step 1 | Drop-off measurement; employer demand signals |
| `resume.upload.started` | Step 2 | Where users drop off |
| `resume.parsed` | Step 3 | Parse-failure rate measurement |
| `match.shown` | Step 4 | Time-to-first-suggestion (target ≤2:00) |
| `suggestion.accepted` | Step 5 | **MOAT EVENT** — context-rich |
| `suggestion.skipped` | Step 5 | **MOAT EVENT** — negative signal is also data |
| `suggestion.edited` | Step 5 | **MOAT EVENT** — highest-value signal (user's correction is training data) |
| `registration.prompt.shown` | Step 5 | Conversion denominator |
| `registration.completed` | Step 5 | Conversion numerator |
| `resume.downloaded.guest_watermarked` | Step 6 | Second gate effectiveness |

Every event includes `session_id` so the post-registration event chain links back to the pre-registration funnel — same user, full attribution.

---

## 7. Failure-Mode Recovery (Dead-End Prevention)

Every step has at least ONE escape hatch that doesn't terminate the funnel:

| Failure | Recovery |
|---|---|
| JD URL won't load | Auto-prompt for paste-text fallback |
| Resume PDF won't parse | Auto-prompt for paste-text fallback |
| User uploads JD instead of resume | Heuristic detect + gentle reroute |
| User uploads resume in wrong language | Phase 1: English/Mandarin only; warn but proceed |
| User pastes JD that's not actually a job | "This doesn't look like a job posting — paste the JD directly?" |
| API error mid-flow | Inline retry button; never lose user's input; auto-save to session |
| Mobile user hits the upload step | Camera capture or "I'll do this on desktop later — email me a link" |

**Last-resort dead-end**: NEVER show a generic "Something went wrong" page. Always provide either retry or an email-me-when-fixed capture form.

---

## 8. Data-Moat Notes Specific to Onboarding

The onboarding flow is the **highest signal-density period** for new users:
- Their first JD is the cleanest demand signal we'll ever get from them (no familiarity bias)
- Their first Accept is the cleanest suggestion-quality signal (no UX-fatigue confound)
- Their drop-off point is a strong feature-quality flag (where does our perceived value drop below their patience?)

For this reason:
- All events fire to `suggestion_signals` and sibling tables EVEN for anonymous sessions
- `session_id` → `user_id` linkage on registration backfills the anonymous data
- Anonymous-but-non-converted users still produce useful aggregate data (employer demand, drop-off heatmap)

This is the most expensive period to lose a user AND the most expensive data per second collected. Onboarding is, structurally, the moat's primary intake valve.

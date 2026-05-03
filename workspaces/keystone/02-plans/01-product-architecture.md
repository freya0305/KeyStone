# KeyStone — Product Architecture Plan

> Phase 02 Plan — 2026-04-29
> Status: Draft for review
> Synthesizes: 28 analysis files + 8 user flows + 9 todo specs

---

## 1. Product Vision (One Paragraph)

KeyStone is an AI-powered resume optimization tool for Singapore job seekers that combines per-job tailoring with full-cycle outcome tracking. Every user interaction — accepting suggestions, logging outcomes, advancing through interview stages — feeds a proprietary dataset that makes the product smarter over time. The strategic goal is a data moat: outcome-linked suggestion effectiveness data that no competitor can replicate without years of accumulated user history.

---

## 2. Core Product Loop

```
User uploads resume + pastes job posting URL
         ↓
AI extracts JD requirements, matches against resume
         ↓
Four-level gap taxonomy (Strong / Transferable / Addressable / Fundamental)
         ↓
Line-by-line revision suggestions (specific to this JD + SG context)
         ↓
User accepts / skips / edits each suggestion
         ↓ ← THIS IS THE DATA MOAT HARVEST
User downloads tailored resume
         ↓
System asks: "Did you submit this?" → creates Application record
         ↓
User logs outcomes (callback / stage advancement / rejection)
         ↓ ← THIS IS THE OUTCOME LABEL
System correlates suggestion patterns → outcomes → improved suggestions
         ↓
Data compounds → unique SG hiring intelligence (employer fingerprints, per-suggestion-type effectiveness)
```

**The loop is the product. Every UX decision either closes the loop or loses signal.**

---

## 3. Information Architecture

### Mode Switch at the Door

| Mode | Entry | Chrome | Primary Action |
|---|---|---|---|
| Guest (unauthenticated) | `/try` | Minimal — logo + Log in only | Experience the core value once |
| Authenticated | `/app` | Left rail + top bar | Dashboard → full application management |

**Rationale**: Guest mode is strictly linear. No nav links. Only escape hatch is "Log in" (conversion event). Authenticated mode is dashboard-first with full power-user surface.

### URL Structure

```
PUBLIC
/                       Landing page (conversion)
/how-it-works            Marketing flow explainer
/pricing                Free vs Pro comparison
/privacy                PDPA + 6-type consent disclosure

GUEST FLOW (no auth, gate at suggestion #4 on subsequent JDs)
/try                    JD-first entry
/try/analyzing          Streaming progress
/try/match              Four-level match + first 3 suggestions
/try/register            Soft gate (only after first Accept)

AUTHENTICATED CORE
/app                    Dashboard (default post-auth landing)
/app/new                New application (resume + JD entry)
/app/applications       All applications list
/app/applications/:id   Single application detail
  /match               Four-level match view
  /suggestions         Suggestion review (primary screen)
  /preview             Tailored resume preview
  /export              Download tailored resume
  /outcome             Stage tracking
/app/resumes           Resume library
/app/insights          Personal analytics
/app/settings          Profile, consent, billing, data

B2B (Phase 2)
/institution            Institution dashboard
/institution/students   Student roster
/institution/insights  Aggregate analytics
```

---

## 4. Data Model (Core Entities)

### suggestion_signals
The primary moat table. Every suggestion interaction is a row.
```
suggestion_id, user_id, application_id, suggestion_set_id
action: accept | skip | edit
original_text, suggested_text, user_text (if edited)
edit_distance (computed)
context_employer_type, context_role_level, context_industry
context_ns_related: boolean
suggestion_type: Reframe | Strengthen | Quantify | Reorder | Add | Remove
created_at
training_consent: boolean (from consent toggle 2)
```

### applications
```
id, user_id, suggestion_set_id (nullable — manual applications have null)
employer, role, source: MCF | LinkedIn | JobStreet | Direct | Referral
applied_date, status: draft | active | auto_closed_no_response | closed
stages: [ { type, date, notes } ]
final_outcome: callback | interview | offer | rejection | no_response
created_at, updated_at
```

### resumes
```
id, user_id
content_hash (dedup)
parsed_json (structured)
sg_flags: { has_nric, has_photo, ns_present }
s3_key
```

### employer_fingerprints (derived, not user-visible table)
Aggregated from application outcomes + suggestion patterns:
```
employer, employer_type: GLC | MNC | Startup | Government | SME
cohort_outcome_stats: { application_count, callback_rate, stage_dropoff }
common_fundamental_gaps: []
suggestion_type_effectiveness: { type: accept_rate }
```

---

## 5. Feature Phases

### Phase 1 — MVP (Months 1–2)
**Goal**: Launch, validate core loop, prime the data moat

| Feature | Priority | Notes |
|---|---|---|
| Resume upload + NRIC masking | P0 | Three-stage mask: upload → re-scan → AI input |
| JD URL parse (MCF, JobStreet, generic) | P0 | URL parse + free-text fallback |
| Four-level match assessment | P0 | Strong/Transferable/Addressable/Fundamental |
| Line-by-line suggestions | P0 | 6 types, SG context, rationale per suggestion |
| Suggestion review flow (Accept/Skip/Edit) | P0 | Keyboard shortcuts, equal visual weight |
| Tailored resume preview (Original/Diff/Tailored) | P0 | Three-view toggle |
| Resume export (PDF/DOCX) | P0 | Watermark for guests |
| Application creation (download-triggered + manual) | P0 | suggestion_set_id linkage is critical |
| Outcome tracking (stages + batch update) | P0 | Pull-based, not push email |
| Six-type PDPA consent | P0 | All toggles, plain-language explanations |
| Guest flow (URL-first, one free JD) | P0 | Gate at suggestion #4 on 2nd JD |
| Free/Pro tier (3 free JDs, then gate) | P0 | Watermark export for free |

### Phase 2 — Interview Prep (Months 3–6)
**Goal**: Extend LTV, close the learning loop through interview stage data

| Feature | Priority | Notes |
|---|---|---|
| JD-specific question generation | P0 | From the JD already in the system |
| Story input + STAR structuring | P0 | Coach, not generator |
| Practice answer evaluation | P0 | Text-based, Haiku for cost control |
| Callback-triggered interview prep entry | P0 | High-motivation moment |
| Story bank (persistent across applications) | P1 | Reuse across JDs |

### Phase 3 — Data Moat Exploitation (Months 6–12)
**Goal**: Surface moat data as product features, build B2B pitch

| Feature | Priority | Notes |
|---|---|---|
| "Where to focus" insights | P0 | Suggestion type → outcome correlation |
| Employer fingerprint previews | P1 | In suggestion rationale, cite corpus data |
| B2B aggregate dashboard | P0 | Cohort-level outcome stats |
| University SSO | P0 | For B2B pilots |

---

## 6. AI Architecture

### Model Routing (Cost Control)
```
Haiku:  JD parsing, resume extraction, match classification
Sonnet:  Gap analysis, suggestion generation, rationale writing
Haiku:  Suggestion evaluation (practice answers), edit distance computation
```

### Cost Ceiling
- Hard cap: SGD 5/user/month
- Degrade to cached results when exceeded (not error)
- Token monitoring from Day 1 (structlog + Redis counter per user/month)

### Prompt Architecture
- System prompt carries SG context (GLC conventions, NS framing, MNC vs government norms)
- Suggestion rationale: 1 sentence, max 25 words, always cites JD requirement OR company type
- Anti-sycophancy rules enforced at prompt level
- No suggestion generated when Strong match — don't manufacture improvements

### Context Management
- JD context window: max 8K tokens (prune from bottom if exceeded)
- Resume: structured JSON from parser, not raw text
- NRIC: never in context. Masked as `S****1234A` before storage

---

## 7. Data Moat Harvest Surface

Every interaction designed to collect signal with minimum friction:

### Explicit Signals (button clicks)
| Signal | Trigger | Value |
|---|---|---|
| Accept / Skip / Edit | Suggestion card buttons | Per-type effectiveness, edit distance |
| Stage added | Got-a-response in batch update | Funnel data |
| Rejection logged with stage | Rejection form | Stage-specific failure rates |
| Offer received + success factors | Offer celebration flow | The labeled outcome |
| Application created from download | Post-download modal | suggestion_set_id linkage |

### Implicit Signals (behavior)
| Signal | Where captured | Value |
|---|---|---|
| Time to decide (latency) | Per suggestion | Confidence calibration |
| Order of suggestion consumption | Navigation | Engagement pattern |
| Re-visits to accepted suggestions | Suggestion card state | Doubt signal |
| Edit distance on edits | Edit save | Direction of correction |
| Section dwell on resume preview | Preview page | Verification interest |
| Download → outcome lag | Application stage | Did they actually apply? |
| Batch update session duration | Session complete | UX health metric |

### Pull-Based Outcome Collection (not push email)
1. **Download-triggered capture** — at resume export, one-click application record
2. **Batch quick-update** — card swipe interface, 30 apps in <3 min
3. **Pre-prep interstitial** — before interview prep, surface pending applications
4. **Single weekly digest email** (max 1/week, only if no login that week)
5. **30-day auto-close** → toast at next login for correction

---

## 8. Design System Summary

### Brand
- **Primary**: Teal-blue `#1E7A8C` (not navy/indigo/purple)
- **Neutral**: Warm stone scale (not cool gray)
- **Match colors**: Strong `#1F8F5F` / Transferable `#C68A1A` / Addressable `#D97338` / Fundamental `#8B4A8B` (plum, NOT red)
- **Destructive**: `#B43D3D` — reserved for system errors only

### Typography
- **UI + Body**: Inter Variable
- **Display (marketing only)**: Fraunces
- **Technical surfaces**: JetBrains Mono
- **Body**: 15px / 1.6 line-height (not 16px — SaaS productivity standard)

### Motion
- `instant`: 80ms (hover, focus)
- `fast`: 160ms (toast, suggestion collapse)
- `base`: 240ms (modal, tab switch)
- `slow`: 360ms (chart enter, page transition)
- Never: >360ms

### Voice
"Senior SG colleague who tells you the truth quickly."
- Specific: cites the JD, the company type
- Direct: no softeners or hedges
- Calm: no excitement performance
- SG-aware: real SG context in rationale

---

## 9. Open Questions

1. **Interview prep entry**: Trigger from callback (high motivation) or always-visible dashboard section? Recommendation: callback-triggered primary, dashboard fallback.
2. **B2B chrome**: Separate `/institution` app or skinned `/app`? Recommendation: skinned `/app` for speed to ship.
3. **Voice input for interview prep**: Phase 2 or Phase 3? Recommendation: Phase 2 only if text-first shows drop-off in user research.
4. **Per-user monthly cost display**: Show in dashboard or admin-only? Recommendation: show in dashboard for transparency ("You've used SGD 1.40 of your SGD 5 monthly AI budget").

---

## 10. What This Plan Does NOT Cover

- Backend framework decision (FastAPI vs Kailash Nexus) — deferred to M0.1
- Database schema details — deferred to M0.2
- CI/CD pipeline specifics — deferred to M0.4
- Frontend component library implementation — deferred to M7
- API endpoint design — deferred to M1–M6 backend todos

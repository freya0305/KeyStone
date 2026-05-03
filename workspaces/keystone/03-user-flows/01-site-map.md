# KeyStone — Site Map & Information Architecture

**Status**: Design specification — MVP v1.0
**Date**: 2026-04-29
**Owner**: UX
**Related**: `02-onboarding-activation.md`, `03-core-workflow-screens.md`, `04-ai-interaction-patterns.md`, `01-analysis/24-ux-core-analysis.md`

---

## 1. Architectural Principle

KeyStone has TWO competing IA pressures:

1. **Funnel pressure** — first-use must be linear, gate-free, single-path. Branching kills activation.
2. **Power-user pressure** — returning users (who file 40–120 applications) need a multi-application dashboard, not the funnel.

The IA reconciles these with a **mode switch at the door**:
- **Guest mode** (no auth) — strictly linear funnel: Landing → JD → Resume → Suggestions → (gate)
- **Authenticated mode** — dashboard-first; the funnel becomes a sub-flow inside "New Application"

This is NOT two products. The same suggestion screen renders in both modes. The chrome around it differs.

---

## 2. Top-Level Site Map

```
PUBLIC (no auth required)
├── /                              Landing page
├── /how-it-works                  Marketing — flow explainer
├── /pricing                       Free vs Pro comparison
├── /universities                  B2B landing (career office decision-maker)
├── /privacy                       PDPA + 6-type consent disclosure
├── /terms
├── /about
└── /trust                         Data handling, AI training opt-out, NRIC masking explainer

GUEST FLOW (no auth, gated at suggestion #4 on subsequent JDs)
├── /try                           First-use entry (JD-first input)
├── /try/analyzing                 Streaming progress (10–15s)
├── /try/match                     Four-level match assessment + first 3 suggestions
└── /try/register                  Soft gate (only after first Accept)

AUTHENTICATED CORE
├── /app                           Dashboard (default landing post-auth)
├── /app/new                       New application (resume + JD entry)
├── /app/applications              All applications list (filterable)
├── /app/applications/:id          Single application detail
│   ├── /match                     Four-level match view
│   ├── /suggestions               Suggestion review (primary screen)
│   ├── /preview                   Tailored resume preview
│   ├── /export                    Download tailored resume (PDF/DOCX)
│   └── /outcome                   Stage tracking (Applied → Response → ...)
├── /app/resumes                   Resume library (master + tailored copies)
├── /app/resumes/:id               Resume editor (raw view, rare use)
├── /app/insights                  Personal analytics — response rate, per-stage pass rate
└── /app/settings
    ├── /profile                   Name, locale (SG default), career stage
    ├── /consent                   6-type granular consent toggles (PDPA)
    ├── /billing                   Stripe — Pro subscription, invoices
    ├── /data                      Export all data, delete account, AI training opt-out
    └── /notifications             Email digest cadence (default weekly if inactive)

B2B (Phase 2 — university career office)
├── /institution                   Institution dashboard
├── /institution/students          Student roster
├── /institution/insights          Aggregate analytics (callback rates by major)
└── /institution/settings          SSO, branding, contract limits
```

---

## 3. Navigation Models

### 3.1 Guest mode chrome (intentionally minimal)

```
┌──────────────────────────────────────────────────────────────────┐
│  [KeyStone logo]                                    [Log in →]   │  ← Top bar, 56px tall
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│                       [content area]                             │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

**Rules**:
- No nav links in guest mode. Only "Log in" (right) and the logo (which goes home, but with a confirm dialog if they're mid-flow).
- No footer until landing page or post-flow.
- Removing nav forces linear flow; the only escape hatch is "Log in" (intentional — that's a conversion event).

### 3.2 Authenticated chrome (left rail + top bar)

```
┌─────────────┬────────────────────────────────────────────────────┐
│ KeyStone    │  [Breadcrumb: Applications / DBS / Suggestions]   │
│             │                                       [👤 user ▾]  │
│ ◉ Dashboard │ ───────────────────────────────────────────────── │
│   New       │                                                    │
│   Apps (37) │                                                    │
│   Resumes   │           [content area]                           │
│   Insights  │                                                    │
│             │                                                    │
│ ─────────   │                                                    │
│   Settings  │                                                    │
│   Help      │                                                    │
│             │                                                    │
│ Free tier   │                                                    │
│ [Upgrade]   │                                                    │
└─────────────┴────────────────────────────────────────────────────┘
```

**Rules**:
- Left rail: 240px wide, fixed. Collapses to 64px icons on screens <1280px.
- "Apps (37)" badge — count of all applications, gives the user a sense of scale (and surfaces logging gaps).
- "Free tier / Upgrade" CTA pinned to bottom of rail. Always visible. Never modal-spammed.
- Breadcrumb is the secondary navigation surface — single-source-of-truth for "where am I."
- User menu (top right): Profile, Billing, Consent, Sign out.

### 3.3 Mobile chrome (≤768px width)

```
┌────────────────────────────────────────┐
│  ☰   KeyStone               [👤]       │  ← 48px tall
├────────────────────────────────────────┤
│                                        │
│           [content]                    │
│                                        │
│                                        │
├────────────────────────────────────────┤
│  [Home]  [+ New]  [Apps]  [More]      │  ← Bottom tab bar, 56px
└────────────────────────────────────────┘
```

- Bottom tab bar replaces left rail on mobile.
- "+ New" is the center-emphasized tab — primary action everywhere.
- Hamburger reveals Settings, Insights, Help, Upgrade.

---

## 4. Coexistence — Four-Level Match + Suggestions on Same Screen

This is the highest-density screen. The match assessment AND the suggestion list must live together because:
- The match is the diagnosis ("which JD requirements you're weak on")
- The suggestions are the prescription ("here's how to fix the weak ones")
- Splitting them across screens loses the cause-effect link, which is the product's pedagogical value.

**Resolution**: A two-pane layout on desktop, accordion on mobile.

```
DESKTOP (≥1280px)
┌──────────────────────────────────────────────────────────────────────┐
│ Match against: Operations Manager — DBS Bank                         │
│ 71% strong match · 8 suggestions to improve                          │
├────────────────────────────────┬─────────────────────────────────────┤
│ MATCH BREAKDOWN (left, 360px)  │ SUGGESTIONS (right, fluid)          │
│                                │                                     │
│ ● Strong (5)        ▾          │ Suggestion 1 of 8                   │
│   ✓ Stakeholder mgmt           │ ┌─────────────────────────────────┐ │
│   ✓ Process improvement        │ │ Original:                       │ │
│   ✓ Cross-team coordination    │ │ "Managed projects across teams" │ │
│   ✓ Data analysis              │ │                                 │ │
│   ✓ Vendor management          │ │ Suggested:                      │ │
│                                │ │ "Led cross-functional delivery  │ │
│ ◐ Transferable (4)  ▾          │ │  of $2M operations programme    │ │
│   → Risk frameworks            │ │  spanning Treasury, Tech & Ops" │ │
│   → Regulatory exposure        │ │                                 │ │
│   → Banking domain             │ │ Because: DBS Operations roles   │ │
│   → SAP exposure               │ │ are programme-led, not project- │ │
│                                │ │ led. "Cross-functional delivery"│ │
│ ◑ Addressable (3)   ▾          │ │ matches the JD's "drive cross-  │ │
│   ⚡ Agile certifications      │ │ team initiatives" requirement.  │ │
│   ⚡ Stakeholder seniority     │ │                                 │ │
│   ⚡ Quantified outcomes       │ │ [✓ Accept]  [✗ Skip]  [✎ Edit]  │ │
│                                │ └─────────────────────────────────┘ │
│ ● Fundamental (2)   ▾          │                                     │
│   ⚠ 7+ years banking exp       │ [← Prev]   1 / 8   [Next →]         │
│   ⚠ MAS regulatory licensing   │                                     │
└────────────────────────────────┴─────────────────────────────────────┘
```

**Rules**:
- Left pane is reference; right pane is action.
- Clicking a left-pane requirement filters the right pane to suggestions tied to that requirement (data linkage made visible).
- Fundamental gaps are accordion-collapsed by default — they're informational, not actionable, and showing them open is demoralizing.
- The "Suggestion 1 of 8" position indicator is critical — users need to know how much work remains.

```
MOBILE (≤768px) — accordion stack
┌────────────────────────────────────┐
│ DBS — Operations Manager           │
│ 71% match · 8 suggestions          │
├────────────────────────────────────┤
│ ● Strong (5)              ▾        │  ← Tap to expand
├────────────────────────────────────┤
│ ◐ Transferable (4)        ▾        │
├────────────────────────────────────┤
│ ◑ Addressable (3)         ▾        │
├────────────────────────────────────┤
│ ● Fundamental (2)         ▾        │
├────────────────────────────────────┤
│ ─────── 8 SUGGESTIONS ──────       │
│                                    │
│ [Suggestion card — full width]     │
│                                    │
│ [✓]  [✗]  [✎]                      │
│                                    │
│        1 / 8                       │
└────────────────────────────────────┘
```

---

## 5. Always-Visible Elements (Authenticated Mode)

These appear on every authenticated screen:

| Element | Location | Purpose |
|---|---|---|
| Logo | Top-left of left rail | Home (dashboard) link |
| Active app indicator | Breadcrumb top | Show which application is in focus |
| User menu | Top-right | Account, billing, consent, sign out |
| Upgrade CTA | Bottom of left rail | Pinned conversion surface (free users only) |
| Help button | Bottom of left rail | Opens contextual help drawer (right side) |

**Removed from chrome on purpose**:
- Notifications bell — KeyStone is intentionally email-first; no in-app inbox to maintain
- Search — applications list is filterable, no global search at MVP
- Settings gear — moved to user menu; settings is rare-touch

---

## 6. Navigation State — What Persists, What Resets

| State | Persistence | Why |
|---|---|---|
| Last viewed application | Session | Returning user resumes where they left off |
| Filter on /applications | URL query param | Shareable, browser-back-friendly |
| Suggestion accept/skip/edit | DB (immediate write) | Data moat — never lost |
| Resume edits in progress | Session + autosave 3s | Low value to persist if user closes browser |
| Onboarding step | localStorage + DB | Recoverable across devices |

---

## 7. Routing Decisions Worth Calling Out

### Why `/try` and not `/app` for guest flow
The URL signals "you're trying it" — psychologically lower-commitment. `/app` implies you're a customer.

### Why `/app/applications/:id/suggestions` (deep nesting)
Each application is a first-class object. Suggestions belong TO an application. The URL structure mirrors the data model and makes deep-linking + browser back behaviour intuitive.

### Why no `/dashboard` at root
`/app` IS the dashboard for authenticated users. Public root `/` stays as the marketing landing page.

### Why `/app/insights` separate from `/app`
Insights page only becomes meaningful after ~5 applications logged. Promoting it to dashboard tile too early shows empty charts (anti-pattern).

---

## 8. State-Aware Routing

The `/app` dashboard renders differently based on user state:

| User state | /app shows |
|---|---|
| Brand new (0 applications) | Big "+ New Application" card, onboarding nudges, empty insights placeholder |
| 1–3 applications | Active applications list, "Track your outcomes" prompt, basic insights |
| 4–9 applications | Full dashboard: applications, response-rate widget, suggestion accept-rate widget |
| 10+ applications | Power-user mode: bulk outcome update banner, percentile widget, employer fingerprint preview |

This gradient avoids the "empty SaaS dashboard" problem (charts with no data feel broken).

---

## 9. URL Structure as Data-Moat Surface

Every authenticated URL implicitly captures a **session intent** that gets logged to `suggestion_signals` (and its sibling tables) when relevant actions fire:

| URL | Captures |
|---|---|
| `/try/match?session=abc123` | Anonymous session ID — links pre-auth events to user post-registration |
| `/app/applications/:id/suggestions?source=email` | Did user arrive from a digest email? (attribution) |
| `/app/applications/:id/outcome?stage=interview-r2` | Stage transition — feeds outcome data |

URL = both a navigation primitive AND a data event source. Both are deliberate.

---

## 10. What's Deliberately NOT in the IA

| Feature | Why excluded at MVP |
|---|---|
| In-app messaging / chat support | Opens support load before there's revenue to fund it. Email only. |
| Public profile / share resume | Out of scope — KeyStone tailors privately, doesn't host. |
| Job board / search jobs | EAA legal risk (Analysis 19). User brings the JD. |
| Cover letter generator | Phase 2. MVP is resume-only. |
| LinkedIn auto-import | OAuth scope review needed; deferred to Phase 2. |
| Recruiter-facing surface | B2B (agencies) is Phase 2. |

---

## 11. Open IA Questions (Track at /todos)

- Where does the "Interview Prep" Phase 2 module slot in? Likely `/app/applications/:id/prep` — adjacent to outcome.
- Should `/app/insights` ever surface employer fingerprints to the user? (Privacy: showing "DBS callback rate from 8 users" is identifiable in small N.) Hold until Month 12.
- B2B `/institution` chrome: full separate app or skinned `/app`? Skinned is faster to ship.

# KeyStone — UX/UI Design Plan

> Phase 02 Plan — 2026-04-29
> Question: How do we design the product so that user interactions continuously build the data moat?
> Integrates: Analysis 03, 10, 24, 25, 26, 27, 28; User Flows 01, 02, 03, 04, 05, 06, 07, 08

---

## 1. The Central UX Thesis

**Every interaction must either close the feedback loop or lose signal.**

The product is not a tool users "finish" — it's a system they return to throughout their job search. The UX design must:
1. Make users WANT to return (value)
2. Harvest signal every time they do (data)
3. Never feel extractive (trust)

If these three goals conflict, value and trust win — but they rarely need to conflict. The design thesis: **when the user gets value, they're generating signal. When they feel in control, they're generating honest signal.**

---

## 2. The Feedback Loop Map

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    KEYSTONE FEEDBACK LOOP                                  │
│                                                                             │
│  SUGGESTION INTERACTION          OUTCOME TRACKING                          │
│  ──────────────────────          ─────────────────                         │
│                                                                             │
│  User sees suggestion          User downloads resume                        │
│  User decides: accept/skip/edit   ↓                                       │
│         ↓                     "Did you submit this?" → Application created  │
│  Signal: which type,           ↓                                         │
│  edit distance,               User gets callback                          │
│  time to decide               User logs outcome                          │
│         ↓                         ↓                                         │
│  Suggestion effectiveness     Stage progression                          │
│  improves for similar         data compounds                              │
│  profiles and JDs                  ↓                                       │
│                                     Outcome-correlated                    │
│                                     suggestion patterns                   │
│                                     emerge                                │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. UX Principles

### P0: Every Click Is a Row

Every user action generates structured data. The UX must never make a decision feel like a dead end.

| Decision | Data Row | UX Treatment |
|---|---|---|
| Accept suggestion | `suggestion_signals.action=accept` | Visual affirmation, then advance |
| Skip suggestion | `suggestion_signals.action=skip` | Immediate, no friction |
| Edit suggestion | `suggestion_signals.action=edit` | Card expands, full editor |
| Still no news | `application.stage=no_news` | One tap, queue advances |
| Got a response | `application.stage=response` | Stage progression begins |
| Download resume | `application.created` | Post-download modal, not gate |

### P1: Reversibility Is the Foundation of Trust

Every AI action has an undo. Users accept higher AI agency when undo is cheap.

- Accept → Undo (30s toast, permanent in card state)
- Edit → Reset to original suggestion or user's original text
- Skip → Try again
- Outcome logged → Edit outcome
- Auto-close → "Update if needed" toast

### P2: Silence Is the Default

The product NEVER asks about every application every time. It asks once, at the right moment, with minimum friction.

- Nudge-eligible = applications aged 7/14/21 days with no activity
- Not nudge-eligible = invisible in batch update
- User sees what's *due*, not what *exists*

### P3: Friction Inversely Proportional to Frequency

| Action | Frequency | Friction |
|---|---|---|
| Still no news | Most common per batch | 1 tap |
| Got a response | Rare per batch | 2 taps + 1 select |
| Rejection | Rare per batch | 2 taps + 1 select |
| Offer received | Very rare | 60s reflection acceptable |

---

## 4. Screen Priorities

### S4: Match Assessment + Suggestions (THE PRIMARY SCREEN)
**Where users spend 80% of their time. Every design decision here compounds.**

**Layout**: Two-pane desktop (Match left 320px, Suggestions right fluid)

```
DESKTOP
┌──────────────────────────────┬─────────────────────────────────────────┐
│ MATCH (left, 320px)          │ SUGGESTIONS (right, fluid)              │
│                              │                                         │
│ ● Strong (5)            ▾   │ Filter: [All] [To do (3)] [Accepted (5)]│
│   ✓ Stakeholder mgmt          │ ───────────────────────────────────    │
│   ✓ Process improvement       │                                         │
│   ✓ Cross-team coord.        │ Suggestion 4 of 8                      │
│   ✓ Data analysis            │ ⚡ Reframe — addresses "regulatory exp" │
│   ✓ Vendor management        │                                         │
│                              │ Your resume says:                      │
│ ◐ Transferable (4)      ▾   │ ┌─────────────────────────────────┐    │
│   → Risk frameworks          │ │ "Worked with audit team on       │    │
│   → Regulatory exposure      │ │  quarterly compliance reviews."   │    │
│   → Banking domain           │ └─────────────────────────────────┘    │
│   → SAP exposure             │                                         │
│                              │ We'd say:                              │
│ ◑ Addressable (3)      ▾    │ ┌─────────────────────────────────┐    │
│   ⚡ Agile certs               │ │ "Partnered with Internal Audit   │    │
│   ⚡ Stakeholder seniority    │ │  on MAS 632-aligned compliance   │    │
│   ⚡ Quantified outcomes      │ │  reviews, covering 12 banking   │    │
│                              │ │  entities quarterly."             │    │
│ ⚠ Fundamental (2)      ▾    │ └─────────────────────────────────┘    │
│   ⚠ 7+ yrs banking exp        │                                         │
│   ⚠ MAS reg licensing         │ Why: DBS expects familiarity with    │
│                              │ MAS 632. Naming it shows domain       │
│ ──────────────               │ literacy.                             │
│ [✏ Edit resume]              │                                         │
│ [⤓ Download draft]          │ [✓ Accept]  [✎ Edit]  [✗ Skip]       │
└──────────────────────────────┴─────────────────────────────────────────┘
```

**Critical design decisions**:

1. **Equal visual weight on all three action buttons** — no nudge toward Accept. Skip is not de-emphasized. An honest Skip is GOOD data.

2. **Edit gets the full card** — not a popup. The edit IS the highest-value training signal.

3. **Fundamental gaps collapsed by default** — informational, not demoralizing. Red is reserved for system errors.

4. **Keyboard shortcuts for power users** — A/S/E for actions, arrows for navigation, numbers 1–9 to jump.

5. **Position indicator always visible** — "Suggestion 4 of 8" tells users how much work remains.

### S4 Mobile: Card Stack

- Match panel becomes a separate tab
- Swipe left = skip, swipe right = accept
- Tap-and-hold = edit
- Card takes ~80% of viewport

---

## 5. The Data Moat UX Moments

### Moment 1: Post-Download Outcome Capture (Most Important)
When user downloads tailored resume → modal appears immediately AFTER download starts:

```
+------------------------------------------------------------+
| Resume downloaded.                                         |
|                                                            |
| Submitting this to DBS Digital Banking?                    |
| [Yes — track this application]   [Just downloading]        |
|                                                            |
| Tracking lets you see your response rate and unlocks       |
| interview prep when you advance.                           |
+------------------------------------------------------------+
```

**Why this is the most important moment**:
- User is at peak value-realization
- They have intent to apply
- One click creates an Application record linked to their suggestion_set_id
- This linkage is what makes the entire outcome data interpretable

**Never block download on this question.**

### Moment 2: Batch Quick-Update (Weekly Habit Surface)
Target: 30 applications in under 3 minutes.

```
+------------------------------------------------------------------+
| Quick check-in                              ✕ Close               |
| 5 applications waiting · ~30 seconds                              |
|                                                                   |
| ┌──────────────────────────────────────────────────────────────┐  |
| │ DBS · Associate, Digital Banking                              │  |
| │ Applied 8 days ago · via LinkedIn                             │  |
| │                                                              │  |
| │ [ Still no news ]    Got a response  ·  Rejected  ·  More ▾ │  |
| └──────────────────────────────────────────────────────────────┘  |
|                                                                   |
| ▢▢▢▢▢   1 of 5                                               |
|                                                                   |
| [Mark all remaining as no news]                                  |
+------------------------------------------------------------------+
```

**Design rules**:
- One card at a time — forces decision, creates progress feeling
- "Still no news" is the default tap — 1 tap per app
- "Mark all remaining" is the escape hatch for power users
- 20 apps in ~25 seconds achievable

### Moment 3: Offer Celebration + Reflection (Richest Data Point)
After "Got an offer" is logged:

```
What helped most? (pick up to 3)
  □ Tailored resume bullets matched the JD
  □ Interview prep questions were on-target
  □ Cover letter / email pitch
  □ Personal network / referral
  □ Existing experience, not the resume tool
  □ Other: [          ]
```

**Why this matters**: The `suggestion_set_id` linkage tells us which suggestion patterns correlate with offers. This is the data VMock cannot have.

---

## 6. The Four-Level Match System

The hardest UX problem: Fundamental gaps must feel like honest information, not a verdict.

**Color system**:
| Level | Color | Hex | Default state |
|---|---|---|---|
| Strong | Green | `#1F8F5F` | Expanded |
| Transferable | Amber | `#C68A1A` | Expanded |
| Addressable | Orange | `#D97338` | Expanded |
| Fundamental | Plum | `#8B4A8B` | **Collapsed** |

**Why Fundamental is plum, NOT red**:
- Red triggers rejection emotional response
- Plum reads as a category, not an alarm
- Red is reserved for system errors (delete account, payment failed)

**Fundamental gap expansion** (only if user taps):
```
⚠ Fundamental gaps

These are requirements your resume can't address with
tailoring alone. Knowing them helps you decide whether
this role is the right fit right now.

⚠ 7+ years banking experience required
  The JD asks for 7+ years; your resume shows 3 years.
  This is something time addresses, not phrasing.
```

**Voice rules for Fundamental**:
- No exclamation marks
- No "MAJOR GAP" headers
- Each gap has a brief explanation that respects the user
- Closing line: "These gaps don't disqualify you."

---

## 7. Loading States — The Trust Test

The analysis wait (10–30 seconds) is where most users drop off. Design:

**Under 10s**: Skeleton cards with shimmer. No spinner. Users perceive content "loading in."

**10–30s**: Progressive disclosure:
```
✓ Parsed JD
✓ Identified GLC employer type
⏳ Generating suggestions...

Did you know?
DBS hires 60% of its Operations roles internally.
External candidates win on demonstrated banking
domain knowledge — not generic project management language.
```

The "Did you know" slot pulls from the SG corpus — demonstrates "we know things ChatGPT doesn't" before suggestions appear.

**Never**: Percentage progress bars (fake), "AI is thinking..." spinner, "Don't refresh!" warnings.

---

## 8. Conversion UX (Gate Placement)

### Gate Logic
- 1st JD: all suggestions free, no gate
- 2nd JD onwards (free tier): first 3 free, gate at 4

### The Gate (appears INSIDE the suggestion card flow)
```
Suggestion 4 of 8
🔒 Free tier shows the first 3 suggestions per job.
   Upgrade to see the next 5 — and unlimited jobs going forward.

   [ Upgrade — SGD 19/mo ]   [ Maybe later ]
```

**Rules**:
- Gate appears INSIDE the suggestion flow, not as a modal
- "Maybe later" is a real option — going back to accepted suggestions still works
- Locked suggestions 4–8 remain visible in the navigation rail (greyed, with lock icon)
- Never show the gate before the first JD (moat-priming guarantee)

### Pricing Page Tone
- Two columns: Free vs Pro, equal visual weight
- "Try the product" / "Apply seriously" — names the use case, not the feature count
- No countdown timers, no "limited offer" — SG buyers read those as scammy

---

## 9. Empty States (Where Trust Is Won or Lost)

Every empty state has:
1. Forward-looking copy ("Your X will appear here once you Y")
2. One concrete next action
3. Single-color line illustration (no mascot, no emoji, no 3D render)

**Dashboard new user**:
```
You haven't tailored a resume yet.
Start with a job you're actually applying to —
the suggestions get more specific the more
context we have.

[ Paste a job URL or full job description ]
[   Analyse this job  →   ]
```

**Insights (not enough data)**:
```
Your insights show up after a few applications.
When you start hearing back, this page tells you:
  · Your response rate vs the SG market
  · Which suggestions actually correlate with callbacks
  · Which employers respond to your profile

[ Update an outcome → ]
```

---

## 10. Trust-Building Patterns (贯穿 every screen)

### The NRIC Moment
When resume containing NRIC is uploaded:
```
✓ Detected and masked: 1 NRIC (last 4 digits hidden)
```
Not: "WARNING: NRIC detected!" Not: silent.

### The "No AI Training Without Consent" Claim
Surfaced in three places, and it must be TRUE:
1. Resume upload: "Your resume is never used to train AI without consent."
2. Settings → Consent → Toggle 2 ("AI improvement")
3. Privacy policy (legal form)

Architecture must enforce: if Toggle 2 is off, `training_consent=false` on every signal row, excluded from any fine-tune corpus.

### Citation Hovers on Data Claims
When rationale cites employer data:
```
DBS hires 60% of its Operations roles internally.[ⓘ]
```
Hover → tooltip:
```
Source: KeyStone employer fingerprint corpus
DBS Bank, 2024 Q1–Q3 hiring data
Aggregated from 47 Operations role outcomes
Updated: Jan 2026
```

---

## 11. Voice and Tone Map

| Screen | Tone |
|---|---|
| Landing page | Confident, specific, clear |
| Onboarding | Calm, instructional |
| Suggestion cards | Editorial, peer-level |
| Match — Strong | Matter-of-fact |
| Match — Transferable | Encouraging |
| Match — Addressable | Constructive |
| Match — Fundamental | Honest, calm |
| Outcome tracking | Curious, supportive |
| Errors | Practical, no theatrics |

### Forbidden Words (anywhere in product)
- "AI-powered" / "Smart" / "Magical" / "Cutting-edge" — AI-slop fingerprints
- "Optimized" — jobscan-coded jargon
- "Synergy" / "leverage" — corporate cliché
- "Simply" / "Just" — diminishes user effort

---

## 12. Keyboard Shortcuts (Power-User Surface)

| Key | Action | Screen |
|---|---|---|
| `A` | Accept suggestion | S4 |
| `S` | Skip suggestion | S4 |
| `E` | Edit suggestion | S4 |
| `↓` / `J` | Next suggestion | S4 |
| `↑` / `K` | Previous suggestion | S4 |
| `1`–`9` | Jump to suggestion N | S4 |
| `⌘+E` | Export resume | S4, S5 |
| `Space` | "Still no news" (batch update) | Batch update |
| `R` | "Got a response" | Batch update |
| `X` | Rejected | Batch update |
| `⌘+K` | Quick switch application | All |
| `?` | Show shortcuts | All |

---

## 13. Accessibility Floor

- All interactive elements ≥44×44px tap target (mobile)
- All color-coded states paired with shape + text label (not color alone)
- WCAG AA: 4.5:1 minimum for body text
- Focus rings never removed for aesthetics
- Tab order matches visual order
- All actions reachable via keyboard
- Live regions for AI streaming (announces "Suggestion 4 ready" to screen readers)

---

## 14. Implementation Priority for UX

| Phase | UX Deliverable | Lines |
|---|---|---|
| M7 | Tailwind config (all tokens), globals.css, shadcn/ui install | ~400 |
| M7 | Suggestion card component (all states: default, accepted, skipped, editing, loading) | ~600 |
| M7 | Match chip component (all 4 levels) | ~150 |
| M7 | Left nav + authenticated chrome | ~300 |
| M8 | Dashboard (3 state variants: 0 apps, 1–9, 10+) | ~500 |
| M8 | Suggestion review screen S4 (desktop + mobile) | ~800 |
| M8 | Resume preview S5 (3-view toggle: tailored/original/diff) | ~400 |
| M9 | Batch quick-update flow | ~600 |
| M9 | Outcome tracking flow S7 | ~500 |
| M9 | Insights dashboard S9 | ~400 |

---

## 15. What This Plan Addresses

✅ Every button click generates a structured data row
✅ Reversibility on every AI action
✅ Pull-based outcome collection (not push email)
✅ Gate placement protects moat-priming (first JD always free)
✅ Fundamental gaps feel informational, not punitive
✅ Loading states build trust, not anxiety
✅ Empty states are forward-looking, not apologetic
✅ Trust signals (NRIC mask, consent, citations) on every relevant screen
✅ Keyboard shortcuts for power users
✅ Accessibility floor on every screen

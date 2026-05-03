# KeyStone — AI Interaction Patterns

**Status**: Design specification — MVP v1.0
**Date**: 2026-04-29
**Scope**: How AI manifests across every surface — language, framing, trust, feedback collection

---

## 1. Foundational Stance: AI as Editor, User as Author

The single most important framing decision in KeyStone:

> **The user wrote their resume. KeyStone is the editor proposing changes. The user decides.**

Every AI-touching surface MUST reinforce this hierarchy. Inversion (AI generates, user passively reviews) destroys both trust AND data quality:

- **Trust**: Users tell themselves "I didn't really get this job — the AI did" — kills retention and word-of-mouth
- **Data quality**: Passive accepts (mindless approval) are noise in `suggestion_signals`. Engaged accepts are signal.

This stance shows up in:
- Copy — "We'd say" / "Why this might land better" (suggesting), not "I generated" / "AI rewrote" (asserting)
- Visual hierarchy — original text and suggested text get equal visual weight
- Accept/Skip/Edit equal prominence — Skip is not de-emphasized
- Edit is celebrated as a core action — "you correct us" is a virtue, not a failure

---

## 2. AI Identity Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Name for the AI | "KeyStone" (the product) — not a persona name | Avoids anthropomorphism; we're a tool, not a colleague |
| Avatar | None on suggestion cards | No bot avatars (AI-slop fingerprint); cards are content, not chats |
| Voice | "We" plural | Conveys editorial team, not single AI; "we" is conversational without claiming singular intelligence |
| Personality | Calm, knowledgeable, specific. NOT enthusiastic. | Matches a senior colleague reviewing your draft, not a cheerleader |
| First-person AI claims | BLOCKED | Never "I think you should…" — we say "We'd say" or "We'd recommend" |
| Apologies / verbal padding | BLOCKED | "Sorry, I can't…" is anthropomorphic theater. Show a structured error. |

**Sycophancy guard**: Suggestion engine MUST NOT generate suggestions when there's nothing to improve. If the resume already aligns well with a JD requirement, that section is marked Strong (green) — no suggestion is generated, no false flag is raised. We DO NOT manufacture suggestions to pad the count.

---

## 3. The Suggestion Anatomy — Detailed Breakdown

```
┌─────────────────────────────────────────────────────────────────────┐
│  Suggestion 4 of 8                                  ← position      │
│  ⚡ Reframe — addresses "regulatory exposure"        ← type + tie    │
│                                                                     │
│  Your resume says:                                  ← attribution   │
│  ┌─────────────────────────────────────────────┐                    │
│  │ "Worked with audit team on quarterly        │  ← user's text     │
│  │  compliance reviews."                       │     (theirs)       │
│  └─────────────────────────────────────────────┘                    │
│                                                                     │
│  We'd say:                                          ← proposal     │
│  ┌─────────────────────────────────────────────┐                    │
│  │ "Partnered with Internal Audit on MAS       │  ← AI's proposal   │
│  │  632-aligned compliance reviews, covering   │     (ours)         │
│  │  12 banking entities quarterly."            │                    │
│  └─────────────────────────────────────────────┘                    │
│                                                                     │
│  Why:                                               ← rationale    │
│  DBS expects familiarity with MAS regulatory frameworks.            │
│  Naming "MAS 632" shows domain literacy that "compliance            │
│  reviews" alone doesn't convey.                                     │
│                                                                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                          │
│  │ ✓ Accept │  │ ✗ Skip   │  │ ✎ Edit   │                          │
│  └──────────┘  └──────────┘  └──────────┘                          │
│   [A]            [S]            [E]                  ← shortcuts   │
└─────────────────────────────────────────────────────────────────────┘
```

### 3.1 The Type+Tie chip (header)

Six types, each tied back to a specific JD requirement:

| Type | Icon | Example chip | Means |
|---|---|---|---|
| Reframe | ⚡ | `⚡ Reframe — addresses "regulatory exposure"` | Same content, different framing |
| Strengthen | ↑ | `↑ Strengthen — addresses "stakeholder management"` | Make claim more credible/specific |
| Quantify | # | `# Quantify — addresses "operational impact"` | Add numbers/scale |
| Reorder | ↕ | `↕ Reorder — addresses "leadership emphasis"` | Move within resume |
| Add | + | `+ Add — addresses "agile methodology"` | New content from existing experience |
| Remove | − | `− Remove — addresses "concision"` | Cut/trim |

**Why this matters**: The chip names the *kind of help* the suggestion provides. This:
- Makes it cognitively easier for users to evaluate (each type implies different acceptance criteria)
- Generates structured feedback data (per-type acceptance rates → which types of suggestion users find valuable)
- Lets the user filter ("Show me only Quantify suggestions") in power-user mode

### 3.2 The two text blocks — visual parity

```
Your resume says:               We'd say:
┌─────────────────────┐        ┌─────────────────────┐
│ Original text...    │        │ Suggested text...   │
└─────────────────────┘        └─────────────────────┘
```

Both blocks:
- Same width
- Same font / size / weight
- Same border style
- Background slightly differentiates: original = #F9FAFB, suggested = #F0FDFA (mild teal tint)

**The visual parity rule**: Never make the suggested text "louder" than the original. If suggested looks more authoritative visually, users feel railroaded. If suggested looks tentative (italic, small, indented), users dismiss it. **Equal weight = user adjudicates.**

### 3.3 The "Why:" rationale

Hard rules:
- Maximum 2–3 sentences. Anything longer goes behind a "Show more" disclosure.
- Always references either:
  - The specific JD requirement being addressed, OR
  - The employer / company-type context (GLC, MNC, etc.), OR
  - Both (preferred)
- Never references "AI" or "model" or "data"
- Never apologetic ("This might be wrong, but…")
- Never overclaiming ("This will get you the job")

**Good rationale examples**:
- "DBS expects familiarity with MAS regulatory frameworks. Naming 'MAS 632' shows domain literacy that 'compliance reviews' alone doesn't convey."
- "Operations roles at GLCs are graded on programme delivery, not project delivery. The phrasing aligns with how DBS hiring managers describe the work."
- "Singapore startup hiring managers value scrappiness signals. 'Built from scratch' lands stronger than 'designed and implemented.'"

**Bad rationale examples (BLOCKED)**:
- "I think this would be better." (subjective, no anchor)
- "Our AI suggests this rewrite." (anthropomorphic, brand-confused)
- "This is more aligned with industry standards." (vague, generic)
- "Recruiters love specificity." (cliché, no anchor)

### 3.4 Action buttons — equal weight, equal data

Three buttons, all the same size, shape, and visual prominence:

```
┌──────────┐  ┌──────────┐  ┌──────────┐
│ ✓ Accept │  │ ✗ Skip   │  │ ✎ Edit   │
└──────────┘  └──────────┘  └──────────┘
   [A]            [S]            [E]
```

- Accept: solid teal background, white text
- Skip: outlined teal border, teal text
- Edit: outlined teal border, teal text

**Why Skip is not de-emphasized**:
- A Skip is GOOD data — it tells us the suggestion was wrong for this user/context
- De-emphasizing Skip pressures users to Accept, polluting accept signal with reluctant accepts
- Power users WILL skip 30–50% of suggestions; that's healthy, not failure

**Why Edit is not de-emphasized**:
- An Edit is the HIGHEST-VALUE training signal — user is correcting our model
- Edit-heavy users are the most engaged users (high LTV, high data value)
- Hiding Edit behind a hover or menu would lose the signal

---

## 4. The Four-Level Match — Communicating Without Alarming

Color discipline for the four levels:

| Level | Color | Hex | Used where | Tone of accompanying language |
|---|---|---|---|---|
| Strong | Green | #059669 | Match panel, ✓ icons | Matter-of-fact: "You have this" |
| Transferable | Amber | #D97706 | Match panel | Encouraging: "Adjacent — let's make it visible" |
| Addressable | Orange | #EA580C | Match panel | Constructive: "Reframe to claim this legitimately" |
| Fundamental | Red | #DC2626 | Match panel ONLY (collapsed by default) | Honest, calm: "This isn't fixable with resume work" |

### 4.1 Why colors are confined to the Match panel

- The suggestion cards do NOT use red/amber/orange. Cards are neutral teal.
- Reason: A red-bordered card feels punitive. Color escalation triggers anxiety in PMET segment particularly.
- The match panel is reference; cards are action. Different contexts, different visual treatment.

### 4.2 Fundamental gaps — the hardest UX problem

The Fundamental section says, essentially: "You don't have what they want."

For PMETs and fresh grads especially, this is emotionally loaded. Bad UX here:
- "MAJOR GAP" header (alarming)
- Red exclamation icons (punishing)
- Big banner at top of screen (demoralizing)

**Our approach**:

```
⚠ Fundamental (2)                                        ▾  ← collapsed
   ⚠ 7+ years banking experience required
   ⚠ MAS regulatory licensing (CMSL or equivalent)
```

When expanded:

```
⚠ Fundamental gaps                                       ▴

   These are requirements your resume can't address with
   tailoring alone. Knowing them helps you decide whether
   this role is the right fit right now.

   ⚠ 7+ years banking experience required
     The JD asks for 7+ years; your resume shows 3 years.
     This is something time addresses, not phrasing.

   ⚠ MAS regulatory licensing (CMSL or equivalent)
     This is a regulated certification. If you're working
     toward it or recently passed, mention that — otherwise
     it's worth knowing this is the bar.

   ─────────
   These gaps don't disqualify you, but be ready to address
   them in the cover letter or interview.
```

**Design principles applied**:
- Honest naming (don't soften "gaps" — adults can handle the word)
- Calm tone (no exclamation marks)
- Each gap has a brief explanation that respects the user
- Concluding line reframes — "don't disqualify you" — empowers rather than discourages
- Never auto-expanded — user opts in to see this

---

## 5. AI Process Visibility (Streaming State)

During the 8-15 second analysis windows, users see what's happening — not a generic spinner.

### Pattern: Streaming checklist with did-you-know

```
Reading the job posting…

✓ Identified employer:    DBS Bank Ltd
✓ Role level:             Senior individual contributor
✓ Industry:               Banking & Financial Services
⏳ Extracting requirements…  (12 found so far)
◯ Detecting company type…

────────────────────────────────────────

Did you know?
DBS hires 60% of its Operations roles internally. External
candidates win on demonstrated banking domain knowledge —
not generic project management language.
```

Why this works:
- **Visible activity**: progress is concrete, not abstract — feels short
- **Specificity per item**: "DBS Bank Ltd" not "your employer" — proves the AI is reading
- **The Did-You-Know slot**: pulls from the SG-specific corpus, demonstrates "we know things ChatGPT doesn't" before the user has even seen suggestions

### What we DO NOT show during streaming

- Generic "AI is thinking…" spinner (vague, anxiety-inducing for slow runs)
- Real-time token-level streaming of internal model output (looks like a chat, wrong frame)
- "Don't refresh the page!" warnings (paternalistic; we should handle reload gracefully)
- Cute animations, dancing dots, brain-with-gears icons (AI-slop fingerprints)

---

## 6. Trust-Building Patterns

KeyStone handles two highly sensitive things:
- The user's resume (personal, often emotionally fraught)
- The user's NRIC (legally sensitive under PDPA)

Trust-building is not a one-time disclosure — it's a continuous pattern across every screen.

### 6.1 The NRIC moment

When a resume containing NRIC is uploaded, the parsing screen says:

```
✓ Detected and masked: 1 NRIC (last 4 digits hidden)
```

NOT:
- "WARNING: NRIC detected!" (alarming)
- "We found sensitive data" (vague, makes user wonder what)
- Silent — no mention (loses the trust opportunity)

The phrasing is matter-of-fact and shows what action was taken. The user thinks: "They handled it."

**Mechanism**: NRIC is masked in the model context (we send `S****1234A` to the LLM, never the full ID). The masked token is also stored in the audit trail rather than the original — defense in depth.

### 6.2 The "no AI training without consent" claim

Surfaced in three places:
1. Resume upload screen: "Your resume is never used to train AI without consent."
2. Settings → Consent → Toggle 2 ("AI improvement" can be turned off)
3. Privacy policy: full legal-form disclosure

Critical: This is a TRUE claim, enforced by the data pipeline. If user has Toggle 2 off, their `suggestion_signals` rows are tagged `training_consent=false` and excluded from any fine-tuning corpus.

If the claim were false, every other trust signal in the product collapses. So:
- Architecture must enforce it (covered in `specs/data-architecture.md`)
- Audit log must record consent state at every signal collection event
- Internal review before any fine-tune confirms `training_consent=true` filter is applied

### 6.3 Citations and provenance

When a suggestion's "Why" rationale references a specific data source ("DBS hires 60% internally"), the rationale should be hover-citeable:

```
DBS hires 60% of its Operations roles internally.[ⓘ]
```

Hovering the [ⓘ] reveals:

```
┌──────────────────────────────────────────────────┐
│ Source: KeyStone employer fingerprint corpus     │
│ DBS Bank, 2024 Q1–Q3 hiring data                 │
│ Aggregated from 47 Operations role outcomes      │
│ Updated: Jan 2026                                │
└──────────────────────────────────────────────────┘
```

Why this pattern matters:
- Distinguishes claims grounded in data from claims that are model inference
- Reinforces "we know SG things ChatGPT doesn't" — the sources are SG-specific
- Sets expectation that suggestions are evidence-based, not vibe-based
- Trust calibration: users learn what's claimed vs what's known

For LLM-derived suggestions (no specific data source), no citation appears — implicit signal that it's general guidance rather than data-backed.

### 6.4 Reversibility everywhere

Every AI action has an undo:
- Accept → Undo accept (30-second window in toast, permanent in suggestion card state)
- Edit → Reset to original suggestion, OR reset to user's resume original
- Skip → Try again
- Outcome logged → Edit outcome
- Auto-close ("no response after 30 days") → "Update if needed" toast on next visit

**Reversibility is the foundation of trust** — users will accept higher AI agency when undo is cheap.

---

## 7. Feedback Collection — The Data-Moat Surface

Every Accept / Skip / Edit is a row in `suggestion_signals`. The UX challenge: make these interactions feel like user agency, not tracking.

### 7.1 Why the buttons must NOT feel like data collection

If the user perceives "I'm being watched":
- Acceptance pressure rises (people choose Accept to be "polite" — useless data)
- Engagement drops (cognitive overhead per click)
- Skips get under-reported (users think Skip is a failure to engage)

If the user perceives "I'm in control":
- Honest accepts and skips alike (clean signal)
- Edits flow naturally (highest-value data)
- Long-term tenure (data accumulates)

### 7.2 Specific design choices that frame buttons as agency

| Choice | Effect |
|---|---|
| Equal visual weight on all three buttons | No nudge toward Accept |
| Skip labelled "Skip" not "Reject" | Lower-stakes phrasing — invites honest no |
| Edit labelled with pencil icon (creator metaphor) | Frames edit as authorship, not correction |
| No "Are you sure?" confirmations | Treats user as a decisive adult |
| Per-suggestion granularity (no "Accept all") | Each click is intentional |
| Undo always visible | Click without dread |
| No "Why did you skip?" survey | Labour for the user; we infer from context |

### 7.3 The implicit-data harvest

Beyond the explicit Accept / Skip / Edit, the UX captures:

| Implicit signal | Where captured | Use |
|---|---|---|
| Time to decide (latency between shown and clicked) | Per suggestion | Confidence calibration: long latency = harder suggestion |
| Order of consumption (sequential vs jumping) | Suggestion navigation | Engagement quality: jumpy users = power-user pattern |
| Re-visits to accepted suggestions | Suggestion card state | Doubt signal: revisited = uncertain |
| Edit distance on edited suggestions | Edit save | Direction of correction: small edit = nearly right; large = directionally wrong |
| Section dwell time on resume preview | Preview page | What did they want to verify? |
| Download → outcome lag | Application stage | Did they actually apply? |
| Re-tailoring same JD | Application list | Quality dissatisfaction signal |

These signals are MORE valuable than explicit "rate this suggestion 1–5" feedback because they're collected without cognitive load AND they can't be gamed.

### 7.4 Explicit feedback — when we ask, and how

We DO ask explicitly in only two places:

**Place 1**: After 3rd Accept on first session — "Are these suggestions feeling specific enough?"

```
┌─────────────────────────────────────────────────────────────┐
│ Quick check — are these suggestions feeling specific to     │
│ DBS Operations Manager, or generic resume advice?           │
│                                                             │
│ [ Specific ]   [ Generic ]   [ Mixed ]   [ Skip ]           │
└─────────────────────────────────────────────────────────────┘
```

- Once per first session, single question, four-option
- "Skip" is offered explicitly (consent to not answer)
- Drives the calibration signal that distinguishes "users who recognize SG-specific intelligence" vs "users who can't tell"

**Place 2**: Outcome capture — "Did the tailoring help?"

```
After: "Got an offer" outcome logged

┌─────────────────────────────────────────────────────────────┐
│ Congrats. Last question — did the tailoring help?           │
│                                                             │
│ ○ Yes, the recruiter mentioned specifics                    │
│ ○ Maybe — hard to tell                                      │
│ ○ Probably not — they were going to hire me anyway          │
│ ○ Skip                                                      │
└─────────────────────────────────────────────────────────────┘
```

- Only at terminal positive outcomes
- Calibration data for "did our suggestions actually correlate with offers"
- Skip is the first option offered

**Anywhere else**: NO unprompted "How are we doing?" surveys. NO NPS modal. NO 5-star ratings on individual suggestions.

---

## 8. Tone for User Segments

Based on three personas, the suggestion engine adjusts copy register (NOT content) by inferred segment.

### 8.1 Inference signals (no explicit segment selector at MVP)

| Signal | Inference |
|---|---|
| Resume has "expected graduation" or graduation date < 18 months ago | Fresh graduate |
| Resume has 5–15 years experience, current role at one company | Mid-career |
| Resume has 15+ years experience OR career break detected OR PMET-coded job titles | PMET / mid-senior |

Optional: WSG/e2i referral query param flips PMET tone explicitly.

### 8.2 Tone variations across the same suggestion type

**Original line in resume**: "Managed projects across teams"

**Suggested**: "Led cross-functional delivery of $2M operations programme"

**Rationale tone — fresh graduate**:
> "DBS Operations roles look for cross-team scope. Even on student projects, naming the scale and the teams involved is the difference between 'I helped' and 'I led'."

**Rationale tone — mid-career**:
> "DBS Operations roles are programme-led, not project-led. 'Cross-functional delivery' matches how DBS hiring managers describe the work in this requirement."

**Rationale tone — PMET**:
> "Your experience IS programme-level. The phrasing in the JD ('drive cross-team initiatives') signals they're looking for someone exactly at your level. Make sure your wording lets them see it."

**Differences applied**:
- Fresh grad: educational ("the difference between…"), encouraging implicit
- Mid-career: peer-level, jargon-comfortable, just-the-facts
- PMET: empowering, validates existing experience, removes implication that they need teaching

**Critical**: The CONTENT (what to change) is identical across personas. The MOTIVATION (why) is what changes.

### 8.3 Tone across screens

| Screen | Tone |
|---|---|
| Landing page | Confident, specific, clear |
| Onboarding | Calm, instructional |
| Suggestion cards | Editorial, peer-level |
| Match panel — Strong | Matter-of-fact |
| Match panel — Transferable | Encouraging |
| Match panel — Addressable | Constructive |
| Match panel — Fundamental | Honest, calm |
| Outcome tracking | Curious, supportive |
| Insights | Analytical, non-comparative when N is small |
| Email reminders | Helpful, low-pressure |
| Errors | Apologetic without being theatrical |
| Upgrade prompts | Direct, value-first |

### 8.4 Forbidden vocabulary (anywhere in product)

| Word | Why forbidden |
|---|---|
| "AI-powered" | Generic, AI-slop fingerprint, doesn't mean anything |
| "Optimized" | Jobscan-coded, jargon |
| "Smart" | Empty (every product claims smart) |
| "Magical" | Anthropomorphic |
| "Game-changing" | Marketing cliché |
| "Cutting-edge" | Marketing cliché |
| "Effortless" | Disrespects user's actual effort |
| "Instant" | Sets expectations we can't meet (10-15s is not instant) |
| "Robot" / "bot" | Anthropomorphic + diminutive |
| "Algorithm" | Either marketing-vague or technical-flexing |
| "Synergy" / "leverage" | Corporate cliché — ironic in a resume tool |
| "Just" | Diminishes user effort ("just upload your resume") |
| "Simply" | Same as "just" |

---

## 9. Anti-Sycophancy Rules

The model is instructed (and the UX enforces) that:

1. **Never agree with user's edits if they reduce specificity.** If user edits "$2M programme" → "big programme", surface a gentle prompt: "Specifics like '$2M' or '12 entities' tend to land better — keep the change anyway?"

2. **Never compliment the resume gratuitously.** "What a great resume!" is BLOCKED. The match panel says what's strong factually; no editorial praise.

3. **If a JD requirement genuinely can't be addressed by tailoring**, classify as Fundamental and DO NOT generate a suggestion that pretends otherwise.

4. **If the model is uncertain about a suggestion**, surface that as a suggestion variant ("We're less sure about this one — the JD's phrasing is ambiguous") rather than presenting it with the same confidence as a high-certainty suggestion.

5. **Never apologize for hard truths.** "Unfortunately your experience doesn't match…" is BLOCKED. State it neutrally: "This requirement asks for 7+ years; your resume shows 3."

---

## 10. Error and Failure Patterns

When AI fails, UX makes the failure information-rich, not theatrical.

### Pattern: Partial-failure suggestion view

If the suggestion engine returns 6 of 8 suggestions before a downstream call fails:

```
6 suggestions ready · 2 still being generated
[Continue with 6]   [Wait for all 8]   [Try again]
```

- Don't block the user on incomplete generation
- Show what we have; let them choose
- Always offer retry

### Pattern: Confidence-calibrated suggestions

If the model is internally low-confidence on a suggestion:

```
Suggestion 5 of 8
⚡ Reframe — addresses "stakeholder seniority"
🤔 Lower confidence — the JD's phrasing here is ambiguous

Your resume says: ...
We'd say: ...

Why: The JD mentions "C-level engagement" but doesn't specify
internal vs external. We're proposing internal framing based
on your DBS experience, but external framing might fit better
if your prior role had board exposure.

[✓ Accept]  [✗ Skip]  [✎ Edit]
```

- The 🤔 emoji + label flags the calibration (one of the few places we use emoji — for state attribution, not decoration)
- "Why" explicitly explains the uncertainty
- User decides with full information

### Pattern: Refusal

The model can refuse to generate a suggestion (e.g., user requests "make me look like I have 10 years experience" via the manual edit interface):

```
We won't help with this kind of edit.

Resume tailoring is about making your real experience visible
to the right people. Inflating experience that isn't there
backfires at interview — and it's not what we're here for.

[Got it]
```

- Refusals are explicit, calm, principled
- Never cute ("Sorry, I can't do that, Dave")
- Never moralizing ("That would be wrong")
- Practical reasoning ("backfires at interview") respects the user's incentive structure

---

## 11. Data Disclosure Patterns

### Pattern: Pre-action disclosure

When a user-initiated action has data implications, disclosure happens BEFORE the action, not buried in TOS.

Example — when user clicks "Save outcome":

```
[Save outcome]

Saves your outcome to:
  · Your private dashboard (always)
  · Anonymous market data, with your consent (currently ON)
```

Not a full modal — a small text line that becomes visible 100ms before the button is clicked (on hover). For mobile, it's always visible above the button.

### Pattern: Post-action receipt

After major data-impacting actions, a confirmation toast names what was saved and where:

```
✓ Outcome saved.
   Your insights are updated. Anonymous version
   contributed to SG market data.   [Settings]
```

The "[Settings]" link goes to the consent toggle for that data type — easy to revoke.

### Pattern: First-time-only disclosure

The first time a user takes a particular kind of action, a slightly more verbose disclosure appears:

```
[First time logging an outcome]

Outcomes you log are paired with the suggestions you used.
Over time, this lets you see which suggestions correlate with
real callbacks — not just which suggestions sounded good.

You can opt out anytime: Settings → Consent → Outcome correlation.

[Got it — log outcome]
```

- Educational, not alarmist
- Names what data is collected and the value to the user
- Explicit opt-out link
- "Got it" frames continuation as informed, not coerced

---

## 12. Free → Pro Conversion UX (AI-aware)

The conversion moment is itself an AI interaction. Bad UX here destroys both conversion AND data trust.

### 12.1 Where the gate appears

For users on subsequent JDs (not the first):

```
Suggestion 4 of 8
🔒 Free tier shows the first 3 suggestions per job.
   Upgrade to see the next 5 — and unlimited jobs going forward.

   You've already accepted 3 suggestions this session — getting
   value from KeyStone? Unlock the rest.

   [ Upgrade — SGD 19/mo ]   [ Maybe later ]
```

- The lock icon appears IN the suggestion card flow (not a separate modal)
- The pitch references THEIR specific session (3 accepts)
- "Maybe later" is a real option — going back to the dashboard or the 3 accepted suggestions still works
- The locked suggestions 4–8 remain visible in the navigation rail (greyed, with lock icon) — preserves the sense of "this is what you're missing" without being aggressive

### 12.2 Why we don't show the gate before the first JD

Per `02-onboarding-activation.md`, the FIRST JD is unlimited. This is non-negotiable — it's the moat-priming guarantee.

The gate logic is:
- 1st JD: all suggestions free, no gate
- 2nd JD onwards (free tier): first 3 free, gate at 4

### 12.3 The pricing page

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│ Two ways to use KeyStone.                                   │
│                                                             │
│ ┌──────────────────────────┬──────────────────────────────┐ │
│ │ Free                     │ Pro             SGD 19 / mo  │ │
│ │ Try the product          │ Apply seriously              │ │
│ │ ─────                    │ ─────                        │ │
│ │ ✓ First job — unlimited  │ ✓ Unlimited jobs             │ │
│ │ ✓ 3 jobs / month         │ ✓ Unlimited suggestions      │ │
│ │ ✓ First 3 suggestions    │ ✓ Outcome dashboard          │ │
│ │   per subsequent job     │ ✓ Email reminders            │ │
│ │ ✓ Watermarked download   │ ✓ Clean download             │ │
│ │                          │ ✓ Insights dashboard         │ │
│ │                          │                              │ │
│ │ [ Use free ]             │ [ Upgrade to Pro ]           │ │
│ └──────────────────────────┴──────────────────────────────┘ │
│                                                             │
│ Cancel anytime. SGD 180/yr (save 21%) on annual billing.   │
│                                                             │
│ ─────                                                       │
│                                                             │
│ Are you a university? See team plans →                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Component details**:
- Two columns, equal visual weight (don't shame Free)
- Concrete features per tier — no marketing fluff
- Honest framing: "Try the product" / "Apply seriously" — names the use case, not the feature count
- Annual savings stated as % (21%), not dollar amount (clearer)
- WSG/credits row appears below if user arrived via WSG referral

### 12.4 Tone in upgrade microcopy

Forbidden:
- "Don't miss out!"
- "Limited time offer!"
- "Upgrade now to unlock your full potential!"
- "Join thousands of successful job seekers!"

Allowed:
- "Unlock the rest of these suggestions."
- "Going to apply to more jobs? Pro removes the limit."
- "Cancel anytime."

---

## 13. AI UX Checklist Applied to KeyStone

| Question | KeyStone answer |
|---|---|
| Can users start without prompt expertise? | Yes — paste JD, upload resume; no prompts |
| Can users see what AI is doing? | Yes — streaming checklists, did-you-know panels, citation hovers |
| Can users stop / modify / redirect mid-action? | Yes — Skip, Edit, undo, retailoring |
| Are AI outputs attributed and distinguishable? | Yes — "We'd say" framing, side-by-side with original, citation tooltips |
| Is context persistence transparent and controllable? | Yes — six-toggle PDPA consent, plain-language explanations, easy export/delete |
| Does AI presentation set appropriate expectations? | Yes — confidence calibration on uncertain suggestions, Fundamental gaps shown honestly |
| Is data collection explicit and reversible? | Yes — pre-action disclosure, post-action receipts, granular consent toggles |
| Can users regenerate / branch / undo? | Yes — undo accept, reset to original, retailor JD, edit any suggestion |

### Anti-patterns avoided

| Anti-pattern | How we avoid it |
|---|---|
| Anthropomorphism without disclosure | No avatar, no AI persona name, "we" not "I" |
| Sycophancy (agrees with everything) | Anti-sycophancy rules, no manufactured suggestions |
| Black-box memory | Six-toggle consent, easy export/delete |
| Silent model downgrades | Confidence calibration shown when low |
| Compute-heavy without draft mode | Streaming output during analysis, partial-failure handling |
| Dead-end conversations | Every state has retry / fallback / next-step |
| Photorealistic avatars for text AI | No avatars at all |
| Feedback theater | Real Skip/Edit weighted equal to Accept |

---

## 14. The Data-Moat Lens — How AI UX Decisions Compound

Every pattern in this document was chosen with two objectives in mind:

| Pattern | User-value reason | Data-moat reason |
|---|---|---|
| Equal visual weight on Accept/Skip/Edit | Frames user as decision-maker | Honest signal — accepts mean accepts, skips mean skips |
| "Why:" rationale required | User understands the suggestion | Each rationale is a labeled training example |
| Suggestion type chip | User knows what kind of help this is | Per-type acceptance rates inform model fine-tuning |
| Edit is celebrated, not hidden | User feels in authorial control | Edit distance + final text is highest-value training data |
| Six-toggle PDPA consent | User feels respected | Consent state per signal makes corpus legally defensible |
| Citation hovers on data-grounded claims | User trusts what's evidence-based | Distinguishes employer-fingerprint signals from model inference in the data |
| No "Are you sure?" confirmations | User has agency, not friction | Friction skews ratio of decisions and pollutes signal |
| Inferred segment-based tone variation | User feels understood | Segment-specific accept rates feed segment-aware models |
| Streaming visible activity | User trusts the AI is working | Per-stage latency feeds infrastructure cost optimization |
| Outcome tracking integrated, not bolted on | User sees what worked | Outcome → suggestion linkage is the metric VMock cannot provide |

The structure: **what feels like care for the user IS the data collection mechanism.** That's the design principle, not a coincidence. Care and capture are aligned; if they ever diverge, retention drops AND data quality drops simultaneously.

---

## 15. Open AI-UX Questions (Track at /todos)

- **Confidence calibration display**: Should low-confidence suggestions be skipped from the count entirely, or displayed with the 🤔 marker? Hypothesis: marker preferred — preserves sample size.
- **Variant suggestions**: Should we ever show 2+ alternative rewrites for one resume line? Risks decision fatigue; postponing to Phase 2.
- **Per-suggestion explainability depth**: When user hovers "Why," should we show the underlying source (employer fingerprint table row, market rule ID)? Hypothesis: yes for citeable claims, no for model-derived guidance.
- **Voice / personality drift across personas**: How aggressive can persona-specific tone be without feeling profiled? Test in pilot; default to subtle.
- **The "regenerate" button**: Should the user be able to ask for a different suggestion on the same line? Risk: turns suggestion engine into chat, dilutes the curated frame. Defer.

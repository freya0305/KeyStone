# 05 — Application Tracking Flows

Tracking creation, batch update, and stage progression. The batch update interaction model in §2 is the most consequential design decision in this document — it is the surface where the data moat is harvested.

## Design Vocabulary

- **Application** — one job submission. Has a `stages[]` array, never a flat status.
- **Quiet** — application's default state when no user input is pending. UI does NOT ask the user about quiet applications.
- **Nudge-eligible** — application has aged into a window where a check-in is statistically warranted (Day 7, 14, 21, 30). Surfaced in batch update.
- **Stage event** — a user-recorded change: response received, advanced to R2, etc. The unit of moat data.
- **Check-in** — the user's session of reviewing nudge-eligible applications. Target: <60s for 20 apps.

## The Smart-Default Principle

```
Default is silence. Action is the exception.
```

The product NEVER asks "anything happen with these?" for every application, every time. It asks once, at the right age, with the lightest possible commitment ("Still no news? Confirm" is one tap). Once confirmed, the application sleeps for another window.

---

## 1. Application Creation

### 1.1 Auto-Creation at Resume Download (Primary Path — ~70% of applications)

**Trigger**: User clicks "Download tailored resume" button after accepting suggestions.

**Modal appears immediately AFTER download initiates** (download is not blocked):

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

Layout: 480px modal, centred. Primary button (left) is solid brand colour; secondary (right) is text-only ghost button. Subtitle is 13px, neutral-600.

**Copy choices justified**:
- "Submitting this" (present tense, second-person implied) — assumes intent without demanding declaration
- "Just downloading" — explicit non-tracking option, no shame; user might be downloading for review
- The benefit framing ("see your response rate", "unlocks interview prep") — connects logging to a personal payoff, never to "help us improve"

**On "Yes"**:
- Application created in DB with `status: pending`, `stages: []`, `created_at: now()`, `employer: <JD-extracted>`, `role: <JD-extracted>`, `suggestion_set_id: <session>` (CRITICAL — this is the outcome→suggestion linkage)
- Toast: "Tracking DBS Digital Banking. Check back in 7 days." (5s, dismissible)
- No further interruption — user continues their session

**On "Just downloading"**:
- No application created
- Toast: "OK. You can add it to tracking anytime from Dashboard." (3s)
- Cookie flag set: if user downloads ≥3 resumes without tracking, show one-time educational modal explaining what tracking unlocks

**Data event logged**: `application.created.from_download` with `{user_id, employer, role, suggestion_set_id, jd_id, opted_in: true|false}`. The opt-out signal is also moat data — tells us about friction.

### 1.2 Manual Creation (Secondary Path — ~20% of applications)

User clicks "+ Add application" from the Dashboard. Used for: applied via LinkedIn directly, applied before finding KeyStone, friend referral, walk-in.

**Form** (single-screen, 5 fields, none required except first two):

```
Add an application

Company *           [DBS                          ]
Role *              [Associate, Digital Banking   ]
Date applied        [2026-04-22]   (defaults to today)
Source              [LinkedIn ▾]   MCF / JobStreet / LinkedIn / Direct / Referral / Other
Notes (optional)    [                              ]

[Cancel]                                  [Add application]
```

Auto-suggest on Company field from a known-employer list (the same list driving employer fingerprints). If user types a new employer, accept it AND queue for canonicalization later.

**On submit**:
- Application created with `created_at = date_applied`, `stages: []`, `source: <selected>`, `suggestion_set_id: null` (user did not use a tailored resume — IMPORTANT for analytics: these applications are the "control group")
- Returns to Dashboard with new card highlighted briefly (1.5s soft glow)

### 1.3 Bulk Import (Tertiary Path — onboarding only)

Surfaced ONCE during onboarding for users who indicate "I've already applied to jobs" on the welcome questionnaire.

```
+------------------------------------------------------------+
| Already applied to some jobs?                              |
| Add them quickly — we'll start tracking from here.         |
|                                                            |
| Company              Role                  Applied         |
| [DBS              ] [Associate         ] [2026-04-15]  [x] |
| [GovTech          ] [Software Engineer ] [2026-04-18]  [x] |
| [+ Add another row]                                        |
|                                                            |
| [Skip — I'll add later]              [Track these 2 jobs]  |
+------------------------------------------------------------+
```

Maximum 20 rows. Each row is one keyboard tab-flow (Company → Role → Date → next row). Skipping is fine; non-coercive.

**Why this matters for moat**: Bulk-imported applications have no `suggestion_set_id` and no tailored resume — they are the most valuable comparison cohort for proving "tailored resumes get more responses". We ASK for them precisely because they make the moat data interpretable.

---

## 2. Batch Update — The Core Interaction

This is the most-used view in the product after the dashboard. Users return here weekly. The design must be ruthlessly fast for the 90% case (no news on most apps) and richly expressive for the 10% case (something happened).

### 2.1 Mental Model

```
Day 0 ----- Day 7 ----- Day 14 ----- Day 21 ----- Day 30
APPLIED     CHECK-IN    CHECK-IN     CHECK-IN     AUTO-CLOSE
            (nudge)     (nudge)      (nudge)      (silent → no-response inferred)
```

Applications appear in batch update ONLY when:
- They have aged into a nudge window (7/14/21 days since last activity), AND
- The user has not visited the app's detail page in the last 24 hours, AND
- The application is not closed (no rejection/offer/withdrawal recorded)

Applications NOT in the nudge window are invisible in this view. The user sees what's *due*, not what *exists*.

### 2.2 Entry Points

Batch update is reached via:
1. Dashboard banner: "5 applications need a quick check-in (≈30s)" → click
2. Weekly digest email link → opens directly to batch update
3. Top nav: "Check in" button (badge count of nudge-eligible)
4. Auto-trigger: after user logs in and has ≥3 nudge-eligible items, the dashboard pre-expands the banner

### 2.3 Layout — The Stack View

NOT a swipe deck (rejected — see analysis doc §2). NOT a grid. A vertical **stack** with a single primary action ("Still no news") that progresses one app at a time, plus quick-tap exception buttons.

```
+--------------------------------------------------------------------+
|  Quick check-in                                  ✕ Close            |
|  5 applications waiting · ~30 seconds                               |
|                                                                     |
|  ┌──────────────────────────────────────────────────────────────┐  |
|  │  DBS · Associate, Digital Banking                             │  |
|  │  Applied 8 days ago · via LinkedIn                            │  |
|  │                                                                │  |
|  │  Heard anything?                                               │  |
|  │                                                                │  |
|  │  [ Still no news ]    Got a response  ·  Rejected  ·  More ▾  │  |
|  └──────────────────────────────────────────────────────────────┘  |
|                                                                     |
|  ▢▢▢▢▢   1 of 5                                                    |
|                                                                     |
|  [Mark all remaining as no news]  ← always visible, bottom-right    |
+--------------------------------------------------------------------+
```

**Layout specifications**:
- Modal is 560px wide on desktop, full-width on mobile
- Card is the only highlighted element on screen — everything else dimmed to neutral-300
- Primary button "Still no news" is large (52px tall, 240px wide), brand colour, left-aligned
- Exception actions are smaller text buttons (32px tall) inline to the right
- "More ▾" reveals: Withdrew, Different stage update (multi-stage), Wrong app (delete)
- Progress dots at bottom show position; count text shows "1 of 5"
- "Mark all remaining as no news" is persistent at bottom — the escape hatch for power users

### 2.4 Interaction Model

**The default tap is "Still no news"**. One tap per app. Card animates left-out (200ms ease-out), next card animates in (200ms ease-in). With 20 apps and 1 tap each, completion in ~25 seconds.

**Keyboard shortcuts** (shown via small hint at first use):
- `Space` or `Enter` = Still no news (advance)
- `R` = Got a response
- `X` = Rejected
- `M` = More options

**The "Mark all remaining as no news" button** — single click clears the entire queue with a confirmation toast: "Marked 12 applications as no news. Undo?" (toast persists 8 seconds with undo). This is the founder's requested escape valve.

**Why one-at-a-time stack and NOT a grid checklist**:
- Grid checklists invite users to skip difficult-to-decide items, leaving incomplete state
- One-at-a-time forces a decision per app, but the decision is tiny (one tap)
- Stack creates a subtle progress feeling (counter + dots) — closure motivation
- For the rare app where user wants to add detail, focused single-card view is the right surface

### 2.5 Exception Flows — When Something Happened

#### 2.5.1 "Got a response" (the highest-value moment)

User taps "Got a response". Card expands inline (no modal — modal would interrupt the queue):

```
┌──────────────────────────────────────────────────────────────┐
│  DBS · Associate, Digital Banking                             │
│  Got a response — that's progress.                            │
│                                                                │
│  When?            Today  ·  Yesterday  ·  [pick date]          │
│                                                                │
│  What kind?                                                    │
│  ○ Phone screening invite                                      │
│  ○ Email asking for more info                                  │
│  ○ HR initial chat                                             │
│  ○ Online assessment / case                                    │
│  ○ Interview invite (skip phone screening)                     │
│  ○ Something else                                              │
│                                                                │
│  [Save and continue]                       [Back]              │
└──────────────────────────────────────────────────────────────┘
```

**Design notes**:
- Headline copy "Got a response — that's progress." is acknowledgement, not celebration yet (celebration is at advancement, not first response)
- Date defaults to "Today" pre-selected — minimum tap path
- Response type is `stage_type` enum mapped to user-readable labels
- "Something else" expands a free-text field (logged but does not block analytics)
- After save: small toast "Logged. Good luck with the next step.", card animates out, queue advances

**Data event logged**: `application.stage_added` with `{application_id, stage_type, format, date, round_number, outcome: "passed"}`. This is the moat moment — first response data is the most predictive signal in our dataset.

#### 2.5.2 "Rejected"

User taps "Rejected". Card expands:

```
┌──────────────────────────────────────────────────────────────┐
│  DBS · Associate, Digital Banking                             │
│  Sorry to hear that. Logging helps refine your next round.   │
│                                                                │
│  When did you find out?     Today  ·  Yesterday  ·  [date]    │
│                                                                │
│  At what stage?                                                │
│  ○ No response (closed by company)                             │
│  ○ After applying — no interview                               │
│  ○ After phone/HR chat                                         │
│  ○ After Round 1 interview                                     │
│  ○ After Round 2                                               │
│  ○ After final round                                           │
│  ○ After offer (rescinded)                                     │
│                                                                │
│  Anything you want to remember? (optional)                     │
│  [                                                            ] │
│                                                                │
│  [Log and close]                            [Back]             │
└──────────────────────────────────────────────────────────────┘
```

**Copy choices**:
- "Sorry to hear that" — brief acknowledgement, no excessive sympathy (would feel patronising for the 海投 user with 30 rejections)
- "Logging helps refine your next round" — frames the log as instrumental to the user's future, not data donation
- The optional notes field is private (never used for moat data, never shown elsewhere) — a safe space

**Data event logged**: `application.rejected` with stage attribution. This is THE most important data for per-stage pass rate analytics.

#### 2.5.3 "More" — Mid-Process Updates

User taps "More ▾". Dropdown:
- "I advanced to a new round" → opens stage progression flow (see §3)
- "I withdrew" → confirmation toast, application closed
- "Got an offer" → CELEBRATION flow (see §3.2)
- "This isn't right" → delete confirmation

### 2.6 Empty State — No Apps Need Check-in

```
+--------------------------------------------------------------------+
|  All caught up.                                                     |
|                                                                     |
|  Your 12 active applications are within their normal response      |
|  windows. We'll let you know when something needs attention.       |
|                                                                     |
|  [Back to dashboard]                                                |
+--------------------------------------------------------------------+
```

This screen is a feature, not a fallback. The user sees evidence the system is doing the watching for them.

### 2.7 Completion State — End of Queue

After last card is processed:

```
+--------------------------------------------------------------------+
|  Done.                                                              |
|                                                                     |
|  ✓ Logged 5 check-ins (4 no news, 1 response received)             |
|                                                                     |
|  Took 38 seconds. Thanks for keeping it accurate — your            |
|  response rate is now based on real data.                          |
|                                                                     |
|  [See your dashboard]   [Add another application]                   |
+--------------------------------------------------------------------+
```

**Why this screen matters**:
- Concrete numbers ("5", "38 seconds") give the user a sense of efficient closure
- "Real data" framing — connects effort to dashboard accuracy
- Two forward paths — view dashboard, OR add an application (capturing manually-tracked apps that user remembered while doing check-in)

**Data event logged**: `batch_update.session_complete` with `{session_id, app_count, no_news_count, response_count, rejection_count, duration_seconds, mark_all_used: bool}`. Duration is a key UX metric — if median climbs above 60s, redesign.

---

## 3. Stage Progression — The Celebration Path

When users advance, the product must feel different. This is the moat's biggest opportunity: stage advancement is the moment users are most willing to log AND most willing to engage with new features (interview prep).

### 3.1 Triggering Advancement

Three entry points to advance a stage:
1. From batch update → "More ▾" → "I advanced to a new round"
2. From application detail page → "Add update" button
3. From a quick-action toast that appears post-login if user has any open application with a recent (<48h) response that hasn't been advanced yet ("Heard back about your DBS interview yet?")

### 3.2 The Advancement Flow

```
+--------------------------------------------------------------------+
|  DBS · Associate, Digital Banking                                   |
|  What just happened?                                                |
|                                                                     |
|  ○ Phone screening — passed, advancing to Round 1                   |
|  ○ Round 1 interview — passed, advancing to Round 2                 |
|  ○ Round 2 — passed, advancing to Round 3 / Final                   |
|  ○ Final round — passed, awaiting offer                             |
|  ○ Got an offer 🎉                                                   |
|  ○ Something different                                              |
|                                                                     |
|  Format of next round:                                              |
|  Phone  ·  Video  ·  In-person  ·  Panel  ·  Technical  ·  Case    |
|                                                                     |
|  Date of next round (if known):  [pick date]                        |
|                                                                     |
|  [Save advancement]                                                 |
+--------------------------------------------------------------------+
```

The options auto-narrow based on the application's current stage — if user is at R1, only R1→R2 transition options surface.

### 3.3 The Celebration Moment

After "Save advancement" on any non-offer advancement:

```
+--------------------------------------------------------------------+
|                                                                     |
|              [confetti micro-animation, 1.2s, restrained]           |
|                                                                     |
|              You're advancing to Round 2 at DBS.                    |
|                                                                     |
|              That puts you in the top 30% of applicants             |
|              who reach this stage.                                  |
|                                                                     |
|              Want to prepare? We can generate                       |
|              interview questions tuned for DBS's R2 format.         |
|                                                                     |
|              [Prepare for Round 2]    [Maybe later]                 |
|                                                                     |
+--------------------------------------------------------------------+
```

**Design specifications**:
- Confetti is 6-8 small geometric shapes, brand colours, 1.2s total — restrained, not gamey
- Headline is 22px, neutral-900, semibold (not 32px — over-celebration feels patronising)
- "Top 30%" benchmark only shows after the user has 15+ applications OR if we have aggregate SG data for the role/employer
- Primary CTA is "Prepare for Round 2" — this is the interview prep handoff (Phase 2 product surface)
- "Maybe later" is intentional escape — never pressure

**Why benchmarks matter here and not on rejection**:
- Advancement is when users are receptive to data
- Rejection benchmarks ("you're below average for R1→R2 conversion") would feel cruel
- Save the comparison data for the empowering moment

### 3.4 The Offer Celebration (Different)

```
+--------------------------------------------------------------------+
|                                                                     |
|         [larger confetti, 2.4s, screen-edge particles]              |
|                                                                     |
|              Offer from DBS.                                        |
|              Congratulations.                                       |
|                                                                     |
|              Tell us how it went?                                   |
|              Your data helps tune suggestions for                   |
|              the next person applying to DBS.                       |
|                                                                     |
|              [Quick reflection — 60 seconds]    [Skip]              |
|                                                                     |
+--------------------------------------------------------------------+
```

**Quick reflection** (the highest-value moat moment in the entire product):

```
What helped most? (pick up to 3)
  □ Tailored resume bullets matched the JD
  □ Interview prep questions were on-target
  □ Cover letter / email pitch
  □ Personal network / referral
  □ Existing experience, not the resume tool
  □ Other: [          ]

What surprised you? (optional, 1 sentence)
[                                                          ]

[Save and celebrate]
```

This is the only moment where we explicitly ask for moat data with full transparency about the use ("helps tune suggestions for the next person applying to DBS"). The user has just received life-changing news; they ARE willing to give 60 seconds. We must not waste this with a bloated form.

**Data event logged**: `application.offer_received` with `{application_id, days_from_apply, suggestion_set_id, success_factors[], surprise_note}`. The `suggestion_set_id` linkage is what makes this data precious — we can later analyse which suggestion patterns correlate with offers.

---

## 4. Auto-Close & Cleanup

### 4.1 30-Day Auto-Close Logic

After 30 days with no activity (no stage events, no user-initiated check-ins), an application's status flips to `auto_closed_no_response`. The application is NOT deleted — it remains in the user's history for response-rate calculations.

### 4.2 The Auto-Close Toast

Next time the user logs in after an auto-close has happened:

```
+--------------------------------------------------------------------+
|  ⓘ  3 applications auto-closed (30 days, no response)              |
|     DBS · GovTech · Accenture                                       |
|                                                                     |
|     Got a response from any of these? [Correct]   [Looks right]    |
+--------------------------------------------------------------------+
```

Persistent banner (not transient toast) at top of dashboard until dismissed. Single dismissal action.

**On "Correct"**: Opens a mini-batch-update with just those 3 apps, allowing user to backfill the actual outcome.

**On "Looks right"**: Banner dismisses. Auto-close becomes permanent.

**Data event logged**: `application.auto_closed` and (if corrected) `application.auto_close_corrected` — the correction rate is a UX metric. If >20% of auto-closes are corrected, the 30-day window is too short.

### 4.3 Archive vs Delete

Auto-closed applications and offer-received applications are ARCHIVED, not deleted. They:
- Appear in the dashboard's "All applications" tab (but not in default "Active" view)
- Continue to count toward response rate / pass rate analytics
- Are searchable by user (some users want to remember a specific one)
- Cannot be edited (frozen, except for explicit "Reopen" action)

User-initiated DELETE is available via application detail menu, with confirmation: "Delete this application? It won't count toward your response rate anymore. This can't be undone." Soft-delete in DB (retain for moat analytics, hide from user) — this requires PDPA-compliant disclosure in privacy policy.

---

## 5. Cross-Cutting Concerns

### 5.1 Edit / Correction Affordance

Every logged stage event has an inline edit action on the application detail page. Users CAN go back and correct mistakes. The data model preserves edit history (`updated_at` per stage) for audit but the user only sees current state.

### 5.2 Mobile-First Considerations

Batch update on mobile:
- Card stack stays one-at-a-time (works on small screens by design)
- Buttons stack vertically: "Still no news" full-width primary, exception buttons in a 3-column row below
- Keyboard shortcuts not applicable; tap targets minimum 48px
- Confetti reduced to particle count 4 (perf)

### 5.3 Friction Calibration — When To Add a Step vs Cut One

A useful heuristic:
- "Still no news" (default outcome) — 1 tap, never more
- Got a response (positive outcome, rare per check-in) — 2 taps + 1 select
- Rejected (negative outcome, rare per check-in) — 2 taps + 1 select
- Advancement (rare, high-value) — 1 select + 1 input + 1 tap
- Offer (very rare, highest-value) — 60s reflection acceptable

Rule: friction MUST be inversely proportional to event frequency. Most-frequent action gets least friction.

### 5.4 Latency Targets

- Card transition animation: 200ms
- Save → next card: <400ms perceived latency (optimistic UI — render the next card immediately, sync to server in background)
- "Mark all remaining" → bulk write: <1.5s with progress indicator if longer
- Application detail page load: <800ms (P75)

---

## 6. Data Events Summary (Moat Surface)

Every interaction in this flow logs a structured event. The events that matter most for the moat:

| Event | Trigger | Why It Matters |
|---|---|---|
| `application.created.from_download` | Auto-create modal Yes | Links application to suggestion_set_id (causal data) |
| `application.created.manual` | Manual form submit | Control-group cohort (no tailored resume) |
| `application.stage_added` | Got-a-response, advancement | Per-stage funnel data |
| `application.rejected` | Rejection logged | Stage-specific failure data — most predictive |
| `application.offer_received` | Offer logged | Reflects success — the labelled outcome |
| `application.advanced` + `success_factors[]` | Offer reflection form | The single richest moat data point |
| `application.auto_closed` | 30-day timeout | "No response" inferred labelled data |
| `application.auto_close_corrected` | User corrects after auto-close | Calibration signal — fix our 30-day assumption |
| `batch_update.session_complete` | End of check-in queue | UX health metric |
| `application.opted_out_at_download` | "Just downloading" tap | Friction signal — informs onboarding |

These events feed the `suggestion_signals`, `application_outcomes`, and `employer_fingerprints` tables defined in the day-1 architecture requirements. The UX exists to make these events fire reliably with minimum user friction.

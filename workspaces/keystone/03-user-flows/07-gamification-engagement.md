# 07 — Gamification, Engagement Loops & Weekly Digest

The engagement strategy must hold one line: **the user's motivation must come from the value of the data to themselves, not from artificial achievement loops**. Job seekers in 海投 mode are stressed, often demoralised. Loud streak-shaming, badge spam, or notification anxiety would actively harm them — and them disengaging would kill the moat.

This doc designs an engagement system calibrated for a stressed audience: quiet rewards, accuracy-as-virtue framing, and a weekly digest email that respects the no-spam constraint.

## Design Principles For This Layer

1. **Reward accuracy, not effort**: The point is not "you logged 5 things this week", it's "your dashboard is now reflecting reality".
2. **Quiet over loud**: Confetti is reserved for genuine outcomes (advancement, offer). Logging a "no news" gets a tick, not fireworks.
3. **No streaks-as-shame**: "You broke your 3-week streak" is harm to a user who didn't get any responses. We do not do this.
4. **Notifications are email-only, weekly cap**: Per the architecture spec — max 1 email per 7 days per user.
5. **The end state is invisible**: A power-user who tracks every app perfectly should hit 100% completeness and then NOT see the gamification widget at all. It exists to coax, not to dominate.

---

## 1. Tracking Completeness — The Core Mechanic

### 1.1 What It Is

A single percentage representing how up-to-date the user's tracking is, displayed as a pill in the top-right of the dashboard. It is the only persistent gamification element.

```
┌──────────────────────────┐
│ Tracking: 88% complete   │
│ ●●●●●●●●○○               │
│ [Improve]                 │
└──────────────────────────┘
```

### 1.2 Calculation

```
completeness = (apps_with_recent_signal / active_or_recent_apps) × 100

where:
  recent_signal = a stage event OR explicit "no news" check-in in past 14 days
  active_or_recent_apps = apps not closed for >30 days
```

A 12-app user who has check-ins on 11 of 12 within the past 14 days = 91% complete.

### 1.3 Visual States

| State | Pill colour | Bar | Copy |
|---|---|---|---|
| 0–40% | Neutral grey | All-empty dots | "Tracking: 32%" |
| 41–70% | Soft amber | Partial dots | "Tracking: 58%" |
| 71–94% | Brand blue | Mostly filled | "Tracking: 88%" |
| 95–99% | Brand blue, subtle gradient | Nearly all filled | "Tracking: 96%" |
| 100% | Soft green | All filled | "All caught up." (different label!) |

**At 100% the label changes from "Tracking: 100%" to "All caught up."** This is a small but important shift — the user sees they have arrived, not that they need to maintain a number.

### 1.4 Threshold Reveals (The Unlock Ladder)

When tracking completeness crosses a threshold UPWARD, a one-time toast fires:

| Crossing | Toast Copy |
|---|---|
| 0% → first non-zero | "Tracking started. Your dashboard updates as you log." |
| → 50% | "Halfway. Your insights are getting more reliable." |
| → 75% | "75% complete. Stage insights are now using mostly current data." |
| → 95% | "Nearly there. One more check-in to be fully caught up." |
| → 100% | "All caught up. Your insights are running on real data." (no further toasts at 100% on subsequent visits) |

These toasts are 4 seconds, dismissible, never sound, never block.

**What we deliberately avoid**:
- Confetti at completeness milestones (saved for actual outcome events)
- Comparative messaging ("You're more diligent than 80% of users") — comparison is for outcome data only, not effort data
- Numerical celebrations like "You're on a 5-day check-in streak" — this is the streak trap

---

## 2. Achievement Toasts — Used Sparingly

Three categories of moments that earn a celebratory toast or screen. Everything outside these categories is silent or low-key.

### 2.1 Outcome-Linked Celebrations (LOUD — confetti permitted)

| Moment | Trigger | UX |
|---|---|---|
| First response | Any application logs first stage advancement past "Applied" | Gentle confetti (1.2s), copy: "First response logged. The hard part is starting." |
| First interview | Any application reaches stage_type = "interview" | Confetti + offer to start interview prep, copy: "Interview at [Company]. Your prep is ready." |
| Round advancement | Any R(n) → R(n+1) | Standard advancement screen (see flow doc §3) |
| Offer | Any application logs offer_received | Larger confetti (2.4s), reflection form (the moat moment) |

### 2.2 Discipline Celebrations (QUIET — toast only)

| Moment | Trigger | Toast |
|---|---|---|
| First batch update completed | User completes first check-in queue | "First check-in done. From now on we'll do this together." |
| 10 applications tracked | App count crosses 10 | "10 applications. Your funnel is starting to mean something." |
| First tailored vs untailored insight | Comparison threshold met | "We can now show what tailoring is doing for you." |
| 30-day tracking accuracy | 30 consecutive days at ≥90% completeness | "A month of consistent tracking. Your data is trustworthy." |

### 2.3 What We Do NOT Celebrate

- Logins (not a virtue, not the user's goal)
- Submitting a single check-in (too small)
- Reaching 100% completeness for the second time (already celebrated once)
- Days/weeks of "streak" (no streaks; see §3)
- Coming back after absence ("Welcome back, we missed you" creates guilt for a stressed user)

---

## 3. Why No Streaks (Founder Decision Point)

A streak-counter ("3-week tracking streak!") is a common engagement pattern but is wrong for this audience.

| Argument For Streaks | Counter |
|---|---|
| Drives recurring engagement | Yes, but creates anxiety. A user who got rejected and stopped checking the product for 2 weeks is already vulnerable. Telling them they broke a streak is salt in a wound. |
| Industry standard for SaaS | Most "industry standard" gamification is calibrated for B2C consumer apps (Duolingo) — not high-stakes life-event tools. |
| Easy to implement | Easy is not a reason. |
| Provides a comparable metric | Tracking completeness IS comparable, without the binary all-or-nothing structure of a streak. |

**Decision**: NO streak counters. Tracking completeness % is the durable engagement mechanic. If the founder wants to revisit, A/B test with strict outcome metric (offer rate per cohort), not engagement metric (DAU).

---

## 4. The Weekly Digest Email

This is the only push channel. Architecture mandate: max 1 per 7 days per user, only if no product login that week, aggregated content (never per-application).

### 4.1 Send Logic

Send conditions (ALL must be true):
- User has not logged into product in past 7 days
- User has ≥1 active application
- User has email digest opt-in (default YES at signup, with PDPA consent)
- At least 1 of: nudge-eligible app exists, OR new milestone unlocked, OR weekly insight available

If no condition triggers, no email. Silence is acceptable.

### 4.2 Subject Line Variants (For Testing)

Test 3 variants in equal-allocation cohorts during first 4 weeks post-launch:

| Variant | Subject | Hypothesis |
|---|---|---|
| A — Action-led | `Quick check-in on your 5 applications (~30s)` | Direct, action-oriented; 海投 user appreciates brevity |
| B — Curiosity | `Your DBS application is at the 7-day mark` | Specific, named; triggers responsibility instinct |
| C — Reflection | `How is your search going this week?` | Soft, human; mid-career user appreciates the framing |

**Measurement**: open rate (primary) + click-through to batch update (secondary) + check-in completion within 24h of email (north star).

**Constraint**: subject MUST NOT use any of: ALL CAPS, emoji except minimal (✓ allowed if relevant), exclamation marks, "URGENT" / "Don't miss out" / spammy hooks. The user can tell. We do not do dark patterns.

### 4.3 Email Body Layout

```
┌────────────────────────────────────────────────────────────────────┐
│  KeyStone                                                           │
│  ───────────────────────────────────────────────────────────       │
│                                                                     │
│  Hi Wei Ming,                                                       │
│                                                                     │
│  Your job search this week:                                        │
│                                                                     │
│      18 active applications                                        │
│      Response rate: 28% (within typical range)                     │
│      5 applications waiting on a quick check-in                    │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │  [ Check in on 5 applications  →  ~30 seconds ]            │    │
│  └──────────────────────────────────────────────────────────┘    │
│                                                                     │
│  ───────────────────────────────────────────────────────────       │
│                                                                     │
│  This week's insight:                                              │
│  Your tailored applications are getting 2x the response rate       │
│  of untailored ones (35% vs 17%). Worth keeping up.                │
│                                                                     │
│  ───────────────────────────────────────────────────────────       │
│                                                                     │
│  Manage email preferences  ·  Unsubscribe                          │
│                                                                     │
└────────────────────────────────────────────────────────────────────┘
```

**Layout specifications**:
- Single-column, 600px max width, mobile-friendly
- Headline numbers (18, 28%, 5) are visually the largest elements (24px)
- ONE primary CTA — "Check in on 5 applications" — opens directly to the batch update queue with one-click auth (JWT magic link valid 24h)
- "This week's insight" is OPTIONAL — only included if user has ≥15 apps AND we have a meaningful insight to surface this week
- No images in body except logo (deliverability)
- Plain-text fallback included (email client compatibility)

### 4.4 The Deep Link Landing State

When user clicks "Check in on 5 applications" from email:

1. JWT auth happens silently (no login prompt)
2. User lands DIRECTLY on the batch update queue (NOT the dashboard first)
3. First card is shown immediately
4. Top of queue has a small banner: "Coming from your Sunday email — let's get through these."
5. After completion, redirects to dashboard with celebration toast: "Done. Thanks for keeping it accurate."

**Why direct-to-queue, not dashboard-first**: Users who click the email button have ALREADY decided to check in. Showing them the dashboard adds a step. The action they want is one tap into the queue.

### 4.5 Unsubscribe Granularity

Email preferences page:

```
What emails do you want from KeyStone?

☑  Weekly digest (current setting — sent only if you haven't logged in)
☑  Achievement notifications (offer received, milestone reached)
☑  Product updates (new features, max once per quarter)
☐  Promotional content (we don't send these — placeholder)

[Save preferences]    [Unsubscribe from all]
```

Unsubscribing from "Weekly digest" does NOT unsubscribe from achievement notifications — these are ALWAYS desirable and rare.

---

## 5. The Engagement Loop (Holistic View)

```
                    ┌────────────────────┐
                    │  USER APPLIES TO   │
                    │     A NEW JOB      │
                    └──────────┬─────────┘
                               │ tailors via product
                               ▼
                    ┌────────────────────┐
                    │  AUTO-CAPTURE      │
                    │  modal at download │
                    └──────────┬─────────┘
                               │ "Yes — track this"
                               ▼
                    ┌────────────────────┐
                    │  APPLICATION       │
                    │  IN QUIET STATE    │
                    └──────────┬─────────┘
                               │ 7 days pass
                               ▼
                    ┌────────────────────┐         no login this week
                    │  NUDGE-ELIGIBLE    │ ──────────────────────────┐
                    └──────────┬─────────┘                            │
                               │                                       ▼
                               │ user logs in              ┌─────────────────────┐
                               ▼                            │  WEEKLY DIGEST      │
                    ┌────────────────────┐                  │  EMAIL SENT         │
                    │  DASHBOARD BANNER  │                  └──────────┬──────────┘
                    │  "5 apps — 30s"    │                             │
                    └──────────┬─────────┘                             │ click
                               │                                       │
                               └───────────────┬───────────────────────┘
                                               ▼
                                    ┌────────────────────┐
                                    │  BATCH UPDATE      │
                                    │  QUEUE (CHECK-IN)  │
                                    └──────────┬─────────┘
                          most apps            │            something happened
                          (no news tap)        │              (response, advance)
                                               ▼
                                    ┌────────────────────┐
                                    │  STAGE EVENT       │
                                    │  LOGGED            │
                                    └──────────┬─────────┘
                                               │
                              ┌────────────────┼─────────────────┐
                              ▼                ▼                 ▼
                    ┌──────────────┐  ┌────────────────┐  ┌──────────────┐
                    │ DASHBOARD    │  │ ADVANCEMENT    │  │ MOAT DATA    │
                    │ ANALYTICS    │  │ → INTERVIEW    │  │ ACCUMULATES  │
                    │ UPDATED      │  │ PREP HANDOFF   │  │ (signals,    │
                    │ (USER GAIN)  │  │ (PRODUCT WIN)  │  │  outcomes)   │
                    └──────────────┘  └────────────────┘  └──────────────┘
```

**Loop properties**:
- Self-sustaining: each completed check-in increases dashboard accuracy, which is the next reason to check in
- Spike-friendly: stage advancement triggers interview prep, which retains and converts to higher LTV
- No-show tolerant: weekly digest reaches absent users without spamming actives
- Outcome-positive: even rejection logging unlocks insights, so the user has a reason to log bad news

---

## 6. Notification Surface Map

To avoid notification overload, every channel and rule is mapped explicitly:

| Channel | When | Frequency Cap | Content |
|---|---|---|---|
| In-product toast (transient, 4s) | Achievement, completeness milestone | No cap | Brief, celebratory or informative |
| In-product banner (dismissible, persistent) | Nudge-eligible apps exist | One banner at a time | "5 apps need check-in" |
| Email — weekly digest | No login in past 7 days, has nudge-eligible | 1 / 7 days | Aggregate summary |
| Email — milestone | Cross 5/10/15/25 application thresholds OR offer received | One per milestone, ever | Brief celebration + dashboard link |
| Email — product updates | Quarterly only | 4 / year max | New features |
| Push notification | NEVER | — | Architecture decision, not revisited |
| SMS | NEVER | — | Architecture decision |

The "no push, no SMS" decision is core to the user trust posture. SG users are deeply averse to job-related SMS (scam prevalence). We do not normalise it.

---

## 7. Anti-Patterns Explicitly Avoided

The following are common engagement patterns deliberately rejected:

- **Streak counters with breakage shaming** — see §3 above
- **Daily login rewards** — would coerce empty engagement; users return when they have something to log
- **Comparative leaderboards** — comparing job-search performance is psychologically toxic
- **Dark-pattern unsubscribe flows** — single-click unsubscribe always available
- **"You're missing out" framing** — never imply data loss for inactivity
- **Fake urgency** ("Action needed in 24h!") — undermines trust on every future communication
- **Push notifications** — explicitly out of architecture
- **Per-application reminders** — explicitly out of architecture (founder constraint)
- **Premium gamification** ("Pro members unlock badges") — gating gamification behind paywall is cheap; paywall is for analytic depth and AI features
- **Anthropomorphic AI mascot** ("KeyBot says: log your apps!") — undermines professional positioning

---

## 8. Mid-Career Switcher Variant

Mid-career users (the segment that pays for Pro) value insights over gamification. For users self-identified as mid-career on signup:

- Tracking completeness pill is shown but smaller / less prominent
- Achievement toasts have alternative copy (more analytical, less encouraging)
  - Fresh grad: "First response logged. The hard part is starting."
  - Mid-career: "First response logged at [Company]. Stage timeline begins."
- Insights zone (Dashboard §4) is expanded by default
- Weekly digest emphasises insight (per-stage trend) rather than action prompt

This is a single feature flag at user-segment level, not a separate UI fork. The segment is captured in the welcome questionnaire.

---

## 9. Engagement Metrics To Watch (For Iteration)

Internal-only metrics (not shown to users) that will tell us if the engagement loop is working:

| Metric | Target Month 6 | Why |
|---|---|---|
| Median tracking completeness across active users | ≥70% | Direct moat health |
| Check-in completion rate (sessions started → finished) | ≥80% | Batch UX health |
| Median time per check-in (per app) | ≤3s | UX speed |
| Weekly digest open rate | ≥35% | Email effectiveness |
| Weekly digest CTR to batch update | ≥15% | Email→action conversion |
| Re-engagement rate (lapsed user → return) | ≥25% within 30 days | Email + life-event recovery |
| Proportion of applications with ≥1 stage event | ≥45% | Effective logging beyond first-response |
| Offer-reflection completion rate | ≥60% of offers logged | The richest moat data point |

If these targets miss, the levers are: subject line testing, batch update friction reduction, dashboard threshold tuning, email body layout iteration. NOT: more emails, push notifications, or harsher gamification.

---

## 10. Data Events Logged From Engagement Layer

| Event | Trigger | Use |
|---|---|---|
| `digest.email.sent` | Weekly send | Volume tracking |
| `digest.email.opened` | Email pixel | Open rate (subject A/B) |
| `digest.email.clicked` | CTA click | CTR |
| `digest.email.unsubscribed` | Unsub action | Health metric — should stay <2% |
| `completeness.threshold_crossed` | 50/75/95/100 | Engagement loop validation |
| `achievement.toast_dismissed` | Toast close | Friction signal |
| `notification.preferences_changed` | Settings save | Preference distribution |

These are operational metrics. They feed the product analytics layer, not the moat. The moat events are in doc 05.

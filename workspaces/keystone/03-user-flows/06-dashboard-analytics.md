# 06 — Dashboard & Analytics

The dashboard is the user's **personal command centre** for their job search. It is NOT an admin panel for the data we collect. Every screen state, copy choice, and component is driven by one principle: the user should think "this helps me", never "I'm filling out a database".

## Frame-Level Layout (L1)

The dashboard is a single scrollable page with three vertical zones:

```
+------------------------------------------------------------------------------+
|  Top bar: logo · Check-in (badge) · Add application · Profile                |
+------------------------------------------------------------------------------+
|                                                                              |
|  ZONE A — Status & action (always visible above fold)                       |
|    - Greeting, current state, primary CTA                                    |
|    - Banner for nudge-eligible apps OR celebration of recent advancement    |
|                                                                              |
+------------------------------------------------------------------------------+
|                                                                              |
|  ZONE B — Funnel snapshot (the headline visual)                              |
|    - Applied → Response → Interview → Final → Offer                          |
|    - Numbers reveal progressively as data accumulates                        |
|                                                                              |
+------------------------------------------------------------------------------+
|                                                                              |
|  ZONE C — Application list (the long-tail surface)                          |
|    - Tabs: Active / Needs check-in / Closed / All                           |
|    - Sortable list, individual stage indicators                             |
|                                                                              |
+------------------------------------------------------------------------------+
|                                                                              |
|  ZONE D — Insights (gated by data threshold; appears only when ≥15 apps)    |
|    - Per-stage conversion, trends, what-helps comparisons                   |
|                                                                              |
+------------------------------------------------------------------------------+
```

Zone allocation: A is ~15% of viewport, B is ~30%, C is ~40%, D is ~15% (and only visible when populated).

**Why this order**: Action first (what should I do now?), funnel second (how am I doing overall?), list third (the working surface for any specific app), insights last (the analytical surface for users who care). Most sessions touch only A and C.

---

## 1. Empty State — User With Zero Applications

The first-time experience after signup. User has analysed a resume but not yet logged any applications.

```
+------------------------------------------------------------------------------+
|  Welcome, Wei Ming.                                                          |
|                                                                              |
|  You have no applications tracked yet.                                       |
|                                                                              |
|  Tracking your applications shows you where you're getting traction —        |
|  response rate, which stages you reach, and which suggestions on your        |
|  resume actually moved the needle.                                           |
|                                                                              |
|  [Add an application]   or   [Tailor a resume to start]                     |
|                                                                              |
|  ─────────────────────────────────────────────────────────────              |
|                                                                              |
|  What you'll see here once you have a few:                                  |
|                                                                              |
|  ┌──────┐    ┌──────┐    ┌──────┐    ┌──────┐    ┌──────┐                  |
|  │  --  │ →  │  --  │ →  │  --  │ →  │  --  │ →  │  --  │                  |
|  │Apply │    │Reply │    │Inter │    │Final │    │Offer │                  |
|  └──────┘    └──────┘    └──────┘    └──────┘    └──────┘                  |
|                                                                              |
|  (Faded preview of funnel — illustrative, not real data)                    |
|                                                                              |
+------------------------------------------------------------------------------+
```

**Copy choices**:
- "You have no applications tracked yet" — direct, non-judgmental
- The benefit ladder is laid out in second paragraph: response rate → stages → suggestion attribution. This sequence mirrors the data unlocks below.
- Two CTAs reflect the two creation paths: manual "Add" or tailor-flow "Tailor"
- Faded funnel preview — hints at what will appear, doesn't pretend they have data

**Data event logged**: `dashboard.viewed_empty` (one-time per user) — used to measure how many users actually log a first application within 7 days of signup.

---

## 2. Early State — 1 to 4 Applications

Funnel skeleton appears with raw counts. No percentages yet (insufficient denominator).

```
+------------------------------------------------------------------------------+
|  Hi Wei Ming. You have 3 active applications.                                |
|                                                                              |
|  ┌─────────────────────────────────────────────────────────────────┐        |
|  │ ⓘ One application is approaching its 7-day check-in window.      │        |
|  │   [Quick check-in]                                                │        |
|  └─────────────────────────────────────────────────────────────────┘        |
|                                                                              |
|  Your funnel                                                                 |
|                                                                              |
|     3              0              0              0              0           |
|  ┌──────┐      ┌──────┐      ┌──────┐      ┌──────┐      ┌──────┐         |
|  │ ███  │  →   │      │  →   │      │  →   │      │  →   │      │         |
|  │Apply │      │Reply │      │Inter │      │Final │      │Offer │         |
|  └──────┘      └──────┘      └──────┘      └──────┘      └──────┘         |
|                                                                              |
|  Response rate, stage conversion, and benchmarks unlock at 5 applications.  |
|                                                                              |
+------------------------------------------------------------------------------+
```

**Design notes**:
- Bars are filled-coloured for stages with data, ghosted (outline only, neutral-300) for empty stages
- Numbers above bars are 24px semibold, neutral-900
- The "unlock at 5" line is a deliberate signpost — sets expectation, motivates next applications
- Banner only appears if there's a nudge-eligible app

---

## 3. Established State — 5 to 14 Applications

Response rate appears. Per-stage pass rates are still gated. The view becomes meaningful.

```
+------------------------------------------------------------------------------+
|  Hi Wei Ming. 12 active applications · 3 closed.                             |
|                                                                              |
|  ┌─────────────────────────────────────────────────────────────────┐        |
|  │ 5 applications need a quick check-in (~30 seconds)                │        |
|  │ [Check in now]                                                    │        |
|  └─────────────────────────────────────────────────────────────────┘        |
|                                                                              |
|  Your funnel                          Response rate: 27%                     |
|                                       (4 of 15 — within typical range)       |
|                                                                              |
|     15             4              2              1              0           |
|  ┌──────┐      ┌──────┐      ┌──────┐      ┌──────┐      ┌──────┐         |
|  │██████│  →   │ ████ │  →   │ ██   │  →   │ █    │  →   │      │         |
|  │Apply │      │Reply │      │Inter │      │Final │      │Offer │         |
|  └──────┘      └──────┘      └──────┘      └──────┘      └──────┘         |
|                                                                              |
|  Per-stage conversion unlocks at 15 applications (3 more to go).            |
|                                                                              |
|  Active applications  ──────────────────  Active · Needs check-in · All     |
|  [list of applications with stage pills]                                    |
|                                                                              |
+------------------------------------------------------------------------------+
```

**Design specifications**:
- Response rate is 18px semibold, neutral-700; "(4 of 15 — within typical range)" is 13px neutral-500
- "Within typical range" framing: never "you're below average". For SG fresh-grad 海投, 15-25% response rate is typical. We anchor positively or neutrally.
- Stage bars are now proportionally filled (not just present/absent) — visual continuity matters
- "3 more to go" is a soft progress indicator toward the next unlock
- Tabbed application list begins at this stage

**The "within typical range" copy logic**:
- < 10%: "Below typical range — let's look at what to adjust" + suggestion to revisit resume
- 10–35%: "Within typical range"
- 35–55%: "Above typical range — strong signal"
- \> 55%: "Exceptional response rate"

We never display the number alone without a frame — naked percentages create anxiety in low ranges.

---

## 4. Mature State — 15+ Applications (Insights Unlocked)

The full analytics surface. Per-stage pass rate and Insights zone are visible.

```
+------------------------------------------------------------------------------+
|  Hi Wei Ming. 18 active · 7 closed · 1 offer pending.                        |
|                                                                              |
|  Your funnel                                  Response rate: 28%             |
|                                                                              |
|     25            7              4              2              1            |
|  ┌──────┐ 28% ┌──────┐ 57% ┌──────┐ 50% ┌──────┐ 50% ┌──────┐              |
|  │██████│  →  │██████│  →  │██████│  →  │██████│  →  │ ███  │              |
|  │Apply │     │Reply │     │Inter │     │Final │     │Offer │              |
|  └──────┘     └──────┘     └──────┘     └──────┘     └──────┘              |
|                                                                              |
|  Application list                                                            |
|  [ ... ]                                                                     |
|                                                                              |
|  ─────────────────  Insights ─────────────────                              |
|                                                                              |
|  Where you're strongest                                                     |
|  Round 1 → Round 2 conversion: 75% (typical: 45%)                           |
|  You're consistently making it past first-round interviews.                  |
|                                                                              |
|  Where there's room                                                          |
|  Application → Response: 28%                                                 |
|  In line with SG fresh grad average. Tailored resumes in your last          |
|  10 applications had 35% response rate vs 17% on untailored.                |
|                                                                              |
|  Tailored resume payoff                                                      |
|  17 applications used tailored resumes  →  35% response                     |
|  8 applications used untailored          →  13% response                     |
|  [chart: side-by-side bars]                                                  |
|                                                                              |
+------------------------------------------------------------------------------+
```

**Design notes**:
- Stage conversion percentages now appear between the bars (e.g., 28% between Apply and Reply)
- Conversions are the most valuable analytics — they appear inline with the funnel, not buried in Insights
- Insights zone follows a "Strongest / Room / Payoff" structure — always lead with strength
- The Tailored vs Untailored comparison is the user-facing demonstration of the moat. It is the answer to "why pay for this product" — and it requires the user to have logged enough untailored apps for the comparison to be meaningful (the bulk import flow on day 1 is what enables this).

### 4.1 Stage Funnel Drilldown

User clicks the "Round 1 → Round 2" stat. Drawer opens from the right:

```
+------------------------------------------+
|  Round 1 → Round 2 conversion            |
|  ✕                                       |
|                                          |
|  Your rate: 75%                          |
|  Typical SG mid-career: 40-50%           |
|  Typical SG fresh grad: 30-45%           |
|                                          |
|  Applications that made R2:              |
|  ✓ DBS · Associate                       |
|  ✓ GovTech · SWE                         |
|  ✓ Accenture · Consultant                |
|                                          |
|  Applications that didn't:               |
|  ✗ Standard Chartered · Analyst          |
|                                          |
|  What R2-passing apps had in common:     |
|  • All used tailored resumes             |
|  • All had Strong-match score ≥ 80%      |
|  • All in financial services or tech     |
|                                          |
|  [Tip: focus next applications on        |
|   roles like these]                      |
|                                          |
+------------------------------------------+
```

**Why this drawer matters**: This is the per-user qualitative pattern surface — the moat data flows back to the user as actionable insight. The user sees themselves in the data.

---

## 5. Application List Component

The list in Zone C is the working surface — users return to it to add updates, view detail, or jump into batch update.

### 5.1 Tabs

- **Active** (default): apps with no terminal stage event (offer/rejection/withdrawal/auto-close)
- **Needs check-in**: subset of Active that are nudge-eligible (overlaps with batch update queue)
- **Closed**: apps with terminal stage events. Includes auto-closed.
- **All**: union

### 5.2 List Item Layout

```
+--------------------------------------------------------------------+
|  DBS · Associate, Digital Banking          Applied 12 days ago     |
|  ●─────●─────○─────○─────○                                         |
|  Applied  Response  R1     R2     Final                            |
|  Last update: Phone screen completed (3 days ago)                  |
|                                                  [Update] [Detail] |
+--------------------------------------------------------------------+
```

**Component spec**:
- Row height: 96px desktop, 120px mobile (taller for tap targets)
- Stage indicator: 5 dots connected with lines. Filled dots = passed, current dot = pulsing brand colour, empty dots = neutral-300 outline
- Stage labels below dots: 11px neutral-500
- "Last update" line: 13px neutral-700
- Two action buttons: "Update" is small ghost button, "Detail" is icon-only chevron

### 5.3 List States

- **Default**: as above
- **Nudge-eligible**: row has thin amber left border (2px), "Last update" line replaced by "Check in?" link
- **Recently advanced** (within 24h): row has soft brand-colour background tint that fades over 5 sessions
- **Auto-closed**: row in neutral-400 text, dot indicator shows last-known stage, with "(auto-closed, no response)" label
- **Offer received**: row has subtle gold accent on the right edge, "Offer pending decision" label

### 5.4 Sort & Filter

Default sort: by `last_activity_date` descending. User can change to: applied date, employer name, current stage, response status.

Filter chips above list: `Pending response` `In interview` `Final stage` `Offers` `Closed`. Multi-select.

---

## 6. Application Detail Page

Reached via "Detail" or by clicking the row. Full screen, not modal.

```
+------------------------------------------------------------------------------+
|  ← Back to dashboard                                                         |
|                                                                              |
|  DBS · Associate, Digital Banking                            [Edit] [Delete] |
|  Applied April 17 via LinkedIn  ·  12 days ago                              |
|                                                                              |
|  Stage progress                                                              |
|  ●───────●───────●───────○───────○───────○                                  |
|  Apr 17  Apr 22  Apr 28   ?                                                 |
|  Applied Phone   R1       R2      Final   Offer                             |
|          screen  passed                                                     |
|                                                                              |
|  [Add update]                                                                |
|                                                                              |
|  Timeline                                                                    |
|  ─ Apr 28 — Round 1 interview (video, 45 min) — passed                      |
|              "Asked about my fintech project. Felt strong."                 |
|  ─ Apr 22 — Phone screening (HR) — passed                                   |
|  ─ Apr 17 — Applied via LinkedIn                                             |
|                                                                              |
|  Resume used                                                                 |
|  ┌────────────────────────────────────────┐                                 |
|  │ ⓘ Tailored on Apr 17                    │                                 |
|  │   16 suggestions accepted, 3 rejected   │                                 |
|  │   [View resume version]                 │                                 |
|  └────────────────────────────────────────┘                                 |
|                                                                              |
|  Interview prep                                                              |
|  ┌────────────────────────────────────────┐                                 |
|  │ Round 2 prep is ready                   │                                 |
|  │   Generated for DBS R2 format           │                                 |
|  │   [Open prep session]                   │                                 |
|  └────────────────────────────────────────┘                                 |
|                                                                              |
+------------------------------------------------------------------------------+
```

**Why this layout**:
- Stage progress at top — most-glanced info
- Timeline below — chronological narrative the user can scroll
- "Resume used" section ties the application to the suggestion set (the moat linkage made visible to the user as a feature)
- Interview prep card is contextual — only appears when there's an active prep relevant to current stage

---

## 7. Progressive Reveal Schedule

The dashboard adds capability as data accumulates. Each unlock is announced via toast on the dashboard the first time the user crosses the threshold.

| Apps Logged | Unlocks | Toast Copy |
|---|---|---|
| 1 | Funnel skeleton (counts only) | "Tracking your first application. The dashboard fills in as you go." |
| 5 | Response rate %, "typical range" framing | "Response rate unlocked. You can now see how you're performing." |
| 10 | Trend sparkline (response rate over time) | "Trend view added. See whether your response rate is climbing." |
| 15 | Per-stage pass rate, full Insights zone | "Stage insights unlocked. See where you're strongest and where to focus." |
| 25 | Tailored vs untailored comparison | "We can now show what tailoring is doing for you." |
| 50 | Employer-pattern insights ("DBS-pattern roles") | "Patterns across employers are clear enough to surface." |

**Why thresholds matter**: They are simultaneously a statistical defensibility floor (we don't show conversion stats with n=2 — the noise would mislead) AND a gamification driver (each unlock is a milestone the user is working toward).

---

## 8. Tracking Completeness Indicator

A small persistent component in the top-right of the dashboard:

```
┌──────────────────────────┐
│ Tracking: 88% complete   │
│ ●●●●●●●●○○               │
│ [Improve]                 │
└──────────────────────────┘
```

**Calculation**: 
- Numerator: applications with at least one logged stage event OR explicit "no news" check-in within the past 14 days
- Denominator: total active + recently-closed applications

**Why "completeness", not "logged":**
- "Logged" implies one-time data entry; completeness implies ongoing accuracy
- "88% complete" is a more flexible target than "all apps logged"

**[Improve] button** opens batch update if any nudge-eligible items exist. Otherwise opens a help drawer explaining what's missing.

**Reward at 100%**: small pill animation, neutral celebration ("All caught up. Your insights are running on real data."). No streak-counter pressure (see gamification doc §3 for streak rationale).

---

## 9. Mobile Adaptations

Dashboard on mobile (≤640px):
- Zone A collapses banner into a single chip with count
- Zone B funnel becomes a vertical stack (5 rows top-to-bottom) with arrows replaced by chevrons
- Zone C list items stack into single-column cards, stage indicator becomes 5 small dots in a horizontal row
- Zone D Insights collapses each card into an accordion (closed by default)
- Tracking completeness pill collapses to circular progress icon in top nav

The funnel-as-vertical-stack is ESSENTIAL — horizontal funnels on mobile force ant-sized text. Vertical preserves legibility.

---

## 10. Loading & Error States

### 10.1 Initial Load
Skeleton screens for each zone (animated shimmer on rectangles matching final layout). Dashboard data target: <1s P75.

### 10.2 Stale Data
If dashboard data is >5 min old when user views, show small refresh chip in top-right. Auto-refresh on user interaction.

### 10.3 Error States
- Failed to load applications: full-page error with retry button. NEVER show empty state on error (would lie to the user).
- Failed to log a stage event: optimistic UI is reverted, error toast with retry. Event queued for retry on reconnect.
- Failed analytics computation: hide affected card, show "Insights catching up — refresh in a moment". Never show wrong numbers.

---

## 11. Data Events Logged From Dashboard

| Event | Trigger | Use |
|---|---|---|
| `dashboard.viewed` | Page load | Engagement metric |
| `dashboard.viewed_empty` | First-time empty state | Onboarding funnel |
| `dashboard.unlock_milestone` | Crossing threshold (5/10/15/25/50 apps) | Engagement loop validation |
| `dashboard.insights.drilldown_opened` | Stage drilldown drawer | Insight engagement |
| `dashboard.tracking_completeness.viewed` | First view of completeness >0 | Gamification efficacy |
| `application.detail.viewed` | Detail page open | Per-app engagement |
| `application.timeline.note_added` | Inline note on timeline event | Qualitative data — useful for moat narratives |

These dashboard events are NOT moat data themselves — they are UX-health metrics. The moat data is logged in the tracking flows (doc 05). The dashboard exists to make those flows worthwhile to use.

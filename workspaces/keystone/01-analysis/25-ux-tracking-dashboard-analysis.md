# 25 — UX Tracking & Dashboard: Design Analysis

This analysis explains the reasoning behind the design choices in `03-user-flows/05`, `06`, and `07`. It captures alternatives considered, trade-offs, data-moat implications, and risks. The flows are the contract; this doc is the rationale.

## 1. The Core Tension Restated

KeyStone's data moat exists only if users log application outcomes at scale. But users have zero intrinsic motivation to log — the data benefits the product more than them in the short term. Every UX decision in tracking flows is calibrated against this tension:

```
Logging effort   ←──────────────────────────────→   Logged data volume
        |                                                       |
        |  HIGH effort     →   user disengages → moat dies     |
        |  ZERO effort     →   no signal at all → moat dies    |
        |  RIGHT effort    →   data flows → moat builds        |
        ▼                                                       ▼
                  Where is "right effort"?
```

The right answer is NOT "minimise effort to zero" (the architecture forbids per-application emails for good reason — users would unsubscribe). It is "make the effort feel like personal benefit". This is the line the designs walk.

---

## 2. Why The Stack View, Not Tinder Swipe Or Grid Checklist

The founder rejected the previous Tinder-swipe interface ("I don't want users clicking for every single one"). Three alternatives were considered:

### Alternative A — Tinder Swipe (REJECTED, founder feedback)
- **Mechanic**: Swipe right for "got response", left for "no news", up for "advanced"
- **Problem**: Even though gestural, requires per-app interaction. Founder's correct objection: most apps are no-news; demanding a tap for each is busywork.
- **Failure mode**: User abandons mid-deck. Partial-state queue. Skewed data (only the apps before the abandonment point have updates).

### Alternative B — Grid Checklist (CONSIDERED, REJECTED)
- **Mechanic**: All nudge-eligible apps in a grid. User checks a box for each "no news"; clicks "got update" link for exceptions.
- **Problem**: Grids invite cherry-picking — user updates the easy ones, leaves ambiguous ones uncheck. Gridded view also hides the count of "still pending".
- **Failure mode**: Persistent "ghost queue" of half-decided apps. Tracking completeness stalls in the 60-70% range.

### Alternative C — Stack View With Default-Action (CHOSEN)
- **Mechanic**: One card at a time, large "Still no news" primary button as default tap. Exception buttons inline.
- **Why it works**: The default tap is the most-frequent outcome. One tap per app, but one tap is the irreducible minimum if we want per-app accuracy. With keyboard shortcut (Space), 30 apps = ~25 seconds.
- **Plus the escape valve**: "Mark all remaining as no news" is the founder's demanded affordance. Power users who trust their memory can clear the deck in one click. The button is persistent (always visible, not hidden in a menu) so it never feels like the system is forcing per-app interaction.

### Why Not Just "Mark All As No News" Always
A single bulk-confirm button alone would be too lossy:
- We never get the chance to ask about exceptions ("Got a response on any of these?")
- The user never enters the headspace of considering a specific application
- Stage events for the 1-2 apps where something happened would be missed

The stack view forces a brief consideration per app while keeping the cost trivially low. The "Mark all remaining" button is the structural escape — it's there to prevent rage-quit, not to be the default path.

### Why Not "Show Only Apps Where Something Is Expected"
Considered: surface only apps that are exactly at Day 7 (or other expected-response milestone). Skip apps in between.

**Why rejected**:
- Doesn't account for apps that respond at Day 3 (some companies are fast)
- A 7-day window is too narrow — many apps respond at Day 10-21
- Users want to feel they have a complete view, not a filtered view they don't understand
- Multi-day windowing IS implemented (the nudge-eligible logic at Day 7/14/21/30) but the UI presents the windowed set as "what needs your attention now", which is honest framing

---

## 3. Why The Auto-Capture Modal At Download, Not At Some Later Point

Three timing options were considered for auto-creating an application record:

| Timing | Pros | Cons |
|---|---|---|
| Before download (gating) | 100% of downloaders see prompt | Coercive — gates the user's primary action behind a tracking decision; will reduce download rate |
| Immediately after download (post-action) | Captures intent at peak motivation; no friction blocker | Some users will dismiss without thinking |
| Some hours later via email | Gives user time to actually apply | Per-application emails are forbidden by architecture (inbox spam for 海投) |
| First login after download | Defers but uses pull surface | User may have downloaded multiple resumes between visits — confusing batch state |

**Chosen: immediately after download (post-action)**. The download is not gated; the modal appears AFTER the file has started downloading, so the user's primary task is complete. This is the moment of peak motivation for tracking — the user just completed the action. The modal is a 2-button choice, not a form.

The opt-out option ("Just downloading") is non-shameful. It also captures a useful signal: `application.opted_out_at_download` — measuring this rate tells us about user intent and lets us target the educational nudge to high-opt-out cohorts.

---

## 4. Why Stages Array, Not Status Enum (UI Implications)

The data model decision (stages array, see day-1 architecture) has direct UX consequences:

- We can show 5-dot progress indicators per application — users see WHERE they are in the funnel
- We can compute per-stage pass rate — the most predictive metric
- We can show stage-specific celebrations (advancing to R2 ≠ advancing to R3)
- We can attribute rejections to a specific stage, which is the data we need most

The alternative (`status: enum`) would have collapsed all of this into a single category and made the funnel visualization meaningless. The stages array data model directly enables the dashboard's value proposition.

The cost is interaction complexity at advancement: the user must select WHICH stage they advanced to. We mitigate this by:
- Auto-narrowing the options based on current stage (only show valid transitions)
- Pre-filling round_number based on count of existing interview-type stages
- Using natural-language labels ("passed Round 1, advancing to Round 2") not data-dictionary terms

---

## 5. Why Progressive Reveal At 5/10/15/25/50 Apps

The thresholds are simultaneously a statistical defensibility floor AND an engagement driver:

### Statistical Defensibility
- Response rate with n=2 is meaningless (50% from 1 of 2 vs 100% from 2 of 2 — both random)
- Response rate at n=5 has wide error bars but begins to be informative
- Per-stage pass rate needs ≥3 applications reaching each stage; n=15 total apps gives reasonable coverage
- Tailored vs untailored comparison needs both cohorts populated; n=25 gives ~10 in each group with 60/40 split

### Engagement Driver
- Each unlock is a milestone, providing a forward-looking goal during the early "data-thin" phase
- The sequence corresponds to escalating sophistication of insight
- Visible "3 more to unlock per-stage" creates motivation to continue logging

Risks:
- Users may stop at the threshold-just-crossed point ("I unlocked it, I'm done")
- Mitigation: Once unlocked, the metric stays visible and updates with every new app, so accuracy improves with continued logging — and the tracking-completeness mechanic continues to operate

---

## 6. The Celebration Asymmetry — Loud For Outcomes, Quiet For Effort

Three categories of celebration with different volume:

| Trigger | Volume | Why |
|---|---|---|
| Outcome event (response, advancement, offer) | LOUD (confetti, screen-overlay, dedicated copy) | Real life moment for user — they're winning, the product reflects it |
| Discipline milestone (10 apps, first batch update) | QUIET (toast only) | Effort is virtue, but celebrating effort too much feels infantilising |
| Logging "no news" | SILENT | Most-frequent action; celebrating it would be noise |

The asymmetry is essential. If we celebrated "no news" logging, we'd be celebrating the user's job-search struggle — psychologically wrong. If we didn't celebrate offers, we'd miss the highest-value emotional moment in the entire product (and the moment we ask for the richest moat data, the offer reflection).

---

## 7. Why No Streak Counters

Considered and rejected. Detailed in `07-gamification-engagement.md` §3. Summary:

- Users with poor results (most users in 海投 mode) will break streaks. A "you broke your 3-week streak" notification when the user is already demoralised is harm.
- Industry-standard gamification is calibrated for low-stakes consumer apps (Duolingo). Job search is high-stakes life event.
- Tracking completeness % is a softer, more durable metric. It can be partially-filled without binary-failure cliff.

If the founder wants to revisit, the test must be: does adding a streak counter increase the OUTCOME metric (offers per cohort) or only the ENGAGEMENT metric (DAU)? Vanity DAU at the cost of user wellbeing is a bad trade.

---

## 8. Auto-Close At 30 Days — Why That Number

The 30-day auto-close window is calibrated against SG response patterns:

- ~75% of SG companies that respond do so within 14 days (per market research, see specs/sg-market-norms.md placeholder)
- ~95% within 21 days
- After 30 days, response probability drops to <2%

So 30 days is a reasonable inference threshold. We frame it explicitly ("auto-closed, no response inferred") and provide the correction affordance — if the user actually got a response and didn't log, "Correct" backfills the truth.

**Risk**: false negatives (user got response, never logged, auto-close marks as no-response). This corrupts the moat data.

**Mitigation**:
- Correction toast surfaces auto-closes prominently
- Correction rate is tracked (`auto_close_corrected` event); if >20%, we tighten or change the algorithm
- Day 21 nudge in batch update is the pre-auto-close last-chance check-in

---

## 9. Email Strategy — Pull Not Push

The architecture mandate: max 1 email per 7 days, only if no login. This document operationalises that into:

- **Weekly digest is conditional**: if user logged in this week, no email
- **Aggregate, not per-app**: digest summarises ALL apps, never reports on each individually
- **Direct-to-action deep link**: clicking the email goes to batch update queue, not dashboard
- **Subject line A/B testing**: 3 candidates, measured by check-in completion (not just open rate)

The hard part is the deliverability. SG email norms:
- Spam filters are aggressive on "transactional" categorisation
- Gmail (most SG users) downranks generic "weekly digest" emails over time
- Mitigation: each email has unique data ("Your DBS application is at the 7-day mark") — varies sufficiently to escape pattern-detection

**Risk**: even one weekly email feels too much for a user with high anxiety. Mitigation: prominent "manage preferences" link in every email; default-on but easy to turn off.

---

## 10. Mobile vs Desktop Trade-offs

The product MUST work on mobile (SG users heavily mobile-first for personal admin tasks). Key decisions:

- **Stack view works identically on mobile**: One card at a time is mobile-native
- **Funnel visualization rotates to vertical on mobile**: Horizontal funnels become illegible at small sizes
- **Keyboard shortcuts disabled on mobile**: Tap targets sized for finger (48px min)
- **Confetti reduced**: Particle count 4 vs 8 desktop, performance-driven
- **Email digest**: Single-column 600px max, mobile-optimised

The expected primary mobile use case is the weekly check-in (user gets digest email on phone, taps through, completes batch update on phone in 30s). This is the most-mobile-critical flow and is designed mobile-first.

---

## 11. Data Moat Implications Per Design Decision

Every UX decision has a moat-data consequence. Mapping them explicitly:

| UX Decision | Moat Data Consequence |
|---|---|
| Auto-capture modal at download | Captures suggestion_set_id linkage at point of intent — REQUIRED for outcome→suggestion attribution |
| Stack view with single primary action | Maximises completion rate of batch updates → higher application_outcomes volume |
| Stages array (not status enum) | Enables per-stage pass rate computation → unique data asset vs VMock |
| Offer reflection form | The richest single moat data point: links outcome → success factors → suggestion set |
| Bulk import in onboarding | Captures untailored "control group" data → enables tailored vs untailored comparison |
| 30-day auto-close inferred-no-response | Provides labelled negative data for response-rate model training |
| Tracking completeness gamification | Drives recurring engagement → higher accuracy of in-window data |
| Stage-specific rejection capture | Pinpoints where users drop off → most predictive feature for personalised suggestions |
| Per-segment dashboard variant (mid-career) | Surfaces analytical use cases that increase Pro conversion → revenue funds moat building |

The pattern: every "user benefit" feature is also a moat feature. This is the only way to align incentives at scale. The product CANNOT survive a strategy where the moat is built on user altruism.

---

## 12. Risks & Open Questions

### Risk 1: Logging Rate Below 20-25% Target
**What it looks like**: Median tracking completeness <40% at Month 6. Insufficient stage_events to compute per-stage pass rates.

**Mitigations**:
- Tighter onboarding: in-product education on dashboard value within first session
- Lower thresholds for unlocks (15→10 for per-stage) IF user retention is strong but data thin
- Subject line tightening on weekly digest (one variant likely outperforms — pick and stick)
- Pre-interview-prep gate: require stage event log before unlocking interview prep (mild coercion, calibrate carefully)

### Risk 2: Auto-Close Corrupts Negative Data
**What it looks like**: Many false-negative "no response" labels because users got responses but didn't log.

**Mitigations**:
- Correction rate monitoring (target <10%)
- Day 14 and Day 21 nudges with 1-tap "still no news" — last chances
- Phase 3 email parsing (read receipts from MCF/JobStreet) auto-corrects retroactively

### Risk 3: User Cognitive Overload
**What it looks like**: Users feel the product is "too much work". Churn at 2-week mark.

**Mitigations**:
- All friction-introducing features are progressive (don't appear until threshold)
- Empty state and 1-app state are radically simple
- Test: time-to-first-meaningful-insight; should be <10 minutes from signup for users with existing applications via bulk import

### Risk 4: PDPA / Privacy Concerns Reduce Opt-In
**What it looks like**: Users decline aggregation consent at signup; signal volume below moat threshold.

**Mitigations**:
- Consent framing emphasises individual benefit ("your dashboard improves") not collective ("help us train AI")
- Granular consent: separate opt-ins for outcome aggregation vs model training (per architecture spec)
- B2B contracts include explicit "no AI training" clause; B2B data is service-only

### Open Question 1: Should Bulk Import Be Surfaced Outside Onboarding?
Some users will want to bulk-add applications later (e.g., they had a busy week and applied to 10 things at once). Currently bulk import only in onboarding.

**Proposed**: Add "Bulk add" link on Dashboard for users with ≥5 existing apps. Same UI as onboarding flow.

**Trade-off**: Risk of users dumping all-at-once and not engaging with check-ins thereafter. Test post-launch.

### Open Question 2: How To Handle "Reopened" Applications?
Edge case: user marks app as rejected, then receives a different role offer from same employer.

**Current design**: User can re-open from detail page (manual). New stages append to existing application.

**Alternative**: Force creation of new application (cleaner data model, less ambiguity).

**Decision pending**: Need to understand how often this happens in SG market data before deciding.

### Open Question 3: When Does Interview Prep Become Required?
Phase 2 product handoff. Currently the design assumes interview prep is OPTIONAL ("Maybe later" button). 

**Tension**: Required prep would force tracker→prep handoff, increasing prep adoption. Optional preserves user agency.

**Decision pending**: Test in Phase 2 launch with both options.

---

## 13. Comparison To Competitive Alternatives

### vs. Manual Spreadsheet Tracking (Most SG Job Seekers Today)
- KeyStone wins on: visualization, automatic insights, per-stage analytics
- Spreadsheet wins on: full user control, no learning curve
- Implication: KeyStone's UX must be at parity-or-better for adding/editing speed. The bulk import and stack view are explicit answers.

### vs. LinkedIn "Saved Jobs" / "Applied" Tracker
- LinkedIn wins on: zero friction (clicks Apply within LinkedIn → auto-tracked)
- KeyStone wins on: cross-platform tracking (works for MCF, direct apps, LinkedIn, JobStreet), per-stage detail, outcome attribution
- Implication: KeyStone must work hard for the LinkedIn-applied-jobs cohort. Auto-capture at resume download is part of the answer; future LinkedIn integration would be ideal.

### vs. Teal / Jobscan Application Trackers
- Teal/Jobscan win on: maturity, polish
- KeyStone wins on: SG-specific (employer fingerprints), moat-data-driven insights (tailored vs untailored comparison)
- Implication: KeyStone's stage-pass-rate analytics is the differentiator. Make it visually unmistakable.

### vs. VMock (The Incumbent)
- VMock has: ATS scoring, university distribution, brand recognition
- VMock LACKS: outcome tracking entirely. They cannot show callback rate change.
- Implication: KeyStone's tracker IS the displacement weapon. The dashboard analytics must be demo-able to a Provost in 60 seconds: "VMock can give you a score. We can give you a callback rate, broken down by employer, calibrated on real outcomes." Design must support that demo without prep.

---

## 14. UX Quality Bar (Heuristic Evaluation)

Self-evaluation against enterprise-AI heuristics:

| Heuristic | Assessment |
|---|---|
| Content-first (70/30 content/chrome) | PASS — Dashboard zones B+C are content; A+D are utility/insight |
| Hierarchy (primary action obvious) | PASS — "Still no news" is unmistakably the primary in batch update |
| Efficient workflows (1-2 clicks for common) | PASS — 1 tap per app for batch update |
| Progressive disclosure | PASS — Insights gated by data threshold; advanced options behind "More" |
| Consistency | PASS — Same stage indicator component across list, detail, batch update |
| Trust patterns (citations, verification, disclosure) | PARTIAL — Need to add disclosure of how AI uses signal data; consent at signup is in place |
| Empty/error states explicitly designed | PASS — Empty state for 0 apps, completion state for 0 nudges, error states defined |
| AI identity disclosure | PARTIAL — Achievement copy is product-voice not AI-voice; this is correct. But analytics framing should disclose statistical confidence levels at low data volumes (currently softened with "typical range" language; could be more explicit). |
| Mobile parity | PASS — Mobile flow defined for every key screen |
| AI slop check (3+ fingerprints) | PASS — No purple-blue gradients, no glassmorphism, no uniform rounded-2xl, no "AI" personality voice |

---

## 15. Implementation Notes For Engineering Handoff

The design specifies behaviour. Engineering must consider:

1. **Optimistic UI is essential for batch update**: Stage events should render immediately; sync to server in background. Failures revert with toast + retry. Without optimistic UI, the 25-second target is unachievable.

2. **JWT magic links for email deep-links**: Email→batch-update flow MUST work without login prompt. JWT valid 24h, single-use per link.

3. **Event log infrastructure**: Every UX event listed in the flow docs should write to an append-only event log (separate from primary state DB). The event log IS the moat data. Treat it with the same backup/retention rigor as production data.

4. **Stage transition validation**: Don't allow R3→R1 (would be invalid). Server-side validation on stage transitions; UI auto-narrows options pre-validation.

5. **Auto-close as scheduled job**: Daily cron over apps with no recent activity. Computes auto_closed status; queues banner for next user login.

6. **Performance on large lists**: User with 100 active applications must still have <1s dashboard load. Pagination, lazy-load timeline events.

7. **Suggestion-set linkage at create**: Critical foreign key. Application creation flow MUST capture `suggestion_set_id` at the point of resume download. Missing this breaks the moat.

8. **PDPA disclosure surfacing**: Privacy policy link visible at all data-aggregating moments (offer reflection form, bulk import, batch update). Not buried in footer.

---

## 16. Open Design Decisions Pending Founder Review

1. **Confetti volume on advancement**: Designed at 1.2s / 6-8 particles. Founder may want more (consumer-celebratory) or less (professional-restrained). Test with 5 SG users.

2. **"Mark all remaining" placement**: Currently bottom-right of batch update modal. Alternative: persistent in top bar. Trade-off: visibility vs accidental clicks.

3. **Email subject line**: 3 candidates proposed. Founder to decide whether to ship with A/B or pick one for launch consistency.

4. **Auto-close window (30 days)**: Could be 21 or 45. Tied to inferred-no-response label confidence. Recommend launching 30, monitor correction rate, tune.

5. **Pro tier dashboard differentiation**: Currently designed identically across Free and Pro. Founder may want Pro-exclusive features (advanced filters, export). Recommend NOT gating analytics — that's the value proof. Gate AI-generation features instead.

6. **Bulk import limit (20 rows)**: Could be 50 with longer scroll. Recommend 20 for V1 to keep onboarding under 5 minutes; raise post-launch if heavily requested.

---

## 17. Summary

The tracking and dashboard UX is the single most consequential surface in the product for moat formation. The design choices encoded:

- Smart-default batch update (stack view + "Still no news" primary) maximises completion rate
- Auto-capture at download captures the suggestion→outcome linkage at point of intent
- Stages-array data model (not status enum) enables per-stage analytics — the unique data asset
- Progressive reveal (5/10/15/25/50) calibrates statistical defensibility AND engagement
- Celebration asymmetry (loud outcomes, quiet effort) preserves user dignity
- No streaks (deliberate rejection) avoids harm to a stressed audience
- Weekly digest only (architecture mandate) respects user inbox
- Tailored vs untailored comparison (Insights zone) makes the value proposition self-demonstrating

If users complete batch updates at ≥80% rate and tracking completeness median reaches ≥70% by Month 6, the moat data flow rate is on track. If those targets miss, the levers are subject lines, friction tuning, and threshold adjustment — not more emails or harder gamification.

The product cannot beg for data. The product must make the dashboard worth keeping accurate. That is the design.

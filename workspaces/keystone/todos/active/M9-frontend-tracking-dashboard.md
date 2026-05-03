# M9 — Frontend: Application Tracking + Dashboard + Settings

> Depends on: M7 (design system), M5 (tracking backend), M6 (payments)
> Implements: workspaces/keystone/03-user-flows/05-07 (tracking, dashboard, gamification)

---

## M9.1 — Applications dashboard page (build)

**What**: The main tracking page — shows active applications, quick stats, and batch check-in banner.

**Layout** (from Analysis 06 §Four-zone dashboard):
- **Zone 1 — Action**: Top banner when nudge-eligible applications exist: "5 applications need a quick check-in (≈30s) →"
- **Zone 2 — Funnel summary**: Personal response rate (if ≥5 apps) + per-stage bar chart
- **Zone 3 — Application list**: Cards, default "Active" view; secondary "All" tab
- **Zone 4 — Insights** (Pro): Trend chart, match-level distribution, benchmark comparison

**Application card design**:
```
┌───────────────────────────────────────────────────────┐
│  DBS · Associate, Digital Banking                      │
│  Applied 8 days ago · via LinkedIn · MatchChip: amber  │
│  Stage: Applied → (waiting)                            │
│  [Update] [View analysis]                              │
└───────────────────────────────────────────────────────┘
```

**Gamification pill**: "Tracking completeness: 72% · Top 30% of users" — persistent top-right of list view. Changes color by tier (Analysis 07).

**Empty state** (no applications yet):
- Illustration + "Your job search will take shape here. Every time you download a tailored resume, we'll ask if you're submitting it."
- CTA: "Analyse a job →"

**Acceptance criteria**:
- Batch check-in banner shows when nudge-eligible apps exist
- Empty state shows when no applications
- Application list shows correct stage indicator
- Gamification pill renders correct tier color

**Implements**: Analysis 06, Analysis 07, workspaces/keystone/03-user-flows/06-dashboard-analytics.md

---

## M9.2 — Applications dashboard wire

**What**: Wire dashboard to real backend data.

**API calls**:
- `GET /api/applications` (M5.1)
- `GET /api/analytics/summary` (M5.4)
- `GET /api/analytics/completeness` (M5.5)
- `GET /api/applications/batch-update` (M5.2) — for banner count

**Charts** (Recharts or Tremor):
- Response rate trend line: single line, `brand-500`, no gridlines
- Applications by stage: bar chart with match-level colors
- NEVER pie charts

**Acceptance criteria**:
- Real application data populates list
- Response rate only shown with ≥5 applications
- Chart renders correctly on mobile (responsive, not cut off)

---

## M9.3 — Batch update modal (build)

**What**: The check-in modal — the most important interaction in the tracking system.

**Build** (from Analysis 05 §2):
```
+--------------------------------------------------------------------+
|  Quick check-in                               ✕                    |
|  5 applications · ~30 seconds                                      |
|                                                                     |
|  ┌──────────────────────────────────────────────────────────────┐  |
|  │  DBS · Associate, Digital Banking                             │  |
|  │  Applied 8 days ago · via LinkedIn                            │  |
|  │                                                                │  |
|  │  [ Still no news ]  Got a response · Rejected · More ▾       │  |
|  └──────────────────────────────────────────────────────────────┘  |
|                                                                     |
|  ▢▢▢▢▢  1 of 5                                                     |
|  [Mark all remaining as no news]                                    |
+--------------------------------------------------------------------+
```

**Interaction model**:
- "Still no news" = primary action: card animates left-out (200ms), next card in
- Exception flows inline (card expands — no new modal):
  - "Got a response": date picker + response type selector
  - "Rejected": date picker + rejection stage selector
  - "More ▾": dropdown with Advanced/Withdrew/Offer/Wrong-app
- Keyboard: `Space/Enter` = no news, `R` = response, `X` = rejected, `M` = more
- "Mark all remaining as no news": one-tap bulk clear with 8-second undo toast
- Progress dots + counter at bottom

**Mobile**: full-screen modal, vertically stacked buttons (no horizontal row on <400px)

**Acceptance criteria**:
- 5 apps with "Still no news" each: modal completes in <5 taps
- "Mark all remaining" clears queue in one tap with undo option
- Exception flows (Got response / Rejected) collect required data
- Keyboard shortcuts work
- Completion screen shows time taken + summary counts

**Implements**: Analysis 05 §2 (Batch Update), Analysis 26 §5.1 (timing tokens)

---

## M9.4 — Batch update modal wire

**What**: Wire batch modal to real batch-update API.

**API calls**:
- `GET /api/applications/batch-update` → load nudge-eligible stack
- `POST /api/applications/batch-update` → submit each action
- `POST /api/applications/batch-update/mark-all-no-news` → bulk clear

**Optimistic UI**: card advances immediately; API call fires in background. If API fails: show error toast, allow retry.

**Event logging**: `batch_update.session_complete` fires with duration on modal close.

**Acceptance criteria**:
- "Still no news" submits and advances immediately (no wait for API)
- "Got a response" creates stage_event in DB (verify)
- Duration logged to PostHog

---

## M9.5 — Stage progression + celebration flows (build + wire)

**What**: Advancement celebration and interview prep handoff.

**Advancement modal** (from Analysis 05 §3.2):
```
DBS · Associate, Digital Banking
What just happened?
○ Phone screening — passed, advancing to Round 1
○ Round 1 — passed, advancing to Round 2
...
○ Got an offer 🎉

Format of next round: [Phone | Video | In-person | Panel | Technical | Case]
Date of next round: [pick]
[Save advancement]
```

**Celebration screen** (post-advancement):
- Restrained confetti (6-8 geometric shapes, brand colors, 1.2s)
- "You're advancing to Round 2 at DBS. That puts you in the top 30%."
- CTA: "Prepare for Round 2" (placeholder — Phase 2 interview prep)
- "Maybe later" always available

**Offer celebration** (different — Analysis 05 §3.4):
- Larger confetti (2.4s)
- Quick reflection form: "What helped most?" (up to 3 checkboxes)
- Optional: "What surprised you?" (1 sentence free text)
- This is the highest-value moat data capture moment

**Wire**: `POST /api/applications/{id}/stages` with advancement data

**Acceptance criteria**:
- Confetti animation plays at correct duration (1.2s advancement, 2.4s offer)
- Interview prep CTA shows for advancement (routes to Phase 2 placeholder page)
- Offer reflection form data sent to API (verify in DB)
- "Maybe later" always works without pressure

**Implements**: Analysis 05 §3 (Stage Progression), Analysis 28 §Risk 5 (interview prep gap — placeholder UX)

---

## M9.6 — Auto-close correction banner (build + wire)

**What**: Banner that appears at login after auto-close events. Shows company names, allows correction.

**Banner** (from Analysis 05 §4.2):
```
ⓘ 3 applications auto-closed (30 days, no response)
   DBS · GovTech · Accenture
   Got a response from any of these? [Correct] [Looks right]
```

**"Correct" → opens mini-batch-update** with just those 3 applications
**"Looks right" → banner dismissed**, auto-close permanent

**Wire**: `GET /api/applications?filter=recently_auto_closed` on login

**Acceptance criteria**:
- Banner shows after auto-close events (test by manually setting `auto_closed_at` on an app)
- "Correct" opens focused batch update with only the auto-closed apps
- Banner dismissed after "Looks right"

---

## M9.7 — Settings + subscription page (build + wire)

**What**: User settings and subscription management.

**Settings page** (`/settings`):
- Profile: name, email (from Clerk — display only), phone number status
- Subscription: current plan + billing date + "Manage subscription →" (Stripe Portal link)
- Consent management: show each consent type with toggle (revocable)
- Data export: "Export all your data" (PDPA right — download JSON of all user data)
- Delete account: confirmation flow with data deletion
- Dark mode toggle (persisted in localStorage)

**Consent toggles** (per compliance spec):
- Storage, AI Processing, Outcome Tracking, Marketing shown as toggles
- Each toggle has a one-sentence explanation
- Revoking AI Processing: "This will disable AI analysis — you won't see suggestions until you re-enable it."
- Registration consent: shown as read-only (cannot be revoked without deleting account)

**Wire**:
- `GET /api/billing/subscription` → subscription status
- `POST /api/billing/create-portal-session` → Stripe Portal
- `PATCH /api/users/consent/{type}` → consent updates
- `GET /api/users/export` → data export download
- `DELETE /api/users/account` → account deletion (with confirmation)

**Acceptance criteria**:
- Stripe Portal link opens correct portal for user's subscription
- Consent revoke works: disable AI Processing → analysis page shows "AI analysis disabled" message
- Data export: downloads JSON file with user's data
- PDPA statement visible in footer: "PDPA Compliant · Your data stays in Singapore · You can delete everything anytime"

**Implements**: specs/compliance.md §Consent Architecture, specs/mvp-scope.md §Compliance done criteria

---

## M9.8 — Onboarding questionnaire + persona detection (build + wire)

**What**: 2-question onboarding after signup to personalize copy and detect user persona.

**Questions** (shown once, after signup, before first analysis):
1. "What brings you to KeyStone today?"
   - Fresh grad, entering workforce
   - Switching industry or function
   - Back on the market (PMET/retrenched)
   - Currently employed, exploring options
2. "How many jobs have you applied to recently?"
   - None yet
   - 1-10
   - 11-50
   - 50+

**Persona derivation**:
- Fresh grad: answer 1 = "Fresh grad"
- Mid-career: answer 1 = "Switching industry"
- PMET: answer 1 = "Back on the market"

**Bulk import** (shown on same screen if answer 2 is "1-10" or more):
- "Add them quickly so we can track from where you are" — compact table entry (from Analysis 05 §1.3)

**Acceptance criteria**:
- Persona stored on user record
- Bulk import creates applications correctly (no suggestion_set_id — control group)
- Onboarding shown exactly once per user

**Implements**: Analysis 21 §Stage 6, Analysis 26 §4.2 (per-persona tone)


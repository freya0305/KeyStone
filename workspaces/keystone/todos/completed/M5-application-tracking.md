# M5 — Application Outcome Tracking

> Depends on: M0.2, M1.1 (auth), M2.5 (download trigger)
> The application tracking is the retention feature and the source of the outcome data moat.
> Implements: specs/product.md §Feature 4, workspaces/keystone/03-user-flows/05-application-tracking-flow.md

---

## M5.1 — Application data model + CRUD API

**What**: Application record management with stage-based data model (not a simple status enum).

**Data model** (from specs/product.md §Feature 4):
```sql
-- Main application record
applications (
  id uuid pk,
  user_id uuid NOT NULL,
  job_analysis_id uuid REFERENCES job_analyses(id) nullable,
  suggestion_set_id uuid nullable,  -- links to which suggestions were applied — causal data
  employer text NOT NULL,
  role text NOT NULL,
  applied_date date,
  source text,  -- MCF|JobStreet|LinkedIn|Direct|Referral|Other
  status text DEFAULT 'applied',  -- applied|responded|screening|interviewing|decided|withdrawn
  final_outcome text,  -- no_response|rejected|offer_received|withdrawn
  notes text,
  auto_closed_at timestamptz,
  created_at timestamptz,
  updated_at timestamptz
)

-- Stage events (child table — normalized for analytics queries)
application_stages (
  id uuid pk,
  application_id uuid NOT NULL REFERENCES applications(id),
  stage_type text NOT NULL,  -- response|screening|interview|final|offer|rejection|withdrawal
  round_number int,  -- 1-5 for interviews
  format text,  -- email|phone|video|in-person|assessment_centre|panel|technical|case
  outcome text,  -- passed|failed|pending|withdrawn
  stage_date date,
  notes text,
  created_at timestamptz
)
```

**Note**: Also maintain `stages jsonb` on `applications` for fast single-record reads. Both representations kept in sync via trigger or service layer (write to both tables).

**CRUD endpoints**:
- `POST /api/applications` — create (manual or from download trigger)
- `GET /api/applications` — list user's applications (status filter, pagination)
- `GET /api/applications/{id}` — detail with full stages
- `PATCH /api/applications/{id}` — update status/notes
- `DELETE /api/applications/{id}` — soft delete (retain for analytics, hide from user; PDPA disclosure required)
- `POST /api/applications/{id}/stages` — add stage event
- `PATCH /api/applications/{id}/stages/{stage_id}` — edit/correct stage

**Important analytics linkage**: `suggestion_set_id` on application record links to `job_analysis_id` → `suggestions` table. This is the causal chain: suggestion → application → outcome. Must be set when application is created from download trigger.

**Acceptance criteria**:
- Application created from download trigger has `suggestion_set_id` populated
- Manual application has `suggestion_set_id = null` (control group)
- Stage event addition updates both `application_stages` table and `applications.stages` JSONB
- Soft delete: application hidden from user but retained in DB

**Implements**: specs/product.md §Feature 4 (data model), workspaces/keystone/03-user-flows/05-application-tracking-flow.md §1

---

## M5.2 — Batch update API

**What**: Power the batch quick-update UI. Users review multiple applications at once; the default action is "no news" (one tap per app). This is the highest-frequency data collection interaction.

**Endpoints**:
- `GET /api/applications/batch-update` — returns applications that are "nudge-eligible" (aged into check-in window, not recently reviewed)
- `POST /api/applications/batch-update` — bulk update: array of `{application_id, action: "no_news|got_response|rejected|advanced"}` + optional stage detail for non-no-news actions
- `POST /api/applications/batch-update/mark-all-no-news` — single call clears entire batch (for the "mark all remaining" button)

**Nudge-eligible logic** (from Analysis 05):
```
Application is nudge-eligible if:
  status IN ('applied', 'responded') AND
  final_outcome IS NULL AND
  auto_closed_at IS NULL AND
  last_activity_at < NOW() - interval_for_nudge_window AND
  user has not visited application detail page in last 24h
Nudge windows: 7 days, 14 days, 21 days since applied_date
```

**Optimistic UI support**: batch-update endpoint returns 200 immediately and writes asynchronously. Client can proceed without waiting. If async write fails (very rare): reconcile on next page load.

**Analytics event logged**: `batch_update.session_complete` with `{session_id, app_count, no_news_count, response_count, rejection_count, duration_seconds, mark_all_used}` — the `duration_seconds` is a UX quality metric.

**Acceptance criteria**:
- Only nudge-eligible applications returned (not ALL active applications)
- "Mark all no news" clears entire batch in single API call
- Batch update completes in <1.5 seconds for 30 applications
- Event logged on session complete with duration

**Implements**: specs/product.md §Feature 4 (Batch quick-update UI), Analysis 05 §2 (Batch Update)

---

## M5.3 — 30-day auto-close background job

**What**: Silent auto-close of applications with no activity for 30 days. Marks as `auto_closed_no_response`. Does NOT delete. User sees correction banner at next login.

**Implementation**:
- Scheduled job: runs daily at 2am SGT (AWS EventBridge → Lambda or Celery beat)
- Query: `SELECT id FROM applications WHERE status NOT IN ('decided', 'withdrawn') AND updated_at < NOW() - INTERVAL '30 days'`
- For each: set `final_outcome = 'no_response'`, `status = 'decided'`, `auto_closed_at = NOW()`
- Write `application_stages` event: `{stage_type: 'rejection', format: 'inferred_no_response', outcome: 'failed', notes: 'Auto-closed after 30 days'}`
- Do NOT notify user at close time; defer to next login (correction banner)

**At next login**: query for applications auto-closed since last login → show correction banner with company names listed

**Idempotency**: job must be safe to run twice (if auto_closed_at already set, skip)

**Dry-run mode**: `--dry-run` flag logs what would be closed without closing

**Acceptance criteria**:
- Integration test: application created 31 days ago → auto-close job runs → status = 'decided', final_outcome = 'no_response'
- Idempotent: running job twice on same application → second run is no-op
- Correction banner: next login after auto-close shows company names for correction

**Implements**: specs/product.md §Feature 4 (Auto-close), Analysis 05 §4

---

## M5.4 — Application analytics (response rate + pass rates)

**What**: Calculate and serve personal response rate and per-stage pass rates for the dashboard.

**Metrics to compute** (per specs/product.md §Feature 4 Dashboard metrics):
- Personal response rate: `applications_with_any_stage_response / total_logged` — shown only after ≥5 applications
- Per-stage pass rates: response rate, response→screen, screen→R1, R1→R2, R1→final, R1→offer
- Applications by stage (histogram)
- Trend line: response rate rolling 30-day
- Match-level distribution: what % of applications at each match level reached R2+

**Calculation approach**: All metrics computed at query time (not pre-aggregated for MVP scale). Materialized views can be added when p95 query time exceeds 500ms.

**Benchmark comparison**: show only when user has ≥15 logged applications (per specs/product.md). SG benchmark data sourced from analyst interview notes (3-6% response rate baseline).

**API**: `GET /api/analytics/summary` → returns all metrics for the dashboard

**Acceptance criteria**:
- Response rate not shown until 5+ applications logged
- Benchmark comparison not shown until 15+ applications logged
- Stage pass rates computed correctly (tested against synthetic dataset of 20 applications)
- p95 query time <500ms for users with ≤200 applications

**Implements**: specs/product.md §Feature 4 (Dashboard metrics), workspaces/keystone/03-user-flows/06-dashboard-analytics.md

---

## M5.5 — Gamification completeness score

**What**: Calculate and serve "tracking completeness %" — the ratio of logged vs unlogged applications, with percentile comparison.

**Formula** (from Analysis 07 §Gamification):
```
completeness = (applications_with_final_outcome_logged + applications_with_stage_events) 
               / total_applications_created
```

**Percentile**: compare user's completeness % to all KeyStone users. At launch (cold start): use fixed benchmarks (bottom quartile = 0-25%, median = 40%, top quartile = 70%+).

**Display tiers** (from Analysis 07):
- 0-39%: Neutral pill, stone color
- 40-69%: Active, brand-primary tint
- 70-99%: Strong, emerald tint, "Great tracking"
- 100%: "All caught up" — special celebration state

**API**: `GET /api/analytics/completeness` → `{score: 0.72, tier: "strong", percentile_rank: "top_30_percent", message: "You're in the top 30% of users"}`

**Accepts criteria**:
- Score updates immediately after any stage event logged
- 100% "All caught up" state triggers once per session (not repeatedly)

**Implements**: specs/product.md §Feature 4 (Gamification), Analysis 07 §tracking completeness


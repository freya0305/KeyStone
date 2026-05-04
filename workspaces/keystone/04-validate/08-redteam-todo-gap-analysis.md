# Red Team — Todo Completeness Gap Analysis

**Date**: 2026-05-04
**Phase**: /redteam — todo audit
**Status**: AUDIT COMPLETE

---

## Executive Summary

The todos are **well-structured and comprehensive** at the feature-specification level. However, there are **17 implementation gaps** between what the todos specify and what the current codebase actually delivers. Most gaps are in backend data models and API endpoints — the todos describe the right work, but the implementation is incomplete.

---

## Critical Gaps (Blocking)

### G1 — SubscriptionTier Enum Wrong (`entities.py:31-35`)

**What**: `SubscriptionTier` has `FREE, SOLO, PRO, TEAM` but actual product has `FREE, BASIC, PRO`.

**Spec**: `specs/business-model.md` (confirmed) — Basic = SGD 9/mo, Pro = SGD 12/mo, NO Solo/Team tier.

**Impact**: Stripe `PRICE_TO_TIER` in `stripe_service.py:35-39` maps `price_solo` and `price_team` — these price IDs don't match the actual product. Users who subscribe will get wrong tiers.

**Fix**: Change `SubscriptionTier` enum to `FREE, BASIC, PRO`; update `PRICE_TO_TIER` to `price_basic` and `price_pro`.

---

### G2 — `application_stages` Child Table Not Implemented (`entities.py:180-206`)

**What**: `Application` model has `stages = Column(JSON, default=list)` (line 192). M5.1 spec requires a separate `application_stages` child table for normalized stage events.

**Spec**: `M5-application-tracking.md:34-44` — child table with `stage_type`, `round_number`, `format`, `outcome`, `stage_date`.

**Impact**: Analytics queries on stages will be slow (JSON extraction). The "normalized for analytics queries" requirement is not met. Batch update and auto-close features (M5.2, M5.3) depend on this structure.

**Fix**: Create `ApplicationStage` model with FK to `Application`. Keep `stages` JSONB column in sync via service layer.

---

### G3 — `suggestion_set_id` Not On `Application` Model (`entities.py:180-206`)

**What**: `Application` model is missing `suggestion_set_id` (FK to `suggestions` or `job_analysis`). M5.1 spec says: "links to which suggestions were applied — causal data."

**Spec**: `M5-application-tracking.md:20` — `suggestion_set_id uuid REFERENCES suggestions(id) nullable`

**Impact**: The core data moat — "suggestion → application → outcome" causal chain — is broken. Analytics cannot determine which suggestions led to which outcomes.

**Fix**: Add `suggestion_set_id` column to `applications` table.

---

### G4 — `user_consents` Table Missing (`entities.py`)

**What**: M1.5 requires a `user_consents` table for six-type per-user consent state. `User` model only has three consent columns (`consent_pdpa`, `consent_marketing`, `consent_ai_training`).

**Spec**: `M1-auth-pdpa.md:119-153` — six consent types: `registration`, `storage`, `ai_processing`, `b2b_sharing`, `outcome_tracking`, `marketing`, `ai_training`.

**Impact**: Consent architecture is incomplete. Cannot properly revoke `storage` consent or gate B2B data sharing.

**Fix**: Create `UserConsent` model with `(user_id, consent_type, granted_at, revoked_at)`. Replace the three consent columns on `User`.

---

### G5 — NRIC Masking Utilities Not Implemented

**What**: M1.4 requires `src/core/nric.py` with `detect_nric()`, `mask_nric()`, `assert_no_nric()`. No such file exists.

**Spec**: `M1-auth-pdpa.md:84-116` — three-stage pipeline: mask at S3 upload → assert before Claude API → sanitize Claude output.

**Impact**: PDPA compliance risk. NRIC numbers in resumes could be sent to Claude API or stored/logged.

**Fix**: Create `keystone/core/nric.py` with the three functions. Integrate at upload pipeline and before Claude calls.

---

### G6 — SMS Phone Verification Not Implemented

**What**: M1.3 requires `/api/auth/phone/send-otp` and `/api/auth/phone/verify` endpoints. No such routes exist.

**Spec**: `M1-auth-pdpa.md:59-80` — Twilio OTP, +65 SG numbers, 6-digit code, 10-min expiry, 3-attempt lockout, phone hash stored.

**Impact**: Anti-abuse gate missing. Unlimited first-analysis gate is vulnerable to multi-account abuse.

**Fix**: Implement Twilio OTP endpoints. Add `phone_hash` column to `User`. Add `phone_verified` flag.

---

### G7 — Stripe `PRICE_TO_TIER` References Non-Existent Price IDs

**What**: `stripe_service.py:35-39` maps `price_solo`, `price_team`, `price_pro`. Actual Stripe prices are `price_basic`, `price_pro`.

**Impact**: Subscription upgrades/downgrades will map to wrong tiers or `FREE` (fallback).

**Fix**: Update `PRICE_TO_TIER` to match actual Stripe price IDs.

---

## High Priority Gaps

### G8 — `last_activity_at` Column Missing From Application

**What**: M5.2 nudge-eligible logic requires `last_activity_at` on `Application` model. Not present.

**Spec**: `M5-application-tracking.md:80-88` — nudge eligibility depends on "user has not visited application detail page in last 24h".

**Fix**: Add `last_activity_at` column, update on every application detail page view.

---

### G9 — `auto_closed_at` Column Missing From Application

**What**: M5.3 auto-close job sets `auto_closed_at`. Not present in `Application` model.

**Spec**: `M5-application-tracking.md:107-113`.

**Fix**: Add `auto_closed_at` column to `applications` table.

---

### G10 — Batch Update API Not Implemented

**What**: M5.2 requires:
- `GET /api/applications/batch-update`
- `POST /api/applications/batch-update`
- `POST /api/applications/batch-update/mark-all-no-news`

None of these endpoints exist.

**Fix**: Implement batch-update endpoints with nudge-eligible logic.

---

### G11 — Auto-Close Background Job Not Implemented

**What**: M5.3 requires a daily scheduled job (2am SGT) to auto-close applications with no activity for 30 days.

**Spec**: `M5-application-tracking.md:104-126`.

**Fix**: Implement Celery beat task or AWS EventBridge + Lambda for auto-close.

---

### G12 — Analytics Endpoints Not Implemented

**What**: M5.4 requires `GET /api/analytics/summary`. M5.5 requires `GET /api/analytics/completeness`.

**Spec**: `M5-application-tracking.md:130-181`.

**Fix**: Implement analytics endpoints with response rate, per-stage pass rates, completeness score.

---

### G13 — `b2b_aggregate_reports` Table Missing

**What**: M0.2 spec references `b2b_aggregate_reports` table. Not in `entities.py`.

**Spec**: `M0-foundation.md` (M0.2 B2B data model).

**Fix**: Add `B2BAggregateReport` model if the spec requires it.

---

### G14 — Rate Limiting Not Wired to Endpoints

**What**: `rate_limit.py` exists but `analyze_match` and other endpoints don't use it.

**Spec**: `M3-job-analysis-engine.md` (M3.6 rate limiting).

**Fix**: Wire `RateLimiter` to `/api/analyze/guest` and authenticated analyze endpoints.

---

### G15 — RLS Enforcement Missing

**What**: B2B tables (`b2b_tenants`, `b2b_users`, `b2b_job_descriptions`) have `tenant_id` but no RLS enforcement in middleware or queries.

**Spec**: `M0-foundation.md` and `entities.py:4` ("RLS must be enforced at database level").

**Fix**: Add RLS middleware or DataFlow-level tenant filtering on all B2B queries.

---

### G16 — `ConsentService` Not Implemented

**What**: M1.5 references `ConsentService.has_consent()`, `.grant()`, `.revoke()`. No such service exists.

**Spec**: `M1-auth-pdpa.md:133-136`.

**Fix**: Create `ConsentService` in `keystone/services/consent.py`.

---

### G17 — `get_current_b2b_user` and `require_tenant_access` Defined But Not Wired

**What**: `clerk_auth.py:195-230` defines `get_current_b2b_user` and `require_tenant_access` but no B2B endpoints use them.

**Spec**: Recruiter endpoints in `b2b_onboarding.py` and `jd_generator.py` should use these.

**Fix**: Wire `get_current_b2b_user` to recruiter endpoints.

---

## Todo Quality Assessment

| Todo | Coverage | Gap Count |
|------|----------|-----------|
| M0-foundation | Good | 1 (b2b_aggregate_reports) |
| M1-auth-pdpa | Good | 3 (NRIC utils, SMS OTP, ConsentService) |
| M2-resume-processing | Partial | PDF/DOCX parsing not wired |
| M3-job-analysis-engine | Partial | Rate limiting not wired |
| M4-suggestions-engine | ? | Could not verify |
| M5-application-tracking | Good | 5 (stages table, suggestion_set_id, batch API, auto-close, analytics) |
| M6-payments | Partial | Stripe PRICE_TO_TIER wrong |
| KY3-pricing | WRONG | References $69/$179, actual is SGD 9/12 |
| M7-M9 (frontend) | ? | Frontend not verified |

---

## Recommendations

1. **Fix SubscriptionTier + Stripe mapping first** — payments are broken until this is fixed
2. **Add missing data models** — `application_stages`, `user_consents`, `suggestion_set_id`, `last_activity_at`, `auto_closed_at`
3. **Implement M1.4 NRIC utilities** — PDPA compliance depends on this
4. **Implement M1.3 SMS OTP** — anti-abuse depends on this
5. **Fix KY3 todos** — update pricing references to SGD 9/12
6. **Implement M5 batch/analytics** — retention features depend on data model fixes

---

## Verified File References

| File | Line(s) | Issue |
|------|---------|-------|
| `src/keystone/models/entities.py` | 31-35 | Wrong SubscriptionTier enum |
| `src/keystone/models/entities.py` | 180-206 | Application missing fields |
| `src/keystone/services/stripe_service.py` | 35-39 | PRICE_TO_TIER references old tiers |
| `src/keystone/services/clerk_auth.py` | 195-230 | B2B deps defined but unused |
| `src/keystone/api/job_seeker.py` | — | Rate limiting not wired |

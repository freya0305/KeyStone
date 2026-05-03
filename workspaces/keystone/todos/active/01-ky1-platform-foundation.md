# KY1 — Platform Foundation (Unblocks Everything)

> Core infrastructure: FastAPI + PostgreSQL + Redis + Claude API layer with circuit breaker.
> All other tracks depend on this.

---

## KY1.1 — Project Scaffold + Tech Stack Decision

**What**: Set up the FastAPI backend project with all dependencies.

**Deliverables**:
- `src/` with FastAPI app structure
- `pyproject.toml` with pinned deps: fastapi, uvicorn, sqlalchemy, alembic, psycopg2-binary, redis, pydantic, python-dotenv, structlog, httpx
- `.env.example` with all env vars
- `docker-compose.yml` for local dev: API + PostgreSQL 16 + Redis
- `/health` endpoint with DB connection check

**Acceptance**: `uvicorn src.main:app` starts clean, `/health` returns `{"status": "ok"}`

---

## KY1.2 — Database Schema + RLS

**What**: Create all tables with Row-Level Security enforced.

**Tables**:
```sql
-- 求职者端
users (id, email, name, subscription_tier, created_at)
resumes (id, user_id, content_hash, parsed_json, s3_key, created_at)
job_analyses (id, user_id, resume_id, job_url, job_parsed_json, match_results, created_at)
suggestions (id, job_analysis_id, section, original_text, suggested_text, rationale, created_at)
suggestion_signals (id, user_id, suggestion_id, action, modified_text, context, created_at)
applications (id, user_id, job_analysis_id, applied_date, status, employer, role, created_at)

-- 猎头端
b2b_tenants (id, name, type, contract_value, seat_count, created_at)
b2b_users (id, user_id, tenant_id, access_level, provisioned_at)
b2b_job_descriptions (id, tenant_id, user_id, title, company, skills_json, content, brand_template, created_at)
b2b_share_links (id, jd_id, expires_at, view_count, created_at)
b2b_templates (id, tenant_id, name, logo_s3_key, brand_colors, created_at)
```

**RLS**: Must enforce tenant isolation on all `b2b_*` tables. User A in Tenant A cannot see User B in Tenant B's data.

**Acceptance**: Fresh DB runs all migrations cleanly, RLS prevents cross-tenant access.

---

## KY1.3 — Claude API Layer with Circuit Breaker

**What**: Unified Claude API client with cost tracking and circuit breaker.

**Deliverables**:
- `src/ai/client.py` — Claude Haiku/Sonnet/Mixtral routing
- Cost tracking per user per month (Redis counter)
- **Circuit breaker**: if Claude API fails 5 times in a row, open circuit for 60s, return graceful error
- Per-request budget: max 4K tokens input for Haiku (prevent overflow truncation)
- All model names from env vars only

**Acceptance**:
- Circuit breaker trips after 5 failures, recovers after 60s
- Haiku requests capped at 4K input tokens
- Cost tracked in Redis, graceful degradation at SGD 5/user/month

---

## KY1.4 — Stripe Integration (Webhook + Checkout)

**What**: Stripe billing integration with proper webhook handling.

**Deliverables**:
- Stripe checkout session creation (Solo/Pro/Team tiers)
- **Webhook handler** (CRITICAL — red team finding F1): `POST /webhooks/stripe` with signature verification
- Updates subscription_tier on successful payment
- Idempotency: same event processed only once
- Free tier: 10 analyses/month

**Acceptance**:
- Webhook processes `checkout.session.completed` and `customer.subscription.deleted`
- No duplicate processing on webhook retry
- Subscription status synced correctly

---

## KY1.5 — Auth + PDPA Consent

**What**: JWT auth with PDPA consent flow.

**Deliverables**:
- `/auth/register`, `/auth/login`, `/auth/refresh`
- JWT in HttpOnly cookie, 24h expiry
- `user_consents` table tracking: PDPA consent, marketing opt-in
- NRIC detection: flag if user uploads document containing NRIC pattern, never store NRIC

**Acceptance**:
- Login returns JWT, protected routes require valid JWT
- NRIC regex pattern detected and redacted from any stored content

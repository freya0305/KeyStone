# M0 — Project Foundation & Dev Environment

> Prerequisite for all other milestones. Unblocks M1–M6 (backend) and M7–M9 (frontend) in parallel.
> Implements: specs/technical.md §Tech Stack

---

## M0.1 — Backend framework decision + project scaffold

**What**: Evaluate FastAPI vs Kailash Nexus for the Python API backend. Make the decision and scaffold the chosen framework. This decision must be made before any backend code is written.

**Decision criteria**:
- Kailash Nexus: use if it provides HTTP endpoints, auth middleware, task queues, and async support out-of-the-box with less custom code
- FastAPI: use if Kailash Nexus adds complexity without sufficient benefit for this domain

**Deliverables**:
- Decision documented in specs/technical.md §Backend decision
- Project scaffold at `src/` with: entry point, router structure, dependency injection setup, environment config loading
- `pyproject.toml` with all dependencies pinned
- `.env.example` with all required environment variable names (keys from .env, never values)
- `docker-compose.yml` for local dev: API + PostgreSQL 16 + Redis

**Acceptance criteria**:
- `uvicorn src.main:app` (or equivalent) starts with zero errors
- `/health` endpoint returns `{"status": "ok"}` with real DB connection check
- All model names in `.env` only — never hardcoded

**Implements**: specs/technical.md §Tech Stack, §Infrastructure

---

## M0.2 — Database schema + migration setup

**What**: Define all PostgreSQL tables, indexes, and row-level security policies. Set up Alembic for schema migrations.

**Tables to create** (from specs/technical.md §Data Model):
```sql
users (id uuid pk, email text unique, name text, created_at, subscription_tier, consent_flags jsonb)
resumes (id uuid pk, user_id fk, content_hash text, parsed_json jsonb, sg_flags jsonb, s3_key text, created_at)
job_analyses (id uuid pk, user_id fk, resume_id fk, job_url text, job_parsed_json jsonb, company_type text, match_results_json jsonb, created_at)
suggestions (id uuid pk, job_analysis_id fk, section text, original_text text, suggested_text text, rationale text, sg_context jsonb, created_at)
suggestion_signals (id uuid pk, user_id uuid, suggestion_id fk, action text, modified_text text, context_company_type text, context_role_level text, context_industry text, context_ns_related boolean, created_at)
applications (id uuid pk, user_id fk, job_analysis_id fk nullable, applied_date date, status text, stages jsonb default '[]', final_outcome text, source text, notes text, employer text, role text, suggestion_set_id uuid nullable, created_at, updated_at)
b2b_tenants (id uuid pk, name text, type text, contract_value numeric, seat_count int, created_at)
b2b_users (id uuid pk, user_id fk, tenant_id fk, provisioned_at, access_level text)
b2b_aggregate_reports (id uuid pk, tenant_id fk, cohort_period text, aggregate_stats_json jsonb, generated_at)
user_consents (id uuid pk, user_id fk, consent_type text, granted boolean, granted_at, revoked_at nullable)
```

**PostgreSQL RLS policies**: `applications` and `b2b_users` must have RLS policies preventing cross-tenant access. Must be enabled before B2B launch.

**Indexes**: content_hash on resumes (hash index), user_id on all user-linked tables, created_at on suggestion_signals and applications for analytics queries.

**Acceptance criteria**:
- All migrations run cleanly on fresh PostgreSQL 16 instance
- `alembic upgrade head` idempotent
- RLS policies tested: tenant A cannot read tenant B's application data
- suggestion_signals table exists with all context fields

**Implements**: specs/technical.md §Data Model, specs/compliance.md §B2B PDPA

---

## M0.3 — Frontend project scaffold (Next.js 14)

**What**: Create the Next.js 14 frontend project with the project's chosen design system configuration. This is the canonical starting state for all frontend milestones.

**Deliverables**:
- `apps/web/` with Next.js 14 App Router, TypeScript strict mode
- Tailwind CSS config with all design system tokens (from Analysis 26):
  - Brand primary: `#1E7A8C` (brand-primary-500) through full scale
  - Neutral: stone-* scale (warm gray, not cool)
  - Match levels: strong `#1F8F5F`, transferable `#C68A1A`, addressable `#D97338`, fundamental `#8B4A8B`
  - Motion tokens: instant 80ms, fast 160ms, base 240ms, slow 360ms
  - Dark mode CSS variables
- `app/globals.css` with all CSS custom properties (light + dark mode)
- shadcn/ui installed and configured
- Inter Variable + Fraunces (or Instrument Serif) + JetBrains Mono font loading
- CJK fallback chain configured
- ESLint + Prettier with project rules
- `@/` path alias configured

**Acceptance criteria**:
- `npm run dev` starts with zero errors
- Tailwind IntelliSense resolves all custom tokens
- shadcn CLI can add new components
- Dark mode toggle works in Storybook

**Implements**: specs/technical.md §Tech Stack, workspaces/keystone/01-analysis/26-design-system-recommendations.md §Part 1-2

---

## M0.4 — CI/CD pipeline setup

**What**: GitHub Actions CI pipeline for both backend (Python) and frontend (Next.js).

**Backend CI**:
- pytest (Tier 1 unit tests, exit on failure)
- mypy --strict
- ruff linting
- Runs on: every PR to main

**Frontend CI**:
- TypeScript type checking (`tsc --noEmit`)
- ESLint
- `next build` (build must succeed)
- Runs on: every PR to main

**Deployment** (Phase 1 — manual deploy, CI just validates):
- No auto-deploy in MVP; founders deploy manually to AWS
- Build artifacts validated in CI

**Acceptance criteria**:
- PR fails CI if tests fail, types fail, or build fails
- CI runs in <5 minutes for both repos
- Badge in README shows CI status

**Implements**: specs/technical.md §Infrastructure

---

## M0.5 — Logging + monitoring baseline

**What**: Structured logging and token usage monitoring from Day 1. Required before any LLM calls are made.

**Backend**:
- Structured JSON logging (use `structlog` or similar)
- Every Claude API call logs: model, tokens_in, tokens_out, cost_sgd_estimate, cache_hit (boolean), endpoint
- LLM cost per user per month tracked in Redis (key: `llm_cost:{user_id}:{YYYY-MM}`)
- `/admin/costs` endpoint (internal only, no auth gate in MVP) showing daily LLM spend

**Why Day 1**: LLM cost ceiling (SGD 5/user/month) must be enforced before real users hit the system. Retrofitting cost tracking is a data loss event.

**Acceptance criteria**:
- Every Claude API call logged with token counts
- Redis counter for per-user monthly LLM cost updates correctly
- When monthly cost exceeds SGD 5, graceful degradation returns cached/simplified results (not an error)

**Implements**: specs/technical.md §AI Cost Model


# Technical Spec — KeyStone

> Last updated: 2026-04-29 (Phase 01 Analysis)
> Stack choices from brief; backend framework (FastAPI vs Kailash Nexus) TBD.

---

## Tech Stack

| Component | Choice | Rationale |
|-----------|--------|-----------|
| Frontend | Next.js 14+ + Tailwind CSS + shadcn/ui | Performance, SSR for SEO, mature component library |
| Backend | Python FastAPI (evaluate Kailash Nexus as alternative — DECISION PENDING) | AI ecosystem, async support |
| Database | PostgreSQL 16+ | Relational data, row-level security for B2B multi-tenancy |
| AI Engine | Claude Haiku (extraction) + Claude Sonnet (analysis + suggestions) | Two-tier routing for cost control |
| Auth | Clerk | Google OAuth, email, future university SSO (SAML) |
| Payments | Stripe (Singapore) | SGD billing, local payment methods, Stripe Tax |
| File Storage | AWS S3 (ap-southeast-1) | PDPA data residency |
| Hosting | AWS (ap-southeast-1) | Singapore region, PDPA compliance |
| Monitoring | TBD (DataDog or AWS CloudWatch) | Token usage monitoring from Day 1 |

**Backend decision pending**: Python FastAPI is the brief's choice. Kailash Nexus/Kaizen/DataFlow could replace significant custom backend code. This decision must be made before coding begins. See open question in brief.

---

## AI Architecture

### Two-Tier Model Routing

| Task | Model | Rationale |
|------|-------|-----------|
| Job URL parsing (extract requirements) | Claude Haiku | Low reasoning complexity; high volume; cost-sensitive |
| Resume parsing (extract structured data) | Claude Haiku | Extraction task; Haiku sufficient |
| Company type detection | Claude Haiku | Classification; fast + cheap |
| Four-level match assessment | Claude Sonnet | Nuanced judgment; requires SG context reasoning |
| Line-by-line revision suggestions | Claude Sonnet | Core value; quality-critical; worth the cost |
| SG-specific intelligence flags (NRIC, photo, NS) | Claude Haiku | Rule-based detection; Haiku handles well |

**Cost ceiling**: Hard limit of SGD 5/user/month on LLM spend. Graceful degradation: serve cached results when ceiling is reached. This must be implemented before launch — not post-launch.

**Enforcement mechanism**:
1. Redis counter per user per month tracking LLM spend (token cost × model price)
2. At 80% of budget (SGD 4/user/month): route to Haiku-only tier (no Sonnet calls)
3. At 100% of budget (SGD 5/user/month): serve cached results only; block live Sonnet calls
4. Counter resets monthly; logged for analytics

### Prompt Architecture

All Claude API calls must use:
- Prompt caching (for system prompts containing SG intelligence rules — these are long and static)
- Model ID from `.env` only (never hardcoded)
- Zero data retention configuration (Anthropic API header: `anthropic-beta: prompt-caching-2024-07-31`)

**SG Intelligence System Prompt** (served as cached system prompt to all Sonnet calls):
- GLC entity list (Temasek portfolio companies, statutory boards, government agencies)
- MNC SG presence list (major multinationals with SG operations)
- NS framing rules per vocation category (combat, logistics, signals, administrative, command)
- Resume photo conventions per company type
- SG education hierarchy context
- Common SG industry/role vocabulary

**Update cadence**: SG intelligence rules updatable via `.env`-referenced config file — not hardcoded in prompts. This allows intelligence updates without code deploys.

---

## Learning Loop Architecture (MUST design before coding)

Every suggestion interaction must log to a signals table:

```
suggestion_signals {
  id: uuid
  user_id: uuid (anonymised — not linked to PII in this table)
  suggestion_id: uuid (links to the specific suggestion generated)
  action: enum(ACCEPTED, REJECTED, MODIFIED)
  modified_text: text (if MODIFIED)
  context_company_type: enum(GLC, MNC, SME, STARTUP, GOVERNMENT)
  context_role_level: enum(ENTRY, MID, SENIOR, MANAGEMENT)
  context_industry: text
  context_ns_related: boolean
  created_at: timestamp
  application_outcome_id: uuid nullable (linked if user logs outcome)
}
```

**PDPA note**: This table must be covered by "AI Training Data" consent (see compliance.md). Users must explicitly opt-in (separate checkbox, not pre-ticked) before their suggestion feedback is used for model training.

**Purpose**: Signal data feeds future model fine-tuning to improve SG-specific suggestion quality. Static SG intelligence is replicable in 90 days; a model trained on 50K+ real SG user accept/reject signals is not.

---

## Data Model (High-Level)

```
users
  id, email, name, created_at, subscription_tier, consent_flags

resumes
  id, user_id, content_hash, parsed_json, sg_flags, created_at, s3_key
  -- s3_key: reference to masked resume in S3

job_analyses
  id, user_id, resume_id, job_url, job_parsed_json, company_type, match_results_json, created_at

suggestions
  id, job_analysis_id, section, original_text, suggested_text, rationale, sg_context, created_at

suggestion_signals
  id, user_id (anon), suggestion_id, action, context_fields..., created_at

applications
  id, user_id, job_analysis_id, submitted_at, status, outcome_stage, notes, created_at

b2b_tenants
  id, name, type (UNIVERSITY|WSG|AGENCY), contract_value, seat_count, created_at

b2b_users
  id, user_id, tenant_id, provisioned_at, access_level

b2b_aggregate_reports
  id, tenant_id, cohort_period, aggregate_stats_json, generated_at
```

**Row-level security**: B2B tenant data (b2b_users, applications by tenant) must use PostgreSQL RLS policies to prevent cross-tenant data access. RLS must be implemented before B2B launch.

---

## Caching Strategy

| Cache Target | TTL | Reason |
|-------------|-----|--------|
| Resume analysis (same content hash) | 30 days | Same resume + different jobs doesn't re-analyse |
| Job parsing (same URL) | 7 days | Job posting unlikely to change in a week |
| SG intelligence system prompt | Anthropic prompt cache (5 min TTL) | Expensive long system prompt; cache per API session |
| User session (Clerk) | Per Clerk config | Auth session management |

**No caching**: suggestion results (these are per-user, per-job, quality-critical)

---

## AI Cost Model

**Estimated cost per Pro user per month** (at typical usage — 20 analyses/month):

| Operation | Volume | Model | Cost Estimate |
|-----------|--------|-------|---------------|
| Job parsing (URL) | 20× | Haiku | ~USD 0.05–0.10 |
| Resume-job match assessment | 20× | Sonnet | ~USD 0.15–0.20 |
| Revision suggestions | 20 jobs × 10 suggestions avg | Sonnet | ~USD 0.20–0.30 |
| Infrastructure (AWS, Clerk, Stripe, etc.) | — | — | ~USD 0.50–1.00 |
| **Total estimated** | | | **USD 0.90–1.60 = ~SGD 1.22–2.16** |

Actual margin at SGD 12/mo with ~SGD 2.16 cost = **~82% gross margin** at typical usage. The brief's 75% estimate is conservative; actual cost model needs calibration with real usage data in Week 1.

**P95 user risk**: A heavy user running 100+ analyses/month could cost SGD 8–15 in LLM calls. The SGD 5/month ceiling with graceful degradation (serve cached/simpler results) is the correct architectural guard.

---

## Infrastructure Requirements

- **AWS ap-southeast-1**: All compute, storage, and database
- **S3**: Resume storage (masked), file parsing worker output
- **RDS PostgreSQL 16+**: Primary database with RLS
- **ECS or Lambda**: API workers (if FastAPI) or Kailash Nexus workers
- **ElastiCache Redis**: Session cache, job parsing cache
- **CloudWatch / DataDog**: Token usage monitoring from Day 1 (cost control)
- **Route53**: DNS
- **ACM**: SSL certificates
- **Stripe Webhook**: Payment event processing

**Minimum viable infrastructure cost**: SGD 500–2,000/month at launch scale (< 1,000 active users).

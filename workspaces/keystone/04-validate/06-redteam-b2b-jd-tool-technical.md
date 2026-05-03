# Red Team: KeyStone B2B JD Tool — CTO/Technical Architect Review

**Reviewer:** Analysis Specialist
**Date:** 2026-05-03
**Documents Reviewed:**
- `workspaces/keystone/02-plans/06-b2b-jd-tool-backend-architecture.md`
- `workspaces/keystone/02-plans/04-technical-architecture.md`

---

## Executive Summary

The architecture is viable for MVP launch but contains **five HIGH-severity findings** that must be addressed before scaling to 500+ organizations. The most critical risks are: (1) single-vendor AI dependency with no circuit breaker or fallback, (2) Haiku's 4K context window is dangerously close to the token budget for complex JDs, (3) Stripe webhook deferral creates a subscription status gap that enables billing fraud, (4) RLS is deferred to v1.1 while the architecture explicitly mandates org-level isolation, and (5) NRIC detection is scoped to only the `requirements` field, leaving three other user-supplied text fields unprotected.

**Complexity: Moderate** — straightforward fixes for most findings; the AI vendor strategy requires a real architectural decision.

---

## Risk Register

| Risk | Likelihood | Impact | Severity | Mitigation Owner |
|------|------------|--------|----------|-----------------|
| Claude API outage kills all JD generation | High | Critical | **HIGH** | Backend |
| Haiku 4K context exceeded by complex JDs | Medium | Major | **HIGH** | Backend/AI |
| Stripe webhook deferred causes subscription bypass | Medium | Critical | **HIGH** | Payments |
| RLS not enforced on Day 1, org data leaks | Low | Critical | **HIGH** | Security |
| NRIC detection gap in 3 of 6 text fields | Medium | Major | **HIGH** | Security/Backend |
| Analytics table grows unbounded, query degradation | High | Significant | **MEDIUM** | Backend |
| No Claude API budget caps, runaway spend | Medium | Major | **MEDIUM** | Finance/DevOps |
| Silent AI failures leave user with no output | Medium | Major | **MEDIUM** | Backend |
| Cached JD served after model version change | Low | Minor | **LOW** | Backend |
| No backup/recovery strategy documented | Low | Major | **LOW** | DevOps |

---

## 1. Scalability to 500+ Orgs

### Finding S1 — Analytics Table Growth (MEDIUM)

**Evidence:** `analytics_events` table stores one row per user action. At 500 orgs with 10 users each, averaging 10 events/day (generate, edit, export, share), the table grows at:

```
500 orgs × 10 users × 10 events × 30 days = 1.5M rows/month
```

No partition strategy is defined. No TTL enforcement beyond soft-delete cleanup. `event_data JSONB` without a GIN index makes aggregate reporting queries slow.

**Impact:** Page load for org analytics dashboard degrades as table grows. Report generation for monthly billing attribution becomes slow or times out.

**Mitigation:**
```sql
-- Partition by month on created_at
CREATE TABLE analytics_events (
  ...
) PARTITION BY RANGE (created_at);

-- Or: TTL enforcement via partition + DROP
CREATE TABLE analytics_events_2026_05 PARTITION OF analytics_events
  FOR VALUES FROM ('2026-05-01') TO ('2026-06-01');
```

**Acceptable if:** Analytics are decoupled from the transactional path via a queue (see §4, Finding S5).

---

### Finding S2 — Redis Memory Budget (LOW)

500 orgs × 50 cached JDs × ~2KB per cached JD = 50MB. With templates and rate limit counters, Redis memory stays well under the free tier ElastiCache limit (750MB). Not a scaling concern at 500 orgs.

---

### Finding S3 — PostgreSQL Connection Pool (MEDIUM)

No connection pool configuration documented. FastAPI with asyncpg default pool is 5 connections. At 500 orgs with 10 concurrent users each, 5,000 potential concurrent users, the pool will exhaust.

**Required configuration:**
```python
# src/core/database.py
from asyncpg import Pool
pool = Pool(min_size=10, max_size=50)  # or per-org sizing
```

---

## 2. Critical Technical Risks

### Finding S4 — Single-Vendor AI With No Circuit Breaker (HIGH)

**Evidence:** `claude.py` calls Claude API directly with no fallback model, no retry with backoff, and no circuit breaker. If Anthropic has an outage or returns elevated error rates, the entire JD generation pipeline fails for all 500 orgs simultaneously.

**Current state:**
```python
# src/core/claude.py — assumed implementation
response = anthropic.messages.create(model="claude-haiku-4", ...)
```

**Required:**
```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
async def generate_jd_with_fallback(prompt: str, org_id: str) -> str:
    try:
        return await claude_haiku.generate(prompt)
    except AnthropicRateLimitError:
        return await claude_sonnet.generate(prompt)  # fallback
    except Exception as e:
        raise JDGenerationError(f"AI unavailable: {e}") from e
```

**Why this is HIGH:** A 30-minute Anthropic outage kills the product for all 500 orgs. Recruitment agencies cannot generate JDs. Churn risk is immediate and high.

---

### Finding S5 — Haiku 4K Context Window Overflow (HIGH)

**Evidence:** Haiku 4 has a 4K token context window (~3,000 words). A complex JD with:
- 30 skills
- 20 requirements
- 5 industry keywords
- tone + length + additional notes

Prompt token estimate:
```
System prompt: ~100 tokens
User prompt: ~30 skills × ~5 tokens + 20 reqs × ~8 tokens + context = ~300 tokens
Output: ~500-800 tokens
Total: ~900-1,200 tokens per call
```

This fits comfortably. **However:** The prompt template does not bound skill/requirement count. A user passing 30 skills each at 10 tokens + 20 requirements each at 15 tokens + job description context can exceed 2,000 input tokens. Adding the system prompt and output buffer, this approaches 4K.

**More critical:** The architecture document says "30 skills max" in validation but the Haiku 4 context window is a hard limit. If a user includes a long job description in `additional_notes`, the 4K limit is exceeded and the API returns a context length error.

**Current validation (partial):**
```python
skills: list[str] = Field(..., min_items=1, max_items=30)  # max 30 skills
requirements: list[str] = Field(default=[], max_items=20)  # max 20 requirements
```

**Gap:** No token count validation. `additional_notes` is unbounded.

**Fix:**
```python
from anthropic import MAX_TOKENS  # or define constant
MAX_INPUT_TOKENS = 3500  # leave room for system prompt + output buffer

def estimate_tokens(text: str) -> int:
    return len(text.split()) * 1.3  # rough estimate

async def generate_jd(input: JDGenerateInput) -> JDResult:
    prompt = build_prompt(input)
    estimated = estimate_tokens(prompt)
    if estimated > MAX_INPUT_TOKENS:
        # Fall back to Sonnet which has 200K context
        model = "claude-sonnet-4-20250514"
    else:
        model = "claude-haiku-4-20250514"
```

**Why this is HIGH:** Production users will hit this error. The error message from the API is opaque. Users will blame the product, not their input.

---

### Finding S6 — Stripe Webhook Deferred to v1.1 (HIGH)

**Evidence:** Day 1 MVP scope explicitly defers "Stripe webhook for subscription changes." The subscription status update flow is not implemented.

**Failure mode:**
1. User upgrades to Pro via Stripe checkout
2. Stripe creates the subscription but the backend never receives confirmation (no webhook)
3. `organizations.subscription_status` remains `active` from initial creation
4. User is billed $69 but the backend thinks they are still on Solo
5. User generates 200 JDs (Solo limit: 50) — no enforcement because backend thinks they are Solo
6. User does NOT get Pro features (template sharing, more templates)
7. User contacts support: "I paid but I don't have Pro features"
8. Revenue leakage + support overhead

**Required for Day 1:**
```python
# src/api/routes/subscription.py
from stripe.webhook import Webhook.construct_event

@router.post("/webhooks/stripe")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig = request.headers.get("stripe-signature")
    event = Webhook.construct_event(payload, sig, settings.STRIPE_WEBHOOK_SECRET)

    match event.type:
        case "customer.subscription.created" | "customer.subscription.updated":
            await subscription_service.sync_from_stripe(event.data.object)
        case "invoice.paid" | "invoice.payment_failed":
            await subscription_service.handle_invoice(event.data.object)
```

**Why this is HIGH:** Without webhooks, subscription status is never updated from Stripe. All revenue processing is unreliable.

---

### Finding S7 — RLS Not Enforced on Day 1 (HIGH)

**Evidence:** The architecture document explicitly describes RLS policies (§6.2) and then says "Full RLS implementation" is deferred to v1.1. The Day 1 scope relies entirely on application-level `org_id` filtering.

**Current application-level isolation:**
```python
# In org_context.py middleware
async def set_org_context(request: Request):
    org_id = get_org_from_clerk_jwt(request)
    await conn.set_session_var("app.current_org_id", org_id)

# In every query
result = await conn.fetch(
    "SELECT * FROM generated_jds WHERE org_id = $1", org_id
)
```

**Gap:** Any bug in a single query — a missing `WHERE org_id = $1` — exposes all orgs' JDs to the requesting user. This is a class of bugs that RLS structurally prevents.

**Current RLS definition (not enforced):**
```sql
ALTER TABLE generated_jds ENABLE ROW LEVEL SECURITY;
CREATE POLICY org_isolation ON generated_jds
  USING (org_id = current_setting('app.current_org_id')::uuid);
```

**Fix:** Enable RLS on Day 1. The application-level filter remains as defense-in-depth.

```sql
ALTER TABLE organizations ENABLE ROW LEVEL SECURITY;
ALTER TABLE jd_templates ENABLE ROW LEVEL SECURITY;
ALTER TABLE generated_jds ENABLE ROW LEVEL SECURITY;
ALTER TABLE analytics_events ENABLE ROW LEVEL SECURITY;

-- Application sets the session variable
SET app.current_org_id = 'uuid-here';
```

**Why this is HIGH:** PDPA violation for a Singapore recruitment tool storing job descriptions (which may contain PII) without proper tenant isolation. Potential for data breach across orgs.

---

## 3. AI Integration Strategy (Haiku vs Sonnet)

### Finding S8 — Haiku Quality vs Recruitment Agency Expectations (MEDIUM)

**Evidence:** The pricing model uses Haiku as the default model for Solo/Pro users. Haiku is optimized for speed and cost, not for nuanced, high-quality text generation.

**Risk:** Recruitment agencies paying $69-$179/month expect professional-quality JDs. Haiku outputs are:
- More generic and less compelling
- Less nuanced in tone adjustments
- More likely to produce boilerplate language

**User impact:** Agencies may switch to competitors after 2-3 weeks of using low-quality Haiku output.

**Recommendation:** A/B test Haiku vs Sonnet quality. If Sonnet produces meaningfully better output (measurable via user edit rate post-generation), the cost difference is worth it for paid tiers.

---

### Finding S9 — Model Version Pinning (MEDIUM)

**Evidence:** The schema stores `model_used VARCHAR(50) -- claude-haiku, claude-sonnet` but not the specific model version (e.g., `claude-haiku-4-20250514`).

**Problem:** When Anthropic updates Haiku to Haiku 5, cached JDs may differ from newly generated ones for identical inputs. The cache key is SHA256 of input only, not model version.

**Fix:**
```python
# Include model version in cache key
cache_key = f"jd:input_hash:{hashlib.sha256((input_hash + model_version).encode()).hexdigest()}"

# Store in DB
INSERT INTO generated_jds (..., model_used) VALUES (..., 'claude-haiku-4-20250514');
```

---

### Finding S10 — No Token Budget Alerting (MEDIUM)

**Evidence:** Redis tracks usage counters but there is no alert when an org approaches or exceeds their monthly limit. The `check_and_increment_usage` function returns `False` when exceeded but the user receives no warning before hitting the limit.

**Impact:** A user at 48/50 JDs generates 2 more (hit limit), then tries a 3rd and gets a hard 429. No warning, no upsell moment.

**Fix:**
```python
async def check_usage_warning(org_id: str, tier: str) -> dict:
    key = f"org:{org_id}:usage:{current_month()}"
    current = await redis.get(key) or 0
    limit = RATE_LIMITS[tier]
    if current >= limit * 0.9:  # 90% threshold
        return {"warning": True, "remaining": max(0, limit - current)}
    return {"warning": False, "remaining": limit - current}
```

---

## 4. Claude API Pricing Changes

### Finding S11 — No Cost Hedge Strategy (HIGH)

**Evidence:** The architecture document explicitly asks "What happens when Claude API pricing changes?" but provides no mitigation.

**Current exposure:** At 25,000 generations/month (500 orgs × 50 JDs), Haiku at $0.001/1K input + $0.005/1K output tokens = ~$150-200/month. If Anthropic raises prices 2x, cost becomes $300-400/month. If they raise 5x (as OpenAI did with GPT-4), cost becomes $750-1,000/month.

**Required hedging strategy:**

1. **Usage caps at the provider level:**
```python
# In .env / AWS Secrets Manager
ANTHROPIC_MAX_USD_PER_MONTH=500

# In billing service
async def check_api_budget():
    current_spend = await billing_service.get_current_month_spend()
    if current_spend >= float(os.environ["ANTHROPIC_MAX_USD_PER_MONTH"]):
        raise BudgetExceededError("AI generation temporarily suspended")
```

2. **Alternative model ready:**
```python
async def generate_jd_fallback(prompt: str) -> str:
    if os.environ.get("USE_FALLBACK_MODEL") == "true":
        return await openai_chat("gpt-4o-mini", prompt)  # OpenAI fallback
    return await anthropic_haiku(prompt)
```

3. **Reserved capacity:** Anthropic offers committed-use pricing with 10-30% discounts for volume commitments. At 500 orgs with predictable monthly volume, this should be negotiated.

---

## 5. Data Model Correctness

### Finding S12 — Missing NOT NULL Constraints (MEDIUM)

**Evidence:**
```sql
-- These fields should be NOT NULL but are nullable
input_tokens INTEGER,        -- logged from API, should be NOT NULL
output_tokens INTEGER,       -- logged from API, should be NOT NULL
stripe_customer_id VARCHAR(255),  -- required once Stripe is wired
model_used VARCHAR(50),      -- should be NOT NULL
```

**Fix:** Add constraints now, before data grows:
```sql
ALTER TABLE generated_jds ALTER COLUMN input_tokens SET NOT NULL;
ALTER TABLE generated_jds ALTER COLUMN output_tokens SET NOT NULL;
ALTER TABLE generated_jds ALTER COLUMN model_used SET NOT NULL;
```

---

### Finding S13 — Missing Audit Columns (MEDIUM)

**Evidence:** No `last_modified_by` on `generated_jds` and no `deleted_by` on soft-delete. For a tool used by recruitment agencies where JDs may contain PII (contact names, emails in "How to Apply"), audit trails are required for PDPA compliance.

**Required additions:**
```sql
ALTER TABLE generated_jds ADD COLUMN last_modified_by VARCHAR(255);
ALTER TABLE generated_jds ADD COLUMN deleted_by VARCHAR(255);
ALTER TABLE jd_versions ADD COLUMN change_type VARCHAR(20) DEFAULT 'edit';  -- edit, delete, restore
```

---

### Finding S14 — No Enforced Template Limits in DB (LOW)

**Evidence:** The architecture specifies Solo: 5 templates, Pro: 20 templates, Team: 100 templates. The application layer checks this in `template_service.py` but there is no DB-level constraint.

**Risk:** A bug in the application check could allow unlimited template creation on any tier.

**Fix:** Add a `template_quota` check in the INSERT trigger or application layer with a DB-level assertion:
```sql
-- Application-level check with DB as last resort
CREATE OR REPLACE FUNCTION check_template_quota()
RETURNS TRIGGER AS $$
DECLARE
  current_count INTEGER;
  quota INTEGER;
BEGIN
  SELECT COUNT(*) INTO current_count FROM jd_templates WHERE org_id = NEW.org_id AND is_deleted = FALSE;
  SELECT tier_to_quota(NEW.tier) INTO quota;
  IF current_count >= quota THEN
    RAISE EXCEPTION 'Template quota exceeded';
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

---

## 6. Security Issues

### Finding S15 — NRIC Detection Gap (HIGH)

**Evidence:** NRIC validation is applied only to `requirements` field:
```python
@field_validator('requirements', mode='after')
@classmethod
def check_no_nric(cls, v):
    nric_pattern = r'\b[A-Z]\d{7}[A-Z]\b'
    for req in v:
        if re.search(nric_pattern, req):
            raise ValueError("NRIC numbers not allowed in requirements")
    return v
```

**Missing validation in:**
1. `title` — "Contact: John Tan S1234567A"
2. `skills` — "Must have valid Singapore ID S1234567A"
3. `additional_notes` — free text with no bounds

**Full fix — validate all user text fields:**
```python
NRIC_PATTERN = re.compile(r'\b[A-Z]\d{7}[A-Z]\b')

def check_no_nric_in_text(text: str) -> None:
    if NRIC_PATTERN.search(text):
        raise ValueError("NRIC numbers are not permitted in any field")

# Apply to every string field
@field_validator('title')
@classmethod
def title_no_nric(cls, v):
    check_no_nric_in_text(v)
    return v

@field_validator('skills', mode='after')
@classmethod
def skills_no_nric(cls, v):
    for skill in v:
        check_no_nric_in_text(skill)
    return v
```

**Additional:** NRIC detection via regex is easily bypassed. Consider:
- Accepting FIN (Foreign Identification Number) in addition to NRIC
- Using a library like `sg-nric` for validation
- Running NRIC detection on `raw_text` before storing

---

### Finding S16 — Clerk JWT Validation Missing Edge Cases (MEDIUM)

**Evidence:** Clerk middleware validates JWT but the document does not mention:
- Token expiry handling (should be < 1 hour for sensitive operations)
- JWT refresh flow (what happens when token expires mid-session)
- Org membership change handling (if user is removed from org, do existing sessions remain valid?)

**Required:**
```python
# src/api/middleware/auth.py
from clerk_sdk import Clerk

clerk = Clerk(os.environ["CLERK_API_KEY"])

async def validate_clerk_token(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(401, "Missing Authorization header")

    token = auth_header.replace("Bearer ", "")
    try:
        claims = await clerk.verify_token(token)
        request.state.user_id = claims.sub
        request.state.org_id = claims.org_id
    except TokenExpiredError:
        raise HTTPException(401, "Token expired")
    except OrgMembershipError:
        raise HTTPException(403, "Not a member of this organization")
```

---

### Finding S17 — No Rate Limit on Auth Endpoints (MEDIUM)

**Evidence:** The rate limit configuration covers only `/generate`, `/list`, and `/export`. Auth endpoints (`/api/v1/auth/*`) are not rate limited.

**Risk:** Brute force attacks on authentication, credential stuffing, or abuse of forgot-password flows.

**Required:**
```python
RATE_LIMITS = {
    "generate": "30/minute",
    "list": "100/minute",
    "export": "20/minute",
    "auth": "10/minute",  # NEW: prevent brute force
}
```

---

### Finding S18 — Redis Without Authentication (LOW for MVP, HIGH for Production)

**Evidence:** No Redis password or TLS configuration in the architecture. AWS ElastiCache should use auth token + in-transit encryption for production.

**For Day 1 MVP:** Acceptable with ElastiCache in a private subnet. For production:
```python
# src/core/redis.py
redis = Redis(
    host=os.environ["REDIS_HOST"],
    port=6379,
    ssl=True,
    password=os.environ["REDIS_AUTH_TOKEN"],  # ElastiCache auth token
)
```

---

### Finding S19 — No Input Sanitization for XSS in JD Output (MEDIUM)

**Evidence:** JDs are stored as JSONB and served via API. The `raw_text` field may contain user-supplied content rendered in the frontend. No output encoding is specified.

**Risk:** Stored XSS if a user includes `<script>` tags in a JD field (e.g., "Required: <script>alert(1)</script>").

**Required:** Frontend must use React's default JSX escaping or `DOMPurify` for raw HTML rendering. Backend should not store raw HTML from user input.

---

### Finding S20 — No Audit Log for Admin Actions (MEDIUM)

**Evidence:** No logging of privileged actions: org creation, subscription changes, member role updates, bulk data exports. For a B2B tool handling recruitment data, audit logging is required for enterprise customers' compliance requirements.

**Required:**
```python
# Log all org-level admin mutations
async def log_admin_action(org_id: str, user_id: str, action: str, details: dict):
    await db.execute(
        """INSERT INTO admin_audit_log (org_id, user_id, action, details, ip_address, created_at)
           VALUES ($1, $2, $3, $4, $5, NOW())""",
        org_id, user_id, action, json.dumps(details), get_client_ip()
    )
```

---

## Cross-Reference Audit

### Document Inconsistencies

1. **`04-technical-architecture.md` vs `06-b2b-jd-tool-backend-architecture.md`**: The older architecture uses a `users` table with `stripe_customer_id` directly on users. The newer B2B JD tool uses `organizations` as the billing entity with Clerk handling user-level auth. These are not reconciled. The product brief should clarify whether this is a separate product from the B2C tool or an evolution of it.

2. **Stripe webhook status**: `06-b2b-jd-tool-backend-architecture.md` §8 Day 1 MVP lists "Stripe webhook for subscription changes" as deferred. But §6.1 PDPA compliance says "Claude API: zero data retention header" — this is not configured anywhere in the code, just stated as a compliance action.

3. **Cost estimate discrepancy**: §9 estimates "500 orgs × 50 JDs × 1000 tokens = $75" for Claude API. This calculation is wrong:
   - 500 × 50 × 1,000 = 25,000,000 tokens (not 25,000)
   - At $0.001/1K tokens = $25 (not $75)
   - The correct estimate at 25,000 generations × ~800 tokens total = ~20M tokens = ~$20-25

---

## Implementation Roadmap

### Phase 1 (Day 1 MVP — Must Fix Before Launch)

1. **Stripe webhook** — implement at least `customer.subscription.updated` and `invoice.paid` handlers
2. **RLS enabled** — even if not fully tested, enable row-level security on all org-scoped tables
3. **NRIC validation on ALL text fields** — `title`, `skills`, `additional_notes` all need validation
4. **Haiku context overflow handling** — add token estimate + fallback to Sonnet when context exceeded
5. **Circuit breaker + retry with fallback** — add fallback to Sonnet on Haiku rate limit

### Phase 2 (Post-Launch v1.1)

1. **Analytics partitioning** — partition `analytics_events` by month
2. **Claude budget caps** — add API-level spending limits with alert
3. **Template quota enforcement at DB level**
4. **Audit log for admin actions**
5. **Auth endpoint rate limiting**

### Phase 3 (Scale to 500+ Orgs)

1. **Connection pool sizing** — tune asyncpg pool for expected concurrency
2. **Redis cluster** — if cache size exceeds single-node capacity
3. **Read replicas** — offload analytics queries to read replica
4. **Committed-use Claude contract** — negotiate volume pricing

---

## Success Criteria

- [ ] Stripe webhook processes subscription events within 5 seconds of Stripe sending them
- [ ] RLS policies reject cross-org queries in all four tables (test with two org IDs)
- [ ] NRIC regex detects S1234567A in title, skills, and additional_notes fields (not just requirements)
- [ ] Haiku context overflow returns user-friendly error with upgrade path to Sonnet
- [ ] Circuit breaker opens after 3 consecutive AI failures; circuit closes after 30 seconds
- [ ] Analytics events table partitionable by month without downtime
- [ ] All four org-scoped tables have proper NOT NULL constraints on required columns
- [ ] Admin audit log captures all org-level mutations
- [ ] Redis uses auth token in production

---

## Appendix: Cost Model Correction

The original estimate in §9 of `06-b2b-jd-tool-backend-architecture.md` contains a math error:

**Original claim:** 500 orgs × 50 JDs × 1000 tokens = $75

**Actual calculation:**
- 25,000 generations × ~800 tokens/generation = 20,000,000 tokens
- Haiku: $0.001/1K input + $0.005/1K output (approximate)
- Assume 60% input, 40% output: 12M input + 8M output
- Cost: (12 × $0.001) + (8 × $0.005) = $0.012 + $0.04 = **$0.052 per 1K tokens**
- Total: 20M tokens × ($0.052/1K) = **~$52/month** (with minimal caching)
- With 40% cache hit rate: **~$31/month**

The $75 estimate is defensible as a conservative upper bound but the stated calculation method is incorrect.

---

*Red team findings complete. High-severity items require resolution before production launch at 500 org scale.*

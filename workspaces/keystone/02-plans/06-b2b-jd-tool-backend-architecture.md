# KeyStone B2B JD Tool — Backend Architecture

> Target: Recruitment agencies (5-20 people), 10-50 JDs/day
> Pricing: Solo $29/mo | Pro $69/mo | Team $179/mo
> Launch: Day 1 MVP

---

## 1. Tech Stack (From Existing Architecture)

| Component | Choice | Rationale |
|-----------|--------|-----------|
| Backend | Python FastAPI | AI ecosystem, async, lean team |
| Database | PostgreSQL 16+ | Relational data, org-level RLS |
| Cache | Redis | JD caching, session, rate limit counters |
| AI | Claude Haiku (generate) + Sonnet (polish) | Cost-quality balance |
| Auth | Clerk | Handles org/team already |
| Payments | Stripe | SGD billing, works with Clerk |
| Hosting | AWS ap-southeast-1 | PDPA compliance |

---

## 2. Data Model (PostgreSQL Schema)

### 2.1 Organizations (Clerk handles primary; we add org-level metadata)

```sql
-- org metadata we manage (Clerk handles users)
CREATE TABLE organizations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  clerk_org_id VARCHAR(255) UNIQUE NOT NULL,  -- maps to Clerk Organization
  name VARCHAR(255) NOT NULL,
  subscription_tier VARCHAR(20) DEFAULT 'solo',  -- solo, pro, team
  subscription_status VARCHAR(20) DEFAULT 'active',  -- active, cancelled, past_due
  stripe_customer_id VARCHAR(255),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_org_clerk ON organizations(clerk_org_id);
```

### 2.2 JD Templates

```sql
CREATE TABLE jd_templates (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  org_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
  created_by VARCHAR(255) NOT NULL,  -- Clerk user ID
  name VARCHAR(255) NOT NULL,
  description TEXT,
  industry VARCHAR(100),  -- tech, finance, healthcare, etc.
  job_family VARCHAR(100),  -- engineering, sales, marketing, etc.
  is_shared BOOLEAN DEFAULT FALSE,  -- available to all org users
  template_data JSONB NOT NULL,  -- {sections: [...], defaults: {...}}
  version INTEGER DEFAULT 1,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_template_org ON jd_templates(org_id);
CREATE INDEX idx_template_industry ON jd_templates(industry);
```

### 2.3 Generated JDs

```sql
CREATE TABLE generated_jds (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  org_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
  created_by VARCHAR(255) NOT NULL,
  template_id UUID REFERENCES jd_templates(id) ON DELETE SET NULL,

  -- Input snapshot
  input_data JSONB NOT NULL,  -- {title, skills: [...], requirements: [...], tone, length}

  -- Output
  generated_content JSONB NOT NULL,  -- {sections: {summary, responsibilities, requirements, benefits, ...}}
  raw_text TEXT NOT NULL,  -- Full JD as plain text for export

  -- Metadata
  generation_mode VARCHAR(20) DEFAULT 'full',  -- full, incremental
  input_tokens INTEGER,
  output_tokens INTEGER,
  model_used VARCHAR(50),  -- claude-haiku, claude-sonnet

  -- Soft delete for recovery
  is_deleted BOOLEAN DEFAULT FALSE,
  deleted_at TIMESTAMP,

  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_jd_org ON generated_jds(org_id);
CREATE INDEX idx_jd_created_by ON generated_jds(created_by);
CREATE INDEX idx_jd_created_at ON generated_jds(created_at);
```

### 2.4 JD Version History

```sql
CREATE TABLE jd_versions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  jd_id UUID REFERENCES generated_jds(id) ON DELETE CASCADE,
  version INTEGER NOT NULL,

  content_snapshot JSONB NOT NULL,  -- Full content at this version
  change_summary TEXT,  -- "Added benefits section", "Toned down requirements"
  input_data JSONB NOT NULL,  -- Snapshot of input that produced this version

  created_by VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),

  UNIQUE(jd_id, version)
);

CREATE INDEX idx_version_jd ON jd_versions(jd_id);
```

### 2.5 Analytics Events

```sql
CREATE TABLE analytics_events (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  org_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
  user_id VARCHAR(255) NOT NULL,  -- Clerk user ID

  event_type VARCHAR(50) NOT NULL,  -- jd_generated, template_created, jd_edited, export_pdf, etc.
  event_data JSONB,  -- {jd_id, template_id, duration_ms, tokens_used, ...}

  -- For aggregate reporting
  plan_tier VARCHAR(20),  -- solo, pro, team (denormalized for easy reporting)
  session_id VARCHAR(255),  -- Group events per session

  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_events_org ON analytics_events(org_id);
CREATE INDEX idx_events_type ON analytics_events(event_type);
CREATE INDEX idx_events_created ON analytics_events(created_at);
```

---

## 3. API Endpoints

### 3.1 JD Generation

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/jd/generate` | POST | Generate a new JD |
| `/api/v1/jd/{id}` | GET | Get generated JD |
| `/api/v1/jd/{id}` | PATCH | Update JD (creates version) |
| `/api/v1/jd/{id}` | DELETE | Soft-delete JD |
| `/api/v1/jd/{id}/versions` | GET | List version history |
| `/api/v1/jd/{id}/versions/{v}` | GET | Get specific version |
| `/api/v1/jd/export/{id}` | GET | Export as PDF/text |

### 3.2 Template Management

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/templates` | GET | List org templates |
| `/api/v1/templates` | POST | Create template |
| `/api/v1/templates/{id}` | GET | Get template |
| `/api/v1/templates/{id}` | PATCH | Update template |
| `/api/v1/templates/{id}` | DELETE | Delete template |
| `/api/v1/templates/shared` | GET | List templates shared by team |

### 3.3 Organization Management

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/org` | GET | Get current org |
| `/api/v1/org` | PATCH | Update org settings |
| `/api/v1/org/members` | GET | List org members (Team plan) |
| `/api/v1/org/members/{id}` | PATCH | Update member role |

### 3.4 Subscription Management

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/subscription` | GET | Get subscription status |
| `/api/v1/subscription/upgrade` | POST | Upgrade plan |
| `/api/v1/subscription/cancel` | POST | Cancel subscription |
| `/api/v1/subscription/invoice` | GET | List invoices |

---

## 4. AI Integration

### 4.1 Model Strategy

| Task | Model | When |
|------|-------|------|
| JD generation (first draft) | Claude Haiku | Solo/Pro users, cost-sensitive |
| JD generation (polish) | Claude Sonnet 4 | Team users, or when Haiku output needs quality boost |
| Tone adjustment | Haiku | Small edits |
| Major rewrite | Sonnet 4 | Full restructuring |

**Day 1 decision**: Use Haiku for all generation. Add Sonnet polish as Pro/Team feature later.

### 4.2 Prompt Structure

```
System Prompt:
"You are a professional job description writer for the Singapore market.
Write clear, concise, and compelling JDs. Include: Summary, Key Responsibilities,
Required Skills, Nice-to-Have, What We Offer, How to Apply.
Do not include: salary ranges, discriminatory language, NRIC requirements."

User Prompt Template:
"""
Job Title: {title}
Industry: {industry}
Job Family: {job_family}
Required Skills: {skills_list}
Experience Level: {experience_level}
Tone: {tone}  -- professional, friendly, startup, corporate
Length: {length}  -- brief (300 words), standard (500 words), detailed (800 words)

Additional Context:
{additional_notes}
"""
```

### 4.3 Caching Strategy (Redis)

| Cache Key Pattern | TTL | Purpose |
|-------------------|-----|---------|
| `jd:input_hash:{hash}` | 7 days | Skip AI for identical inputs |
| `jd:generated:{id}` | 1 hour | Cache full JD for rapid edits |
| `template:{id}` | 24 hours | Template data |
| `org:{id}:rate_limit:{month}` | 30 days | Spend tracking |
| `session:{id}` | 24 hours | Rate limit counters |

**Input hash**: `SHA256(title + sorted(skills) + requirements + tone)` — same inputs = same output.

### 4.4 Cost Optimization

**Per-user monthly limits**:
- Solo ($29): 50 JD generations/month
- Pro ($69): 200 JD generations/month
- Team ($179): 500 JD generations/month

**Implementation**:
```python
# Redis counter per org per month
RATE_LIMITS = {
    "solo": 50,
    "pro": 200,
    "team": 500
}

def check_and_increment_usage(org_id: str, tier: str) -> bool:
    key = f"org:{org_id}:usage:{current_month()}"
    current = redis.get(key) or 0
    if current >= RATE_LIMITS[tier]:
        return False  # Rate limited
    redis.incr(key)
    redis.expire(key, 30 * 24 * 3600)  # 30 days
    return True
```

**Cache hit = no AI call**: If input hash matches cached generation, return cached result. This dramatically reduces AI costs for agencies reusing similar inputs.

---

## 5. Key Backend Flows

### 5.1 JD Generation Flow

```
POST /api/v1/jd/generate
├── 1. Authenticate (Clerk JWT)
├── 2. Check org subscription status
├── 3. Check rate limit (Redis counter)
│   └── If exceeded → 429 Too Many Requests
├── 4. Compute input hash (SHA256)
│   └── If cache hit → return cached JD
├── 5. Build prompt from input
├── 6. Call Claude Haiku API
│   └── Log: input_tokens, output_tokens, duration_ms
├── 7. Parse and validate response
├── 8. Store in PostgreSQL (generated_jds)
├── 9. Emit analytics event
└── Return: {id, content, raw_text, cached: false}
```

### 5.2 Template Customization Flow

```
POST /api/v1/templates
├── 1. Authenticate
├── 2. Validate template_data structure
├── 3. Check org plan allows template creation
│   └── Solo: 5 templates, Pro: 20 templates, Team: 100 templates
├── 4. Store template
└── Return: {id, name, template_data}
```

**Template Data Structure**:
```json
{
  "sections": [
    {"id": "summary", "required": true, "default": "A leading company..."},
    {"id": "responsibilities", "required": true, "default": ""},
    {"id": "requirements", "required": true, "default": ""},
    {"id": "benefits", "required": false, "default": ""},
    {"id": "how_to_apply", "required": true, "default": "Send your resume to..."}
  ],
  "defaults": {
    "tone": "professional",
    "length": "standard"
  }
}
```

### 5.3 Team Collaboration Flow

```
Scenario: Team member creates JD, manager wants to share

1. User A creates JD with template
2. User A marks JD as "shared" (if Team plan)
3. User B in same org sees shared JDs in list
4. User B can edit (creates new version) or copy to their own
5. All edits tracked in jd_versions table
```

**Permissions**:
- Solo: All JDs private to creator
- Pro: Can share templates, not JDs
- Team: Can share JDs within org, collaborative editing

### 5.4 Version History Flow

```
PATCH /api/v1/jd/{id}
Body: {content: {...}, change_summary: "Toned down requirements"}
├── 1. Authenticate
├── 2. Verify ownership (creator or org member)
├── 3. Create new version record
│   └── Increment version number
│   └── Store previous content as snapshot
├── 4. Update current content
└── Return: {id, version: new_version}
```

---

## 6. Security & Compliance

### 6.1 PDPA Considerations

**Data we store**:
- Job descriptions (may contain PII if user includes contact info)
- User/org metadata (from Clerk)
- Analytics events (aggregated, no PII in event_data)

**What we do NOT store**:
- Resume files (stateless processing only)
- NRIC numbers (detected and rejected at input)

**Compliance actions**:
1. All data in AWS ap-southeast-1 (data residency)
2. Claude API: zero data retention header
3. Soft delete with 90-day retention before hard delete
4. Org can request full data export (GDPR-like right)
5. Org can request full data deletion

```sql
-- Soft delete implementation
UPDATE generated_jds SET is_deleted = TRUE, deleted_at = NOW() WHERE id = $1;
-- Hard delete worker runs daily, deletes where deleted_at < NOW() - 90 days
```

### 6.2 Organization-Level Isolation

**PostgreSQL Row-Level Security**:

```sql
ALTER TABLE organizations ENABLE ROW LEVEL SECURITY;
ALTER TABLE jd_templates ENABLE ROW LEVEL SECURITY;
ALTER TABLE generated_jds ENABLE ROW LEVEL SECURITY;
ALTER TABLE analytics_events ENABLE ROW LEVEL SECURITY;

-- RLS policies
CREATE POLICY org_isolation ON organizations
  USING (org_id = current_setting('app.current_org_id')::uuid);

CREATE POLICY org_isolation ON jd_templates
  USING (org_id = current_setting('app.current_org_id')::uuid);

CREATE POLICY org_isolation ON generated_jds
  USING (org_id = current_setting('app.current_org_id')::uuid);
```

**Application-level**: Every query includes `org_id` filter. Clerk middleware sets current org context.

### 6.3 API Rate Limiting

```python
RATE_LIMITS = {
    "generate": "30/minute",  # JD generation
    "list": "100/minute",     # List endpoints
    "export": "20/minute",    # PDF export
}

# Redis sliding window
def check_rate_limit(org_id: str, endpoint: str) -> bool:
    key = f"rate:{org_id}:{endpoint}:{minute_window()}"
    count = redis.incr(key)
    if count == 1:
        redis.expire(key, 60)  # 1 minute window
    return count <= 30  # or whatever limit
```

### 6.4 Input Validation

```python
# JD input validation
class JDGenerateInput(BaseModel):
    title: str = Field(..., min_length=3, max_length=200)
    skills: list[str] = Field(..., min_items=1, max_items=30)
    requirements: list[str] = Field(default=[], max_items=20)
    tone: Literal["professional", "friendly", "startup", "corporate"] = "professional"
    length: Literal["brief", "standard", "detailed"] = "standard"
    industry: str | None = Field(default=None, max_length=100)
    template_id: UUID | None = None

    # No NRIC patterns allowed
    @field_validator('requirements', mode='after')
    @classmethod
    def check_no_nric(cls, v):
        nric_pattern = r'\b[A-Z]\d{7}[A-Z]\b'
        for req in v:
            if re.search(nric_pattern, req):
                raise ValueError("NRIC numbers not allowed in requirements")
        return v
```

---

## 7. Project Structure

```
src/
├── api/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── jd.py               # JD generation endpoints
│   │   ├── templates.py        # Template endpoints
│   │   ├── org.py              # Org management
│   │   └── subscription.py     # Stripe webhook + sub endpoints
│   ├── middleware/
│   │   ├── __init__.py
│   │   ├── auth.py             # Clerk JWT validation
│   │   ├── org_context.py      # Set org_id in request state
│   │   └── rate_limit.py       # Rate limiting
│   └── dependencies.py         # Shared dependencies
├── core/
│   ├── __init__.py
│   ├── config.py               # Settings from .env
│   ├── database.py             # PostgreSQL connection
│   ├── redis.py                # Redis client
│   └── claude.py               # Claude API client
├── services/
│   ├── __init__.py
│   ├── jd_service.py           # JD generation business logic
│   ├── template_service.py     # Template management
│   ├── analytics_service.py    # Event logging
│   └── subscription_service.py # Stripe integration
├── models/
│   ├── __init__.py
│   ├── jd.py                   # Pydantic models for JDs
│   ├── template.py             # Pydantic models for templates
│   └── organization.py         # Pydantic models for orgs
└── workers/
    ├── __init__.py
    └── cleanup.py              # Soft-delete cleanup worker
```

---

## 8. Day 1 MVP Scope

**Must have**:
- JD generation (Haiku only)
- Basic templates (CRUD)
- Org identification via Clerk
- Solo plan (hard-coded)
- Soft delete with 90-day cleanup
- Redis caching for identical inputs
- Basic analytics events

**Can defer to v1.1**:
- Pro/Team plans with different limits
- Template sharing between users
- Version history UI
- PDF export
- Stripe webhook for subscription changes
- Full RLS implementation

---

## 9. Estimated Costs (Month 1)

| Item | Estimate |
|------|----------|
| AWS (EC2 + RDS + Redis) | $200 |
| Claude API (500 orgs × 50 JDs × 1000 tokens) | $75 |
| Clerk | $25 |
| Stripe | Free |
| **Total** | **~$300/month** |

At 50 JDs/org/month × 500 orgs = 25,000 Haiku generations × ~$0.001 = $25. Caching reduces this significantly.

---

*Architecture ready for implementation.*

# M4 — Suggestions Engine (Core Value)

> Depends on: M0.2, M1.5 (consent), M2.2 (resume parsing), M3.4 (match assessment)
> This is the core product — everything else supports it.
> Implements: specs/product.md §Feature 3, specs/technical.md §Learning Loop

---

## M4.1 — Line-by-line revision suggestion generator (Claude Sonnet)

**What**: Generate specific, JD-targeted revision suggestions for resume bullets classified as Transferable or Addressable.

**Input**: `job_analysis_id` (which has resume_id + parsed JD + match results)
**Scope**: ONLY bullets classified as Transferable or Addressable. Fundamental gaps are flagged but not "fixed." Strong matches are celebrated, not changed.

**Output per suggestion**:
```json
{
  "id": "sug_uuid",
  "job_analysis_id": "...",
  "section": "experience.DBS_2019-2022",
  "original_text": "Responsible for managing a team",
  "suggested_text": "Led 8-person cross-functional team across 3 business units, improving reporting efficiency by 30%",
  "rationale": "This GLC values quantified team leadership; 'responsible for' is ambiguous in SG public sector context.",
  "sg_context": { "company_type": "GLC", "jd_requirement_id": "req_3" },
  "match_level": "transferable"
}
```

**Quality constraints** (enforced at generation time — these are NOT optional):
- Rationale field: MUST contain at least one specific reference to (a) JD-specific vocabulary, OR (b) company type name, OR (c) SG market-specific convention
- Suggestions that are generic (rationale contains: "be more specific", "add quantifiable", "improve your", "consider adding") → REGENERATE, max 2 retries before flagging as quality failure
- The AI writes the suggestion as "We'd say" not "I recommend" (avoid first-person AI framing)
- Banned AI phrases in output: "I'm an AI", "as an AI assistant", "I'd be happy to", "great question", "in conclusion" — strip or regenerate if found

**Model**: Claude Sonnet (quality-critical)
**SG system prompt**: same cached prompt as M3.4

**Note**: Do NOT generate suggestions for text that has no corresponding match assessment. If a resume section has no JD requirements mapped to it, skip it.

**Acceptance criteria**:
- Every generated rationale references company type OR JD requirement (tested on 10 resume+JD pairs)
- Generic suggestion test: CI pipeline test with test inputs → reject if generic phrases found
- Suggestions cover all Transferable + Addressable bullets (not just a subset)
- Generation for 10 suggestions ≤15 seconds (p95)

**Implements**: specs/product.md §Feature 3, Analysis 28 §Risk 1 (Specificity rule)

---

## M4.2 — Suggestion signals table — Day 1 architecture (CRITICAL)

**What**: Log EVERY Accept/Reject/Modify action to `suggestion_signals`. This is the data moat. Must be in place before first user interaction.

**Schema** (from specs/technical.md §Learning Loop):
```sql
suggestion_signals (
  id uuid pk,
  user_id uuid NOT NULL,    -- anonymised (not PII-linked in THIS table)
  anon_session_id uuid,      -- for pre-signup interactions
  suggestion_id uuid NOT NULL REFERENCES suggestions(id),
  action text NOT NULL CHECK (action IN ('ACCEPTED', 'REJECTED', 'MODIFIED')),
  modified_text text,        -- if MODIFIED: what the user actually wrote
  context_company_type text,
  context_role_level text,
  context_industry text,
  context_ns_related boolean default false,
  context_tenant_type text,  -- 'B2C' | 'B2B' — CRITICAL for training exclusion
  created_at timestamptz NOT NULL
)
```

**CRITICAL: `context_tenant_type` field**: every signal must be tagged `B2C` or `B2B`. Training pipeline query MUST filter `WHERE context_tenant_type = 'B2C'`. This is the architectural separation between B2B aggregate data and B2C training pipeline.

**Anonymous signal support**: Signals logged BEFORE user signs in use `anon_session_id`. When user signs up → backfill `user_id` on all signals from that session (background job after signup). `anon_session_id` is a signed cookie value — not PII.

**API endpoints**:
- `POST /api/suggestions/{suggestion_id}/accept`
- `POST /api/suggestions/{suggestion_id}/reject` (optional body: `{reason: "not_relevant|too_generic|have_better|other", free_text: "..."}`)
- `POST /api/suggestions/{suggestion_id}/modify` (body: `{modified_text: "..."}`)

Each writes to `suggestion_signals` with full context. Optimistic: return 200 immediately, write asynchronously (max 100ms write path).

**Acceptance criteria**:
- Every Accept/Reject/Modify API call results in a `suggestion_signals` row within 100ms
- Anonymous signals captured (no auth required)
- `context_tenant_type` = `B2B` for all B2B-provisioned users — integration test verifies
- Backfill job: sign-up after 3 anon accepts → 3 signal rows get user_id populated
- Zero signals from B2B users pass through training query: `SELECT * FROM suggestion_signals WHERE context_tenant_type = 'B2C'`

**Implements**: specs/technical.md §Learning Loop (MUST design before coding), specs/product.md §Feature 3 (Learning loop), day1_architecture_requirements.md

---

## M4.3 — Free tier gating

**What**: Enforce free tier limits. First JD = unlimited suggestions (no auth required). Subsequent JDs = first 3 suggestions visible; rest gated behind Pro.

**State tracking**:
- Anonymous user: `first_jd_consumed` flag in signed cookie (set when first JD analysis is initiated)
- Authenticated free user: `first_jd_consumed` boolean on `users` record + `subscription_tier = 'free'`
- Pro user: no gate

**Gate behavior**:
- Suggestions endpoint `GET /api/job-analyses/{id}/suggestions`:
  - If user is Pro or this is their first JD: return all suggestions
  - If free + not first JD: return first 3 suggestions + `{gated: true, gated_count: N, gate_context: "6 more suggestions for your Experience section, which covers 60% of this JD's requirements"}`
- The `gate_context` must reference the specific section and JD coverage, NOT generic "upgrade to unlock" copy

**Paywall gate content preview** (per Analysis 28 §Risk 3):
- Copy: "6 more suggestions — this is where Pro comes in" (NOT "Upgrade to unlock premium features")
- Show WHAT is gated: "6 more suggestions for your Experience section (60% of this JD's requirements)"
- Show 3-day free trial option (no credit card required)
- Show "Or analyse a different job free" — always provide the exit path

**Acceptance criteria**:
- First JD analysis (anon): all suggestions visible, no paywall
- Second JD analysis (anon): 3 suggestions visible + gate UI
- Pro user: all suggestions always visible
- Gate context message references specific section name + JD coverage percentage

**Implements**: specs/product.md §Feature 3 (Free tier limit), specs/mvp-scope.md §Feature 3

---

## M4.4 — LLM cost ceiling + graceful degradation

**What**: Hard ceiling of SGD 5/user/month LLM spend. Must be implemented before launch.

**Cost tracking** (Redis):
- Key: `llm_cost:{user_id}:{YYYY-MM}` (TTL: 35 days)
- Increment on every Claude API call: estimate cost from token counts
- Cost rates (for ceiling calculation, not billing):
  - Haiku input: $0.25/M tokens
  - Haiku output: $1.25/M tokens
  - Sonnet input: $3.00/M tokens
  - Sonnet output: $15.00/M tokens

**Ceiling behavior** (when SGD 5 exceeded):
- Resume analysis: return cached parsed_json if available; if not: serve simplified extraction (skip Haiku, use regex-only parsing)
- Match assessment: return cached result if available; if not: return `{degraded: true, message: "Analysis quota reached for this month — your previous analyses are still available."}`
- Suggestions: return cached suggestions if available; if not: return first 3 cached suggestions only

**Do NOT show a confusing error**: The user sees "Results from your previous analysis" — not "API cost limit exceeded."

**Admin alert**: When any user hits 80% of ceiling → log warning. At 100% → alert (CloudWatch alarm or similar).

**Acceptance criteria**:
- Integration test: simulate SGD 5 cost → next API call returns degraded response, not error
- Degraded response shows user-friendly message, not internal error
- Cost meter accurate: test with known token counts → verify SGD estimate

**Implements**: specs/technical.md §AI Cost Model (SGD 5/user/month ceiling), specs/mvp-scope.md §Technical done criteria

---

## M4.5 — Suggestions API endpoint (wire M4.1 + M4.2 + M4.3 + M4.4)

**What**: `GET /api/job-analyses/{id}/suggestions` — returns suggestions for a job analysis, applying gating and cost ceiling logic.

**Response**:
```json
{
  "suggestions": [...],
  "gated": false,
  "gated_count": 0,
  "gate_context": null,
  "total_count": 14,
  "match_summary": { "strong": 8, "transferable": 3, "addressable": 2, "fundamental": 1 }
}
```

**Suggestion ordering** (per Analysis 24 §Part 2 Decision 4):
- Transferable + Addressable first (these are actionable — the core value)
- Strong last ("already working") — shown in sidebar/secondary section
- Fundamental at the bottom, collapsed by default

**Streaming**: suggestions are generated one-at-a-time and streamed to the frontend. First suggestion should appear within 5 seconds of initiating generation.

**Acceptance criteria**:
- Suggestions ordered: Transferable/Addressable before Strong, Fundamental at bottom
- Streaming: first suggestion appears within 5 seconds
- Accept/Reject/Modify actions all write to suggestion_signals
- Gated response shows correct gate context message

**Wire todo**: connects M4.1 (generation) + M4.2 (signals) + M4.3 (gating) + M4.4 (cost ceiling)

**Implements**: specs/product.md §Feature 3, Analysis 24 §Part 2 (suggestion presentation order)


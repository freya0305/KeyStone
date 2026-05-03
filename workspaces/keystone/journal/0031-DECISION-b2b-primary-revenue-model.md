# Journal 0037 — DECISION: B2B as Primary Revenue Engine, B2C as Data Infrastructure

**Date**: 2026-04-30
**Type**: DECISION
**Author**: co-authored
**Supersedes**: 0027, 0033 (merged)
**Topic**: B2B revenue architecture and B2C strategic role
**Phase**: analyze
**Tags**: [business-model, b2b, b2c, revenue, strategy]

---

## Decision: B2B Is Primary Revenue; B2C Is Data Infrastructure

### The Strategic Reframe

**What we are**: A B2B data company that uses B2C as a data collection mechanism.

**Revenue logic**:
- B2C free users → outcome data
- Outcome data → B2B contracts (university, agency)
- B2B revenue → funds further data collection
- Repeat

**What we are NOT**: A B2C subscription business trying to maximize paid users.

### B2B Revenue Architecture

| Stream | Deal Size | Sales Cycle | Year 1 | Year 2 | Year 3 |
|--------|-----------|------------|---------|--------|--------|
| Agency deals | SGD 600–2,400/yr | 2–4 weeks | SGD 6–14K | SGD 15–25K | SGD 25–40K |
| University pilots | Free → SGD 15–30K | 9–18 months | SGD 0 | SGD 15–30K | SGD 50–100K |
| **Total B2B** | | | **SGD 6–14K** | **SGD 30–55K** | **SGD 75–140K** |

### Why Agency Deals First

Agency deals are the cash flow bridge for Months 1–12:
- 2–4 week close cycle (vs 9–18 months for universities)
- Owner/director decision, no procurement
- SGD 600–2,400/year per agency; 5–10 deals in Year 1
- Proves the B2B model before university procurement closes

### Why University Outreach Starts Day 1

18–24 month procurement cycle means conversations started today become revenue in Year 2–3:
- Delay = delay revenue
- Free pilots build outcome data
- Year 1 paid contracts unlikely; Year 2+ is realistic

### Alternatives Considered

1. **B2C-only model** — Rejected. LTV (SGD 36) < CAC (SGD 40–80) for paid acquisition. Unit economics don't work without B2B institutional revenue.

2. **B2C as primary, B2B as secondary** — Rejected. University procurement takes 9–18 months. B2C alone cannot fund operations through the ramp period.

3. **B2B-only (no B2C)** — Rejected. B2C is the data accumulation engine. Without live user outcome data, the B2B pitch lacks evidence.

## Decision: Annual Plan = Career Ecosystem Pass (Not Lock-In)

### The Old Framing (Rejected)

Annual Plan as "churn reduction" — get users to prepay 12 months to prevent cancellation when they find a job.

**Why it failed**: Job seekers find work in 2–4 months. They will not prepay 12 months for a product they plan to leave in 3 months.

### The New Framing

**Annual Plan = Career Ecosystem Pass**

- **Target user**: Someone who just GOT a job and wants to stay tracked for their next career move
- **Trigger moment**: "Offer Received" → upgrade prompt appears
- **Includes**: 1× 30-min career advisor session (SGD 150+ value) + post-hire tracking
- **This is NOT LTV maximization** — it is ecosystem engagement for users who WANT to stay

### Why This Moment Is the Right One

Users who just received an offer have:
- Highest purchase intent of their entire search
- Clearest understanding of product value (it just worked)
- Post-hire tracking needs (career development, next move preparation)
- Annual plan addresses their next job search, not this one

---

## Consequences

- B2C optimization shifts from "maximize paid conversion" to "maximize outcome logging rate"
- B2C growth channels must be near-zero CAC (organic, referral, university distribution)
- B2B sales velocity is the primary revenue driver in Year 1–2
- Data quality (not user count) is the key B2C metric

---

## Files Updated

| File | Change |
|------|--------|
| `specs/business-model.md` | B2B as primary revenue, B2C as data engine |
| `memory/project_keystone.md` | B2B-as-primary, Annual Plan reframe |
| `01-analysis/44-B2B-growth-velocity-and-funding-model.md` | B2B growth velocity, contract timelines |

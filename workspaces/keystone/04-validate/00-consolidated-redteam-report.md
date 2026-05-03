# KeyStone — Consolidated Red Team Report

**Date**: 2026-04-29
**Sources**: Analyst validation, Value auditor, Security audit, Round 2 strategic findings
**Status**: BLOCKING — 4 CRITICAL blockers, 11 HIGH findings
**Phase gate**: `/todos` cannot proceed until CRITICAL findings are addressed

---

## Executive Summary

The four plans are well-structured and internally consistent. The UX/UI design is strong. The data moat strategy is intellectually honest about timelines. However, the plans rest on **two heroic assumptions that are not supported by evidence**:

1. **B2C acquisition will reach the volume required** to make the data flywheel work
2. **The competitive window is 18-36 months** — when Round 2 established it is 4-8 weeks

Additionally, **4 CRITICAL security/compliance gaps** must be resolved before any user data is processed.

**Verdict**: The plans are executable but the commercial thesis is underdetermined. Focus must shift to B2B contract signing as the primary survival mechanism, not B2C volume.

---

## CRITICAL Blockers — Must Resolve Before /todos

These findings block progression to implementation. They cannot be resolved by "building better" — they require strategic decisions.

### CRITICAL 1: Capital Gap — No Stated Runway

**Source**: Round 2 Finding

| Item | Amount |
|------|--------|
| Monthly infrastructure burn | SGD 2.6-3K |
| Founder personal burn (SG) | SGD 3-5K/month |
| **Total monthly burn** | **SGD 5.6-8K** |
| Month 12 realistic MRR | SGD 1.5-4.6K |
| **Gap at Month 12** | **SGD 1-6.5K/month** |
| Capital needed for Year 1 | **SGD 60-90K** |

The plan assumes survival without external capital. This is not credible.

**Decision required**: How is Year 1 operations funded? Personal savings? Startup SG grant? Angel investment? **This decision changes the entire build strategy.**

---

### CRITICAL 2: Outcome Logging Rate — Assumed, Not Validated

**Source**: Analyst validation (RED FLAG 4)

The data moat requires 1,000+ logged outcomes by Month 12-18. This requires **15-20% of applications generating a logged outcome**. No evidence supports this rate.

- If actual rate is 5%: 20,000 applications needed → moat delayed to Month 24-36
- If actual rate is 3%: 33,333 applications needed → moat may never materialize

**Decision required**: Is there a design mechanism to validate the outcome logging rate assumption before building the full moat architecture?

---

### CRITICAL 3: DPO/DPIA — Launch-Blocking PDPA Requirements Have No Plan

**Source**: Security audit (C-2)

The compliance spec states: "Do not launch with real user data without a DPO engaged." The architecture plan mentions neither DPO engagement nor DPIA completion as a gate or milestone.

- DPO engagement: required before any user data processing
- DPIA completion: required before NRIC handling (which is core to Phase 1 MVP)

**Decision required**: Who owns DPO engagement? What is the timeline? This is a legal requirement, not a feature.

---

### CRITICAL 4: NRIC Masking — Architecture Not Defined

**Source**: Security audit (C-1)

Three-stage masking is listed as a feature description, not an architectural constraint. The compliance spec mandates three specific stages with enforcement mechanisms. The plan does not specify:

- Named utility module for masking functions
- Stage 2 assertion/enforce mechanism before AI API call
- Stage 3 AI-output sanitization
- Integration points in the codebase

**Decision required**: Before any resume parsing code is written, the NRIC masking architecture must be defined as a shared utility.

---

## HIGH Findings — Significant Risk

### H-1: Competitive Window Is 4-8 Weeks, Not 18-36 Months

**Source**: Round 2 Finding + Analyst validation (RED FLAG 3)

The data moat plan says "VMock would need 12-18 months to close the gap." The competitive reassessment says "4-8 weeks for a well-funded US team to reach SG competitive parity."

These statements are **in direct conflict**. If a competitor can replicate KeyStone's features in 4-8 weeks, the 12-18 month moat timeline is irrelevant.

**Impact**: The moat strategy assumes an undisturbed window. The competitive reality shows the window can close in under two months.

---

### H-2: B2C User Acquisition Has No Credible Path

**Source**: Analyst validation (RED FLAG 2)

The plan requires 5,000-8,000 registered free users to reach 200-330 paying Pro users. No acquisition strategy is described.

- No paid acquisition budget identified
- No viral growth mechanism described
- University SSO listed as B2B (Phase 3), not B2C acquisition
- "Volume is the strategy" is a goal, not a plan

**Impact**: If B2C acquisition fails, the data flywheel never spins up and B2B has no differentiated product to sell.

---

### H-3: The Data Moat Takes Longer Than a Typical Job Search

**Source**: Analyst validation (RED FLAG 1)

| Moat Milestone | Timeline | Typical Job Search |
|----------------|----------|-------------------|
| First patterns | Month 3-4 | User may already have a job |
| Fine-tunable corpus | Month 6-8 | Job search long over |
| Outcome calibration | Month 12-18 | 2-3 job searches |
| Employer fingerprint | Month 18-24 | 3-4 job searches |

**Impact**: The median user gets a job and churns before the moat produces a single meaningful insight for them. The product is optimized for accumulating data across users, not for retaining individual users.

---

### H-4: Fine-Tuning Corpus Requires 80K Signals, Not 10K

**Source**: Round 2 Finding

160 segments × 500 examples minimum = 80,000 signals for segment-level fine-tuning. 10K at Month 6-8 = 62 examples/segment — statistically unusable.

**Required pivot**: Build proprietary RAG corpus instead (employer fingerprints, recruiter knowledge, JD pattern library). RAG is usable at any data volume; fine-tuning requires 80K+ signals.

---

### H-5: B2C Is a Data Pipeline, Not a Revenue Business

**Source**: Round 2 Finding

Year 1 B2C revenue = SGD 11K-23K. This does not fund operations. **SGD 19/month optimizes for margin; it may pessimize for data volume and survival.** Consider SGD 9-12/month to lower conversion friction and accelerate data accumulation.

---

### H-6: Organic Ceiling Below Break-Even

**Source**: Round 2 Finding

- Organic ceiling: ~3-5K registered users/year → 120-300 Pro users → SGD 27K-68K ARR
- Break-even requires: SGD 100K ARR
- **Gap: SGD 32-73K ARR**

Organic alone cannot reach break-even. The plan needs either: paid acquisition or a lower break-even target.

---

### H-7: Year 2 Revenue Projection Is 2-3x Optimistic

**Source**: Round 2 Finding

University procurement = 15-21 months from first conversation. Conversations start Month 3-6 → first contracts Month 18-24 → **Year 3 at earliest, not Year 2.**

Realistic Year 2 ARR: SGD 120-250K (not SGD 328-756K projected).

---

### H-8: LTV Treadmill Requires 13-21% of SG Market Annually

**Source**: Round 2 Finding

400 concurrent Pro = 133 new Pro/month = 2,660 new registered/month = 32K/year. That's **13-21% of the entire 150-250K SG addressable market annually.**

Structurally impossible for a niche tool without paid acquisition.

---

### H-9: Outcome Calibration Claim Is Dishonest at Launch

**Source**: Round 2 Finding

Leading with "calibrated on SG hiring manager behaviour" as the differentiator vs VMock is **fraudulent** when a sophisticated B2B buyer asks for methodology and sample size.

**Required fix**: Replace with "outcome tracking infrastructure" — factual, verifiable, and builds credibility.

---

### H-10: Teal Is the Real B2C Competitor (Not VMock)

**Source**: Round 2 Finding

Teal already does per-job tailoring + outcome tracking. A Teal user who pastes SG context manually gets 85-90% of KeyStone's output. **Teal is the comparison that matters for B2C buyers.**

Current competitive spec does not list Teal as HIGH B2C threat.

---

### H-11: Free Tier Anti-Abuse — Phone Verification Missing

**Source**: Round 2 Finding

No mechanism prevents multi-account abuse. "First analysis: unlimited suggestions" gives full product value without payment.

**Required**: SMS phone verification (SGD ~0.05/verification) before launch. Must be in Phase 0.

---

## Security Findings — Must Resolve Before User Data Processing

### CRITICAL Security (from Security Audit)

| ID | Finding | Required Action |
|----|---------|----------------|
| C-1 | NRIC masking architecture not defined | Define shared utility module with three functions before any parsing code |
| C-2 | DPO/DPIA not in plan | DPO engagement as M0 milestone |
| C-3 | NRIC masking has no test plan | Specific test cases as implementation deliverables |
| C-4 | Clerk auth integration has zero security details | Define session management, token validation, logout |
| C-5 | Stripe PCI DSS compliance unspecified | Clarify card data flow — does it touch KeyStone servers? |

### HIGH Security (from Security Audit)

| ID | Finding |
|----|---------|
| H-1 | Six consent types collapsed to single boolean in data model |
| H-2 | Stripe/Resend data residency not verified |
| H-3 | Consent revocation mid-session has undefined behavior |
| H-4 | S3 access controls absent |
| H-5 | Data deletion mechanism missing |
| H-6 | Audit logging not in architecture |
| H-7 | Resend email security unspecified |
| H-8 | Anthropic zero retention not technically enforced |
| H-9 | Employer fingerprint anonymization unverified |
| H-10 | Cost ceiling bypassable (Redis counter not atomic) |
| H-11 | Rate limiting unspecified |

---

## Findings Already Resolved (From Previous Round)

These were identified and resolved in the previous session — documented here for completeness:

| Finding | Resolution |
|---------|------------|
| PDPA vs. training conflict | Hard separation: B2B → aggregate only; B2C → explicit separate consent |
| Outcome logging rate 15-20% optimistic | Revised to 3-6%; UX framed as personal tracker not data collection |
| Free tier abuse | SMS phone verification selected |
| Batch mode missing | Added to scope before B2C public launch |
| Interview prep bundling | Included in Pro positioning from MVP |
| PMET features missing | Added as distinct feature module |

---

## What the Plans Got Right

These are genuine strengths worth preserving:

1. **UX/UI design is strong** — "every click is a row" is an excellent principle; the four-level match system is well-designed
2. **PDPA compliance architecture is sound** — the three-stage consent model is correct; the implementation just needs enforcement
3. **The pull-based outcome collection design is right** — post-download modal, batch quick-update, weekly digest
4. **Moat-priming (first JD free) is correct** — users must experience full value before hitting the paywall
5. **60-30-10 heuristic is practical** — ships 60% + 30%, not 100% of some things and 0% of others
6. **The B2B pivot is strategically correct** — once contracts are signed, the switching cost is real; B2C is fragile

---

## Required Decisions Before /todos

| Decision | Owner | Impact if Not Made |
|----------|-------|-------------------|
| Year 1 funding source | Founder | Build strategy changes entirely |
| DPO engagement timeline | Founder | Cannot launch with real users |
| Outcome logging rate validation approach | Product | Moat timeline may be 3x longer |
| Free tier price (SGD 9-12 vs 19) | Founder | Affects volume vs revenue tradeoff |
| NRIC masking utility architecture | Tech lead | PDPA violation risk |
| Phone verification implementation | Tech lead | Anti-abuse gap |

---

## For Discussion

1. The data moat strategy is honest about timelines but the B2C plan assumes the moat works on the same timeline as a job search. Should the product pivot to career management (ongoing, not just job search) to extend user lifetime?

2. The B2B argument is strongest when KeyStone has outcome data. But getting outcome data requires B2C users. Is there a way to bootstrap B2B relationships before having outcome data to show?

3. The competitive window is 4-8 weeks. Does KeyStone have a different competitive argument that doesn't depend on features? (Relationship with career centres? Early institutional contracts?)

4. The capital gap is SGD 60-90K for Year 1. Is this a problem to solve before building, or is it assumed to be solved by the founder's personal resources?

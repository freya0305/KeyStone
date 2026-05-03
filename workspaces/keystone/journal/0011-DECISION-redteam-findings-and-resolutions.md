---
type: DECISION
date: 2026-04-29
created_at: 2026-04-29T12:00:00Z
author: co-authored
session_id: 874f263b-1879-49b0-9e64-1f293538aedb
project: keystone
topic: Strategy red team findings and founder decisions — 6 issues identified, all resolved
phase: analyze
tags: [redteam, pdpa, data-moat, free-tier, product, decisions]
---

## Red Team Summary

Three parallel agents (strategic risks, B2B buyer perspective, product assumptions) identified 6 issues. All resolved by founder decision. See workspaces/keystone/04-validate/ for full agent reports.

---

## Critical Issue 1: PDPA vs. Data Moat Training Conflict

**Finding:** Universities will not consent to any model training on student data. Hard veto line per SIT career director perspective. Current spec conflates B2B signal collection with model training rights.

**Decision:** Architecture must enforce a hard separation:
- B2B institutional data → aggregate outcome dashboards only; NEVER used for model training
- B2C user data → explicit separate consent at signup; the only source for fine-tuning
- MOU template must explicitly exclude model training in plain language

**Open question raised by founder:** B2C is hard to grow at launch without competitive advantage (GPT/LinkedIn parity). If B2C is slow, the training data pipeline is also slow. Are there alternative data sources beyond B2C? (Resolved in journal 0012.)

---

## Critical Issue 2: Outcome Logging Rate Revised to 3–6%

**Finding:** 15-20% assumption was 4x optimistic. Real-world rate (Teal, LinkedIn) is 3-6%. Data moat timeline extends to ~40-48 months at B2C scale, not 18 months.

**Decision:**
- All financial projections and moat timelines to be updated to use 3-6% base rate
- UX framing for outcome logging: user-facing dashboard utility ("your personal job search tracker"), not data collection mechanism
- Ongoing exploration of mechanisms to improve logging rate is a standing product objective

**Specs to update:** specs/market.md (moat timeline), specs/business-model.md (outcome data assumptions)

---

## Critical Issue 3: Free Tier Anti-Abuse — Phone Verification

**Finding:** No mechanism prevents multi-account abuse. "First analysis: unlimited suggestions" gives full product value without payment.

**Decision:** Option A selected — SMS phone number verification (SGD ~0.05/verification). One phone number = one account. Acceptable friction for SG market. Must be implemented before launch.

---

## Issue 4: Batch Mode for Spray-and-Pray Users

**Finding:** Most SG job seekers send 40+ applications/month. Per-job tailoring asks for behavior change. Need "batch mode": one resume + N job URLs → N tailored variants.

**Decision:** Agreed. Batch mode to be added as a /todos item. Not blocking MVP but in scope before B2C public launch.

---

## Issue 5: Interview Prep — Bundle into Pro Positioning from Day 1

**Finding:** 5-10% callback trigger rate makes interview prep a reacquisition feature, not retention. But bundling it in Pro increases perceived value for 100% of users.

**Decision:** Agreed. Feature may be delivered in Phase 2, but Pro pricing communication from MVP will include "interview prep included" as perceived value. User pays for the option, not only for the trigger.

---

## Issue 6: SG Intelligence — Rebuild Around PMET Pain

**Finding:** NRIC detection and NS framing serve fresh grads (lower willingness-to-pay). Retrenched PMET (highest WTP) need: career pivot narrative reframing, age-neutral language, seniority repositioning. None currently scoped.

**Decision:** Agreed. PMET-specific features (career pivot language, seniority reframing) to be added to /todos as a distinct feature module alongside the existing SG intelligence features.

---

## For Discussion

1. The PDPA training separation means the data moat speed is directly coupled to B2C growth speed. If B2C grows at 200 users/month, the moat is real by Month 18. If B2C grows at 50 users/month, the moat is Year 3+. What is the most realistic B2C monthly growth assumption given no competitive advantage at launch?
2. Recruitment agency data partnerships (see journal 0012) could bootstrap training data before launch. How much historical placement data would 5-10 boutique SG agencies realistically share, and under what commercial terms?
3. The "ongoing exploration of mechanisms to improve logging rate" — at what point should this become a formal product experiment with defined success criteria rather than an open-ended objective?

---
name: 0031-DECISIONS-redteam-responses
description: 12 product decisions from redteam findings round
type: DECISION
date: 2026-04-30
author: co-authored
topic: Redteam Product Corrections
phase: analyze
tags: [redteam, product, corrections, pricing, compliance]
---

# Journal 0031 — DECISIONS: Redteam Responses and Product Corrections

**Date**: 2026-04-30
**Type**: DECISION
**Author**: co-authored
**Phase**: analyze

---

## Decision Summary

12 product decisions made in response to redteam findings across pricing, compliance, competitive positioning, and acquisition strategy.

---

## Alternatives Considered

### 1. Year 1 Funding Source
- **Option A**: VC seed round (SGD 500K+) — Rejected. Too early, too slow, dilutive.
- **Option B**: Personal funds + grants + angel — **Selected**. Balances speed with minimal dilution.

### 2. DPO Approach
- **Option A**: Internal DPO hire — Rejected. SGD 60-80K/year burn too high.
- **Option B**: Virtual DPO service — **Selected**. SGD 200-500/month, external provider.

### 3. NRIC Masking Architecture
- **Option A**: Client-side masking — Rejected. Insecure, easily bypassed.
- **Option B**: Server-side + validation layer — **Selected**. Backend regex detection, immediate masking before AI processing.

### 4. Competitive Window Framing
- **Option A**: Treat as closing risk — Rejected. Creates anxiety without action.
- **Option B**: Structural asymmetry framing — **Selected**. SG market is 0.07% of global; Teal structurally cannot prioritize it.

---

## Key Consequences

| Decision | Impact |
|----------|--------|
| Personal funds + angel bridge | Burn runway 12-18 months without VC pressure |
| Virtual DPO | Compliance operational cost SGD 200-500/month vs SGD 5-7K internal |
| Server-side NRIC masking | Engineering complexity increases; PDPA risk decreases |
| Organic-only B2C | Slower growth but LTV/CAC remains positive |
| Agency deals priority | Revenue starts Month 2-3 vs Month 12+ for universities |
| Referral program P1 | 1-2 day build, highest quality users, immediate feedback loop |

---

## Files Updated

| File | Change |
|------|--------|
| specs/mvp-scope.md | Pricing corrected: SGD 19→SGD 12, SGD 190→SGD 144 |
| memory/project_keystone.md | All 12 decisions recorded |
| (all marketing files) | Remove "calibrated on SG hiring manager behavior" language |

---

## For Discussion

1. Is 12 decisions in one session too many to track? Should we create separate DECISION entries per topic?
2. Given the founder capacity constraint, should we delegate more execution (Reddit, LinkedIn) to contractors?
3. What is the minimum viable compliance stack before Month 1 launch?

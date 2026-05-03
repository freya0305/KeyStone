# Redteam Round 1 — Validation Report

**Date**: 2026-04-30
**Scope**: Full business model redteam + strategic gap analysis
**Agents**: 3 parallel (business model audit, strategic gap analysis, pricing/number audit)

---

## CRITICAL Findings (FIXED)

### CRITICAL-1: mvp-scope.md — Basic Tier Priced at SGD 12 Instead of SGD 9

**File**: `specs/mvp-scope.md` L70
**Finding**: Stripe configuration stated "SGD 12/month Basic" — Basic must be SGD 9/month.
**Impact**: If used for Stripe config, all Basic users would be overcharged SGD 3/month.
**Status**: FIXED — edited to "SGD 9/month Basic, SGD 12/month Pro"

---

### CRITICAL-2: Analysis 43 — Internally Contradictory Break-Even Figures

**File**: `workspaces/keystone/01-analysis/43-corrected-financial-model.md`
**Finding**: Opening summary stated "~550 Pro users" for break-even; body text said "~300"; other tables said "400-450" and "SGD 192K ARR". Four different figures in one document.
**Impact**: No clear strategic target; business decisions impossible.
**Status**: FIXED — Executive Summary corrected to "~300 users, ~SGD 43K ARR". Section 7 rewritten.

---

### CRITICAL-3: Analysis 43 — Year 1 B2C Revenue Math Doesn't Add Up

**File**: `workspaces/keystone/01-analysis/43-corrected-financial-model.md` L241
**Finding**: Document claimed "Year 1 Total ARR: ~SGD 60-70K" but the monthly table's cumulative revenue through Month 12 = ~SGD 17,800 actual.
**Impact**: Revenue projections overstated by 3-4×.
**Status**: FIXED — Section 6 rewritten with corrected figures (SGD 21-50K total Year 1).

---

## CRITICAL Gaps Identified (Not Fixed — Require Human Action)

### Gap 1: No Capital Runway Plan

**Severity**: CRITICAL
**Finding**: Year 1 revenue (SGD 21-50K) does not cover Year 1 burn (SGD 43-75K). Gap of SGD 0-54K requires bridge financing. No explicit runway plan documented.
**Owner**: Founder
**Action**: Model three scenarios; decide on angel raise before launch

---

### Gap 2: EAA Opinion Letter — No Timeline, Owner, or Budget

**Severity**: CRITICAL
**Finding**: MVP launch blocker "EAA non-applicability opinion letter obtained" has no plan. If KeyStone resume suggestions constitute "employment advice" under Singapore Employment Act, product cannot launch.
**Owner**: Founder + lawyer
**Action**: Engage employment lawyer in Week 1-2; budget SGD 3-8K

---

### Gap 3: Single Founder Burnout Risk — No Mitigation Plan

**Severity**: CRITICAL
**Finding**: Single founder executing B2C acquisition, B2B outreach, MVP development, design partner management, Reddit, LinkedIn, compliance simultaneously. Month 1-3 workload = 60-80 hrs/week.
**Owner**: Founder
**Action**: Define founder-only vs delegatable tasks; identify potential co-founder by Month 2

---

### Gap 4: PDPA DPO — No Engagement Plan or Budget

**Severity**: CRITICAL
**Finding**: "External DPO must be engaged" stated as constraint but no plan for which DPO, cost, or timeline.
**Owner**: Founder
**Action**: Get 2-3 DPO quotes in Week 1; budget SGD 500-2K/month

---

### Gap 5: Startup SG Tech Treated as Certainty, Not Contingency

**Severity**: CRITICAL
**Finding**: Government grant referenced as funding source but rejection/downside not modeled.
**Owner**: Founder
**Action**: Apply Month 1; do NOT let any commitment depend solely on approval

---

### Gap 6: 2% Conversion Scenario Not Modeled

**Severity**: CRITICAL
**Finding**: Business model assumes 4-5% conversion. At 2%: Year 1 B2C ARR = ~SGD 180-360, leaving SGD 43K+ burn unfunded.
**Owner**: Founder
**Action**: Define "if Month 3 conversion < 2.5%, then [specific action]"

---

### Gap 7: Data Moat Accumulation Rate Too Slow for Competitive Window

**Severity**: CRITICAL
**Finding**: 1,000 users × 5 apps/month × 5% logging = 250 outcomes/month. 6-month VMock response window = ~1,500 records. Not statistically significant. Plan assumes 18-month window.
**Owner**: Product
**Action**: Reframe moat as "institutional relationships + SG-specific interpretation" not raw data volume

---

## HIGH Findings

### Gap 8: Week 1-4 Execution Plan Has No Specific Milestones

**Finding**: GTM plan describes channels but not week-by-week actions with owners and deliverables.
**Action**: Write 4-week sprint plan with specific milestones.

---

### Gap 9: No Named First Design Partners

**Finding**: "Source from founder network" is aspirational. No named individuals identified.
**Action**: Map 10 specific named prospects by end of Week 1.

---

### Gap 10: Referral Mechanic Has No Defined Incentive Structure

**Finding**: Tier 1 priority channel has no definition of what referrer/referred receives.
**Action**: Define before launch: 1 Pro analysis credit per referral, cap 3/month.

---

### Gap 11: No Career Coach Outreach List or Script

**Finding**: Tier 1 priority channel has no target list or personalization scripts.
**Action**: Produce 20-coach target list with 3-sentence personalization in Week 1.

---

### Gap 12: Month-by-Month Cash Flow Not Modeled

**Finding**: Annual projections hide monthly timing. Founder may run out of money in Month 3-4 before revenue arrives.
**Action**: Build Month 1-18 cash flow model; identify minimum bank balance.

---

### Gap 13: No Legal Entity or Incorporation Plan

**Finding**: Cannot open corporate bank account, sign university contracts, or apply for Startup SG Tech without incorporated entity.
**Action**: Incorporate Singapore Pte Ltd in Week 1-2 (SGD 400-1K via ACRA).

---

## MEDIUM Findings

### Gap 14: Competitive Window Before VMock Response May Be 6 Months, Not 18

**Finding**: VMock has existing SG university architecture. Adding outcome tracking = 3-6 month engineering effort.
**Action**: Assume 6-month window; prioritize institutional signings over data accumulation.

---

### Gap 15: No PMF Numeric Gates

**Finding**: Month 6 review criteria are qualitative ("trending upward").
**Action**: Define specific thresholds: conversion rate ≥2.5%, engagement ≥55% of paid users.

---

### Gap 16: Post-Hire Retention Features Deferred to Year 2, But LTV Problem Is Immediate

**Finding**: Annual Plan is the only retention mechanism for post-hire users; requires marketing to people who just got hired.
**Action**: Partner with 1 recruitment agency to refer post-hire users into Annual Plan from Day 1.

---

## Cross-Reference Audit Summary

| Check | Status |
|-------|--------|
| All specs state Basic = SGD 9 | FIXED — was SGD 12 in mvp-scope.md |
| All specs state Pro = SGD 12 | PASS |
| All specs state Annual = SGD 144 | PASS |
| Conversion rate 4-5% consistent | PASS |
| Break-even = 300 users consistent | FIXED — was ~550 in Analysis 43 summary |
| Annual Plan = ecosystem pass | PASS |
| "Offer Received" trigger in mvp-scope | ADDED |
| University timeline consistent | PASS (Analysis 44 more granular) |
| Agency deal size consistent | PASS |

---

## Three Urgent Actions Before Month 1

1. **Incorporate company** (1 day, unblocks everything: bank account, grants, contracts)
2. **Engage employment lawyer for EAA assessment** (Week 1, SGD 3-8K)
3. **Model 2% conversion downside scenario** (2 hours, determines viability)

---

## Convergence Status

- CRITICAL findings: 3 found, 3 fixed ✓
- CRITICAL gaps: 7 identified, **3 resolved by human decisions** (Gap 2: EAA lawyer engaged, Gap 4: DPO engaged, Gap 6: conversion response = strengthen B2B data exchange)
- **Gap 1 (capital plan), Gap 3 (burnout), Gap 5 (Startup SG Tech)** — decisions recorded in Journal 0036
- HIGH gaps: 6 identified, 0 fixed (require founder action)
- Round 2: Ready to proceed — all CRITICAL findings fixed, all CRITICAL gaps have documented decisions or owner

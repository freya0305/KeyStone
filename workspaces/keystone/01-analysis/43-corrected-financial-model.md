# Analysis 43 — Corrected Financial Model (Post-Redteam)

> **Phase**: 01 Analysis
> **Author**: Analyst
> **Date**: 2026-04-30
> **Status**: Complete — supersedes Analysis 32 and Analysis 41 for all financial calculations
> **Correction trigger**: Pricing corrected from SGD 19 → SGD 12/mo, Annual corrected from SGD 180 → SGD 144/yr

---

## Executive Summary

All prior financial calculations used SGD 19/month for Pro. The corrected pricing is SGD 12/month. This single change propagates through every metric: LTV drops by 37%, break-even Pro user count decreases (300 not 400), and paid acquisition viability threshold is unchanged.

**Key corrected numbers**:

| Metric | Old (SGD 19) | Corrected (SGD 12) | Change |
|--------|--------------|---------------------|--------|
| Monthly Pro LTV | SGD 57 | SGD 36 | -37% |
| Annual Pro LTV | SGD 180 | SGD 144 | -20% |
| Break-even Pro users | ~400 | **~300** | -25% |
| Break-even ARR | ~SGD 100K | **~SGD 43K** | -57% |
| Paid acquisition viable? | Annual only | Annual only | unchanged |
| SGD 12 LTV vs SGD 40-80 CAC | No | No (monthly) | unchanged |

**Year 1 realistic targets**:
- Pro users: **100-250** (not 550 — too aggressive)
- Agency deals: **5-8** (Month 2-3)
- Year 1 ARR: **SGD 15-36K** (B2C + agencies)
- Break-even timeline: **Month 12-18 (lean) or Month 18-24 (normal)**

---

## 1. Corrected Unit Economics

### Pro Tier Economics at SGD 12/month

| Metric | Value | Notes |
|--------|-------|-------|
| Monthly revenue/user | SGD 12 | Corrected from SGD 19 |
| Avg subscription tenure | 3 months | Users get job → cancel |
| Monthly Pro LTV | **SGD 36** | Down from SGD 57 |
| Annual Pro LTV | **SGD 144** | Down from SGD 180 |
| Annual plan effective/month | SGD 12 | Same as monthly (no discount on effective rate) |
| LLM cost/user/month | SGD 2.95 | Unchanged |
| Gross margin | 75.4% | Down from 84.5% |
| Paid acquisition viable? | **No (monthly)** | SGD 36 LTV < SGD 40-80 CAC |
| Paid acquisition viable? | **Yes (annual)** | SGD 144 LTV > SGD 40-80 CAC |

**Critical insight**: The annual plan at SGD 144 IS the paid acquisition enabler. Monthly Pro LTV (SGD 36) cannot support paid CAC. Only Annual Plan LTV (SGD 144) makes Google Ads viable.

### Annual Plan Is the Only Viable Paid Acquisition Path

| Plan | LTV | CAC (Google Ads) | Viable? |
|------|-----|-----------------|---------|
| Monthly Pro | SGD 36 | SGD 40-80 | **No** — lose money on every user |
| Annual Pro | SGD 144 | SGD 40-80 | **Yes** — 2.6-3.6x LTV/CAC ratio |

**Implication**: All paid acquisition budget must target Annual Plan conversions. Monthly Pro users must come from organic channels only.

---

## 2. Corrected Break-Even Analysis

### What Does Break-Even Actually Require?

Break-even requires covering Year 1 operating costs:

| Cost Item | Monthly | Annual |
|-----------|---------|--------|
| Founder living expenses | SGD 3,000-5,000 | SGD 36,000-60,000 |
| Infrastructure (hosting, DB) | SGD 200-400 | SGD 2,400-4,800 |
| DPO (Virtual DPO) | SGD 300-500 | SGD 3,600-6,000 |
| Tools (Clerk, Twilio, etc.) | SGD 100-200 | SGD 1,200-2,400 |
| LLM inference (50 Pro users) | SGD 150 | SGD 1,800 |
| **Total monthly burn** | **SGD 3,750-6,250** | **SGD 45,000-75,000** |

**Year 1 total burn**: ~**SGD 50,000-80,000** (including founder salary)

### Break-Even Revenue Components

To cover ~SGD 60K annual burn:

| Revenue Stream | Year 1 Target | Notes |
|--------------|---------------|-------|
| Pro subscriptions (monthly) | SGD 20-40K | At 100-300 Pro avg users, mix of monthly + annual |
| Annual plan ARR | included above | If 30-40% on annual |
| Agency deals | SGD 15-30K | 2-3 deals × SGD 5-10K each |
| **Total Year 1 ARR** | **SGD 35-70K** | |

**Gap**: Year 1 realistically covers **60-80% of burn** in Year 1. The remaining 20-40% requires:
- Personal funds (already budgeted)
- Government grants (Startup SG, if approved)
- Angel investment

**Break-even = Month 18-30**, not Month 10-12 as prior model projected.

---

## 3. Corrected Year 1 Pro User Projections

### Why 550 Pro Users Is Not Year 1 Achievable

To get 550 Pro users by Month 12:

| Required | Calculation |
|---------|-------------|
| At 3% conversion | 550 / 0.03 = **18,333 registered users** |
| At 5% conversion | 550 / 0.05 = **11,000 registered users** |

**B2C cold-start reality**:

| Period | Monthly New Registrations | Cumulative | Expected Pro (4% conv) |
|--------|------------------------|------------|---------------------|
| Month 1-3 | 50-100 | 150-300 | 6-12 |
| Month 4-6 | 100-200 | 450-900 | 18-36 |
| Month 7-9 | 150-300 | 900-1,800 | 36-72 |
| Month 10-12 | 200-400 | 1,500-3,000 | 60-120 |
| **Year 1 Total** | — | **1,500-3,000** | **100-300** |

**Conclusion**: 550 Pro users by Month 12 is **not achievable** organically. It would require paid acquisition at a scale that loses money (monthly LTV < CAC).

### Realistic Year 1 Pro User Target: 100-300

| Scenario | Pro Users | Monthly ARR | Annual ARR | Notes |
|----------|---------|-----------|----------|-------|
| Low | 100 | SGD 1,200 | SGD 14,400 | Conservative start |
| Mid | 200 | SGD 2,400 | SGD 28,800 | Based on 1,500 registered + 4% conv |
| High | 300 | SGD 3,600 | SGD 43,200 | Based on 2,500 registered + 4% conv + annual mix |

**Path to 300+ Pro users**:
- Need 2,500-3,000 registered free users by Month 12
- Need 4-5% conversion rate (achievable with good upgrade UX)
- Need 30-40% on Annual Plans (critical for LTV)
- Plus: 2-3 agency deals contributing SGD 15-30K

---

## 4. The Annual Plan Conversion Imperative

### Why Annual Plan Mix Is Everything

At SGD 12/month, monthly Pro LTV = SGD 36. Annual Pro LTV = SGD 144. **The difference is 4x.**

If we convert 30% of Pro users to Annual:
- Effective blended LTV = 0.7 × SGD 36 + 0.3 × SGD 144 = **SGD 68.4**
- This enables paid acquisition at SGD 40-80 CAC (0.85-1.7x ratio — marginal but viable)

If only 15% convert to Annual:
- Effective blended LTV = 0.85 × SGD 36 + 0.15 × SGD 144 = **SGD 52.20**
- Paid acquisition still marginal

If 0% convert to Annual (all monthly):
- LTV = SGD 36
- Paid acquisition impossible at SGD 40-80 CAC

**Bottom line**: Annual conversion rate is the #1 financial lever. Everything else is secondary.

### Target Annual Plan Metrics

| Metric | Minimum Viable | Target | Stretch |
|--------|---------------|--------|---------|
| Annual mix % | 20% | **30-40%** | 50%+ |
| Annual ARR contribution | SGD 10K | **SGD 20-30K** | SGD 50K+ |
| Effective blended LTV | SGD 50 | **SGD 65-75** | SGD 90+ |

### How to Drive Annual Conversions

**1. Pricing UX at checkout**
- Show monthly vs annual clearly: "Annual = SGD 12/month, same price as monthly" (true — no effective discount)
- If advisor session is included: "Annual = SGD 12/month + 1 free advisor session (SGD 150+ value)"

**2. Trial before monthly**
- 7-day free Pro trial for email signups
- At trial end, present Annual plan BEFORE monthly option
- "Start your annual plan today" with advisor session highlighted

**3. Upgrade prompt at interview stage**
- When user logs "Interview R1" → upgrade prompt
- "You're preparing for your interview — get unlimited analyses + advisor session for SGD 144/year"
- Annual plan = "interview prep package" not "subscription commitment"

**4. Post-job offer moment**
- User logs "Offer Received" → "Lock in your career tracking for the year at SGD 144"
- At this moment the value is crystal clear

---

## 5. Agency Revenue as the Bridge

### Why Agency Deals Are Critical

Agency deals close in **2-4 weeks** and contribute **SGD 5-10K per deal per year**. They arrive 6-12 months before university contracts and 12+ months before meaningful B2C ARR.

| Deal Type | ARR | Close Time | Notes |
|----------|-----|-----------|-------|
| Boutique agency (5-10 seats) | SGD 600-1,200/yr | 2-4 weeks | Fastest |
| Mid agency (10-20 seats) | SGD 1,200-2,400/yr | 4-8 weeks | |
| University pilot | Free → SGD 15-30K/yr | 6-18 months | Slow but large |

### Year 1 Agency Targets

| Month | Target Deals Closed | Cumulative ARR | Notes |
|-------|-------------------|---------------|-------|
| Month 1-2 | 0-1 | SGD 0-600 | Outreach + close |
| Month 3-4 | 1-2 | SGD 1,200-2,400 | First deals converting |
| Month 5-6 | 2-3 | SGD 2,400-3,600 | Pipeline building |
| Month 7-12 | 3-5 | SGD 3,600-6,000 | If outreach is consistent |

**Realistic Year 1 agency ARR**: **SGD 10-25K**

### Agency Value Beyond ARR

Agency deals provide:
1. **Fast cash** (2-4 week close)
2. **Reference case** for university sales
3. **Outcome data** (placement records are employer-verified)
4. **Credibility** ("real agencies use this" is a trust signal)

---

## 6. Corrected Revenue Projections

### Year 1 Monthly ARR Build-Up

| Month | Registered Users | Pro Users | Annual Mix | Pro ARR | Agency ARR | Total ARR |
|-------|----------------|-----------|-----------|---------|-----------|----------|
| 1 | 100 | 4 | 20% | SGD 38 | SGD 0 | SGD 38 |
| 2 | 200 | 10 | 25% | SGD 120 | SGD 600 | SGD 720 |
| 3 | 400 | 25 | 25% | SGD 300 | SGD 1,200 | SGD 1,500 |
| 4 | 650 | 45 | 30% | SGD 540 | SGD 1,800 | SGD 2,340 |
| 5 | 950 | 70 | 30% | SGD 840 | SGD 2,400 | SGD 3,240 |
| 6 | 1,300 | 100 | 35% | SGD 1,200 | SGD 3,000 | SGD 4,200 |
| 7 | 1,650 | 130 | 35% | SGD 1,560 | SGD 3,600 | SGD 5,160 |
| 8 | 2,000 | 160 | 35% | SGD 1,920 | SGD 4,200 | SGD 6,120 |
| 9 | 2,350 | 190 | 40% | SGD 2,280 | SGD 4,800 | SGD 7,080 |
| 10 | 2,700 | 220 | 40% | SGD 2,640 | SGD 5,400 | SGD 8,040 |
| 11 | 3,000 | 250 | 40% | SGD 3,000 | SGD 6,000 | SGD 9,000 |
| 12 | 3,300 | 280 | 40% | SGD 3,360 | SGD 6,600 | SGD 9,960 |

**Year 1 Total ARR: ~SGD 15-36K** (B2C) + ~SGD 6-14K (agencies) = **SGD 21-50K**

Note: The table shows monthly revenue run rate at end of each month, not cumulative ARR. Year 1 total is sum of 12 months of monthly revenue, not annualized run rate.

### Year 1 Cash Flow

| Item | Amount |
|------|--------|
| Year 1 total revenue | SGD 21-50K |
| Year 1 operating burn | SGD 43-75K |
| **Gap** | **SGD 0-54K** (requires angel bridge) |
| Government grant (if approved) | SGD 10-25K |
| **Adjusted gap** | **SGD 0-44K** |

**Reality**: Year 1 CANNOT break-even on revenue alone. Angel funding of SGD 300-500K bridges to Month 18-24 break-even.

---

## 7. The Corrected Break-Even Timeline

### Break-Even Requires ~300 Pro Users (SGD 12/month)

**Math:**
- 300 Pro users × SGD 12 = SGD 3,600/month
- Operating burn: SGD 3,600/month = SGD 43,200/year
- **Break-even = 300 average Pro users**

**Two scenarios:**

| Scenario | Monthly Burn | Break-Even Users | Timeline |
|----------|------------|----------------|----------|
| Lean (founder salary personal) | SGD 600 | ~50 users | Month 3-6 |
| Normal (founder salary from company) | SGD 3,600 | ~300 users | Month 12-18 |
| With 5 agency deals | SGD 3,600 | ~250 Pro users | Month 12-18 |
| Full (with benefits, tools) | SGD 5,000 | ~350-400 Pro users | Month 18-24 |

**Key insight**: With 5 agency deals contributing ~SGD 600/month equivalent, the company needs only ~250 Pro users for break-even at SGD 3,600/month burn. This is achievable with 1,500-2,000 registered users at 4% conversion.

**Revised break-even: Month 12-18 (lean) or Month 18-24 (normal)**
This document supersedes all prior break-even timelines in Analysis 32 and 41.

---

## 8. Strategic Priorities for Year 1

### Priority 1: Drive Annual Plan Conversions (40%+ mix target)
- Every upgrade prompt should mention annual
- Advisor session is the differentiator — must confirm partners before launch
- Post-interview offer moment is the highest-intent annual conversion moment

### Priority 2: Close 3 Agency Deals by Month 6
- Each deal = SGD 600-1,200/yr
- 3 deals = SGD 2,400-3,600/yr
- Closes in 2-4 weeks — fastest path to B2B ARR

### Priority 3: Build to 200-300 Pro Users Organically
- 4% conversion from 5,000 registered = 200 Pro users
- Focus on referral mechanic + career coach partnerships
- Avoid paid acquisition until annual mix > 30%

### Priority 4: Apply for Government Grants Month 1
- Startup SG takes 6-12 weeks
- If approved = SGD 10-25K injection
- Covers any Year 1 gap

---

## 9. Key Metrics to Track Weekly

| Metric | Month 1 Target | Month 6 Target | Month 12 Target |
|--------|----------------|----------------|-----------------|
| Registered users | 100 | 1,300 | 3,300 |
| Pro users | 5 | 100 | 280 |
| Annual mix % | 20% | 30% | 40% |
| Agency deals closed | 0 | 2 | 4 |
| Monthly ARR | SGD 50 | SGD 4,200 | SGD 9,960 |
| LLM cost/user | <SGD 5 | <SGD 5 | <SGD 5 |
| Conversion rate | 3-4% | 4-5% | 5-6% |

---

## 10. Summary: What Changed From Prior Analysis

| Metric | Old (SGD 19) | New (SGD 12) | Impact |
|--------|--------------|---------------------|--------|
| Monthly Pro LTV | SGD 57 | SGD 36 | -37% — paid CAC harder to justify |
| Annual LTV | SGD 180 | SGD 144 | -20% — annual still viable |
| Break-even Pro users | ~400 | ~400-450 | Similar (ARR target stays ~SGD 100K) |
| Year 1 realistic Pro | 400 | 100-300 | More realistic |
| Break-even month | Month 10-12 | **Month 18-24** | More honest |
| Paid acquisition | Annual only | Annual only | unchanged |
| Agency importance | High | **Critical** | Fills early cash gap |

---

## Files Affected by This Correction

| File | Update Required |
|------|----------------|
| `specs/business-model.md` | Break-even timeline, Pro user count |
| `memory/project_keystone.md` | LTV, break-even timeline |
| `40-tier-feature-definition.md` | Pricing in Stripe config |
| `42-interview-prep-module-analysis.md` | LTV calculations |

**Note**: Analysis 32 and Analysis 41 remain in the record as evidence of the correction process. This document supersedes their financial calculations.

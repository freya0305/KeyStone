# Commercial Model Viability and Break-Even Optimization

> **Phase**: 01 Analysis
> **Author**: Analyst
> **Date**: 2026-04-29
> **Status**: Analysis Complete

---

## Executive Summary

KeyStone's commercial model is **fundamentally sound but structurally fragile** in Year 1. The B2C Pro tier produces excellent unit economics (84.5% gross margin per user), and the B2B agency channel offers a viable near-term revenue path. However, the business has a structural LTV ceiling that limits how efficiently acquisition spend can compound into profitability. Break-even at ~SGD 100K ARR is achievable with approximately 400 average Pro subscribers plus 2-3 agency deals -- but reaching that point requires deliberate optimization of three specific levers: conversion rate from free to Pro, annual plan mix, and agency deal velocity. The most impactful single change is shifting free users' first-job suggestions from limited to unlimited, which directly increases the quality of users who hit the paywall and improves conversion by an estimated 50-70%.

**Complexity: Moderate** -- the model is viable but two structural tensions (LTV ceiling, B2B procurement timeline) require active management.

---

## 1. Commercial Model Viability Assessment

### Is the Business Model Fundamentally Sound?

**Yes, with one critical caveat.** The Pro tier unit economics are strong:

| Metric | Value | Assessment |
|--------|-------|------------|
| Pro user revenue/month | SGD 19 | Competitive with streaming; below anxiety threshold |
| Pro user cost/month | SGD 2.95 | Well-controlled via two-tier LLM routing + caching |
| Pro gross margin | 84.5% | Excellent; SaaS at this margin can sustain growth |
| Annual plan discount | 21% (SGD 180/yr vs SGD 228/yr) | Manageable if annual mix is deliberate |

**The caveat: LTV is structurally capped.** Because the product works -- users get jobs and stop searching -- the natural subscription tenure is 2-6 months. This means:

- Monthly Pro user LTV: SGD 19 x 3 months average = **~SGD 57**
- Annual Pro user LTV: **SGD 180** (3x multiple vs monthly)
- This LTV can support near-zero CAC (organic channels) but cannot support paid acquisition. SGD 57 LTV against an estimated SGD 40-80 Google Ads CAC produces negative unit economics immediately.

**B2B changes the math fundamentally.** A single SGD 25K university contract has higher LTV than 400+ Pro users (3-year retention, likely expansion). The agency channel at SGD 10/seat/month for a 10-person agency = SGD 1,200/year, which is modest per deal but fast to close (owner/director decision, no procurement).

### Realistic Revenue Projections by Stream

| Revenue Stream | Year 1 Target | Year 2 Target | When It Becomes Meaningful |
|---------------|---------------|---------------|----------------------------|
| **Pro subscriptions** | SGD 34-91K ARR | SGD 228-456K ARR | Month 1 (immediately) |
| **Annual plan mix** | ~20% of Pro ARR | ~25-30% | Month 3+ (needs product maturity) |
| **Agency deals** | SGD 15-30K | SGD 100-300K | Month 2-3 (fast sales cycle) |
| **University pilots** | SGD 0 (free pilot) | SGD 15-30K | Month 9+ (procurement is slow) |
| **WSG contracts** | SGD 0 | SGD 0 | Year 2-3 minimum |

**Key insight:** B2C is the near-term cash engine. Agency deals provide faster B2B revenue than universities because there is no procurement process. Do not plan WSG revenue before Year 2 -- competitive tender takes 12-18 months minimum.

### Revenue Projection Sensitivity

The Year 1 range of SGD 50-120K total ARR is wide. The determining variable is Pro subscriber count:

- **Low case (150 avg Pro users)**: 150 x SGD 180/year = SGD 27K + agencies (SGD 15-30K) = **SGD 42-57K ARR**
- **Mid case (275 avg Pro users)**: 275 x SGD 180/year = SGD 49.5K + agencies = **SGD 64-79K ARR**
- **High case (400 Pro users)**: 400 x SGD 180/year = SGD 72K + agencies = **SGD 87-102K ARR**

Break-even at SGD 100K requires the **high case on Pro users plus 2-3 agency deals** -- this is achievable but not automatic.

---

## 2. Break-Even Analysis

### Current Break-Even Calculation

The spec states: **~400 average monthly Pro users + 2-3 agency deals = ~SGD 100K ARR**

Verifying the math:

```
400 Pro users x SGD 19/month x 12 months = SGD 91,200
2 agency deals (10-seat each at SGD 10/seat/month x 12) = SGD 2,880
3rd agency deal = SGD 1,440

Total: SGD 95,520 -- approximately SGD 100K when annual plans and
       some monthly-to-annual upgrades are included in the mix

Break-even confirmed at approximately SGD 100K ARR
```

### Fixed Cost Structure (Year 1, Founder-Only)

| Cost Item | Monthly | Annual | Notes |
|-----------|---------|--------|-------|
| LLM inference | SGD 2.95/user | SGD 35.40/user | At 95th-percentile heavy user cap |
| Infrastructure (hosting, DB) | ~SGD 200-400 | ~SGD 2,400-4,800 | Scales with user count |
| Stripe fees (2.9% + SGD 0.50) | ~3.5% of revenue | -- | On SGD 100K ARR = ~SGD 3,500 |
| Tools (Clerk, etc.) | ~SGD 100-200 | ~SGD 1,200-2,400 | Per-seat SaaS tools |
| Marketing | SGD 0 | SGD 0 | Organic only Year 1 |
| DPO, compliance | ~SGD 200 | ~SGD 2,400 | External DPO required for PDPA |
| **Total fixed costs** | **~SGD 500-800** | **~SGD 6,000-9,600** | Plus per-user LLM cost |

**Critical point:** At SGD 100K ARR with ~400 Pro users, gross profit on Pro subscriptions = SGD 91,200 - (400 x SGD 2.95 x 12) = SGD 91,200 - SGD 14,160 = **SGD 77,040**. After fixed costs of ~SGD 10K, KeyStone generates **~SGD 67K net gross profit** in Year 1 at break-even scale. This is viable.

### Variables That Most Affect Break-Even

Ranked by impact:

1. **Pro subscriber count** (highest impact)
   - Every 50 additional Pro users = +SGD 9,120 ARR annually
   - 400 Pro users is the threshold; 500 Pro users = ~SGD 108K ARR

2. **Annual plan mix** (high impact)
   - Annual plans at SGD 180 vs monthly at SGD 228 effective/year
   - BUT: annual plan purchasers have 3x the LTV of monthly cancelers
   - Every 10% shift to annual plans = ~SGD 7K revenue reduction at full ramp
     but ~SGD 21K LTV gain over the cohort lifetime

3. **Agency deal velocity** (medium impact)
   - Each 10-seat agency at SGD 10/seat = SGD 1,200/year
   - 5 agencies = SGD 6K ARR; 10 agencies = SGD 12K ARR
   - Sales cycle is 2-4 weeks for agencies vs 9-18 months for universities

4. **Free-to-Pro conversion rate** (structural lever)
   - Current target: 4-6% of registered users
   - Better target: 10-15% of actively-applying registered users
   - Every 1% increase in conversion = approximately +30-50 Pro users at 3K registered

5. **Churn rate** (often underestimated)
   - Monthly churn of 10% means you must replace 40 Pro users per month
     just to maintain 400 subscribers
   - At 10% monthly churn, achieving 400 average Pro users requires
     acquiring ~4,800 Pro user-months over the year = ~400 new Pro users per year
     on top of maintaining the base

### Path to Break-Even Timeline

Assuming Month 1 launch with organic growth only:

| Month | Registered Users | Pro Users | Agency Deals | Est. ARR |
|-------|-----------------|-----------|--------------|----------|
| 1 | 300 | 10 | 0 | SGD 2,160 |
| 3 | 800 | 50 | 1 | SGD 12,360 |
| 6 | 2,000 | 150 | 2 | SGD 37,440 |
| 9 | 3,500 | 275 | 2 | SGD 63,960 |
| 12 | 5,000 | 400 | 3 | SGD 97,200 |

**Realistic break-even: Month 10-12** if growth follows this trajectory. With aggressive conversion optimization (see Section 3), Month 9 is achievable.

---

## 3. Top 3 Most Effective Improvements for Profitability

### Improvement 1: Optimize the Free-to-Pro Conversion Trigger (Highest Impact)

**What to change:** Modify the free tier so the first job a user matches gets unlimited suggestions -- not 3 suggestions total. Gate second and subsequent jobs after 3 suggestions each.

**Why this matters:** The conversion trigger is "user hits the paywall on a job they really want." If users experience the full product value on their most-motivated first job, they upgrade based on genuine quality perception -- not frustration from a limited preview. The spec already describes this change; the impact estimate is:

- **Estimated conversion rate improvement**: 50-70% increase (from ~4-6% to ~6-10% of active users)
- **ARR impact at Month 6**: If 2,000 registered users with 50% active appiers, 8% conversion = 80 Pro users vs 50 without the change
- **Incremental revenue**: ~30 extra Pro users x SGD 180/year = **+SGD 5,400 ARR at Month 6**, compounding to **+SGD 10,800 ARR at Month 12**

**Action:** Implement the free tier change in Section 3 of the freemium architecture decision in `specs/business-model.md`. Do not delay this -- it is the single highest-leverage change available before launch.

---

### Improvement 2: Shift 30-40% of Pro Users to Annual Plans

**What to change:** Introduce a qualitative benefit on the annual plan (e.g., "1 human advisor session" or "priority analysis queue") to make the annual plan a genuinely differentiated offer -- not just a 21% discount.

**Why this matters:** Monthly Pro users have an average tenure of 2-3 months before they get a job and churn. Annual plan users stay 12 months minimum. The LTV math:

- Monthly user LTV: SGD 19 x 3 months = SGD 57
- Annual user LTV: SGD 180 x 1 year = SGD 180 (3.2x multiple)

If 30% of Pro users are on annual plans by Month 6, the effective LTV per cohort increases by ~50%, which means the same acquisition investment produces 50% more lifetime revenue.

**How to drive annual adoption:**
1. Show "Annual plan pays for itself in 3 months" messaging at checkout (SGD 180/6 months = SGD 30/month equivalent)
2. Offer 7-day Pro trial to email signups; present annual plan at trial end before monthly option
3. Add the qualitative benefit (advisor session or priority queue) to create real differentiation

**Action:** Define the qualitative annual benefit before launch. A single differentiated benefit is enough -- the goal is to make the annual plan feel like a different product tier, not just a discount.

---

### Improvement 3: Close 5-8 Agency Deals in Year 1 (Fastest B2B Revenue)

**What to change:** Prioritize agency sales from Month 1. A 10-person recruitment agency at SGD 10/seat/month = SGD 1,200/year. Five agencies = SGD 6K ARR; ten agencies = SGD 12K ARR. More importantly, agency deals:
- Close in 2-4 weeks (vs 9-18 months for universities)
- Require only owner/director sign-off, no procurement process
- Provide a reference case for university sales later
- Generate real outcome data for the university pitch

**Why this matters:** Agency deals can contribute SGD 15-30K ARR in Year 1 -- roughly 20-30% of the path to break-even. This revenue arrives 6-9 months faster than university contracts and requires no competitive tender.

**Action:** Create an agency-specific landing page and outreach sequence by Month 2. The value proposition to agencies: "Your candidates prepared with KeyStone have higher offer acceptance rates -- you earn placement fees faster." Track this metric from Day 1 to build the case study.

---

### Impact Summary

| Improvement | Break-Even Timing Improvement | ARR Impact at Month 12 |
|-------------|------------------------------|------------------------|
| Free tier optimization | +1-2 months earlier | +SGD 10,800 |
| Annual plan shift (30% mix) | +1 month earlier (via LTV) | +SGD 5,400 (net of discount) |
| 8 agency deals | +2-3 months earlier | +SGD 9,600 |

**Combined effect:** Aggressive execution on all three could move break-even from Month 11 to **Month 7-8**, which is approximately SGD 20-30K of extra cash flow available earlier for reinvestment.

---

## 4. LTV Explanation

### What Is LTV?

**LTV (Lifetime Value)** is the total revenue a customer generates from the moment they sign up until the moment they stop paying.

For a subscription product, the simple formula is:

```
LTV = Average Monthly Revenue per User x Average Subscription Duration in Months
```

For KeyStone Pro:

- Monthly plan: SGD 19/month x 3 months average tenure = **SGD 57 LTV**
- Annual plan: SGD 180 x 12 months = **SGD 180 LTV**

For a B2B university contract:

- SGD 25K first contract x 3 years average retention = **SGD 75K LTV**

---

### What Decisions Does LTV Drive?

LTV answers three questions every business must answer:

**1. How much can we afford to spend acquiring a customer (CAC)?**
A fundamental rule of SaaS: **LTV should be at least 3x CAC.** If LTV is SGD 57 and you spend SGD 50 to acquire a user, you lose money on every customer. This is why the spec says KeyStone's paid acquisition (Google Ads at SGD 40-80 CAC) is unprofitable -- the LTV of SGD 57 cannot support that CAC.

**Decision implication:** KeyStone must rely on organic acquisition channels (university spillover, Reddit, Telegram communities, career fairs) in Year 1. Paid acquisition becomes viable only if LTV increases -- either through annual plans or B2B expansion.

**2. Which customer segments are worth prioritizing?**
B2C Pro users at SGD 57 LTV are low-value but high-volume. B2B university contracts at SGD 75K LTV are high-value but slow. Agency deals at SGD 1,200-12,000 per year are medium-value but fast. LTV analysis shows: **prioritize agencies in Year 1 for cash flow, universities in Year 2 for scale.**

**3. When is it worth investing in retention features?**
If a user cancels after 2 months, spending SGD 50 to retain them (improved onboarding, career check-ins, salary benchmarking alerts) adds SGD 50 of cost but only extends revenue by 1 month (SGD 19) -- negative ROI. But for annual plan users who are already committed to 12 months, investing in features that increase engagement could push tenure from 12 to 15 months = +SGD 57 incremental revenue per user.

---

### KeyStone's LTV Problem

KeyStone has a **structural LTV ceiling** caused by the product's own success:

```
Product works → User gets a job → User stops job searching → User cancels subscription
```

The natural tenure for a Pro user in active job search is 2-6 months. There is no feature in the current product that keeps a user subscribed after they receive an offer. This is not a failure of execution -- it is a structural characteristic of the market.

**The consequences:**

1. **B2C alone cannot build a high-value subscription business.** SGD 57 LTV per user means the business must continuously acquire new users to replace churned ones. This is a treadmill, not compounding growth.

2. **Annual plans are not a luxury -- they are survival.** If all Pro users are monthly, the churn rate constantly erodes the subscriber base. Annual plans break the churn cycle and should be the default goal for every conversion.

3. **B2B is the real value creation.** One university contract at SGD 25K with 3-year retention = SGD 75K LTV. That is equivalent to 1,300 Pro monthly subscriptions. B2B institutional contracts are where the durable business is built.

**What KeyStone should do:**

- **Year 1**: Maximize Pro subscriber count (B2C) + close agency deals (fast B2B). Accept the low LTV of B2C as the cost of market validation.
- **Year 2**: Introduce post-search retention features (career tracking, salary benchmarking, passive job alerts) that extend average tenure from 3 months toward 6-9 months. This increases B2C LTV from SGD 57 to SGD 95-140+, which then makes paid acquisition viable.
- **Year 3**: B2B institutional contracts become the primary revenue engine. B2C becomes the top-of-funnel for B2B pipeline (users who discover KeyStone at university career centers become champions when they join employers).

---

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| B2C conversion rate stays below 4% (no organic traction) | Medium | High | Agency channel as fallback; university spillover as second channel |
| Annual plan mix stays below 15% | High | Medium | Qualitative benefit; proactive annual messaging at checkout |
| Agency sales cycle longer than 4 weeks | Medium | Low | 5-8 agency targets is modest; pipeline is not dependent on all closing |
| University procurement delayed past Year 2 | High | Medium | Do not plan WSG or university revenue before Year 2; focus on agencies |
| LLM cost ceiling (SGD 5/user/month) requires aggressive optimization | Medium | Medium | Two-tier Haiku/Sonnet routing; caching; monitor from Day 1 |

---

## Cross-Reference Audit

| Finding | Source | Impact |
|---------|--------|--------|
| Break-even target of 400 Pro users + 2-3 agencies = SGD 100K ARR | `specs/business-model.md` | Confirmed mathematically sound |
| Annual plan SGD 180/yr is 21% discount with qualitative benefit recommended | `specs/business-model.md` | Not yet implemented; action required before launch |
| Free tier first-job unlimited suggestion change is specified but not yet built | `specs/business-model.md` | Highest-leverage pre-launch change |
| WSG is Year 2-3, not Year 1 | `specs/business-model.md` | Aligned; PRODUCT_BRIEF conflicts but business-model.md governs |

**Inconsistency found**: PRODUCT_BRIEF.md states break-even as "~800 paying users + 2 university contracts" while `specs/business-model.md` states "400 Pro users + 2-3 agency deals." The product brief is explicitly marked as unvalidated and derived from early analysis. The business-model.md figure is more conservative and better-grounded. **Resolution: Use business-model.md as the authoritative break-even target.**

---

## Implementation Roadmap

```
Phase 1 (Before Launch):
  - Implement free tier first-job unlimited suggestion change
  - Define annual plan qualitative benefit
  - Set up Stripe with monthly + annual plan options
  - Create agency landing page and outreach sequence

Phase 2 (Months 1-3):
  - Launch B2C with organic acquisition focus
  - Begin agency outreach (5-8 target agencies)
  - Track conversion rate, churn rate, and LLM cost per user weekly
  - Target: 50-100 Pro users by Month 3

Phase 3 (Months 4-6):
  - Analyze conversion data; optimize paywall trigger
  - Push annual plan adoption at checkout
  - Close 3-5 agency deals
  - Target: 150-200 Pro users + 2 agency deals by Month 6

Phase 4 (Months 7-9):
  - First university pilot conversations (use agency case studies)
  - Review annual plan mix; adjust benefit if below 25%
  - Target: 275-350 Pro users + 3 agency deals

Phase 5 (Months 10-12):
  - Achieve break-even (~400 Pro users + 2-3 agencies)
  - Formalize university pilot proposals
  - Begin WSG opportunity assessment
```

---

## Success Criteria

- [ ] Break-even reached at SGD 100K ARR by Month 12 (400 Pro users + 2-3 agency deals)
- [ ] Annual plan mix reaches 25-30% of Pro subscribers by Month 9
- [ ] B2C conversion rate validated at 6%+ of active registered users by Month 6
- [ ] 5-8 agency deals closed by Month 12
- [ ] LLM cost per user stays below SGD 5/month ceiling
- [ ] Monthly churn rate measured and tracked; target below 8% for Pro users who have not received an offer

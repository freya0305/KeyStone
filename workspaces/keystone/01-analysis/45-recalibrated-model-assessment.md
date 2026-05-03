# Analysis 45 — Recalibrated Break-Even & Model Viability Assessment

> **Phase**: 01 Analysis
> **Author**: Analyst
> **Date**: 2026-04-30
> **Status**: Complete
> **Purpose**: Honest assessment of whether the KeyStone model holds together

---

## Executive Summary

**The model has real structural problems that need to be addressed before launch.**

### Critical Findings

| Issue | Severity | Impact |
|-------|----------|--------|
| specs/business-model.md still uses OLD pricing (SGD 19) | CRITICAL | All B2C revenue projections are 37% too high |
| B2C LTV ceiling is SGD 36, not enough for paid acquisition | CRITICAL | Cannot scale B2C via Google Ads |
| 400-450 Pro users required for break-even | HIGH | Requires 10,000+ registered users at 4% conversion |
| University revenue arrives at Month 18-24, not Year 1 | HIGH | Gap between burn and revenue in Year 1 |
| Conversion rate assumption (4-5%) may be optimistic | MEDIUM | Registered → paid conversion is hard |

**Bottom line**: The model CAN work, but only if:
1. Fix the pricing in business-model.md immediately
2. Accept that Year 1 needs angel bridge funding (not self-sustaining)
3. Agency deals are the only reliable Year 1 B2B revenue
4. B2C growth depends entirely on organic channels (no paid acquisition)

---

## 1. Corrected Break-Even Analysis

### 1.1 Corrected Cost Structure

| Cost Item | Monthly | Annual | Notes |
|-----------|---------|--------|-------|
| Founder living expenses | SGD 3,000 | SGD 36,000 | Only if not personally funded |
| Infrastructure (AWS, DB) | SGD 300 | SGD 3,600 | |
| Tools (Clerk, Twilio, etc.) | SGD 150 | SGD 1,800 | |
| LLM inference (50 Pro users) | SGD 150 | SGD 1,800 | |
| **Total operating burn** | **SGD 3,600** | **SGD 43,200** | Excludes founder salary if personally covered |

**Minimum viable burn (founder personally funded)**: SGD 600/month = SGD 7,200/year

### 1.2 Break-Even Revenue Requirements (CORRECTED)

At SGD 12/month Pro pricing (not SGD 19):

| Revenue Source | Per User | Break-Even Units | ARR |
|---------------|----------|-----------------|-----|
| Pro users only | SGD 12/mo | 300 users | SGD 43,200 |
| Pro + Basic mix (60/40) | SGD 10.8 avg | 300 users | SGD 38,880 |
| Pro + Basic (50/50) | SGD 10.5 avg | 300 users | SGD 37,800 |

**Break-even requires 300 average Pro-equivalent users** (at SGD 12/user/month)

### 1.3 User Funnel Required

To reach 300 Pro users:

| Stage | Conversion | Required | Notes |
|-------|-----------|----------|-------|
| Registered users | — | 6,000-7,500 | At 4-5% conversion |
| Active applying users | 50% of registered | 3,000-3,750 | Users who complete ≥1 analysis |
| Free → Paid conversion | 4-5% | 120-188 | Of active users |
| Free tier exhaustion trigger | — | 60-94 | Users who hit limit and upgrade |

**Alternative path via interview trigger**:
- Users who reach "Interview Stage" have 10-20× higher conversion intent
- If 10% of Pro users reach interview stage = 30 users/month hitting upgrade moment
- But only ~300/month active users → only 30 new interviews/month
- Need to scale user base first

### 1.4 Revised Break-Even Timeline

| Scenario | Monthly Burn | Year 1 Burn | Year 1 Revenue | Gap | Angel Needed? |
|----------|------------|-------------|----------------|-----|---------------|
| Lean (founder personally funded) | SGD 600 | SGD 7,200 | SGD 20-57K | Covered | NO |
| Normal (SGD 3,600/mo) | SGD 3,600 | SGD 43,200 | SGD 20-57K | SGD 0-23K | YES |
| Full (SGD 5,000/mo) | SGD 5,000 | SGD 60,000 | SGD 20-57K | SGD 3-40K | YES |

**Revised break-even timeline**: Month 12-18 if:
- Lean burn (personally funded founder)
- 200+ Pro users by Month 12
- 5+ agency deals

**If founder salary required**: Month 18-24 with SGD 300-500K angel bridge.

---

## 2. Revenue Projections — Corrected

### 2.1 B2C Revenue (CORRECTED for SGD 12 pricing)

| Year | Registered Users | Pro Users | Monthly ARR | Annual ARR |
|------|----------------|-----------|-------------|-----------|
| 1 | 1,500-3,000 | 60-150 | SGD 720-1,800 | SGD 8,640-21,600 |
| 2 | 5,000-10,000 | 200-500 | SGD 2,400-6,000 | SGD 28,800-72,000 |
| 3 | 15,000-30,000 | 600-1,500 | SGD 7,200-18,000 | SGD 86,400-216,000 |

**CORRECTED from prior projections that used SGD 19/month**

### 2.2 B2B Revenue (Confirmed)

| Year | Agency Deals | Agency ARR | University Contracts | University ARR | B2B Total |
|------|-------------|-----------|-------------------|---------------|-----------|
| 1 | 5-12 | SGD 6-14K | 0 (free pilots) | SGD 0 | SGD 6-14K |
| 2 | 10-20 | SGD 12-24K | 1-2 | SGD 15-30K | SGD 27-54K |
| 3 | 20-40 | SGD 24-48K | 3-5 | SGD 50-100K | SGD 74-148K |

### 2.3 Total Revenue (CORRECTED)

| Year | B2C | B2B | Total | vs Old (SGD 19) |
|------|------|------|-------|-----------------|
| 1 | SGD 9-22K | SGD 6-14K | **SGD 15-36K** | -37% vs prior |
| 2 | SGD 29-72K | SGD 27-54K | **SGD 56-126K** | -30% vs prior |
| 3 | SGD 86-216K | SGD 74-148K | **SGD 160-364K** | -25% vs prior |

**The pricing correction (SGD 19 → SGD 12) reduces Year 1 revenue projections by ~37%.**

---

## 3. Model Viability Assessment

### 3.1 Is the Model Valid? YES, WITH CAVEATS

**The core value proposition is sound**:
- SG job seekers genuinely need resume tailoring
- First-job-free unlimited is a strong conversion hook
- Interview stage upgrade trigger is high-intent
- Outcome data moat is genuinely defensible (Teal cannot replicate)

**The structural problem: B2C LTV is too low for paid acquisition**

| Metric | Value | Problem |
|--------|-------|---------|
| Monthly Pro LTV | SGD 36 | < SGD 40-80 CAC |
| Annual LTV | SGD 144 | Paid acquisition barely viable |
| Avg subscription length | 3 months | Users churn when they get jobs |

**This means**:
- Cannot use Google Ads or any paid channel for B2C acquisition
- All B2C growth must be organic (referral, Reddit, community)
- Growth will be slower than models that assume paid acquisition

### 3.2 Is B2B-as-Primary Valid? YES

**Agency channel is validated**:
- 2-4 week sales cycle (fast)
- SGD 600-1,200/deal (modest but meaningful)
- No procurement overhead below SGD 30K

**University channel is realistic**:
- 18-24 months to first paid contract
- Year 1 is free pilots, Year 2+ is real revenue
- SGD 15-30K first contracts are below tender threshold

**The B2B model works IF**:
- Founder prioritizes agency outreach from Day 1
- University pilots start in Month 1-3
- Patience for 18-24 month university cycle

### 3.3 Is Annual Plan-as-Ecosystem-Pass Valid? YES

**The reframe is correct**:
- Job seekers won't prepay 12 months
- But users who GET jobs might pay to stay tracked
- "Offer Received" moment is high-intent

**But there is a problem**: The Annual Plan requires users to:
1. Complete their job search successfully
2. Decide to stay in the KeyStone ecosystem
3. Pay SGD 144 upfront

**This is a very narrow funnel**. Only a fraction of users who get jobs will want post-hire tracking.

---

## 4. Critical Issues That Must Be Fixed

### Issue 1: specs/business-model.md Uses WRONG Pricing

**Status**: CRITICAL — this is an active error in the codebase

The file still states:
- Pro: SGD 19/month (should be SGD 12)
- Annual: SGD 180/year (should be SGD 144)
- All revenue projections are 37% too high

**Fix required**: Update specs/business-model.md immediately

### Issue 2: B2C Projections Are Overstated

**Prior projection (using SGD 19)**:
- Year 1 B2C: SGD 34-91K

**Corrected projection (using SGD 12)**:
- Year 1 B2C: SGD 9-22K

**The difference**: SGD 25-69K less Year 1 B2C revenue

### Issue 3: Break-Even "400 Pro Users" Was Based on Wrong Price

**Prior (SGD 19)**:
- 400 users × SGD 19 = SGD 7,600/month = SGD 91K ARR

**Corrected (SGD 12)**:
- 400 users × SGD 12 = SGD 4,800/month = SGD 58K ARR
- At SGD 3,600/month burn, need ~300 users for break-even

---

## 5. Honest Scenario Analysis

### Scenario A: Lean Launch (Founder Personally Funded)

| Factor | Value |
|--------|-------|
| Monthly burn | SGD 600 (infra only) |
| Founder salary | Personal funds |
| Year 1 revenue target | SGD 15-36K |
| Break-even | Month 6-12 (if 100+ Pro users) |
| Angel needed? | NO |
| Feasibility | HIGH |

**This is viable if founder can personally cover living expenses.**

### Scenario B: Normal Launch (With Angel Funding)

| Factor | Value |
|--------|-------|
| Monthly burn | SGD 3,600 |
| Year 1 burn | SGD 43,200 |
| Year 1 revenue | SGD 15-36K |
| Gap | SGD 7-28K |
| Angel raise needed | SGD 300-500K |
| Break-even | Month 18-24 |
| Feasibility | MEDIUM |

**This is viable with SGD 300-500K angel bridge.**

### Scenario C: Aggressive Launch (With Paid Acquisition)

| Factor | Value |
|--------|-------|
| Monthly burn | SGD 5,000+ |
| Paid acquisition | SGD 40-80 CAC |
| LTV | SGD 36 (monthly) / SGD 144 (annual) |
| Paid CAC viable? | NO (monthly), MARGINAL (annual) |
| Strategy | Annual-only paid acquisition |
| Feasibility | LOW |

**This does not work. Cannot use paid acquisition for monthly B2C.**

---

## 6. What MUST Be True For Model to Work

### For Year 1 Viability

| Assumption | Required | Current Estimate | Gap |
|-----------|----------|-----------------|-----|
| Registered users | 1,500-3,000 | 50-100/month organic | Need referral + community |
| Pro conversion rate | 4-5% | Unknown | Need to validate |
| Agency deals | 5-8 | 0.5-0.9/month close rate | Need aggressive outreach |
| University pilots | 2-3 | 0 started | Need to begin outreach |
| Monthly burn | ≤SGD 3,600 | SGD 3,600 | No gap |
| Government grant | SGD 10-25K | Not approved | Risk |

### For Break-Even by Month 18-24

| Assumption | Required | Risk |
|-----------|----------|------|
| 300+ Pro users | 300 | High — needs strong B2C growth |
| 5+ agency deals | 5 | Medium — outreach-dependent |
| 1 university contract | 1 | High — 18-24 month cycle |
| Government grant | Approved | Risk — 6-12 week process |
| Founder personally funded | Partial | Medium — personal cash required |

---

## 7. Revised Recommendations

### 7.1 Immediate Fixes (Before Any Further Analysis)

1. **Update specs/business-model.md** — Fix SGD 19 → SGD 12, SGD 180 → SGD 144
2. **Update all financial projections** — Based on corrected pricing
3. **Update memory file** — With corrected Year 1 revenue estimates

### 7.2 Strategic Adjustments

1. **Target Scenario B (Normal Launch)** — Lean but with angel funding bridge
2. **Raise SGD 300-500K** — Not for growth, but for survival through Month 18-24
3. **Prioritize agency deals** — Only reliable Year 1 B2B revenue
4. **Accept B2C is slow organic growth** — No paid acquisition possible
5. **Start university outreach NOW** — 18-24 month cycle means Day 1

### 7.3 What to Tell Investors

**Honest pitch**:
- "We are a lean B2B SaaS, not a growth-at-all-costs B2C"
- "Year 1 revenue is SGD 15-36K; we need angel bridge to cover SGD 43K burn"
- "Break-even at Month 18-24 with 300 Pro users + 5 agency deals"
- "We are not building a B2C subscription business — we are building a data moat"
- "B2C is free users generating outcome data that B2B buyers will pay for"

**The pitch is actually stronger if we stop pretending B2C is the revenue driver.**

---

## 8. Final Assessment

### Is the Model Viable? YES, with significant caveats

**The model works IF**:
- [ ] Founder accepts lean operations (personally funded salary OR SGD 300K raise)
- [ ] B2C growth is organic only (no paid acquisition)
- [ ] Agency deals are prioritized from Day 1
- [ ] University outreach starts immediately
- [ ] Government grants are applied for in Month 1

**The model fails IF**:
- [ ] Founder expects B2C to drive revenue (it won't at SGD 12/user/month)
- [ ] Paid acquisition is attempted for B2C (LTV < CAC)
- [ ] University timeline is underestimated (18-24 months is real)
- [ ] Government grants are counted on (6-12 week process, not guaranteed)

### The Fundamental Insight

**KeyStone is not a B2C subscription business. KeyStone is a B2B data company that uses B2C as a data collection mechanism.**

The subscription revenue (SGD 12/month) is not the point. The point is:
1. Get free users to generate outcome data
2. Use outcome data to prove product works
3. Sell B2B contracts (university, agency) using that data
4. Use B2B revenue to fund further data collection

**If the founder accepts this framing, the model is viable.**
**If the founder expects B2C subscription revenue to fund operations, the model fails.**

---

## Appendix: Corrected Numbers Summary

| Metric | Old (SGD 19) | Corrected (SGD 12) | Change |
|--------|--------------|---------------------|--------|
| Monthly Pro LTV | SGD 57 | SGD 36 | -37% |
| Annual Pro LTV | SGD 180 | SGD 144 | -20% |
| Year 1 B2C revenue | SGD 34-91K | SGD 9-22K | -73% to -76% |
| Year 1 total revenue | SGD 50-120K | SGD 15-36K | -70% |
| Break-even users | 400 | 300 | -25% |
| Break-even ARR | ~SGD 100K | ~SGD 43K | -57% |
| Paid acquisition | Annual only | Annual only | unchanged |

# Red Team: KeyStone Business Model

> **Red team date**: 2026-04-30
> **Reviewer**: quality-reviewer
> **Sources**: `32-commercial-model-and-break-even-optimization.md`, `41-break-even-risks-and-cac-analysis.md`, `40-tier-feature-definition.md`

---

## Executive Summary

The business model has a **critical pricing discrepancy** that invalidates the entire financial model. The Pro tier is stated as SGD 12/month in the feature definitions but SGD 19/month in the commercial model and break-even analysis. Every LTV, CAC, and break-even calculation in the analysis documents uses SGD 19 — producing numbers that are 58% too high. This single error means the actual path to break-even requires 58% more Pro subscribers than modeled.

Beyond the pricing discrepancy, the model has structural risks in B2B timing, B2C conversion validation, and the first-job unlimited free tier that collectively could prevent reaching break-even before runway expires.

---

## CRITICAL Issues (Must Fix Before Launch)

### Finding 1: Pro Tier Pricing Discrepancy — All Financial Projections Invalid

**Evidence**:
- `40-tier-feature-definition.md` §7.1: Pro = SGD 12/month
- `40-tier-feature-definition.md` §9.1 Stripe config: Pro = SGD 12/month
- `32-commercial-model-and-break-even-optimization.md` line 26: "Pro user revenue/month | SGD 19"
- `32-commercial-model-and-break-even-optimization.md` line 72: "400 Pro users x SGD 19/month"
- `32-commercial-model-and-break-even-optimization.md` line 219: "Monthly Pro LTV = SGD 19 × 3 months = SGD 57"
- `41-break-even-risks-and-cac-analysis.md` line 88: "Monthly Pro | SGD 19/month | 3 months | SGD 57"

**Impact**: Every financial calculation in both analysis documents is wrong by 58%.

Recalculated at SGD 12/month:
- Monthly Pro LTV: SGD 12 × 3 months = **SGD 36** (vs SGD 57 modeled)
- Annual Pro LTV: SGD 144/year = **SGD 144** (vs SGD 180 modeled)
- Break-even at 400 Pro users: 400 × SGD 12 × 12 = **SGD 57,600** (vs SGD 91,200 modeled)
- CAC viability: SGD 40-80 CAC vs SGD 36 LTV — **paid acquisition is deeply unprofitable** at the lower price too, but the gap is now worse

**Break-even recalculation** at SGD 12/month:
```
400 Pro × SGD 12 × 12 = SGD 57,600
3 agency deals × SGD 1,440 = SGD 4,320
Total: SGD 61,920 — NOT SGD 100K
```

The stated "SGD 100K break-even" target does not match the pricing in the feature definitions. Either the break-even target must be revised to ~SGD 62K, or the pricing must be updated to SGD 19/month across all documents.

**Fix required**: Decide on actual pricing (SGD 12 or SGD 19) and make it consistent across ALL documents before any financial projection is used for decisions.

---

### Finding 2: B2B Revenue Timing Risk — No University Revenue Until Year 2, Agencies May Not Scale

**Evidence** (`41-break-even-risks-and-cac-analysis.md`):
- University deals: "6-18 months procurement" → earliest meaningful revenue is Month 18-24
- University pilots start Month 9 (free), Year 2 contracts SGD 15-30K
- WSG contracts: "Year 2-3 minimum"
- Agency deals: "2-4 weeks sales cycle" but "8 agency deals in Year 1" requires 20-40 conversations

**The timing problem**:
- Break-even is modeled at Month 10-12 with 400 Pro users + 2-3 agency deals
- Agency deals contribute SGD 15-30K Year 1 at SGD 1,200-4,800 per deal
- But agency sales requires personal outreach and is described as "relationship business" — not scalable
- If agency deals fall short (say only 1 closes instead of 3), Year 1 ARR is ~SGD 30-40K below projection

**The runway question**: If break-even slips to Month 18-24 (as the documents acknowledge is possible), what funds operations? The analysis assumes break-even at Month 10-12. No contingency is modeled for a 6-12 month slip.

**Fix required**: Model a downside scenario where agency deals = 0 in Year 1. Quantify minimum viable Pro subscriber count to survive 18 months on B2C revenue alone. This is the actual break-even scenario that needs validation.

---

### Finding 3: First-Job Unlimited Free Tier May Eliminate Upgrade Incentive

**Evidence** (`40-tier-feature-definition.md` §1.1):
- "The FIRST job analyzed after registration = UNLIMITED suggestions"
- "This is the full-value demonstration — no gates, no limits"
- "After the first job, subsequent analyses fall under the 3/month limit"

**The conversion logic assumes**: User gets full value on first job, still wants more, upgrades.

**The structural risk**: If the user's first job search ends successfully (they get an offer using only the free tier), they experienced the full product, paid nothing, and have zero reason to ever upgrade. The model assumes users will have multiple job searches — but the first-job seeker (fresh grad) may only need one.

**The second-job assumption**: The model depends on users hitting the paywall on a *second* job. But:
- Many job seekers send 10-20 applications for their first job and get an offer
- By the time they need a second job (12-18 months later), they have a resume that already worked once
- The urgency to upgrade may not recur

**The upgrade trigger depends on frustration, not outcome**: The analysis notes "the real upgrade moment is NOT running out of analyses — it is reaching the INTERVIEW STAGE." But a user who got their offer using only free unlimited suggestions has already demonstrated they can win without paying. The interview-stage trigger assumes users haven't already succeeded with the free product.

**Fix required**: Validate the assumption that users need a second job search before the free tier runs out of value. If 30%+ of free users get an offer on their first job search using only free suggestions, the upgrade funnel collapses.

---

### Finding 4: Interview-Stage 10-20× Conversion Premium Is Unvalidated

**Evidence** (`40-tier-feature-definition.md` line 99):
- "Interview stage users have 10-20× higher conversion intent than resume-tailoring-only users"

This is stated as fact but no source is cited, no baseline is provided, and no data is referenced.

**The claim is central to the entire conversion strategy**: Pro upgrade is triggered by reaching interview stage. If the 10-20× multiplier is wrong:
- If actual multiplier is 3-5×, the conversion rate model is overstated
- If interview-stage users are rare (<5% of free users), the total Pro subscriber count is unachievable
- If interview-stage users convert at the same rate as other users, there is no special upgrade moment

**No validation evidence**:
- No A/B test data cited
- No industry benchmark cited
- No user research cited
- The range 10-20× is a 2× spread — too wide to be actionable

**Fix required**: This claim must be validated with user research or early cohort data before the product roadmap is built around it. At minimum, a 3-5× range should be established from existing job-search platform data or Singapore employment statistics.

---

## MEDIUM Issues (Should Fix)

### Finding 5: Annual Plan "No Discount" Positioning Destroys the Primary Conversion Trigger

**Evidence** (`40-tier-feature-definition.md` §7.2):
- "Do NOT position Annual as 'save SGD 0 vs monthly.' Monthly Pro = SGD 12 × 12 = SGD 144. Annual = SGD 144. There is no discount."

**The problem**: If there is no discount, what is the annual plan's conversion rationale? The documents propose:
- "Career advisor session" as the differentiator
- "Priority feature access" as the differentiator

But the advisor session is **not confirmed with actual partners** before launch (Finding from `41-break-even-risks-and-cac-analysis.md` Risk 2a). If it launches without confirmed advisors, the annual plan's primary differentiator is fictional.

**Without a discount AND without confirmed advisor partners**, the annual plan has no reason to exist. Users will choose monthly because:
- No financial incentive to commit 12 months upfront
- The "benefit" (advisor session) may not be bookable
- Locking in SGD 144 feels risky for an unproven product

**Alternative perspective**: The conventional SaaS wisdom is that annual plans should offer 10-20% discount precisely because they solve the churn problem (users who churn cost more than the discount). Hiding the discount in favor of an unconfirmed benefit is optimizing for the wrong conversion driver.

**Fix required**: Either confirm advisor partners and build the booking flow before launch, OR reposition Annual with a genuine 15-20% discount as the primary conversion driver.

---

### Finding 6: LLM Cost Ceiling of SGD 5/User/Month May Be Architectural Debt

**Evidence** (`41-break-even-risks-and-cac-analysis.md` line 279):
- "LLM cost ceiling (SGD 5/user/month) requires aggressive optimization"

And `41-break-even-risks-and-cac-analysis.md` line 30:
- "Pro user cost/month = SGD 2.95"

The analysis uses SGD 2.95/user/month as the cost basis, but notes this requires "two-tier Haiku/Sonnet routing + caching." This is an architectural requirement that must be implemented, not a given.

**The risk**: If the caching and routing architecture is not in place at launch:
- Heavy users could generate 50+ suggestions per job
- At SGD 0.01-0.05 per suggestion (estimated LLM cost), 50 suggestions = SGD 0.50-2.50 per job
- Active job seekers applying to 10 jobs/month could generate SGD 5-25 in LLM costs against SGD 12 revenue

**Fix required**: The two-tier routing and caching architecture must be implemented before launch, not as a post-launch optimization. The break-even model uses SGD 2.95/user/month as the cost basis — if actual costs run higher, every LTV calculation is wrong.

---

### Finding 7: Basic Tier (SGD 9/month) Appears to Have Negative Unit Economics

**Evidence** (`40-tier-feature-definition.md` §1.2):
- Basic includes UNLIMITED job analyses
- Basic price: SGD 9/month
- LLM cost at heavy usage: SGD 5/user/month (the ceiling)
- Infrastructure costs: ~SGD 200-400/month fixed + per-user costs

**The math problem**: If Basic users are heavy job seekers (they upgraded specifically because they want unlimited analyses), they could generate LLM costs approaching SGD 5/user/month. At SGD 5 cost vs SGD 9 revenue, Basic tier generates SGD 4 gross margin per user — before infrastructure, before Stripe fees.

Stripe fees on SGD 9: ~3.5% + SGD 0.50 = ~SGD 0.82
Infrastructure per-user: allocated share of SGD 200-400/month across all users

Basic tier may be **margin-negative at moderate-to-heavy usage**. The tier is described as a "price-sensitive user acquisition" tier, but if those users generate negative gross margin, acquiring them at any CAC is unprofitable.

**Fix required**: Model Basic tier actual costs at different usage levels. If Basic users generate >SGD 5.50/user/month in LLM costs (plausible for active job seekers), the tier is margin-negative. Consider:
- Capping Basic analyses at a lower number (e.g., 10-15/month) to limit LLM exposure
- Or accepting that Basic is a loss-leader and treating its costs as customer acquisition investment

---

## LOW Issues (Nice to Have)

### Finding 8: Post-Job Outcome Logging ("P0 — Near-Zero Cost") Underestimates Implementation Effort

**Evidence** (`41-break-even-risks-and-cac-analysis.md` §3, Feature A):
- Listed as "P0 — launch with" because it is "near zero cost"
- Implementation: "Automated email sequence triggered when user hasn't logged in for 14 days"

**The nice-to-have concern**: "Near-zero cost" refers only to LLM inference costs. The actual implementation requires:
- Email automation infrastructure (or integration with email provider)
- User preference/opt-in for post-job emails (PDPA compliance)
- The outcome logging UX flow
- 30/90-day check-in email sequences
- Re-activation flow if user left role

This is not zero-cost to implement. It is low-cost relative to other features, but it is still a sprint of engineering work.

**Mitigation**: Acknowledge this is a Month 2-3 feature, not a launch feature. Or implement a minimal version (one "congratulations" email) at launch and expand the sequence later.

---

### Finding 9: Agency Value Proposition Assumes Outcome Tracking That Requires Pro Tier

**Evidence** (`41-break-even-risks-and-cac-analysis.md` §3):
- Agency value prop: "candidates prepared with KeyStone → higher offer acceptance rate"
- This metric requires tracking which candidates used KeyStone, what suggestions they accepted, and whether they received offers
- But **free users do not get outcome tracking** (`40-tier-feature-definition.md` line 34: "No outcome tracking")

If agencies refer free users, those users generate zero outcome data. The agency's value proposition ("we'll prove offer acceptance improves") requires those users to be on Pro, which requires the agency to pay or to have the candidate pay.

**Fix required**: Define the agency pilot model clearly:
- Do agencies pay per seat (SGD 10/seat/month)?
- Do candidates get free Pro trials during the pilot?
- How is outcome data captured if candidates use the free tier?

---

### Finding 10: CAC Benchmarks (SGD 40-80) Are Not SG-Specific

**Evidence** (`41-break-even-risks-and-cac-analysis.md` line 98):
- Google Search Ads CAC: SGD 40-80
- No source cited for Singapore market

**The concern**: CAC benchmarks from US/UK markets are not directly applicable to Singapore. Singapore has:
- Smaller population (5.9M) — lower search volume, potentially higher CPC due to competition
- Different job board ecosystem (JobStreet, MyCareersFuture rather than Indeed)
- Higher digital ad costs due to small market

Actual Singapore Google Ads CPC for recruitment/job search keywords may differ significantly. The CAC model should be validated with actual Singapore ad platform data before concluding paid acquisition is unviable.

---

## Summary Table

| Finding | Severity | Issue | Evidence |
|---------|----------|-------|----------|
| 1 | CRITICAL | Pricing discrepancy (SGD 12 vs SGD 19) — all financials invalid | Multiple docs contradict each other |
| 2 | CRITICAL | B2B timing risk — no university revenue until Year 2, agency scaling uncertain | 41-break-even-risks line 62-78 |
| 3 | CRITICAL | First-job unlimited may eliminate upgrade incentive | 40-tier-feature-definition §1.1 |
| 4 | CRITICAL | Interview-stage 10-20× conversion premium unvalidated | 40-tier-feature-definition line 99 |
| 5 | MEDIUM | Annual "no discount" positioning without confirmed advisor partners | 40-tier-feature-definition §7.2 + 41-break-even-risks Risk 2a |
| 6 | MEDIUM | LLM cost ceiling (SGD 5) requires architecture not yet built | 41-break-even-risks line 279 |
| 7 | MEDIUM | Basic tier may have negative unit economics at heavy usage | 40-tier-feature-definition §1.2 |
| 8 | LOW | Post-job outcome logging underestimates implementation effort | 41-break-even-risks §3 |
| 9 | LOW | Agency value prop requires outcome tracking but free users have none | 40-tier-feature-definition line 34 |
| 10 | LOW | CAC benchmarks not SG-specific | 41-break-even-risks line 98 |

---

## Priority Actions Before Launch

1. **Resolve pricing discrepancy**: SGD 12 or SGD 19 — choose one and update ALL documents
2. **Validate 10-20× interview conversion claim** with user research or industry data
3. **Confirm advisor partner relationships** before marketing the annual plan benefit
4. **Model downside scenario**: 0 agency deals in Year 1 — can KeyStone survive 18 months on B2C only?
5. **Build and test two-tier LLM routing+caching** before relying on SGD 2.95/user/month cost model
6. **Model Basic tier unit economics** at different usage levels — confirm it is not margin-negative

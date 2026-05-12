# KeyStone Pricing Analysis

> Generated: 2026-05-10

## Current Pricing Snapshot

### B2C (Job Seeker)

| Tier  | Price        | Status                                           |
| ----- | ------------ | ------------------------------------------------ |
| Guest | Free         | Upload resume + 1 job preview, no account needed |
| Free  | Free         | 3 job analyses/month, email required             |
| Pro   | SGD 12/month | Unlimited analyses, weekly digest                |

### B2B Agency (JD Generator)

| Plan         | Price         | Users | JD Generations |
| ------------ | ------------- | ----- | -------------- |
| Agency Basic | SGD 49/month  | 1     | 50/month       |
| Agency Pro   | SGD 129/month | 1     | Unlimited      |
| Agency Team  | SGD 299/month | 5     | Unlimited      |
| Free Tier    | Free          | —     | 20/month       |

### Education Contracts (Planned)

| Stage   | Price       | Notes                    |
| ------- | ----------- | ------------------------ |
| Pilot   | SGD 0       | 50-200 seats, 1 semester |
| Year 1  | SGD 15-30K  | Full cohort, 1 programme |
| Year 2+ | SGD 50-100K | Full licence             |

---

## Unit Economics Analysis

### Gross Margin by Tier

| Tier         | Revenue/mo | Cost/mo  | Gross Margin    | Margin %    |
| ------------ | ---------- | -------- | --------------- | ----------- |
| Free user    | SGD 0      | SGD 0.80 | **-SGD 0.80**   | Cost center |
| Pro          | SGD 12     | SGD 2.95 | **+SGD 9.05**   | **75%**     |
| Agency Basic | SGD 49     | SGD 1.90 | **+SGD 47.10**  | **96%**     |
| Agency Pro   | SGD 129    | SGD 1.90 | **+SGD 127.10** | **99%**     |
| Agency Team  | SGD 299    | SGD 9.50 | **+SGD 289.50** | **97%**     |

**Key insight:** B2B agency margins are near-100% because the only cost is seat infrastructure. LLM usage for JD generation is negligible vs B2C resume analysis.

### LTV Comparison

| Segment      | Monthly Revenue | Avg Tenure | LTV       | Gross Profit LTV |
| ------------ | --------------- | ---------- | --------- | ---------------- |
| B2C Pro      | SGD 12          | 3 months   | SGD 36    | **SGD 27**       |
| Agency Basic | SGD 49          | 12 months  | SGD 588   | **SGD 565**      |
| Agency Pro   | SGD 129         | 12 months  | SGD 1,548 | **SGD 1,525**    |
| Agency Team  | SGD 299         | 12 months  | SGD 3,588 | **SGD 3,474**    |

**B2B agency LTV is 21-56x higher than B2C.** The business is structurally underpriced for its B2C segment.

---

## Break-Even Analysis

**Break-even requirement:** ~300 Pro users = SGD 43K ARR

| Scenario                | Revenue        | Burn         | Gap            |
| ----------------------- | -------------- | ------------ | -------------- |
| 100 Pro + 0 B2B         | SGD 1,200/mo   | SGD 3,600/mo | -SGD 2,400     |
| 250 Pro + 0 B2B         | SGD 3,000/mo   | SGD 3,600/mo | -SGD 600       |
| 250 Pro + 1 Agency Team | SGD 3,299/mo   | SGD 3,600/mo | -SGD 301       |
| 300 Pro + 1 Agency Team | SGD 3,600/mo + | SGD 3,600/mo | **Break-even** |

**Time to break-even from launch:**

- Month 1-3: 20-50 paying users → burn -SGD 3,000 to -3,600/mo
- Month 4-6: 50-100 paying users → burn -SGD 2,100 to -2,400/mo
- Month 7-12: 100-250 paying users → burn -SGD 600 to -2,100/mo
- **Break-even: Month 14-18** (without B2B contract)

**Runway concern:** At SGD 3,600/month burn with SGD 20K reserves, runway is ~5-6 months. Need SGD 30-40K total to reach break-even.

---

## Agency Pricing Assessment

### Current Pricing vs Market

| Competitor          | Pricing                | Notes                   |
| ------------------- | ---------------------- | ----------------------- |
| Textio (Enterprise) | ~USD 100-200/seat/mo   | JD writing + pipeline   |
| LinkedIn Recruiter  | ~SGD 200-400/seat/mo   | Full recruitment suite  |
| Skillroads          | ~USD 19-49/mo          | Resume builder          |
| Jobalytics          | ~USD 15-29/mo          | Resume keyword analyzer |
| **KeyStone Agency** | **SGD 49-299/seat/mo** | JD generator only       |

**Assessment:** KeyStone Agency pricing is **significantly below market** for a JD-specific tool:

- SGD 49/seat/mo = ~USD 37/seat/mo → below even consumer tools
- SGD 129/seat/mo = ~USD 97/seat/mo → competitive with consumer resume tools, far below enterprise
- Singapore market (20-40% discount vs US) makes SGD 129 comparable to ~USD 60-80 enterprise tools

### Recommendation: Raise Agency Pricing

| Current             | Recommended       | Rationale                                  |
| ------------------- | ----------------- | ------------------------------------------ |
| Agency Basic SGD 49 | **SGD 79/month**  | 1 user, 50 JD, below value delivered       |
| Agency Pro SGD 129  | **SGD 199/month** | 1 user, unlimited — primary revenue driver |
| Agency Team SGD 299 | **SGD 449/month** | 5 users, should feel like a team deal      |

**At recommended pricing, with 5 agency clients:**

- 2 Agency Pro + 3 Agency Basic = 2×199 + 3×79 = **SGD 575/month**
- vs current: 2×129 + 3×49 = **SGD 375/month**
- Delta: **+SGD 200/month** (+53%)

**Even at 50% conversion from current pricing to new pricing, net revenue increases.**

---

## Education Partnership Pricing

### Singapore University Market

| University | Career Centre Size | Typical Contract | Key Decision Maker |
| ---------- | ------------------ | ---------------- | ------------------ |
| NUS        | ~30,000 students   | SGD 50-200K/year | Dean + Procurement |
| NTU        | ~33,000 students   | SGD 50-200K/year | VP + Procurement   |
| SMU        | ~10,000 students   | SGD 30-150K/year | Dean + Procurement |
| SUSS       | ~20,000 students   | SGD 20-100K/year | Provost            |

### Recommended Education Pricing Structure

| Tier                     | Price           | Scope                         | Notes                                                 |
| ------------------------ | --------------- | ----------------------------- | ----------------------------------------------------- |
| **Pilot**                | SGD 0           | 50-200 students, 1 semester   | Structured measurement, co-branding                   |
| **Year 1**               | **SGD 25-40K**  | Full cohort, 1 programme      | Based on 3,000-5,000 students × SGD 8-12/student/year |
| **Year 2+**              | **SGD 60-90K**  | Full licence, all students    | Premium for unlimited, support SLA                    |
| **Enterprise (NUS/NTU)** | **SGD 80-120K** | Full university + white-label | Highest tier                                          |

**Rationale for SGD 25-40K Year 1:**

- Careerist, GradConnection, Handshake all in SGD 20-80K range for Singapore universities
- Our differentiation: AI-powered personalization vs static job boards
- Year 1 should be positioned as "pilot expansion" to avoid procurement process (avoids 3-quote GeBIZ requirement for >SGD 6K)
- Year 2+ contracts can push to SGD 60-90K with pilot outcome data

### WSG Pricing

| Stage                | Price           | Notes                                     |
| -------------------- | --------------- | ----------------------------------------- |
| Initial engagement   | SGD 0 (grant)   | GeBIZ requirement: >SGD 6K needs 3 quotes |
| Formal contract      | SGD 40-80K/year | 12-18 month procurement timeline          |
| **Year 1 realistic** | SGD 0-15K       | Grant-funded pilot                        |

**WSG is Year 2-3 revenue, not Year 1.**

---

## Path to Profitability

### Monthly Revenue Targets

| Month | Target Revenue | Requires                            |
| ----- | -------------- | ----------------------------------- |
| 3     | SGD 1,000      | 80+ Pro users OR 3 Agency Basic     |
| 6     | SGD 2,500      | 150+ Pro users + 3-5 agency clients |
| 12    | SGD 4,800      | 300+ Pro users + 5-8 agency clients |
| 18    | SGD 8,000      | Break-even + SGD 4K buffer          |

### Priority Actions

1. **Close 2-3 agency deals in 60 days** (even at SGD 49/month, 3 deals = SGD 147/month; at SGD 199/month = SGD 597/month)
2. **Raise agency pricing** to SGD 79/199/449 (see above)
3. **Implement annual B2C plan** (SGD 120/year) to lock in LTV at 3-4x monthly churn rate
4. **Target 1 university pilot** in 90 days (free pilot, Year 1 contract by Month 9-12)
5. **Cut burn to SGD 2,000/month** if runway < 4 months without B2B revenue

---

## Summary: Is Current Pricing Reasonable?

| Segment               | Verdict              | Reason                                                                        |
| --------------------- | -------------------- | ----------------------------------------------------------------------------- |
| B2C Pro (SGD 12)      | **Adequate for now** | Below LinkedIn Premium (SGD 40-50), competitive. Raise to SGD 15-18 post-PMF. |
| Agency Basic (SGD 49) | **Underpriced**      | Should be SGD 79-99 for 50 JD/month value                                     |
| Agency Pro (SGD 129)  | **Underpriced**      | Should be SGD 199-249 for unlimited JD                                        |
| Agency Team (SGD 299) | **Underpriced**      | Should be SGD 449-549 for 5 seats                                             |
| Education Year 1      | **Appropriate**      | SGD 15-30K range correct; recommend SGD 25-40K with scope                     |

**The core problem is not pricing — it's speed of B2B sales.** B2C alone cannot reach break-even in 12 months. The business needs 5-8 agency clients by Month 12 to be cash-flow positive.

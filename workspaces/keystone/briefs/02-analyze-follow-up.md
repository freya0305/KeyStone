# KeyStone — Redteam Response & New Analysis Brief

**Date**: 2026-04-29
**Context**: Response to consolidated redteam report (04-validate/00-consolidated-redteam-report.md)

---

## User Decisions on Critical Blockers

### 1. Year 1 Funding
- **Decision**: Personal funds + government grants (SGD 60-90K) is acceptable for startup
- **Focus shift**: Commercial model viability, time-to-profitability, profit margins
- **Research needed**: Profitability timeline, unit economics, path to positive contribution margin

### 2. Outcome Logging Rate (3-5%)
- **Decision**: Accepted as realistic
- **Priority**: Explore how to acquire more real user data via compliant channels
- **Hypothesis to validate**: Recruitment agency partnerships — free体验 in exchange for their users' feedback/outcome data
- **Research needed**: PDPA compliance of such partnerships, alternative compliant data channels
- **Why it matters**: Data sufficiency for building technical moat and value proposition

### 3. Competitive Window — Rejected Concept
- **Decision**: No "competitive window" assumption — we don't want an easily-replicable product
- **Research needed**:
  - Find KeyStone's UNIQUE value proposition
  - Specifically: what can we do that competitors CANNOT replicate
  - Why competitors can't replicate it (structural reasons)
- **Focus**: Deep competitive moat analysis, not feature comparison

### 4. B2C Acquisition Channels
- **Priority**: Practicality + data reliability
- **Research needed**: Give 3-5 concrete B2C acquisition directions with:
  -落地可行性 (practicality)
  -数据可靠性 (data quality/reliability)
  -Expected volume
  -Cost
- **Willing to explore and validate** if needed

### 5. Pricing Research (SGD 19/month)
- **Question**: Is SGD 19/month too high for target users?
- **Research needed**:
  - Simulated target user research on:
    - Willingness to pay
    - Pain points using competitors
    - What they want KeyStone to solve
  - Based on findings: propose optimizations to current plan/pricing

### 6. Break-Even Optimization
- **Why important**: Break-even = profit margin = commercial value
- **Research needed**:
  - Detailed break-even analysis
  - Top 3 most effective improvement points/ideas
  - How to optimize for profitability

### 7. LTV — User Decision Needed
- **User says**: "I don't understand LTV, tell me what decisions I need to make"
- **Research needed**: Explain LTV in plain language, what decisions it drives for KeyStone

### 8. Marketing Language Sanitization
- **Decision**: Remove fraudulent/exaggerated claims
- **Research needed**: Audit all marketing language for overclaiming
- **Replace with**: Factual, verifiable statements
- **Example to fix**: "calibrated on SG hiring manager behaviour" → "outcome tracking infrastructure"

### 9. How We Win vs Teal (Deep Analysis)
- **Teal is the real B2C competitor** (per redteam H-10)
- **Research needed**:
  - What can KeyStone do that Teal cannot?
  - What does Teal do well that we can't replicate?
  - Strategic positioning to win against Teal
  - Why Teal can't easily copy our advantages

### 10. Free Tier Anti-Abuse
- **Decision**: Add phone verification to free tier
- **Research needed**:
  - SMS verification providers (Singapore)
  - Cost estimate (SGD ~0.05/verification mentioned in redteam)
  - Implementation approach
  - Is this Phase 0 requirement?

---

## Key Questions to Answer in Analysis

1. What is our ACTUAL unique moat (not aspirational)?
2. What is the shortest path to 1,000 logged outcomes?
3. How do we reach break-even faster?
4. What is the correct pricing tier that maximizes both data volume AND revenue?
5. What concrete B2C channels can we execute on with SGD 0-5K marketing budget?
6. What structural advantages do we have that Teal cannot replicate in 4-8 weeks?

---

##已知信息 (from previous analysis)

- Core: AI resume optimization for SG job seekers
- Tech moat: outcome-calibrated data (not features)
- Data strategy: suggestion_signals + application_outcomes + employer_fingerprints
- Stage-based outcome tracking (not status enum)
- PDPA compliance: 3-stage NRIC masking, 6-type consent
- B2B-first: lock university pilot before public launch
- Free tier: 3 analyses/month; Pro: SGD 19/month or SGD 180/year
- Target: Monthly Active Activated Users (MAAU)
- Incentive: Pull-based outcome logging (NOT per-app emails)

# Data Scale and Moat Timeline

> Analysis: 38 — Data Scale and Moat Timeline
> Author: analyst
> Date: 2026-04-29
> Status: Complete
> Confidence: Medium-High (quantitative model; user inputs on agency/university volumes are assumptions to validate in Month 1)

---

## Executive Summary

KeyStone's moat is built on outcome-calibrated resume intelligence — the ability to tell universities and agencies not just "here is a suggested resume edit" but "here is a suggested edit that correlates with offers at Company X, based on data from N Singapore job seekers." This moat compounds with every B2C user and every outcome record. The critical threshold for B2B credibility is 2,000+ verified outcome records, reachable by Month 9-12 if distribution channel partnerships launch in Month 2. The moat becomes competitively prohibitive at 10,000+ outcome records with employer cross-reference — this is the 24-30 month target.

---

## 1. Distribution Channel Data Generation

### 1.1 Channel Architecture

**Three data channels, each with different quality/value characteristics**:

| Channel | Volume | Data Quality | Speed to Data |
|---------|--------|--------------|---------------|
| Agency referrals | Medium | High (verified outcomes from placement records) | Fast (referrals apply to jobs; outcomes trackable) |
| University MOU | High | High (verified student outcomes via career centre) | Medium (semester cycles) |
| B2C organic | High | Medium (self-reported outcomes) | Medium (requires consent chain) |
| Design partners | Low | Very High (deep integration, employer visibility) | Fast (if employer consents to share) |

### 1.2 Agency Referral Channel — 6-Month Projection

**Assumption**: 5 agency partners by Month 3, each referring 15-25 candidates/month who use KeyStone.

| Month | Agency Partners | Referrals/Month | KeyStone Signups | Application Records | Outcome Records |
|-------|----------------|-----------------|-----------------|--------------------|--------------------|
| 1-2 | 1-2 (pilot) | 10-20 | 5-15 | 20-60 | 0-5 (early, outcomes pending) |
| 3-4 | 3-4 | 30-60 | 20-45 | 100-200 | 15-40 (3-month lag on outcomes) |
| 5-6 | 5 | 75-125 | 50-90 | 300-500 | 80-160 (outcomes start flowing) |
| **6-month total** | **5** | **~400** | **~200** | **~800** | **~150** |

**Outcome record definition**: A record where (a) user applied to a job, (b) user reports hired/not hired, (c) employer name disclosed (with PDPA consent). 3-month lag reflects typical job search-to-offer cycle.

**Agency referral data value**: Agency referrals come with placement context — the agency knows which employer the candidate applied to, and can (with consent) surface whether the placement was made. This is the highest-quality outcome data because it is employer-verified, not self-reported.

### 1.3 University MOU Channel — 6-Month Projection

**Assumption**: 1 university MOU signed Month 2-3, covering 200-500 students (one programme or graduating class).

| Month | Students Covered | Monthly Active | Application Records | Outcome Records |
|-------|-----------------|----------------|--------------------|--------------------|
| 1-3 (pilot setup) | 0 | 0 | 0 | 0 |
| 4-6 (pilot active) | 200-500 | 80-200 | 200-600 | 0-50 (semester end outcomes) |

**University data note**: University outcome data arrives in bulk at semester end (May/June or November/December). A pilot running from February to April produces outcome data in May-June. A pilot running from August to November produces outcome data in November-December. Plan the pilot timing to align with semester end for maximum data yield.

**6-month university total**: 0-50 outcome records (if pilot starts Month 3). First meaningful university outcome data arrives at Month 9-12.

### 1.4 Design Partners (Employer) — 6-Month Projection

**Assumption**: 1-2 design partner employers (companies that agree to share hiring outcomes with KeyStone in exchange for early access to calibrated candidates).

| Month | Employer Partners | Candidates Referred | Application Records | Outcome Records |
|-------|------------------|--------------------|--------------------|--------------------|
| 1-3 | 0-1 | 0-50 | 0-100 | 0-10 |
| 4-6 | 1-2 | 50-150 | 100-300 | 20-60 |
| **6-month total** | **1-2** | **~150** | **~300** | **~50** |

**Design partner data value**: Employer-partnered data is the highest quality because (a) outcomes are employer-verified, (b) employer-specific acceptance patterns emerge, (c) KeyStone can say "we have hiring data from [Employer] showing X pattern." This is the moat-builder — no competitor can replicate employer-verified outcome data without the same employer relationships.

### 1.5 Combined 6-Month Projection

| Channel | Application Records | Outcome Records |
|---------|--------------------|--------------------|
| Agency referrals | ~800 | ~150 |
| University MOU | ~400 | 0-50 |
| Design partners | ~300 | ~50 |
| B2C organic | ~2,000 | ~200 |
| **Total** | **~3,500** | **~400-450** |

**Month 6 milestone**: ~450 outcome records. This is insufficient for competitive moat but sufficient for internal product validation and early B2B conversations ("here is what we are building").

---

## 2. Moat Building Timeline

### 2.1 The Four Moat Layers

KeyStone's moat builds in four layers, each requiring a different data threshold:

| Layer | Description | Data Required | Strategic Value |
|-------|-------------|---------------|----------------|
| **Layer 1: Coverage** | Enough resume-job pairs to make suggestions statistically meaningful | 500+ application records | Product works; suggestions are grounded in real data |
| **Layer 2: Calibration** | Outcome-correlated scoring (which suggestions correlate with offers) | 2,000+ verified outcomes | B2B credibility; university pilot pitch |
| **Layer 3: Specialisation** | Employer-specific patterns (which resume edits work at Company X vs Y) | 5,000+ outcomes with employer cross-reference | Employer-partner value proposition |
| **Layer 4: Compounding** | Fine-tuning model on SG-specific resume patterns | 10,000+ outcome records | Technically prohibitive for competitors to replicate |

### 2.2 Month-by-Month Milestones

| Month | Outcome Records (Cumulative) | Moat Layer | B2B Implication |
|-------|------------------------------|------------|-----------------|
| 1 | 0-50 | None | Too early for B2B pitch |
| 2 | 50-100 | Layer 1 (coverage) | B2C product validation only |
| 3 | 100-200 | Layer 1 | First agency deal conversations; pilot pitch deck has sample data |
| 4 | 200-350 | Layer 1 → Layer 2 (early) | University pilot running; can show pilot team usage metrics |
| 6 | 400-450 | Layer 2 (early) | University Year 1 pitch deck shows 400+ outcome records |
| 9 | 1,000-1,500 | Layer 2 (calibration) | Sufficient for competitive university tender; B2B pitch uses "2,000+ Singapore job seekers" framing |
| 12 | 2,000-3,000 | Layer 2 (calibration) | Strong enough to win competitive tender; agency pitch uses calibrated outcome data |
| 18 | 4,000-6,000 | Layer 2 → Layer 3 (early) | Employer-specific patterns emerge; design partner conversations strengthen |
| 24 | 7,000-12,000 | Layer 3 (specialisation) | Sufficient for fine-tuning; employer fingerprinting is operationally useful |
| 30 | 12,000-20,000 | Layer 3 → Layer 4 (early) | Fine-tuning becomes viable; employer-specific scoring is a real moat |

### 2.3 When Fine-Tuning Becomes Viable

**Fine-tuning threshold**: 10,000+ verified outcome records with consistent schema (resume text, job target, employer, outcome).

**Why this matters for B2B**: A fine-tuned model trained on Singapore-specific resume patterns (local employer expectations, phrasing norms, industry-specific keywords) outperforms a general-purpose LLM for resume analysis tasks. This is the technical moat that makes KeyStone's suggestions meaningfully better than what a general AI assistant produces.

**Interim strategy (before fine-tuning viable)**: Prompt engineering with SG-specific few-shot examples + retrieval-augmented generation (RAG) against the outcome database. This achieves 80% of fine-tuning's value with 10% of the data requirement.

### 2.4 When Employer Fingerprints Emerge

**Employer fingerprint definition**: A statistically significant pattern of which resume characteristics correlate with offers at a specific employer. For example: "Candidates who emphasise 'stakeholder management' in resumes are 34% more likely to receive offers from [Bank A], but the opposite is true at [Tech Company B]."

**Threshold for employer fingerprinting**:
- Minimum: 100+ outcome records from a single employer
- Reliable: 300+ outcome records from a single employer
- Comprehensive (full employer profile): 500+ outcome records from a single employer

**At 6 months**: 0 employer has 100+ records. Employer fingerprints do not exist yet.
**At 12 months**: 1-3 employers may have 50-100 records. Early patterns, not yet reliable.
**At 18 months**: 5-10 employers may have 100+ records. Fingerprints are operationally useful.
**At 24 months**: 15-25 employers may have 100+ records. Employer-specific recommendations are a real differentiator.

**The employer fingerprint flywheel**:
```
More B2C users → more applications to employer X
    → more outcome records from employer X (when users report results)
    → employer X fingerprint emerges
    → KeyStone tells employer X "your candidates who used KeyStone had Y% higher offer rate"
    → employer X refers candidates through KeyStone
    → more users applying to employer X
    → more outcome records from employer X
```

---

## 3. Speed to Profitability

### 3.1 Can Distribution Channel Data Support Profitability?

**Yes, but on a 12-18 month horizon, not 6 months.**

The distribution channel data (agency referrals + university MOU + design partners) generates outcome records at a rate that supports a compelling B2B pitch by Month 9-12. The B2B revenue that results from that pitch arrives 3-6 months after the pitch (agency: 2-4 weeks; university: 6-12 months). So the full cycle from "start data collection" to "B2B revenue from data-driven pitch" is 12-18 months.

**Month-by-month financial projection including data-to-revenue lag**:

| Month | Outcome Records | B2B Pipeline Stage | B2B Revenue | Cumulative B2B Revenue |
|-------|----------------|--------------------| ------------|------------------------|
| 1-3 | 0-200 | Agency outreach + pilot setup | SGD 0 | SGD 0 |
| 4-6 | 200-450 | 1-2 agency deals signed | SGD 5-15K | SGD 5-15K |
| 7-9 | 450-900 | University pilot running; agency expansion | SGD 10-20K | SGD 15-35K |
| 10-12 | 900-2,000 | University Year 1 contract closes (SGD 15-30K) | SGD 25-40K | SGD 40-75K |
| 13-18 | 2,000-4,000 | 2-3 agency deals + 1 university Year 1 + 1 Year 2 upgrade pipeline | SGD 50-80K | SGD 90-155K |
| 19-24 | 4,000-8,000 | 5-8 agency deals + 2 university contracts + WSG pilot | SGD 100-160K | SGD 190-315K |

**Profitability (B2B + B2C combined, lean ops)**: Month 18-24.

### 3.2 How Data Quality Translates to B2B Sales Velocity

**The relationship is non-linear**:

| Outcome Record Count | B2B Sales Effect | Close Rate Multiplier |
|---------------------|------------------|----------------------|
| 0-200 | "We are building something" | 0.5x (unqualified prospect) |
| 200-500 | "Here is a pilot with sample data" | 1.0x (credible concept) |
| 500-1,000 | "Our pilot showed X% improvement" | 1.5x (evidence-based pitch) |
| 2,000-3,000 | "We have statistically significant data from Singapore job seekers" | 2.0-2.5x (data-driven case study) |
| 5,000+ | "We have employer-specific calibrated scoring" | 3.0x+ (competitive moat) |

**Mechanism**: Each doubling of outcome records shifts the B2B conversation from "would this work?" to "prove it works" to "this clearly works." The close rate improvement compounds because (a) objections are answered with data, (b) case studies become employer-specific, (c) reference accounts become more credible.

### 3.3 When Does Data Make the B2B Pitch "Undeniable"?

**The "undeniable" threshold** is when the B2B prospect cannot make a decision without KeyStone's data. This happens at Layer 3 (employer-specific specialisation):

- University career centre cannot justify NOT using KeyStone if their own outcome data shows KeyStone-prepared students have higher offer rates
- Recruitment agency cannot differentiate on candidate quality if KeyStone has employer-validated outcome patterns their recruiters do not have access to
- Employer cannot evaluate resume quality at scale without the calibrated scoring that KeyStone's outcome database enables

**Timeline to "undeniable"**: Month 24-30, when:
- 10,000+ outcome records exist
- 10+ employers have 200+ records each (employer-specific patterns are statistically significant)
- 3+ university career centres have 2+ years of tracked outcome data

**The practical implication**: "Undeniable" is a 24-30 month target. In Year 1, the pitch is "we are building the data that will make this undeniable." In Year 2, the pitch is "here is statistically significant evidence." In Year 3, the pitch is "you cannot make a data-driven hiring decision without us."

---

## 4. The Data-to-B2B Flywheel

### 4.1 The Virtuous Cycle (Quantified)

```
More B2C Users
        │
        ▼ (every 1,000 new B2C users)
+1,500 application records/year
+150 new outcome records/year
        │
        ▼
Better Calibration
        │
        ▼ (every 2,000 cumulative outcomes)
+0.5x B2B close rate
= Faster B2B sales cycle
        │
        ▼ (every B2B close)
+1 employer or university relationship
= More structured data access
        │
        ▼ (every new employer relationship)
+200-500 employer-verified outcome records/year
= Higher quality outcome data
        │
        ▼ (back to top)
More B2C Users
```

**The compounding effect**: Each cycle of the flywheel produces higher-quality data (employer-verified vs self-reported) and faster B2B sales velocity. The flywheel accelerates, not just grows.

### 4.2 Flywheel Velocity Metrics

Track these monthly to measure flywheel health:

| Metric | Month 3 Target | Month 6 Target | Month 12 Target |
|--------|----------------|----------------|-----------------|
| Outcome records (cumulative) | 200 | 450 | 2,000 |
| Outcome records (employer-verified) | 20 | 100 | 500 |
| B2B close rate (vs industry baseline) | 1.0x | 1.3x | 2.0x |
| B2B sales cycle (agency) | 4 weeks | 3 weeks | 2 weeks |
| University pilot conversion rate | N/A | 30% | 60% |
| Employer design partner count | 0 | 1 | 3 |

### 4.3 The Data Moat Is Self-Reinforcing

**Why competitors cannot replicate this quickly**:

1. **Time**: 12-18 months minimum to accumulate sufficient outcome records for Layer 2 calibration. A competitor starting today would reach KeyStone's Month 12 position in Month 24.

2. **Consent chain**: PDPA-compliant outcome tracking with explicit user consent for employer follow-up is a legal infrastructure that takes months to design and implement correctly. KeyStone has this from Day 1.

3. **Employer relationships**: The flywheel requires employers to share hiring data. This requires trust and integration work. Every month KeyStone delays a competitor, it deepens employer relationships that are difficult to displace.

4. **University MOU lock-in**: Once KeyStone is embedded in a university's career workflow (with outcome tracking), switching costs are high. The university has calibrated its processes to KeyStone's data format.

5. **Fine-tuning corpus**: When KeyStone reaches 10,000+ outcome records, training a fine-tuned model requires (a) the data, (b) the ML infrastructure, (c) the validation pipeline. Competitors need all three simultaneously.

---

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| B2C users don't consent to outcome tracking | Medium | Outcome record count falls below threshold | Design consent flow with clear value proposition ("help us help you get hired"); make opting out the exception, not the norm |
| Agency referral volume lower than projected | Medium | 6-month outcome record target misses by 30-50% | Diversify to 2-3 additional agencies in Month 3-4; supplement with organic B2C |
| University outcome data arrives at semester end (bulk, not continuous) | High | Pitch meetings happen before outcome data is available | Plan pilot timing to align with semester start; use leading indicators (application volume, suggestion engagement) as proxies |
| Employer design partners don't share verified outcomes | Medium | Outcome quality stays at self-reported level | Negotiate data sharing agreement with employer before design partner designation; structure as mutual benefit |
| Competitor launches before KeyStone accumulates 2,000 outcomes | Low (Year 1) | Price pressure on B2B in Year 2 | Accelerate B2C growth through university pilot spillover; first-mover employer relationships are the primary moat |

---

## Success Criteria

- [ ] Month 6: 400+ outcome records (cumulative) — validates data infrastructure
- [ ] Month 9: 1,000+ outcome records — sufficient for credible B2B university pitch
- [ ] Month 12: 2,000+ outcome records with employer cross-reference on 20%+ — Layer 2 calibration achieved
- [ ] Month 12: First employer design partner with 100+ verified outcome records
- [ ] Month 18: 5,000+ outcome records; employer-specific patterns emerge for 3-5 employers
- [ ] Month 24: 10,000+ outcome records; fine-tuning feasibility confirmed
- [ ] Flywheel metrics trending up each quarter (close rate, sales cycle, referral volume)

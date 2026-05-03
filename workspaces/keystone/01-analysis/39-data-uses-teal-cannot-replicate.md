# Analysis 39 — What KeyStone Data Enables That Teal Structurally Cannot Do

> Phase 01 Analysis — 2026-04-29
> Triggered by: User's Point 3 (what to DO with data Teal cannot provide) and Point 8 (real differentiation beyond features)
> Reference: 01-analysis/14-data-moat-technical-defensibility.md

---

## The Core Answer

The moat is not "we have SG data."

The moat is: **"We can tell you WHICH suggestions actually WORK for SG employers, calibrated on real outcomes."**

Teal can add features in weeks. They can copy resume version management, JD parsing, and suggestion generation in a single sprint. What they cannot copy is the training signal — thousands of SG applications linked to specific suggestions and real hiring outcomes. That data does not exist anywhere except in KeyStone's systems. It cannot be bought, scraped, or synthesised.

This document describes what that data MAKES POSSIBLE — the specific, concrete capabilities that become achievable once KeyStone has sufficient SG outcome corpus.

---

## The Fundamental Structural Difference

| What Teal Has | What Teal Cannot Build (Without 18+ Months of SG Data) |
|---------------|------------------------------------------------------|
| Generic outcome tracking | SG employer-specific response pattern fingerprints |
| URL save for any JD | Outcome-calibrated suggestion quality by employer |
| Resume version management | Segment-level calibration on real SG user outcomes |
| Any country's users | SG institutional cohort analytics (university contracts) |
| Any market's feedback | DBS/GovTech/EY specific callback lift metrics |

Teal's architecture optimises for engagement and retention in any market. It has no structural reason to collect outcome-linked suggestion data, and no SG user base to collect it from even if it tried.

---

## Specific Capabilities That Require SG Outcome Data

### A. Outcome-Calibrated Suggestion Ranking

**NOT:** "We suggest you quantify your achievements."

**BUT:** "We suggest you quantify your achievements — because SG applications that mention quantified team leadership outcomes receive 23% higher callback rates at GLCs."

The difference is the difference between an opinion and a measurement. Every suggestion KeyStone makes can eventually carry a calibrated confidence interval derived from real SG outcome data.

**What this requires:**
- Thousands of SG applications
- Each application linked to the specific suggestions accepted/rejected
- Outcome logged (no response / callback / interview / offer)
- Sufficient volume per suggestion type to calculate statistical significance

**Teal structurally cannot do this:**
- Teal has no SG users → no SG suggestion-outcome pairs
- Even if Teal added outcome logging tomorrow, they would need 12-18 months to accumulate enough SG data to calibrate
- By then, KeyStone's calibration is 12-18 months more mature

---

### B. Employer-Specific Response Pattern Fingerprints

**NOT:** "DBS prefers candidates with leadership experience."

**BUT:** "DBS Digital Banking: applications that mention 'team leadership + specific metrics' receive 31% higher callback rates. Applications that use 'responsible for' phrasing receive 18% lower callback rates. Sample size: 847 applications, 312 outcomes."

This is employer intelligence that no resume tool can produce without owning the outcome data for that employer. Career advisors at universities currently have no data on this at all — they rely on anecdotal advice from seniors and LinkedIn posts.

**What this requires:**
- 500+ applications with outcomes per employer
- Suggestions tagged with the employer identity (not just "GLC" — actual employer name)
- Outcome logging linked to specific suggestion sets

**Teal structurally cannot do this:**
- Teal does not tag JDs by specific employer — only by company_type
- Teal has no SG employer relationships to anchor outcome data to
- Even with 500 SG applications, Teal would need the suggestion-outcome linkage AND employer tagging AND outcome logging — none of which are in their architecture

**First employer fingerprint achievable:** Month 18-24 for top SG employers (DBS, GovTech, Accenture, EY, McKinsey, MAS) given a university pilot with 500 students × 40-80 applications each.

---

### C. Segment-Specific Calibration

**NOT:** "Mid-career switchers should use functional resume formats."

**BUT:** "Finance-to-Tech switchers in Singapore: applications that use 'transferable skills framing' combined with certification highlights receive 2.1x higher callback rates than tech-native applicants using the same approach. This pattern holds for banking-to-fintech transitions but NOT for engineering-to-tech."

Segment-level calibration requires outcome data labelled by user segment AND employer type AND suggestion type — a three-dimensional matrix that only becomes statistically significant with thousands of outcome logs.

**What this requires:**
- User segments: fresh_grad / mid_career_switcher / returnee / senior_executive
- Outcome logs tagged with segment identity
- Cross-segment outcome comparison within the same employer/role type

**Teal has:**
- Segment labels (they track user types)
- Outcome tracking (if they added it)
- No SG outcome data to validate segment-specific patterns against

---

### D. Institutional Cohort Analytics (The Killer App for B2B)

**The pitch to a university career director:**

> "After one semester, we can show you: students who used KeyStone's DBS-specific suggestions for their GLC applications had a 23% first-round interview rate. Students who did not use KeyStone had 8%. We can show you this because every KeyStone user consented to aggregate outcome tracking as part of their university onboarding."

This is a provable, B2B-saleable, institutional-grade analytics claim. It is not a product feature — it is a verified outcome statement backed by cohort data.

**What this requires:**
- University MOU with explicit outcome tracking consent
- Institutional cohort identification (users linked to university, not just anonymous)
- Aggregate outcome reporting by institution and employer type
- Sufficient volume per institution (minimum 200+ users per cohort for statistical significance)

**Teal structurally cannot do this:**
- Teal has no university relationships → no institutional cohorts
- Teal's generic user base cannot be disaggregated by institution
- Teal cannot show "KeyStone users at [University] had 2.3x higher callback rate for GLC applications" because they cannot identify which users are from that university
- This requires explicit data partnerships that take 12-24 months to negotiate

**B2B sale cycle:** University career centre sees a dashboard showing their specific student outcomes. They renew or expand based on measurable student success. This is a fundamentally different sales motion than "buy resumes tool for your students."

---

## The Narrative for B2B Buyers

The differentiation statement for a university career director who already has VMock or Teal:

> "VMock tells students what to fix on their resume. Teal tracks which jobs students applied to. KeyStone tracks which CHANGES actually GOT STUDENTS INTERVIEWS at DBS, GovTech, and Accenture — because we follow the outcome all the way to the offer. After one semester, we can show you: students who used KeyStone's DBS-specific suggestions had a 31% higher first-round interview rate. Can your current tool give you that number?"

Teal cannot say this. KeyStone can, after 12-18 months of data collection.

---

## The Honest Timeline

| Milestone | Timeline | What KeyStone Can Show |
|-----------|----------|------------------------|
| Month 0 | Launch | Nothing yet — data is being collected |
| Month 6 | Directional trends | Small-sample suggestion preference patterns |
| Month 12 | Statistically meaningful | Callback rate differences by suggestion type (if 1,000+ outcomes) |
| Month 18 | Employer-specific claims | DBS/GovTech callback lift metrics (if 500+ per employer) |
| Month 24+ | Institutional cohort | University-specific outcome dashboards for B2B renewal conversations |

**The honest position at launch:** "We are building the first outcome-calibrated resume guidance system for Singapore. Our suggestions are informed by SG-specific intelligence. In 18 months, we will be able to show you which suggestions actually work — because we are measuring the outcomes."

---

## What This Means for Product Architecture

The capabilities above require specific architectural decisions from Day 1. These cannot be retrofitted:

1. **Every suggestion must be individually identifiable** — suggestion_id logged with every accept/reject/modify action
2. **Outcome logs must reference the specific suggestion set used** — not just "user applied to DBS" but "user applied to DBS using suggestion set #847"
3. **Employer identity must be captured at JD analysis time** — not "GLC" but "DBS Digital Banking"
4. **PDPA consent for aggregate outcome reporting** — explicit at signup, covering institutional cohort analytics
5. **Segment labels on all users** — fresh_grad / mid_career / etc., captured at onboarding

If any of these are missing at launch, the first 6-12 months of user data cannot be used for the moat-building purposes described in this document.

---

## Summary: The Structural Moat

| Data Type | What It Enables | Teal's Structural Barrier |
|-----------|----------------|---------------------------|
| Suggestion signals (accept/reject/modify) | Fine-tuned suggestion model on SG preferences | No SG users = no signal volume |
| Outcome logs (callback/no-callback/offer) | Calibrated suggestion quality by employer | No SG outcome data to calibrate against |
| Employer-tagged applications | Employer-specific response fingerprints | No employer identity in their JD parsing |
| Institutional cohort data | B2B dashboard for university career centres | No university relationships or cohort identifiers |
| Segment-labeled outcomes | Segment-specific calibration | Has segments but no SG outcomes to validate |

**The moat is not the AI model.** The model is copyable. The moat is not the features. Features are copyable in weeks.

**The moat is the measurement infrastructure.** The accumulated, validated, SG-specific outcome data that tells you which suggestions actually work — calibrated on real hiring decisions, linked to specific employers, broken down by user segment and institution.

Teal cannot build this without starting over. KeyStone started over on Day 1.

---

## References

- `01-analysis/14-data-moat-technical-defensibility.md` — foundational data moat architecture, signal types, accumulation rates
- `01-analysis/38-competitor-teal-analysis.md` — Teal's capabilities and structural limitations

---
type: DISCOVERY
date: 2026-04-29
created_at: 2026-04-29T13:00:00Z
author: agent
session_id: 874f263b-1879-49b0-9e64-1f293538aedb
project: keystone
topic: CORRECTION of 0012 — historical agency data sharing is PDPA-blocked; correct model is distribution channel, not data supplier
phase: analyze
tags: [agency-partnership, pdpa, data-moat, distribution, correction]
---

## Correction to Journal Entry 0012

Entry 0012 proposed: "5 boutique SG agencies × 150 placements/year × 2 years history = ~1,500 real SG resume-JD-outcome pairs before launch."

**This is not executable.** Under Singapore PDPA (2012, amended 2021), historical candidate data collected for recruitment purposes cannot be re-used for AI model training without per-candidate consent. Anonymization to PDPC standards is technically possible but loses most of the contextual value. The "historical batch data" model is a legal risk that is not worth pursuing.

## Correct Partnership Model

The agency is a **distribution channel**, not a data supplier.

**What changes**: Agencies don't share data. They refer candidates to KeyStone as a B2C tool. Candidates register individually, give B2C training consent, and generate real in-context usage data.

**Why this is actually better**: Forward-looking in-context data (candidate actively applying to real jobs right now) has higher signal quality than retrospective historical data (candidate already placed, data is static).

**Revised data volume estimate**:
- 5 agencies × 15-20 candidate referrals/month × 6 months = 450-600 real B2C users (vs. claimed 1,500 static pairs)
- 450-600 users × 10 applications × 3-6% logging rate = 135-360 logged outcomes
- Smaller than the 0012 estimate, but legally clean and higher signal quality

## The Persuasion Argument (Corrected)

Lead with operational pain, not data:
> "Your consultants spend X hours per week editing candidate resumes. KeyStone removes that work. Your consultants do BD instead."

Do NOT lead with data exchange. The value proposition is: better-prepared candidates → faster placements → fee arrives sooner.

Commercial structure: 12-month free seats + agency recommends KeyStone to candidates. One page, two-week exit clause, no data sharing clause.

## For Discussion

1. If the agency's primary value to KeyStone is distribution (not data), does the "free seats" incentive create enough motivation for agencies to actively recommend KeyStone? Or do they need an additional incentive (e.g., commission on Pro subscriptions from referred candidates)?
2. The distribution channel model depends on recruiter consultants actually remembering and recommending KeyStone to candidates in their workflow. What is the UX or workflow integration that makes this recommendation habitual rather than one-time?
3. If KeyStone can eventually provide agencies with a dashboard showing "candidates you referred: average callback rate improvement X%", does that create a stronger ongoing incentive than free seats alone?

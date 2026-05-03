---
type: DISCOVERY
date: 2026-04-29
created_at: 2026-04-29T11:05:00Z
author: co-authored
session_id: 874f263b-1879-49b0-9e64-1f293538aedb
project: keystone
topic: Outcome-calibrated suggestion signals are the only durable technical moat — all other advantages are replicable within weeks
phase: analyze
tags: [technical-moat, data, learning-loop, fine-tuning, vmock, competitive]
---

## Discovery

With VMock already in SG universities (corrected in 0009), the competitive question shifts from "how do we get here first" to "how do we build something VMock cannot replicate by catching up."

The only category of advantage that meets this bar is **outcome-calibrated data** — specifically:

1. **Suggestion signals**: per-action accept/reject/modify from SG users, tagged with company_type, role_level, industry, and user segment. This is human preference data for SG job applications; it is the raw material for fine-tuning a suggestion model on SG-specific preferences.

2. **Application outcome data**: when users log callback/no-response/interview outcomes, each outcome links back to the exact suggestions used on that application. This produces a calibration dataset that turns "we think this suggestion is good" into "we measured this suggestion improves callback rates at DBS by 15%."

3. **SG employer fingerprints**: after 500+ applications to the same employer, employer-specific response patterns emerge — what resume signals actually trigger callbacks at each major SG employer. No competitor has this without SG users logging SG outcomes.

**VMock's structural gap**: VMock scores against an ATS model, not against SG hiring manager behaviour. They cannot answer "did students who improved their VMock score get better callbacks?" because their architecture doesn't collect outcomes. This gap cannot be closed by writing code — VMock needs SG outcome data first.

## Why This Is Non-Replicable

The data accumulates only while the product is in use. There is no shortcut:
- Cannot be bought (no one is selling SG job seeker outcome datasets)
- Cannot be synthesised (synthetic data has the wrong calibration signal)
- Cannot be scraped (outcomes are private)
- Cannot be approximated from US/UK data (SG hiring norms are different)

A competitor who arrives in SG 24 months from now does not enter a level playing field. They enter a market where KeyStone has 24 months of accumulated SG signal and outcome data that cannot be replicated in any shorter timeframe.

## The Critical Prerequisite

The data moat only accumulates if the right architecture is in place from Day 1:

1. `suggestion_signals` table built at MVP launch — every accept/reject/modify logged with full context
2. Application outcome logging in the UX from launch — not added later
3. PDPA consent for signal aggregation explicit at signup
4. Employer-level tagging on every JD (not just company_type — actual employer name)
5. Outcome-suggestion linkage — each outcome references the specific suggestion set used

**These cannot be retrofitted.** The first 6-12 months of user data is lost for moat-building purposes if any of these are missing at launch.

## The Timeline Is Honest

The data moat does not exist at launch. It is being built from Day 1. Realistic milestones:

- 2,000 signals → first segment-specific preference patterns (Month 3-4)
- 10,000 signals → fine-tunable corpus (Month 6-8)
- 1,000 logged outcomes → outcome-calibrated scoring (Month 12-18)
- 500 outcomes per employer → employer fingerprint (Month 18-24)

At Month 0, KeyStone has a strong product but no data moat. At Month 18 with 1,000+ active users logging outcomes, KeyStone has something structurally irreproducible.

## For Discussion

1. The data moat only materialises if users log application outcomes voluntarily. What UX mechanics maximise outcome logging rates? (Prompt at resume download vs. reminder email at Day 7 vs. in-app notification when a common callback window passes.) What logging rate is needed and what design choices achieve it?
2. At 1,000 logged outcomes, the dataset is large enough to detect callback lift but possibly too small to be statistically convincing to a sceptical B2B buyer. What is the minimum dataset size to make the claim "students who used KeyStone got 23% higher callback rates" defensible in a university procurement conversation — and can it be reached within a single academic semester?
3. VMock's SG presence makes the data race more urgent: if VMock adds outcome tracking to its SG university deployments (a rational response to learning about KeyStone's architecture), the head start shrinks. How quickly could VMock add this feature to its existing SG deployments, and does KeyStone have enough time to establish an irreversible data lead?

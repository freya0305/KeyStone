---
type: DECISION
date: 2026-04-29
created_at: 2026-04-29T14:20:00Z
author: co-authored
session_id: 874f263b-1879-49b0-9e64-1f293538aedb
project: keystone
topic: Explicit MVP v1.0 scope — 4 features + 2 architectural requirements; interview prep excluded from MVP
phase: analyze
tags: [mvp, scope, product-decisions]
---

## Decision

KeyStone v1.0 ships with exactly 4 features and 2 non-negotiable architectural requirements:

**4 features**:
1. Resume Upload + SG Analysis (NRIC, NS, PMET intelligence)
2. JD Input + Four-Level Match Assessment
3. Line-by-Line Revision Suggestions (the core product)
4. Application Outcome Tracking + Email Reminders (stage-aware)

**2 architectural requirements** (not features — infrastructure):
1. Suggestion signal logging (`suggestion_signals` table, every Accept/Reject/Modify)
2. B2C training consent separation (separate checkbox, gates training pipeline)

**Excluded from MVP**: Interview Preparation Module (moves to Phase 2 with bundled Pro from Day 1 positioning but no implementation work until Phase 2).

## Why Interview Prep Moves to Phase 2

This overrides an earlier discussion about bundling interview prep in Pro from Day 1. The confusion:
- **Marketing/pricing**: interview prep IS positioned as a Pro value from Day 1 (it's in the pitch) ✅
- **Implementation**: the actual module is NOT implemented in v1.0 ✅
- **Stated in Pro features**: "Coming soon — Interview Preparation" is acceptable as a pro-tier promise

This is not deception — it's standard SaaS pre-launch positioning. The module must be delivered within 60 days of MVP launch or the promise erodes.

## First Use is Gate-Free

No signup required for first JD analysis. Registration is prompted after the user has seen value (accepted their first suggestion or wants to export the modified resume). This is a hard constraint on the MVP UX — removing it would kill the free-tier acquisition funnel.

## Design Partner Gate

MVP launch is conditional on: ≥50 design partners completing the full workflow with outcome logging consent. This ensures the product launches with non-zero training data rather than pure cold start.

## For Discussion

1. The "no signup for first use" rule conflicts with signal logging (we can't attribute a signal to an anonymous user). How should pre-registration suggestion signals be handled — logged anonymously with a session token, discarded, or associated after registration?
2. "Interview prep coming soon" as a Pro-tier promise has a 60-day delivery window. What is the acceptable minimum Phase 2 interview prep feature that fulfills the promise without being a disappointment? (The full 4-step module from Analysis 11, or a simpler question bank?)
3. Weekly digest email is listed as Phase 2, but it reuses the same email infrastructure as the Day 3/10/21 reminders. Should it be pulled into MVP given the low marginal development cost?

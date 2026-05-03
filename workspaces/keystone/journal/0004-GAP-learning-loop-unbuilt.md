# GAP: Learning Loop Is Unbuilt and Is the Actual Moat

**Type**: GAP
**Phase**: 01-analyze
**Date**: 2026-04-29

## Gap Identified

The brief describes the "Singapore intelligence engine" as a static knowledge base (NS framing rules, GLC/MNC conventions, NRIC removal guidance). This is replicable in 60-90 days by any competitor who reads the same resources and writes the same system prompts.

The actual moat — which the brief does not architect — is a **learning loop**: every time a user accepts or rejects a suggestion, the engine learns which suggestion patterns are preferred in which contexts. After 50,000 accept/reject signals across varied SG roles and company types, the model's SG-specific judgment is trained on real user behavior that no competitor has.

## Specific Learning Signals Available

1. **Accept/reject per suggestion** → which phrasings SG job seekers prefer for which role types
2. **Modify signals** (user rewrites a suggestion) → what the user meant vs what the engine suggested
3. **Company-type corrections** ("you flagged this as MNC but it's GLC") → refines company taxonomy
4. **Outcome correlation** (suggestion pattern X → callback logged) → which suggestions actually improve callback rates
5. **NS-framing acceptance rate by industry** → finance vs tech vs government roles have different NS framing norms

## Why This Matters

- Static SG intelligence: competitor replicates in 60-90 days
- Learning-loop-trained SG intelligence at 50K signals: competitor needs 18 months of users to replicate

## Required Product Decision

The learning loop requires an explicit architecture decision before coding begins:
1. Accept/reject UI must log signals to a training database (not just a UX interaction)
2. Data model must include signal-type, context (company type, role level, industry), and outcome correlation fields
3. Privacy/PDPA consent must cover "your suggestions feedback improves the engine for all users" — requires explicit consent at signup

This is a **pre-launch architectural decision**, not a future feature. The data structure needs to be right from Day 1; retrofitting signal capture after launch is a migration project.

## Blocking Status

This gap does not block launch, but every week without logging signals is a week of moat-building capacity wasted. **Prioritize in MVP architecture design, even if the ML training loop is Phase 2.**

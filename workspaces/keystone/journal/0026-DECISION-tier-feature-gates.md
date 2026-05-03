---
name: 0028-DECISION-tier-feature-gates
description: Tier feature gates finalized with upgrade trigger mechanics
type: DECISION
date: 2026-04-30
author: co-authored
topic: Tier Feature Gates
phase: analyze
tags: [pricing, tiers, b2c, upgrade-flow]
---

# Journal 0028 — DECISION: Tier Feature Gates Finalized

**Date**: 2026-04-30
**Type**: DECISION
**Author**: co-authored
**Phase**: analyze

---

## Decision: Pricing Tiers

| Tier | Price | Analyses | Suggestions | Tracking | Export |
|------|-------|----------|-------------|---------|-------|
| Free | 0 | First job: unlimited; post-reg: 3/mo | Full list | Manual | No |
| Basic | SGD 9/mo | 5/mo | First 3 visible | Manual | No |
| Pro | SGD 12/mo | Unlimited | Full list | Stage-based + auto | PDF + DOCX |
| Annual | SGD 144/yr | Unlimited | Full list | Stage-based + auto | PDF + DOCX + advisor session |

**Critical upgrade trigger**: User runs out of analyses on the job they really want → emotional moment → upgrade.

**Annual differentiation**: Not a discount. A "commitment package" with 1× advisor session included.

---

## Alternatives Considered

1. **SGD 19 Pro pricing** — Rejected. Misaligned with primary B2C acquisition channel (fresh grads). Too expensive for the entry-level segment.

2. **Free tier with full suggestions** — Rejected. Inverted value proposition where paying gave users fewer visible suggestions.

3. **Analysis-count-based upgrade trigger** — Deferred. Later refined to "interview stage" trigger per DISCOVERY 0040.

---

## Rationale

The tier structure creates a clear value ladder:
- Free tier enables low-friction onboarding with unlimited first-job experience
- Basic tier at SGD 9 targets price-sensitive fresh grads
- Pro tier at SGD 12 targets mid-career switchers who value unlimited tailoring
- Annual tier at SGD 144 positions as ecosystem pass, not discount

The upgrade trigger ("run out of analyses on a job you really want") creates an emotional moment tied to real job-seeking frustration, not a quota limitation.

---

## Consequences

- Free tier remains ad-supported but high-quality entry point
- Basic tier generates modest ARR from price-sensitive segment
- Pro tier is primary revenue driver via annual conversion
- Cross-reference fix required: specs/mvp-scope.md needed pricing correction (SGD 19→SGD 12, SGD 190→SGD 144)

---

## For Discussion

1. Should the "first job unlimited" in Free tier be time-limited (e.g., first 30 days)?
2. Is the 3-suggestion preview in Basic tier too restrictive, or does it create healthy upgrade motivation?
3. How do we communicate the Annual Plan as "ecosystem pass" without making it feel like a discount?

---
type: DISCOVERY
date: 2026-04-29
created_at: 2026-04-29T14:00:00Z
author: co-authored
session_id: 874f263b-1879-49b0-9e64-1f293538aedb
project: keystone
topic: Multi-round interview tracking multiplies data value and LTV; simple status enum is insufficient
phase: analyze
tags: [data-model, interview-tracking, ltv, product-spec]
---

## Discovery

SG professional roles typically require 2–4 interview rounds. The original product spec modelled "Interview scheduled" as a single terminal status. This is structurally wrong for three reasons:

1. **Data loss**: "Interview scheduled" conflates Round 1 with Round 4, destroying per-stage pass rate data — the most valuable outcome signal KeyStone can accumulate.

2. **LTV underestimate**: The interview prep module was designed to trigger once (at first response). With multi-round triggering, LTV extension is 75–90% (vs the original 50–67% estimate). PMET users averaging 2.8 rounds generate ~1.6 months additional subscription vs 1 month in the old model.

3. **Missed engagement opportunity**: Each stage transition is a natural re-engagement event. A user who received Round 2 confirmation has high motivation to prepare — this is the highest-intent moment in the product.

## Correct Model

Each application record contains a `stages` array, not a status string:

```
stages: [{stage_type, round_number, date, format, outcome}]
```

Stage types: response | screening | interview | final | offer | rejection | withdrawal

This enables per-stage pass rate analytics ("you get to R1 at market average rate but your R1→R2 pass rate is below benchmark") — a unique insight no competitor in SG provides today.

## Architectural Implication

This data model must be built from Day 1. Adding multi-round tracking after launch requires a migration of all existing application records. The incremental cost of building it right initially is low; the migration cost is high.

## For Discussion

1. The stage tracking adds user friction (more fields to fill in). What's the minimum information required to make per-stage pass rates meaningful — is round_number sufficient, or is `format` (panel vs technical) also needed for segmentation?
2. At what stage count does "per-stage pass rate" become statistically meaningful for benchmark comparisons? If we need 30+ data points per stage, which stages should get priority tracking in the early data accumulation phase?
3. The interview prep module triggers at each stage transition, but users may not return to KeyStone until days after the transition. How does the trigger timing interact with the email reminder cadence?

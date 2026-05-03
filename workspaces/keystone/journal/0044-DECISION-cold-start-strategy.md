# Journal Entry

## DECISION: Cold Start Strategy — Build First, Gather Data Concurrently

**Slug**: cold-start-strategy-build-first
**Type**: DECISION
**Date**: 2026-04-30

## Decision

Cold start strategy: build MVP first, then gather data during and after launch. Expert seed data is a TODO for pre-launch phase, not a blocker.

## Rationale

- Product priority over perfect data preparation
- Can't validate user need without a working product
- Data requirements documented; will accumulate while product runs
- Launch first (Week 8-10) with raw LLM, no RAG
- RAG activated once real user data accumulates (Month 3-6)

## Updated Cold Start Plan

```
Day 1:    Build MVP
Day 30:   Launch (LLM direct generation, no RAG)
Day 60:   First batch of real user data
Day 90:   Data volume sufficient → activate RAG
Day 180:  Data volume sufficient → activate Bandit
```

## Expert Seed Data TODO (Not Blocker)

- Collect 200-300 expert golden cases
- Sources: career coaches, HR professionals, public resume datasets
- Timing: After MVP complete, before Launch
- NOT a prerequisite for development

## Files

- `workspaces/keystone/04-validate/01-redteam-full-report.md`
- `workspaces/keystone/journal/0041-RISK-cold-start-trap.md` (superseded by this decision)

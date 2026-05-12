# Task 27: Wire JD Generator frontend to market data API

**Status**: pending
**Priority**: P0
**Source**: /redteam audit

## Description

B2B VP gap: frontend never calls /recruiter/skills/lookup.

## Requirements

1. On industry+title change, fetch skill suggestions from /recruiter/skills/lookup API
2. Display "Based on N JDs, X% require Y skill" stats
3. Replace hardcoded SKILLS_SUGGESTIONS with dynamic data
4. Show generation_source to indicate if market data was used

## Value Proposition

JD generation for recruiters — tell you what skills the market actually requires.

## Files to modify

- apps/web/src/app/(recruiter)/recruiter/jd/page.tsx
- src/keystone/api/jd_generator.py (response format)

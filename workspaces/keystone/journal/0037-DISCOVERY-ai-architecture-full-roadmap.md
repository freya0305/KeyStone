# Journal Entry

## DISCOVERY: Full AI/ML Architecture Roadmap — 4-Phase Iterative Reduction Plan

**Slug**: full-ai-architecture-roadmap-8-components
**Type**: DISCOVERY
**Date**: 2026-04-30

## What Was Discovered

User confirmed three goals:
1. Build self-buildable databases from Day 1
2. Gradually reduce AI model calls over iterations to reduce costs
3. Expects to need RAG, SHAP, Bandit — asked what else exists

Research identified 8 distinct ML/AI components organized into a 4-phase roadmap:

### Phase 1 (Day 1) — Infrastructure First
- PostgreSQL, Redis, Rule Engine, Vector DB, Embedding Model
- AI calls: 100% baseline, $3-5K/month per 1000 users

### Phase 2 (Month 3-6) — RAG Activates
- RAG reduces AI calls by 40-50%
- A/B Testing framework activates
- Cost drops to $1.5-2K/month per 1000 users

### Phase 3 (Month 6-12) — Bandit + Collaborative Filtering
- Bandit: auto-learns suggestion ranking
- Collaborative Filtering: finds similar users/resumes
- Feature Store: precomputed features for ML
- AI calls reduce by additional 30-40%

### Phase 4 (Month 12+) — Predictive Models
- Prediction model: predicts which suggestion leads to best outcome
- SHAP: explains predictions
- Knowledge Graph: skill relationship network
- Learning to Rank: advanced suggestion ordering
- Cost drops to $0.5-0.7K/month per 1000 users

## Key Insight: Cost Reduction Path

The architecture creates a natural cost reduction flywheel:

```
More suggestion feedback data
     ↓
Better RAG retrieval quality
     ↓
Fewer AI calls needed (AI only for novel cases)
     ↓
Lower costs
     ↓
Can serve more users with same budget
     ↓
More data (flywheel continues)
```

## Files Created

- `workspaces/keystone/01-analysis/01-ml-research/05-iterative-ai-reduction-roadmap.md` — Full 8-component roadmap

## Related

- Follow-up: PostgreSQL schema design for Phase 1
- Follow-up: Redis cache strategy
- Follow-up: Vector database setup (Pinecone vs Chroma)

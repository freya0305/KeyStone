# Journal Entry

## DISCOVERY: ML Architecture Gap in KeyStone Product Brief

**Slug**: ml-analysis-reveals-architecture-gap
**Type**: DISCOVERY
**Date**: 2026-04-30

## What Was Discovered

The current KeyStone product brief describes AI/ML capabilities at the **feature level** ("AI analyzes resume", "AI suggests changes") but has **no ML architecture** — no component diagram, no data flow, no cost model, no scaling path.

Three distinct layers were found to be missing:

### Layer 1: "LLM as Tool" vs "LLM as Model"
Current plan uses LLM for everything. This is correct for MVP but masks the gap between:
- **LLM as Tool** (calling Haiku/Sonnet like an API) — works now, $3-5K/month for 1000 users
- **LLM as Model** (fine-tuned, trained on proprietary data) — not possible yet, requires 10K+ outcome records

### Layer 2: The "Suggestion Feedback" Data Loop Is the Core Moat
The brief emphasizes **outcome tracking** as the moat, but the actual AI moat is the **suggestion feedback loop**:

```
User sees suggestion → Adopts/Rejects/Modifies → Recorded
     ↑                                               │
     └────────── 1000+ records → AI learns ──────────┘
```

This is what enables outcome-calibrated suggestion ranking. Without this loop, AI suggestions remain "generic advice" forever.

### Layer 3: Cost Architecture Is Non-Trivial
MVP LLM cost: ~$3-5/user/month (unsustainable at scale)
Optimized LLM cost: ~$0.17/user/month (via caching + vector embedding)
The gap is 20-30x — affects pricing strategy directly.

## Why This Matters

1. **No ML architecture = no engineering plan** — can't estimate dev time, infra cost, or build sequence
2. **Data moat is NOT automatic** — requires deliberate data collection infrastructure from Day 1
3. **Cost model affects pricing** — $3/user/month LLM cost vs $0.17 is the difference between profitable and unprofitable Pro tier

## Files Created

- `01-analysis/01-ml-research/01-what-ml-keystone-actually-needs.md` — 3-layer ML taxonomy
- `01-analysis/01-ml-research/02-ml-component-map.md` — 7 functional modules mapped to tech components + cost model
- `01-analysis/01-ml-research/03-data-infrastructure.md` — data hierarchy by priority
- `01-analysis/02-architecture-options/01-three-tier-architecture.md` — full system architecture

## Related

- Follow-up: Need to determine actual build sequence vs cost optimization sequence
- Follow-up: Need to decide vector database choice (Pinecone vs Chroma vs Qdrant)
- Follow-up: Need to validate whether the 3-tier cost model (LLM → LLM+RAG → LLM+RAG+Predictor) matches funding timeline

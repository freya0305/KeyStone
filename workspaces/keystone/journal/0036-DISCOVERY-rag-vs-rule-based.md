# Journal Entry

## DISCOVERY: RAG + Rule-Based Hybrid Architecture Is Achievable From Day 1

**Slug**: rag-rule-based-hybrid-keystone
**Type**: DISCOVERY
**Date**: 2026-04-30

## What Was Discovered

User asked whether KeyStone can build "own database" infrastructure from Day 1 instead of depending entirely on AI model calls. This revealed a layered architecture answer:

### The Four AI Dependency Layers

1. **Data Collection (100% self-buildable from Day 1)**
   - PostgreSQL: user behavior, suggestion feedback, outcome tracking
   - No AI model involved — pure data infrastructure

2. **Rule-Based Systems (80% self-buildable from Day 1)**
   - NRIC detection via regex
   - Resume format parsing
   - Job platform URL detection
   - Skill tag matching for 4-level assessment

3. **Vector Database + RAG (Buildable from Day 1, effective only after 6 months of data)**
   - Pinecone/Chroma stores resume vectors + job vectors
   - Similar case retrieval: "has this kind of resume line + job type + suggestion ever worked before?"
   - RAG = AI first consults database, then generates

4. **Language Generation + Complex Reasoning (Cannot self-build)**
   - Natural language suggestion generation
   - Explaining "why this suggestion works"
   - Handling novel/unseen resume formats

### RAG Is NOT a Replacement for AI Models

Key clarification: RAG (Retrieval Augmented Generation) doesn't replace AI models. It supplements them.

- **Without RAG**: AI generates suggestions from "memory" (model's training data)
- **With RAG**: AI first consults "case studies" (KeyStone's own database), then generates

The database quality determines how much the AI relies on external model vs internal knowledge.

### Bandit + SHAP Timeline

- **Bandit**: Learns which suggestion types work best. Activates after 100+ suggestion feedback records. Not a Day 1 capability.
- **SHAP**: Explains AI predictions (why this suggestion has 73% adoption probability). Critical for B2B explainability requirements. Activates after 12+ months.

### The Core Moat Is Suggestion Feedback Data

The "suggestion feedback loop" (user adopts/rejects/modifies → recorded → AI learns) is what enables all downstream ML:

```
Suggestion Feedback Data (1000+ records)
     ↓
RAG Quality Improves
     ↓
Bandit Ranking Activates
     ↓
Predictive Model Trainable
```

Without deliberate Day 1 data collection infrastructure, none of these activate.

## Files Created

- `workspaces/keystone/01-analysis/01-ml-research/04-do-we-need-ai-models.md`

## Related

- Follow-up: Should Pinecone or Chroma be chosen for vector DB? (cost vs maintenance tradeoff)
- Follow-up: How to implement the suggestion feedback loop at the UX level?
- Follow-up: What's the minimal viable RAG setup for Day 1?

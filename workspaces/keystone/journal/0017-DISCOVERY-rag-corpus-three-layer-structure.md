---
type: DISCOVERY
date: 2026-04-29
created_at: 2026-04-29T14:30:00Z
author: agent
session_id: 874f263b-1879-49b0-9e64-1f293538aedb
project: keystone
topic: RAG corpus is three distinct layers with different build timelines; employer fingerprints are the pre-launch priority
phase: analyze
tags: [rag-corpus, data-moat, pre-launch, employer-fingerprints]
---

## Discovery

The RAG corpus is not a single dataset — it is three structurally different layers with different sources, build methods, and timelines:

**Layer 1: Employer Fingerprints** (buildable pre-launch)
- 50 major SG employers' hiring preferences, language expectations, cultural keywords
- Built via: recruiter interviews (SGD 100-200/session × 10 sessions) + JD corpus analysis
- Format: YAML documents per employer
- Timeline: 4–8 weeks of pre-launch work

**Layer 2: SG Market Rules** (buildable pre-launch)
- 200 rules covering NS framing, age-neutral language, photo guidance, GLC culture, industry vocab
- Built via: recruiter interviews, MOM/Fair Consideration Framework public docs, NUS/NTU career guides
- Format: YAML rule documents with rationale and examples
- Timeline: parallel with Layer 1

**Layer 3: User Preference Signals** (only accumulates post-launch)
- Accept/Reject/Modify patterns per company_type × role_level × industry
- Built via: product usage (automatic)
- Format: structured signal records in the suggestion_signals table
- Timeline: begins Day 1 of launch; meaningful at Month 6 (100K+ signals)

## Key Implication

Layers 1 and 2 can be built BEFORE the product launches with ~SGD 1,000-2,000 investment (recruiter interview fees) and significant founder time. This means the product does NOT launch into a cold-start RAG state — it launches with genuine SG market intelligence.

Layer 3 is what creates the irreproducible moat. Layers 1-2 can be replicated by a competitor in 60-90 days. Layer 3 cannot be replicated because it requires real user interactions over time.

## Recruiter Interview as Investment

10 recruiter interviews × SGD 150/session = SGD 1,500 total. Each interview extracts:
- 3–5 employer-specific fingerprints (from their placement history)
- 10–20 market rules (SG-specific patterns they observe repeatedly)

This is the highest-ROI pre-launch data investment available. It creates content no competitor can buy off the shelf.

## For Discussion

1. What validation mechanism ensures the employer fingerprints extracted from recruiter interviews are accurate? A recruiter's perception of what DBS wants might lag actual DBS hiring practice by 12-18 months. How do we maintain fingerprint freshness?
2. The 50-employer target for pre-launch seems arbitrary. Is it better to have 50 shallow fingerprints or 10 deep ones? Given user concentration in fresh-grad tech roles, deep fingerprints for Grab/Sea/GovTech/DBS may be more valuable than shallow coverage of 50 employers.
3. Should the RAG corpus structure be defined in `specs/technical.md` or as a standalone spec file? As the primary defensibility asset, it probably warrants its own spec section with schema definitions.

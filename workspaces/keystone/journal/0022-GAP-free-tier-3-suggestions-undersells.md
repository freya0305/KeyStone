---
type: GAP
date: 2026-04-29
created_at: 2026-04-29T22:05:00Z
author: agent
session_id: current
project: keystone
topic: Implementation blocked — backend framework decision not made, users table missing
phase: redteam
tags: [implementation-blockers, technical, scope]
---

## Gaps

Two execution-blocking issues found during analyst validation:

### GAP 1: Backend Framework Decision Not Made

**Source**: 04-implementation-sequencing.md §Phase 0

The plan says "FastAPI vs Kailash Nexus evaluation" at M0.1. But every subsequent implementation task depends on this decision:
- Router structure
- Dependency injection
- Database ORM choices
- Authentication integration
- API versioning strategy

**Impact**: Phase 0 cannot begin until this decision is made.

**Decision required**: FastAPI (familiar, large ecosystem) or Kailash Nexus (integrated, newer)?

### GAP 2: Users Table Missing From Data Model

**Source**: 03-data-moat-strategy.md §2

The data model shows `suggestion_signals.user_id` and `applications.user_id`, but the **users table schema is never documented**. Every entity references it but none define it.

Required fields that must be specified:
- `id` (UUID)
- `email` (unique, for auth)
- `phone` (for verification, after anti-abuse decision)
- `created_at`
- `consent_flags` (six independent consent states)
- `subscription_status` (free/pro)
- `subscription_end_date`

**Impact**: Cannot build auth, consent, or subscription systems without this schema.

### GAP 3: Free Tier at 3 Suggestions Per JD

**Source**: 04-pricing.md §4 recommendation; 02-ux-ui-design-plan.md §8

The pricing analysis explicitly recommends: **"Increase free tier from 3 to 10 suggestions on first match."**

The UX plan still shows 3 suggestions with gate at #4.

**Impact**: Primary conversion bottleneck not resolved. Users hit the wall before experiencing full value.

## For Discussion

1. FastAPI vs Nexus — does the founder have a preference based on team capabilities?
2. Users table — should this be a M0 deliverable explicitly stated in the implementation plan?
3. Free tier — should this be updated to 10 suggestions on first JD before /todos?

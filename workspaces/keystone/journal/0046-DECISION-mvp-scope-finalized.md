# Journal Entry

## DECISION: MVP Scope v1.0 Finalized — 3 Autonomous Deliverables Complete

**Slug**: mvp-scope-v1-complete
**Type**: DECISION
**Date**: 2026-04-30

## Decisions Made

### MVP Scope v1.0 Confirmed

| # | Feature | Frontend |
|---|---------|----------|
| 1 | JD Parsing (URL/text) | ❌ Backend only |
| 2 | Resume Parsing | ❌ Backend only |
| 3 | Match Score | ✅ Display |
| 4 | Skill Match Details | ✅ Display |
| 5 | Suggestions (3-5) | ✅ Display |
| 6 | Resume Editor | ✅ Display |
| 7 | Resume Export (PDF/Word) | ✅ Display |
| 8 | **Outcome Tracking** | ✅ Added per user feedback |
| 9 | Singapore-specific | ✅ In suggestions |

### Key Clarifications

- JD and resume parsing NOT shown to user (backend only)
- User only sees: match score, skill details, suggestions
- Outcome tracking IN MVP (core data collection mechanism)
- Resume export IN MVP (user needs to see changes before applying)

## 3 Deliverables Completed Autonomously

1. **User Interview Design** (`02-plans/02-user-interview-design.md`)
   - 10 questions covering: pricing validation, pain points, acquisition channels
   - Target: 10-15 interviews
   - Success criteria defined

2. **Acquisition Strategy** (`02-plans/03-acquisition-strategy.md`)
   - First 100 users: career coach partnerships + LinkedIn
   - Referral mechanism design
   - Year 1 target: 2,400 registered users
   - CAC: $3.5/user (via referral-heavy model)

3. **Technical Architecture** (`02-plans/04-technical-architecture.md`)
   - Full data model (users, resumes, jobs, analyses, outcomes, suggestion_feedback)
   - API design (all endpoints)
   - AI call strategy (Phase 1: no cache, Haiku+Sonnet)
   - 10-week development timeline
   - Monthly cost: ~$700 (100 users)

## Files

- `workspaces/keystone/02-plans/01-mvp-scope-v1.md` — MVP Scope v1.0
- `workspaces/keystone/02-plans/02-user-interview-design.md` — Interview Design
- `workspaces/keystone/02-plans/03-acquisition-strategy.md` — Acquisition Strategy
- `workspaces/keystone/02-plans/04-technical-architecture.md` — Technical Architecture

## Status

MVP scope and three planning documents complete. Ready for next phase.

## Related

- Follow-up: Engineer assignment for technical architecture review
- Follow-up: Start user interviews (Week 1 action item)
- Follow-up: Career coach outreach (Week 1 action item)

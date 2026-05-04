# DECISION: M4 Implementation Choices

**Date**: 2026-05-04
**Phase**: /implement

## Decisions Made

### 1. Suggestion Signals Architecture (M4.2)
- Created new `src/keystone/api/suggestions.py` router
- Used SHA256 hash of Clerk ID for anonymized_user_id (PDPA compliance)
- Added context extraction from JobAnalysis job_parsed_json for company_type, role_level, industry
- Support for authenticated users only (no anonymous signals in M4.2)

### 2. Application Tracking (M5.1 + M5.2)
- Extended existing `job_seeker.py` with full CRUD + batch update
- JSON `stages` and `application_stages` table kept in sync via service layer
- Soft delete via `auto_closed_at` timestamp
- Batch update optimized for <1.5s on 30 applications

### 3. Free Tier Gating (M4.3)
- First JD detection via counting existing job_analyses for user
- Gate context message includes section name + JD coverage percentage
- Clear paywall copy: "6 more suggestions — this is where Pro comes in"

### 4. LLM Cost Ceiling (M4.4)
- Redis-backed with in-memory fallback for local dev
- SGD 5/month ceiling with graceful degradation
- Degraded responses show cached content or user-friendly message (not errors)

## Incomplete
- M4.1 `generate_suggestions()` function - helper functions created but main function not exported

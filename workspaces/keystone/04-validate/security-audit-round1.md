# KeyStone Security Audit Round 1

**Date**: 2026-05-11
**Auditor**: security-reviewer
**Scope**: `src/keystone/api/job_seeker.py`, `apps/web/src/components/keystone/InterviewPrepModal.tsx`

---

## Findings

### 1. INTERNAL_API_KEY Timing-Safe Comparison

**Status**: PASSED

**Location**: `src/keystone/api/job_seeker.py:71`

```python
if x_internal_api_key is None or not secrets.compare_digest(x_internal_api_key, settings.INTERNAL_API_KEY):
```

**Analysis**: Uses `secrets.compare_digest()` for constant-time comparison, preventing timing attacks.

---

### 2. Suggestion-Outcome Correlation SQL Injection

**Status**: PASSED

**Location**: `src/keystone/api/job_seeker.py:2268-2269`

```python
if limit_match_level:
    query = query.where(Suggestion.match_level == limit_match_level)
```

**Analysis**: Uses SQLAlchemy ORM query builder. All queries use parameterized SQL through SQLAlchemy's expression language. No raw SQL concatenation found. `limit_match_level` flows through `get_suggestion_outcome_correlation(db, limit_match_level=match_level)` and is used in a SQLAlchemy `.where()` clause which parameterizes automatically.

---

### 3. Gamification Endpoint Authorization

**Status**: PASSED (with observation)

**Location**: `src/keystone/api/job_seeker.py:3473-3476`

```python
@router.get("/analytics/gamification", response_model=GamificationStats)
async def get_gamification_stats(
    user: AuthUser = Depends(get_current_user),
```

**Analysis**: Endpoint requires authentication via `get_current_user` dependency. PASSED.

**Observation**: The separate `/suggestions/outcomes/correlate` endpoint (line 2319) uses `optional_current_user`, allowing anonymous access. This endpoint returns aggregate platform statistics (signal counts, response rates by match_level) rather than per-user data. This appears intentional for public analytics but worth confirming with product team.

---

### 4. Interview Prep Modal Data Handling

**Status**: PASSED

**Location**: `apps/web/src/components/keystone/InterviewPrepModal.tsx:39-58`

```typescript
if (mode === "prep") {
  await apiRequest(`/job-seeker/applications/${application.id}`, {
    method: "PATCH",
    body: {
      status: "interview",
      notes: notes.trim() || undefined,
    },
  });
} else {
  await apiRequest(`/job-seeker/applications/${application.id}/stages`, {
    method: "POST",
    body: {
      stage_type: "interview",
      outcome: outcome || "completed",
      notes: notes.trim() || undefined,
      stage_date: nextRoundDate || undefined,
    },
  });
}
```

**Analysis**: Only non-sensitive fields are transmitted: `application.id`, `status`, `notes`, `stage_type`, `outcome`, `stage_date`. The `employer` and `role` fields from the `Application` interface are used only for UI display in the modal header (lines 81-86), not sent to any API. No sensitive data exposure found.

---

### 5. Hardcoded Credentials Check

**Status**: PASSED

**Searched**: `password`, `api_key`, `secret`, `token` in `apps/web/src/`

**Findings**:

- `apps/web/src/app/(auth)/sign-up/[[...sign-up]]/page.tsx` - `password` is a React `useState('')` for user input, not hardcoded
- `src/keystone/services/claude_client.py` - `api_key` appears only in context of `TokenUsage` type/class and `input_tokens`/`output_tokens` pricing constants, not actual credentials

No hardcoded secrets, API keys, or passwords found.

---

## Summary

| Check                                        | Status |
| -------------------------------------------- | ------ |
| INTERNAL_API_KEY timing-safe comparison      | PASSED |
| Suggestion-outcome correlation SQL injection | PASSED |
| Gamification endpoint authorization          | PASSED |
| InterviewPrepModal data handling             | PASSED |
| No hardcoded credentials                     | PASSED |

**Issues Found**: 0

**Observations**: 1

- `/suggestions/outcomes/correlate` allows anonymous access (`optional_current_user`). Verify this is intentional for the aggregate analytics use case.

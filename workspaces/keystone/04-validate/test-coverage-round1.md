# Test Coverage Audit - Round 1

**Date**: 2026-05-11
**Phase**: /redteam Test Coverage Audit
**Audit Method**: grep-based import verification per `rules/testing.md` Audit Mode

## Verification Summary

| New Module                                           | Has Tests | Status  |
| ---------------------------------------------------- | --------- | ------- |
| `src/keystone/services/application_auto_close.py`    | NO        | **GAP** |
| `src/keystone/services/skill_etl.py`                 | NO        | **GAP** |
| `src/keystone/api/job_seeker.py`                     | NO        | **GAP** |
| `apps/web/src/app/(recruiter)/recruiter/jd/page.tsx` | NO        | **GAP** |

## Detailed Findings

### 1. `application_auto_close.py` - NO TESTS

**Module path**: `src/keystone/services/application_auto_close.py`
**Test search**: `rg "application_auto_close" tests/` → 0 matches
**Status**: GAP

This service module has no test coverage. It needs:

- Unit tests for the auto-close logic
- Integration tests if it interacts with database/queue

### 2. `skill_etl.py` - NO TESTS

**Module path**: `src/keystone/services/skill_etl.py`
**Test search**: `rg "skill_etl" tests/` → 0 matches
**Status**: GAP

This ETL service has no test coverage. It needs:

- Unit tests for skill extraction/transformation/load
- Integration tests against real database

### 3. `job_seeker.py` - NO TESTS

**Module path**: `src/keystone/api/job_seeker.py`
**Test search**: `rg "job_seeker" tests/` → 0 matches
**Status**: GAP

The API module includes `get_suggestion_outcome_correlation()` function but has no tests. Needs:

- Unit tests for API endpoints
- Integration tests for database interactions

### 4. `apps/web/src/app/(recruiter)/recruiter/jd/page.tsx` - NO TESTS

**Module path**: `apps/web/src/app/(recruiter)/recruiter/jd/page.tsx`
**Test search**: `ls apps/web/tests/` → "NO tests/ directory in apps/web"
**Status**: GAP

The JD Generator page has API calls:

- `POST /recruiter/jd/generate` - JD generation
- `GET /recruiter/skills/lookup` - skill suggestions

No test infrastructure exists for the web app.

## Additional Findings

### Gamification Tests - NOT FOUND

**Search**: `rg "gamification" tests/` → 0 matches
**Status**: No gamification tests exist in the codebase

### Suggestion-Outcome Correlation - SOURCE EXISTS, NO TESTS

**Search**: `rg "suggestion_outcome" src/keystone/` → Found in `job_seeker.py`

```
src/keystone/api/job_seeker.py:async def get_suggestion_outcome_correlation(
src/keystone/api/job_seeker.py:    return await get_suggestion_outcome_correlation(db, limit_match_level=match_level)
```

**Status**: Function exists but has no test coverage

## Test Infrastructure Status

Existing tests in `tests/`:

- `tests/unit/` - 9 test files (nric_detector, llm_cost_tracker, circuit_breaker, jd_fetcher, jd_parser, company_classifier, match_assessor, suggestion_generator, s3, resume_parsing)
- `tests/integration/` - empty (no test files)
- `tests/regression/` - 1 test file
- `tests/sdk/` - 1 test file
- No `tests/e2e/` directory exists

## Gap Summary

| Gap                                                  | Severity | Recommendation                              |
| ---------------------------------------------------- | -------- | ------------------------------------------- |
| application_auto_close.py                            | HIGH     | Add unit + integration tests                |
| skill_etl.py                                         | HIGH     | Add unit + integration tests                |
| job_seeker.py (incl. suggestion_outcome_correlation) | HIGH     | Add API unit tests + integration tests      |
| apps/web tests                                       | HIGH     | Create tests/ directory with Playwright E2E |
| No integration test infrastructure                   | MEDIUM   | Set up Docker-based integration tests       |
| No E2E tests                                         | MEDIUM   | Add Playwright E2E for critical user flows  |

## Recommended Actions

1. **Immediate**: Add unit tests for `application_auto_close.py`, `skill_etl.py`, `job_seeker.py`
2. **Short-term**: Create `apps/web/tests/` with Playwright setup
3. **Medium-term**: Add integration tests in `tests/integration/` with real Docker services
4. **Medium-term**: Add E2E tests for JD generator user flow

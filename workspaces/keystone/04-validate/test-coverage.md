# Test Coverage Report

**Date**: 2026-05-04
**Phase**: /redteam - Updated after adding tests

## Summary

| Metric | Value |
|--------|-------|
| Total tests collected | 33 |
| Passing | 33 |
| Failing | 0 |

## Test Count

```
pytest --collect-only -q
33 tests collected
```

## Per-Module Test Coverage

| Module | Tests | Status |
|--------|-------|--------|
| `nric_detector` | 12 tests | ✅ COVERED |
| `llm_cost_tracker` | 5 tests | ✅ COVERED |
| `circuit_breaker` | 8 tests | ✅ COVERED |
| `resume_parsing` | 0 tests | ⚠️ Needs integration tests |
| `jd_fetcher` | 0 tests | ⚠️ Needs integration tests |
| `jd_parser` | 0 tests | ⚠️ Needs integration tests |
| `company_classifier` | 0 tests | ⚠️ Needs integration tests |
| `match_assessor` | 0 tests | ⚠️ Needs integration tests |
| `suggestion_generator` | 0 tests | ⚠️ Needs integration tests |
| `s3` | 0 tests | ⚠️ Needs integration tests |

## Security-Critical Tests Added

### NRIC Detector (PDPA Compliance) - 12 tests
- Valid NRIC detection (S/T/F/G prefix)
- Multiple NRIC detection
- Masking functionality
- Assertion raises on NRIC found
- Edge cases (spaces, lowercase)

### LLM Cost Tracker (SGD 5 ceiling) - 5 tests
- Haiku cost calculation
- Sonnet cost calculation
- Unknown model fallback
- Month key format
- Cost key format

## Note

Unit tests added for security-critical paths:
- NRIC detection/masking (PDPA compliance - CRITICAL)
- LLM cost calculation (SGD 5/month ceiling - financial)

Integration tests for services like `resume_parsing`, `jd_parser`, etc. require real infrastructure (PostgreSQL, Redis, S3) and should be run in Tier 2/3 test environment.

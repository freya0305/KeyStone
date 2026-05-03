# RISK: Red Team Findings — KeyStone Implementation

**Date**: 2026-05-04
**Type**: RISK
**Summary**: Security audit found 2 CRITICAL, 6 HIGH issues in initial implementation

---

## CRITICAL

### 1. Hardcoded DB credentials with defaults
- **File**: `src/keystone/core/__init__.py:20`
- **Issue**: `database_url = "postgresql+asyncpg://keystone:keystone@localhost:5432/keystone"`
- **Fix**: Removed defaults, `database_url` and `redis_url` now required in `.env`
- **Risk**: If `.env` fails to load, app falls back to hardcoded credentials

### 2. RLS modeled but not implemented
- **File**: `src/keystone/models/entities.py`
- **Issue**: RLS policies documented in comments but no actual PostgreSQL RLS policies
- **Risk**: B2B tenant data could leak across tenants
- **Status**: Deferred — requires Alembic migration + actual policy definitions

---

## HIGH

### 3. NRIC detector never called (dead code)
- **File**: `src/keystone/services/nric_detector.py`
- **Issue**: `detect_nric()` defined but never imported or called anywhere
- **Risk**: PDPA compliance hollow — NRIC numbers could be stored
- **Fix**: Need to integrate into resume upload pipeline
- **Status**: Deferred — not yet in upload flow

### 4. Stripe webhook handlers were stubs
- **File**: `src/keystone/services/stripe_service.py`
- **Issue**: `handle_checkout_completed()` etc only logged, didn't update DB
- **Risk**: Payments confirmed but subscription tier never updated
- **Fix**: Implemented actual DB updates with proper error handling

### 5. In-memory idempotency fails under multi-worker
- **File**: `src/keystone/services/stripe_service.py`
- **Issue**: `_processed_events: set[str]` — in-memory set doesn't work with uvicorn workers
- **Risk**: Same Stripe event processed multiple times under load
- **Fix**: Changed to Redis-based idempotency with 7-day TTL

### 6. JWT auth stubbed out, fake UUIDs used
- **File**: `src/keystone/api/jd_generator.py`
- **Issue**: `user_id: uuid.UUID  # TODO: Get from auth token`
- **Risk**: No authentication — anyone can create JDs under any identity
- **Fix**: Auth implementation deferred to KY1.5
- **Status**: Open — requires real JWT validation

### 7. test_circuit_breaker.py API incompatibility
- **File**: `tests/test_circuit_breaker.py`
- **Issue**: Tests passed `failure_threshold=N` directly to `CircuitBreaker()` but dataclass only accepts `config: CircuitBreakerConfig`
- **Risk**: Tests would fail at runtime
- **Fix**: Updated to use `CircuitBreakerConfig(failure_threshold=N)` correctly

---

## MEDIUM

### 8. Share link view count race condition
- **File**: `src/keystone/api/jd_generator.py:227-229`
- **Issue**: `share_link.view_count += 1` — non-atomic read-modify-write
- **Risk**: Lost increments under concurrent access
- **Fix**: Use atomic UPDATE or database-level increment

### 9. No rate limiting
- **File**: All endpoints
- **Risk**: DoS via expensive LLM calls
- **Status**: Deferred — add `@limiter` decorator

---

## Actions Taken

1. ✅ Removed hardcoded DB/Redis defaults
2. ✅ Implemented Stripe webhook handlers with real DB updates
3. ✅ Changed idempotency to Redis-based
4. ✅ Fixed circuit breaker test API incompatibility
5. ⏳ RLS policies — deferred to migration phase
6. ⏳ NRIC integration — deferred to resume upload flow
7. ⏳ JWT auth — deferred to KY1.5
8. ⏳ Rate limiting — deferred

# KeyStone Security Audit

**Date**: 2026-05-04
**Auditor**: Security Review Agent
**Scope**: NRIC handling, Auth (Clerk JWT), SQL injection, Stripe webhooks, data exposure

---

## Finding 1: In-Memory Rate Limiting Under Multi-Worker Deployment

**Description**: The rate limiter in `src/keystone/services/rate_limit.py` uses an in-memory dictionary (`_rate_limit_store`) to track request counts. Under a multi-worker deployment (e.g., uvicorn with multiple workers or Gunicorn), each worker maintains its own independent rate limit state, allowing an attacker to bypass rate limits by routing requests to different workers.

**File**: `src/keystone/services/rate_limit.py:19`

```python
_rate_limit_store: dict[str, list[float]] = defaultdict(list)
```

**Severity**: MEDIUM

**Status**: Known Issue - documented in code comment "Simple in-memory rate limiter for MVP. Production should use Redis-based rate limiting."

**Recommendation**: Replace in-memory store with Redis-based rate limiting. The Redis client is already available in the project (`src/keystone/services/stripe_service.py:60` uses `redis.from_url`). Implement sliding window rate limiting using Redis sorted sets.

---

## Finding 2: No Rate Limit on Internal Auto-Close Endpoint

**Description**: The internal auto-close endpoint at `POST /job-seeker/internal/auto-close-applications` has no rate limiting or authentication. While labeled "internal," it is mounted on the same public router without any secret or IP restriction.

**File**: `src/keystone/api/job_seeker.py:2607-2638`

```python
@router.post("/internal/auto-close-applications")
async def auto_close_stale_applications(
    days_inactive: int = 30,
    db: AsyncSession = Depends(get_db),
):
```

**Severity**: HIGH

**Recommendation**: Either:
1. Add a static API key check via header (e.g., `X-Internal-API-Key`)
2. Move to a separate internal router with network-level restriction
3. Require authentication (but this would couple internal jobs to user auth)

---

## Finding 3: Clerk JWT Auto-Provisioning Creates Users Without Consent Check

**Description**: The `get_current_user` function auto-provisions new B2C users on first authentication without checking if the user has completed the consent flow. A new user hitting any protected endpoint will have a User record created with default consent flags (`consent_pdpa=False`, `consent_marketing=False`, `consent_ai_training=False`).

**File**: `src/keystone/services/clerk_auth.py:153-164`

```python
# Auto-provision new B2C users
if user is None:
    email = payload.get("email", f"{clerk_id}@clerk.dev")
    name = payload.get("name", email.split("@")[0])
    user = User(
        clerk_id=clerk_id,
        email=email,
        name=name,
    )
    db.add(user)
    await db.commit()
```

**Severity**: MEDIUM

**Note**: This may be intentional for Clerk OAuth flow. Consent is checked separately at AI processing endpoints via `ConsentService.check_ai_processing()`. The User record creation is separate from consent grant.

---

## Finding 4: Missing Security Tests

**Description**: No dedicated security tests exist for:
- NRIC redaction and detection
- SQL injection prevention
- JWT validation edge cases
- Stripe webhook signature verification

**Severity**: MEDIUM

**Recommendation**: Add security-focused tests in `tests/security/`:
- Test NRIC regex patterns with various formats
- Test that parameterized queries are used (no string interpolation)
- Test Clerk token expiration handling
- Test Stripe signature verification failure cases

---

## PASSED Checks

### NRIC Exposure
- **Status**: PASSED
- `nric_detector.py` implements regex pattern for SG NRIC (`S/F/G + 7 digits + letter`)
- Three-stage protection:
  1. Stage 1: `mask_resume_text()` masks before S3 upload (`job_seeker.py:243`)
  2. Stage 2: `assert_no_nric()` raises before Claude API calls (`job_seeker.py:946, 1362, 1667`)
  3. Stage 3: `mask_nric()` sanitizes Claude output (`job_seeker.py:1388, 1693`)
- `SuggestionSignal.anonymized_user_id` stores SHA256 hash, not user ID (`entities.py:199`)
- `phone_hash` stores SHA256 of phone, not actual phone (`entities.py:78`)

### Auth (Clerk JWT)
- **Status**: PASSED
- `clerk_auth.py` uses `python-jose` with JWKS caching
- All protected endpoints use `Depends(get_current_user)`
- Token verification with proper audience and issuer validation (`clerk_auth.py:107-113`)
- `verify_clerk_token()` raises `HTTPException` on invalid/expired tokens

### SQL Injection Prevention
- **Status**: PASSED
- All database queries use SQLAlchemy ORM with parameterized queries
- No raw SQL string interpolation found
- Examples: `select(User).where(User.clerk_id == clerk_id)`, `select(Application).where(Application.id == application_id)`

### Stripe Webhook Security
- **Status**: PASSED
- `verify_stripe_signature()` uses official Stripe SDK (`stripe_service.py:63-84`)
- `stripe.Webhook.construct_event()` verifies signature against raw request body
- Redis-based idempotency with `SET NX` prevents duplicate event processing (`stripe_service.py:87-96`)
- Event ID stored with 7-day expiry

### Data Exposure
- **Status**: PASSED
- No PII in structured logs (NRIC, passwords, credit cards)
- `content_sanitizer.py` implements field masking
- `mask_sensitive_fields()` function for dict sanitization
- Export endpoint returns user data via API (appropriate for authenticated user)

### Secrets Management
- **Status**: PASSED
- All secrets via environment variables (`.env`)
- `pydantic-settings` with `SettingsConfigDict(env_file=".env")`
- No hardcoded secrets found in codebase
- `stripe_webhook_secret`, `clerk_secret_key`, etc. all from settings

### Frontend Security
- **Status**: PASSED
- ClerkProvider wraps entire app (`layout.tsx:35`)
- Bearer token attached to all API requests via `getToken()` (`api.ts:19-22`)
- API_BASE configurable via `NEXT_PUBLIC_API_URL` environment variable
- No sensitive data stored in localStorage beyond preferences (dark mode)

---

## Summary

| Category | Status | Severity |
|----------|--------|----------|
| NRIC Exposure | PASSED | - |
| Auth (Clerk JWT) | PASSED | - |
| SQL Injection | PASSED | - |
| Stripe Webhook | PASSED | - |
| Data Exposure | PASSED | - |
| Secrets Management | PASSED | - |
| Frontend Security | PASSED | - |
| Rate Limiting | NEEDS FIX | MEDIUM |
| Internal Endpoint Protection | NEEDS FIX | HIGH |
| Security Tests | NEEDS IMPROVEMENT | MEDIUM |

**Critical Issues**: 0
**High Issues**: 1 (internal endpoint)
**Medium Issues**: 2 (rate limiting, tests)
**Passed**: 7 categories

---

## Recommendations

1. **HIGH**: Add authentication/API key check to `/internal/auto-close-applications` endpoint
2. **MEDIUM**: Replace in-memory rate limiting with Redis-based implementation for production
3. **MEDIUM**: Add security unit tests for NRIC detection, SQL injection prevention, JWT validation
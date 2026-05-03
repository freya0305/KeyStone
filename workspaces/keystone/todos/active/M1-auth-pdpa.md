# M1 — Auth + PDPA Compliance Layer

> Depends on: M0.1, M0.2
> Must be complete before any real user data is processed.
> Implements: specs/compliance.md (full), specs/technical.md §Auth

---

## M1.1 — Clerk auth integration (backend)

**What**: Integrate Clerk as the auth provider. Backend validates Clerk JWTs on all authenticated endpoints.

**Deliverables**:
- Clerk SDK installed + configured with project API keys from `.env`
- FastAPI middleware that validates Clerk JWT on every protected route
- `get_current_user()` dependency that returns user record from DB (creates if first login)
- Unprotected routes: `POST /api/analyze/guest` (first-use, no auth), `GET /health`
- All other API routes require valid Clerk JWT

**User creation on first Clerk login**:
- Auto-create `users` record from Clerk user data (email, name)
- Set `subscription_tier = "free"` by default
- Initialize `consent_flags = {}` (empty — no consent given yet)
- Do NOT assume any consent at user creation time

**Acceptance criteria**:
- Unauthenticated request to protected endpoint returns 401
- Valid Clerk JWT returns 200 with user context
- New user record created in DB on first login
- Model IDs in `.env` only

**Implements**: specs/technical.md §Auth, specs/compliance.md §Consent Architecture

---

## M1.2 — Clerk auth integration (frontend)

**What**: Integrate Clerk in Next.js frontend. Provide login/signup pages and auth state management.

**Deliverables**:
- `ClerkProvider` wrapping app layout
- `/sign-in` and `/sign-up` pages using Clerk components (styled to match design system)
- `useAuth()` hook available throughout app
- Guest mode: user can complete first analysis without signing in (no auth gate)
- Auth prompt triggers after: accepting first suggestion, attempting to download resume, hitting second JD analysis
- `"Save your work"` copy — NOT `"Sign up"` (per Analysis 24 §Decision 2)
- After auth: restore in-progress analysis from anonymous session (see M1.3)

**Acceptance criteria**:
- Google OAuth login works end-to-end
- Email + password login works
- Guest can reach suggestion page without auth
- Auth prompt fires at correct trigger points only

**Implements**: specs/mvp-scope.md §Feature 3 (no signup required for first use), workspaces/keystone/01-analysis/24-ux-core-analysis.md §Decision 2

---

## M1.3 — SMS phone verification (anti-abuse)

**What**: SG mobile phone number verification at account creation. One phone number = one account. Prevents multi-account abuse of the unlimited-first-analysis gate.

**Deliverables**:
- Twilio (or equivalent) SMS OTP integration for SG +65 numbers
- Backend: `POST /api/auth/phone/send-otp` (sends 6-digit OTP to phone)
- Backend: `POST /api/auth/phone/verify` (validates OTP, marks phone as verified on user record)
- Phone number stored on user record (hashed — not plaintext, only hash for deduplication check)
- Check: if phone hash already exists on another account → reject with `"This phone number is linked to an existing account."`
- Frontend: phone verification screen in onboarding flow (after Google OAuth signup)
- OTP expires in 10 minutes; max 3 attempts before lockout (10 min lockout)

**Cost**: ~SGD 0.05 per verification — negligible. Budget for 10,000 signups = SGD 500/year.

**Acceptance criteria**:
- SG +65 mobile receives OTP within 30 seconds
- Attempting to register a second account with same phone returns error
- Phone number stored only as hash — cannot be reverse-derived from DB
- OTP locked after 3 failed attempts

**Implements**: specs/mvp-scope.md §Feature 3 (Anti-abuse), specs/product.md §Feature 3 Anti-abuse

---

## M1.4 — NRIC masking pipeline (three-stage shared utility)

**What**: Shared utility function for NRIC detection and masking. Used at all three pipeline stages. Inline masking at individual call sites is BLOCKED — all code must call this shared utility.

**Pattern**: NRIC regex `[STFGstfg]\d{7}[A-Za-z]`

**Shared utility** (`src/core/nric.py`):
- `detect_nric(text: str) -> list[str]` — returns all NRIC matches found
- `mask_nric(text: str) -> str` — replaces all NRIC matches with `[NRIC_REDACTED]`
- `assert_no_nric(text: str) -> None` — raises `NRICDetectedError` if any NRIC found (used before AI API calls)

**Stage 1 — upload to S3**:
- Call `mask_nric()` on extracted text before writing to S3
- Log detection event (not the NRIC value): `{user_id, detected_count, timestamp}`
- Add to resume's `sg_flags.nric_detected = true` if any found
- Notify frontend to show: "We detected an NRIC number in your resume. We've recommended removing it."

**Stage 2 — before Claude API call**:
- Call `assert_no_nric()` on payload just before sending to Claude
- If assertion fails (edge case — unusual formatting survived Stage 1): call `mask_nric()` and log anomaly

**Stage 3 — Claude output to DB**:
- Sanitise AI-generated suggestions for NRIC-like patterns (AI may generate example strings)
- Store sanitised output only

**Acceptance criteria**:
- 100% NRIC masking: test suite with 20 NRIC patterns (including edge cases: lowercase, embedded in sentences, adjacent to punctuation) — all must be masked
- `assert_no_nric` raises on any surviving pattern before AI call
- No NRIC value appears in any DB column, log entry, or API response
- Unit tests: `test_nric_masking_all_prefixes`, `test_nric_assert_raises`, `test_nric_stage1_stage2_stage3`

**Implements**: specs/compliance.md §NRIC Handling (full three-stage pipeline)

---

## M1.5 — Six-type consent architecture

**What**: Database-backed consent state per user per consent type. Every data processing pipeline must check consent before processing.

**Six consent types** (from specs/compliance.md):
1. `registration` — mandatory for account creation
2. `storage` — storing resume + application data
3. `ai_processing` — sending data to Claude API
4. `b2b_sharing` — aggregate data with institutional clients
5. `outcome_tracking` — storing application outcomes
6. `marketing` — newsletters + promotional emails (NOT pre-ticked)
7. `ai_training` — B2C only: feedback used for model improvement (separate from ai_processing, explicit opt-in)

**Backend**:
- `user_consents` table (from M0.2): stores per-user per-type consent state with timestamps
- `ConsentService.has_consent(user_id, consent_type) -> bool`
- `ConsentService.grant(user_id, consent_type)` and `ConsentService.revoke(user_id, consent_type)`
- Middleware: every endpoint in `ai_processing` path calls `has_consent(user_id, "ai_processing")` — returns 403 with `"enable_ai_processing_consent_required"` error code if not granted
- B2B data gate: any pipeline touching B2B user data checks `b2b_tenant_training_blocked(tenant_id) = True` (hard-coded True for ALL B2B tenants) — training pipeline raises if called with B2B data

**Frontend**:
- Consent collection screen (shown after signup, before first AI analysis)
- Each consent shown individually with plain-language explanation
- `ai_training` consent explicitly separated from `ai_processing` consent — user can enable AI analysis without enabling training
- Marketing consent: checkbox, not pre-ticked, PDPA requirement
- All consent state persisted to backend on confirm

**Acceptance criteria**:
- Sending resume to Claude without `ai_processing` consent returns 403
- `ai_training` consent is independent of `ai_processing` consent
- Revoking `storage` consent stops data writes (but does not delete existing data — deletion is a separate action)
- B2B user data NEVER reaches training pipeline — integration test verifying the gate

**Implements**: specs/compliance.md §Consent Architecture (full), specs/product.md §Feature 3 (Learning loop PDPA note)

---

## M1.6 — Privacy policy + legal text

**What**: PDPA-compliant privacy policy and terms of service. Required before any real user data is processed.

**Deliverables**:
- Privacy policy covering all six consent types with plain-language explanation
- Data residency statement: "All data stored in Singapore (AWS ap-southeast-1)"
- Data export / deletion rights (PDPA requirement)
- AI processing transparency: "Your resume content is sent to Anthropic's Claude API for analysis. Anthropic is configured to retain zero data."
- B2B training separation clause: "Data from institutional clients is never used for AI model training."
- Published at `/privacy` and `/terms`
- DPO name + contact must be added once DPO is engaged (placeholder acceptable for design partner phase)

**Note**: This is a legal document — founders must review with SG counsel before real-user launch. This todo creates the draft; legal review is a pre-launch gate (see M12).

**Implements**: specs/compliance.md §PDPA Obligations, specs/mvp-scope.md §Compliance done criteria


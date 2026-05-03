# Redteam Round 2 — Validation Report

**Date**: 2026-04-30
**Scope**: Spec compliance, pricing consistency, technical architecture, compliance design
**Agents**: 4 parallel (spec compliance, user flows, technical/compliance, moat/competitive)
**Status**: ALL CRITICAL FINDINGS FIXED

---

## CRITICAL Findings Fixed

### CRITICAL-1: PRODUCT_BRIEF.md — Old Pricing (SGD 19/180)

**File**: `PRODUCT_BRIEF.md`
**Finding**: Pro tier stated at SGD 19/month (correct: SGD 12), Annual at SGD 180 (correct: SGD 144), break-even at "800 users" (correct: ~300), unit economics at SGD 19 revenue (correct: SGD 12).
**Status**: FIXED — all pricing updated to SGD 12 Pro / SGD 144 Annual / 300 user break-even.

### CRITICAL-2: specs/users.md — Wrong LTV Figures

**File**: `specs/users.md`
**Finding**: Persona 1 LTV showed SGD 57 (should be SGD 36 = 3×SGD 12). Persona 2 showed SGD 180 annual (should be SGD 144). Persona 2 also stated SGD 108-228 at SGD 19 pricing.
**Status**: FIXED — Persona 1 corrected to SGD 36; Persona 2 corrected to SGD 72-144 (6-12 months × SGD 12) or SGD 144 annual.

### CRITICAL-3: specs/market.md — TAM at Wrong Price

**File**: `specs/market.md`
**Finding**: TAM calculated at SGD 19/mo × 3-4 months = SGD 8.6M-19M. Should be SGD 12/mo.
**Status**: FIXED — TAM recalculated: SGD 5.4M-12M/year.

### CRITICAL-4: specs/compliance.md — PDPA Consent Conflates Purposes

**File**: `specs/compliance.md`
**Finding**: "AI Processing" consent covered both API analysis AND model training. These are legally distinct PDPA purposes requiring separate consent.
**Status**: FIXED — split into "AI Analysis" (required for service) and "AI Training Data" (separate opt-in checkbox, not pre-ticked).

### CRITICAL-5: specs/technical.md — Suggestion Signals Wrong Consent Reference

**File**: `specs/technical.md`
**Finding**: suggestion_signals table referenced "AI Processing" consent (now split). Model training use case was ambiguous.
**Status**: FIXED — now references "AI Training Data" consent specifically.

### CRITICAL-6: specs/product.md — Google OAuth Phone Verification Bypass

**File**: `specs/product.md`
**Finding**: Anti-abuse rule "1 phone = 1 account" only applied to email+phone signup. Google OAuth had no phone verification requirement.
**Status**: FIXED — added explicit requirement: phone verification required BEFORE free tier entitlement is activated, regardless of signup method.

### CRITICAL-7: specs/gtm.md — LTV Reference Wrong

**File**: `specs/gtm.md`
**Finding**: "CAC of SGD 40-80 against LTV of SGD 57" used corrected LTV from Persona 1.
**Status**: FIXED — updated to SGD 36-144 LTV range; clarified paid acquisition only viable for Annual Plan.

---

## HIGH Findings Fixed

### HIGH-1: NRIC Regex Incomplete

**File**: `specs/compliance.md`, `specs/product.md`
**Finding**: NRIC pattern only covered S/T/F/G prefix. Did not include M/N (PR) or FIN (foreigners).
**Status**: FIXED — patterns expanded to `[STFGstfgMN]\d{7}[A-Za-z]` (citizen/PR) and `[KLPkpmn]\d{7}[A-Za-z]` (FIN).

### HIGH-2: Content Hash Function Unspecified

**File**: `specs/product.md`
**Finding**: Resume content hash caching mentioned but hash function not specified.
**Status**: FIXED — added "SHA-256 minimum" to content hash specification.

### HIGH-3: LLM Cost Enforcement Mechanism Unspecified

**File**: `specs/technical.md`
**Finding**: SGD 5/user/month cost ceiling stated but enforcement mechanism not defined.
**Status**: FIXED — added Redis counter per user/month, 80% Haiku fallback threshold, 100% hard block.

### HIGH-4: Data Retention Schedule Missing

**File**: `specs/compliance.md`
**Finding**: No explicit data retention schedule for user data types.
**Status**: FIXED — added Data Retention Schedule section with per-data-type retention periods and deletion triggers.

### HIGH-5: Weekly Digest Scope Conflict

**Files**: `specs/mvp-scope.md` vs `workspaces/keystone/01-analysis/40-tier-feature-definition.md`
**Finding**: mvp-scope.md listed weekly digest as Phase 2; 40-tier-feature-definition.md listed it as Pro v1.0 feature.
**Status**: FIXED — mvp-scope.md updated to reflect Pro v1.0 feature. Confirmed by product.md Feature 4 design (weekly digest is primary outcome logging mechanism).

---

## Verified Correct (No Changes Needed)

| Item | Source | Status |
|------|--------|--------|
| Basic = SGD 9 | specs/business-model.md, specs/mvp-scope.md, 40-tier-feature-definition.md | PASS |
| Pro = SGD 12 | specs/business-model.md, specs/mvp-scope.md, 40-tier-feature-definition.md | PASS |
| Annual = SGD 144 | specs/business-model.md, specs/mvp-scope.md, 40-tier-feature-definition.md | PASS |
| Break-even = ~300 users | specs/business-model.md, Analysis 43 | PASS |
| Pro margin ~75% | specs/business-model.md | PASS |
| Suggestion signals table design | specs/technical.md | PASS |
| Google OAuth + phone verification rule | specs/product.md (now explicit) | PASS |
| User flow documents | workspaces/keystone/03-user-flows/ (7 files) | PASS (created by Round 1) |

---

## Round 2 Validation Summary

- **CRITICAL findings**: 7 found, 7 fixed ✓
- **HIGH findings**: 5 found, 5 fixed ✓
- **Remaining gaps**: Require human action (not AI-fixable) — see Journal 0035/0036

## Files Modified This Round

| File | Changes |
|------|---------|
| PRODUCT_BRIEF.md | Pricing (3 items), unit economics, break-even, B2B strategy text |
| specs/users.md | Persona 1 LTV, Persona 2 LTV |
| specs/market.md | TAM recalculation |
| specs/compliance.md | PDPA consent split (AI Analysis / AI Training Data), NRIC regex, data retention schedule |
| specs/technical.md | Consent reference fix, margin correction, LLM cost enforcement mechanism |
| specs/product.md | Google OAuth phone verification, NRIC/FIN regex, SHA-256 content hash |
| specs/gtm.md | LTV reference in paid acquisition section |
| specs/mvp-scope.md | Weekly digest moved from Phase 2 to Pro v1.0 |

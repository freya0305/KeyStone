# Task #15 — Remove Annual Plan

> Status: pending | Priority: CRITICAL | Depends on: none

---

## What

Annual Plan (SGD 144/year) is cancelled. Remove from: pricing page UI, billing backend, Stripe dashboard. Only Pro monthly (SGD 12/month) remains.

---

## Deliverables

### 1. Pricing Page — remove annual toggle

**File**: `apps/web/src/app/pricing/page.tsx`

Remove:

- Monthly/Annual toggle or tab
- Annual plan description and price (SGD 144/year)
- Any "Save X%" badge for annual
- Any "Most Popular" badge on annual

Keep:

- Guest tier
- Free tier
- Pro monthly SGD 12/month

### 2. Billing backend — remove annual plan type

**File**: `src/keystone/services/stripe_service.py` OR `src/keystone/api/billing.py`

Remove:

- `price_annual_pro` variable and annual Stripe price ID
- Any `create_annual_checkout()` function
- Annual plan in subscription tier enum

Update:

- Pro subscription to only accept monthly SGD 12

### 3. Frontend billing — remove annual checkout

**File**: `apps/web/src/app/(app)/app/settings/page.tsx` or billing component

Remove:

- "Switch to Annual" button
- Annual plan upgrade flow

### 4. Stripe Dashboard (manual)

Cancel/Archive the annual plan SKU in Stripe dashboard if it exists:

- Find product "KeyStone Pro Annual" or similar
- Set status to "Archived"

---

## Acceptance Criteria

- [ ] Pricing page shows only: Guest, Free, Pro monthly SGD 12
- [ ] No monthly/annual toggle visible
- [ ] Backend billing API rejects or ignores annual plan requests
- [ ] No annual plan in Stripe product list (archived)

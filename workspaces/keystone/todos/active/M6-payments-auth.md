# M6 — Payments + Subscription Management

> Depends on: M0.2, M1.1 (Clerk auth), M4.3 (free tier gating)
> Implements: specs/business-model.md §B2C Tiers, specs/mvp-scope.md §Payments and Auth

---

## M6.1 — Stripe integration (backend)

**What**: Stripe SGD billing for monthly and annual Pro subscriptions.

**Products to create in Stripe**:
- `keystone_pro_monthly`: SGD 19/month (recurring)
- `keystone_pro_annual`: SGD 190/year (recurring) — equivalent to ~SGD 15.83/month

**Backend endpoints**:
- `POST /api/billing/create-checkout-session` — creates Stripe Checkout session for chosen plan
  - Returns `{checkout_url: "https://checkout.stripe.com/..."}` — redirect user to Stripe-hosted checkout
  - Metadata: `{user_id, plan_id}` on the session for webhook reconciliation
- `POST /api/billing/webhook` — receives Stripe webhook events
  - `checkout.session.completed` → update `users.subscription_tier = 'pro'`, store `stripe_customer_id` and `stripe_subscription_id`
  - `invoice.payment_succeeded` → log renewal
  - `invoice.payment_failed` → downgrade to free after grace period (3 days)
  - `customer.subscription.deleted` → downgrade to free immediately
- `POST /api/billing/create-portal-session` — Stripe Customer Portal for self-serve subscription management (cancel, switch plans, update payment method)
- `GET /api/billing/subscription` — return current subscription status

**Stripe Checkout configuration**:
- Currency: SGD
- Tax: Stripe Tax configured for Singapore (9% GST)
- Success URL: `https://keystone.sg/pro/welcome?session_id={CHECKOUT_SESSION_ID}`
- Cancel URL: `https://keystone.sg/pricing`

**Idempotency**: Stripe webhook events must be idempotent. Store processed event IDs to prevent double-processing.

**Acceptance criteria**:
- Monthly checkout: user clicks "Subscribe" → Stripe Checkout → payment succeeds → `subscription_tier = 'pro'` in DB
- Annual checkout: same flow, different plan
- Webhook `invoice.payment_failed` after 3 days: user downgraded to free
- Customer Portal: user can cancel subscription without contacting support
- GST calculated correctly on SGD invoices

**Implements**: specs/business-model.md §B2C Tiers, specs/mvp-scope.md §Payments and Auth

---

## M6.2 — Pro subscription frontend

**What**: Pricing page and subscription management UI.

**Pricing page (`/pricing`)**:
- Three tiers: Guest (free), Free, Pro (SGD 19/mo or SGD 190/yr)
- Toggle: Monthly / Annual (annual = 2 months free framing)
- Annual price: "SGD 190/year — save SGD 38 vs monthly"
- CTA: "Get Pro" → Stripe Checkout redirect
- No countdown timers. No scarcity. No "limited offer." (per Analysis 26 §3.7 Modal)
- Tax clarity: "Prices exclude 9% GST"

**Pro welcome page** (`/pro/welcome`):
- Shown after successful checkout
- Confirms Pro activation
- One CTA: "Start analysing jobs →"

**Subscription management (in Settings)**:
- Current plan display
- Billing portal button: "Manage subscription, cancel, or change plan →" → Stripe Portal
- Next billing date + amount

**Upgrade prompt** (Paywall gate component — used throughout app):
```
┌────────────────────────────────────────────────────┐
│  ✦ 6 more suggestions for this role                 │
│  (For your Experience section — 60% of this JD)    │
│                                                     │
│  [Unlock all — SGD 19/month]                        │
│  Try Pro free for 3 days (no card needed)           │
│                                                     │
│  Or analyse a different job for free                │
└────────────────────────────────────────────────────┘
```

**3-day free trial** (Stripe trial period, no card required):
- `POST /api/billing/create-trial` — creates Stripe customer + subscription with 3-day trial, no payment method required
- After trial: user receives email to add payment method (Stripe-handled)
- Trial users get full Pro access for 3 days

**Acceptance criteria**:
- Monthly and annual checkout flows complete end-to-end
- GST displayed correctly
- 3-day trial: full Pro access with no card for 3 days
- Paywall gate component shows specific gated section name + suggestion count
- No scarcity/countdown language in any copy

**Implements**: specs/business-model.md §B2C pricing, Analysis 28 §Risk 3 (Paywall friction), Analysis 24 §Part 4 (Gate design)

---

## M6.3 — Pro feature gating middleware (frontend)

**What**: Client-side components that enforce Pro feature gates consistently.

**Gated features**:
- Suggestions beyond the first 3 on non-first JDs
- Dashboard analytics / Insights tab (full analytics locked for free users after Month 1)
- Batch mode (Phase 2 — not yet, but gate architecture must be in place)

**`useSubscription()` hook**: returns `{tier: 'free'|'pro', isGated: boolean, gatedReason: string}`

**Gate component**: `<ProGate feature="suggestions_beyond_3" section="Experience" count={6}>` renders gate UI if user is free tier.

**Acceptance criteria**:
- Free user sees gate at correct trigger points
- Pro user sees no gates
- Gate component renders correct section name and count

**Implements**: specs/mvp-scope.md §Feature 3 (free tier limit)


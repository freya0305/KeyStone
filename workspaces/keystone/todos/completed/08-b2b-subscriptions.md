# Task #11 — B2B Stripe Subscription Management

> Status: pending | Priority: CRITICAL | Depends on: none

---

## What

Full B2B Stripe subscription flow for Agency Basic (SGD 79/mo), Agency Pro (SGD 199/mo), Agency Team (SGD 449/mo). Enforce JD generation limits per tier. Handle webhooks. Tenant invite flow for Agency Team.

---

## Deliverables

### 1. B2B Stripe Products (Stripe Dashboard)

Create three B2B products manually in Stripe:

- **Agency Basic**: SGD 79/month, 1 seat, 50 JD generations/month
- **Agency Pro**: SGD 199/month, 1 seat, unlimited JD generations
- **Agency Team**: SGD 449/month, 5 seats, unlimited JD generations

Note: Create in test mode first, migrate to live.

### 2. B2B Tenant model

**File**: `src/keystone/models/entities.py`

```python
class B2BTenant(Base):
    __tablename__ = "b2b_tenants"
    id: int
    name: str  # Company name
    stripe_subscription_id: str
    tier: str  # "basic" | "pro" | "team"
    seat_count: int
    jd_generation_count: int  # Reset monthly
    jd_limit: int  # 50 for basic, -1 for unlimited
    created_at: datetime
    updated_at: datetime

class B2BUser(Base):
    __tablename__ = "b2b_users"
    id: int
    tenant_id: int  # FK to b2b_tenants
    email: str
    name: str
    role: str  # "owner" | "member"
    invited_at: datetime
    joined_at: datetime | None
```

### 3. B2B checkout endpoint

**File**: `src/keystone/api/b2b_onboarding.py`

```python
@router.post("/b2b/checkout")
async def create_b2b_checkout(
    tier: str,  # "basic" | "pro" | "team"
    email: str,
    company_name: str,
):
    # Create or get B2BTenant
    # Create Stripe checkout session with B2B product price
    # Return checkout URL
    pass

@router.post("/b2b/portal")
async def get_b2b_portal(current_user: User = Depends(get_current_user)):
    # Return Stripe customer portal URL for subscription management
    pass
```

### 4. B2B subscription webhook handler

**File**: `src/keystone/api/webhooks.py` (extend existing)

Handle events:

- `checkout.session.completed` → create B2BTenant
- `customer.subscription.updated` → update tier/limits
- `customer.subscription.deleted` → suspend tenant
- `invoice.payment_failed` → notify tenant owner

### 5. JD generation limit enforcement

**File**: `src/keystone/api/jd_generator.py`

```python
@router.post("/recruiter/jd/generate")
async def generate_jd(
    ...,  # existing params
    current_user: User = Depends(get_current_user),
):
    # Get user's B2B tenant
    tenant = await db.b2b_tenants.get_by_user(current_user.id)

    if tenant:
        if tenant.jd_limit == -1:  # unlimited
            pass
        elif tenant.jd_generation_count >= tenant.jd_limit:
            raise HTTPException(429, "JD generation limit reached for this month")
        tenant.jd_generation_count += 1
        await db.b2b_tenants.save(tenant)

    # Proceed with JD generation
    pass
```

### 6. Team invite flow (Agency Team only)

```python
@router.post("/b2b/invite")
async def invite_team_member(
    email: str,
    current_user: User = Depends(get_current_user),
):
    # Verify current user is tenant owner
    # Check seat count < tier limit
    # Send invite email
    # Create B2BUser record with joined_at = None
    pass

@router.post("/b2b/accept-invite")
async def accept_invite(
    invite_token: str,
    name: str,
):
    # Verify token
    # Create Clerk user if needed
    # Update B2BUser.joined_at = now
    pass
```

---

## Acceptance Criteria

- [ ] Recruiter can select Agency Basic/Pro/Team and checkout via Stripe
- [ ] Stripe webhook creates B2BTenant on successful payment
- [ ] Basic tier enforced: 50 JD generations/month, blocks at limit
- [ ] Pro/Team tier: unlimited JD generations
- [ ] Team tier: owner can invite up to 5 members
- [ ] Subscription cancellation suspends tenant access
- [ ] B2B portal URL returned for subscription management

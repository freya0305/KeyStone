# Task #10 — B2C Training Consent Checkbox at Registration

> Status: pending | Priority: CRITICAL | Depends on: none

---

## What

Sign-up page must show separate AI training opt-in checkbox (distinct from service consent). Gate suggestion_signals pipeline: only log signals for users who opted in. Consent recorded in database.

---

## Deliverables

### 1. Sign-up page: add training consent checkbox

**File**: `apps/web/src/app/(auth)/sign-up/[[...sign-up]]/page.tsx`

Add below the existing consent checkbox:

```typescript
<div className="consent-section">
  <label>
    <input
      type="checkbox"
      name="ai_training_consent"
      checked={aiTrainingConsent}
      onChange={(e) => setAiTrainingConsent(e.target.checked)}
    />
    <span>
      I agree to contribute my resume and application data to improve KeyStone's
      AI suggestions. My data is anonymized and used only for aggregate
      skill frequency analysis. I can revoke this consent at any time in settings.
    </span>
  </label>
</div>
```

State:

```typescript
const [aiTrainingConsent, setAiTrainingConsent] = useState(false);
```

### 2. Backend: record consent at registration

**File**: `src/keystone/api/auth_phone.py` (extend verify endpoint)

The verify endpoint already creates the user. Add consent recording:

```python
@router.post("/api/auth/phone/verify")
async def verify_phone(
    phone: str,
    code: str,
    consent_ai_training: bool = False,  # NEW param
    ...existing params
):
    # Existing: verify OTP, get/create user

    # NEW: record consent
    if consent_ai_training:
        await db.consents.create(
            user_id=user.id,
            consent_type="AI_TRAINING",
            granted=True,
            granted_at=datetime.utcnow(),
        )
    else:
        # Record explicit refusal
        await db.consents.create(
            user_id=user.id,
            consent_type="AI_TRAINING",
            granted=False,
            granted_at=datetime.utcnow(),
        )

    return {"token": token, "user": {...}}
```

### 3. Backend: gate suggestion_signals on consent

**File**: `src/keystone/services/suggestion_signals.py` (new file)

```python
async def log_signal(
    user_id: int,
    suggestion_id: int,
    action: str,  # "ACCEPTED" | "REJECTED" | "MODIFIED"
    suggestion_text: str,
    original_text: str,
) -> None:
    # Check consent
    consent = await db.consents.get(
        user_id=user_id,
        consent_type="AI_TRAINING"
    )

    if not consent or not consent.granted:
        # Log anonymously - no user association
        await db.signals.create(
            suggestion_id=suggestion_id,
            action=action,
            user_id=None,  # Anonymous
            suggestion_text=suggestion_text,
            original_text=original_text,
            # No training_pipeline flag set
        )
    else:
        # Log with user association for product improvement
        await db.signals.create(
            suggestion_id=suggestion_id,
            action=action,
            user_id=user_id,
            suggestion_text=suggestion_text,
            original_text=original_text,
            training_pipeline=True,
        )
```

### 4. Consent page in settings

**File**: `apps/web/src/app/(app)/app/settings/page.tsx`

Add consent management section:

```typescript
<div className="consent-settings">
  <h3>Data & Privacy</h3>
  <label>
    <input
      type="checkbox"
      checked={user.consents.ai_training}
      onChange={(e) => updateConsent('AI_TRAINING', e.target.checked)}
    />
    <span>AI Training Consent</span>
  </label>
  <p>Revoke at any time. Affects future suggestions only.</p>
</div>
```

---

## Acceptance Criteria

- [ ] Sign-up page shows separate AI training opt-in checkbox
- [ ] Checkbox is unchecked by default (opt-in only)
- [ ] Backend records consent decision at user creation
- [ ] Suggestion signals only include user ID if consent.granted == True
- [ ] Settings page allows consent revocation
- [ ] Revoking consent stops future signal logging (existing data unchanged)

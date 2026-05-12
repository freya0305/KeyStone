# Task #14 — Batch Quick-Update UI

> Status: pending | Priority: CRITICAL | Depends on: Task #13 (application auto-creation)

---

## What

Batch quick-update UI for application status updates. Designed for updating 30 applications in under 3 minutes. Persistent banner when returning to product. Card-per-application with [Got response] / [No news] / [Skip] action buttons.

---

## Deliverables

### 1. Batch update banner component

**File**: `apps/web/src/app/(app)/layout.tsx` or a shared Banner component

```typescript
// Show banner when user has ≥1 pending applications
{pendingCount > 0 && (
  <div className="batch-update-banner">
    <span>You have {pendingCount} applications pending update</span>
    <button onClick={() => router.push('/app/applications?batch=true')}>
      Update Now
    </button>
    <button onClick={dismissBanner}>Later</button>
  </div>
)}
```

### 2. Batch update page (/app/applications?batch=true)

**File**: `apps/web/src/app/(app)/app/applications/page.tsx`

When `batch=true`:

- Show card-per-application layout (not table)
- Each card shows: Company, Job Title, Days since last update, Current stage
- Three action buttons per card:
  - [Got response] → opens stage update modal
  - [No news] → increments no-news counter, stays pending
  - [Skip] → dismisses card from batch view

### 3. Batch update API endpoint

**File**: `src/keystone/api/applications.py`

```python
@router.patch("/applications/batch-update")
async def batch_update_applications(
    updates: list[BatchUpdateItem],  # [{id, action, stage_data}]
    current_user: User = Depends(get_current_user),
):
    results = []
    for update in updates:
        if update.action == "got_response":
            await update_application_stage(
                application_id=update.id,
                stage="response",
                outcome="received",
                user_id=current_user.id,
            )
        elif update.action == "no_news":
            await db.application_updates.create(
                application_id=update.id,
                action="no_news",
                created_at=datetime.utcnow(),
            )
        # Skip: no action needed
        results.append({"id": update.id, "status": "ok"})
    return {"results": results}
```

### 4. Pending count API

**File**: `src/keystone/api/applications.py`

```python
@router.get("/applications/pending-count")
async def get_pending_count(current_user: User = Depends(get_current_user)):
    apps = await db.applications.list(user_id=current_user.id)
    pending = [a for a in apps if a.needs_update]  # No update in 7+ days
    return {"count": len(pending)}
```

---

## Acceptance Criteria

- [ ] Returning user sees batch update banner if pending applications exist
- [ ] Banner has [Update Now] and [Later] actions
- [ ] Batch page shows card-per-application layout
- [ ] Each card has [Got response] / [No news] / [Skip] buttons
- [ ] Batch update submits all changes in one API call
- [ ] Skipped cards don't reappear in batch view until new stage update needed

# Task #12 — Application Quality Gate (≥2 Status Updates)

> Status: pending | Priority: CRITICAL | Depends on: none

---

## What

Only applications with ≥2 status updates count as "active applications" in analytics and JD training data. Applications with only the auto-created record are excluded from aggregate analytics but their JD URLs are still logged anonymously for skill frequency training.

---

## Deliverables

### 1. Query filter for active applications

**File**: `src/keystone/services/analytics.py` (new file)

```python
async def get_active_applications(user_id: int) -> list[Application]:
    """Only applications with ≥2 status updates."""
    apps = await db.applications.list(user_id=user_id)
    active = []
    for app in apps:
        stage_count = await db.application_stages.count(application_id=app.id)
        if stage_count >= 2:
            active.append(app)
    return active

async def log_jd_for_training(user_id: int, job_url: str, job_title: str) -> None:
    """Log JD URL anonymously for skill frequency training. No user association."""
    # Only log if application is NOT active (single-stage)
    # Active applications are linked via user consent, handled separately
    await db.jd_generation_logs.insert(
        job_url_hash=hashlib.sha256(job_url.encode()).hexdigest(),
        job_title=job_title,
        logged_at=datetime.utcnow(),
        # NO user_id - anonymous
    )
```

### 2. Update analytics queries

**File**: `src/keystone/api/job_seeker.py` — response rate endpoint

```python
@router.get("/analytics/response-rate")
async def get_response_rate(current_user: User = Depends(get_current_user)):
    # Only count active applications (≥2 updates)
    active_apps = await analytics.get_active_applications(current_user.id)

    total = len(active_apps)
    responded = sum(1 for a in active_apps if a.has_response)
    rate = responded / total if total >= 5 else None  # Min 5 for display

    return {"response_rate": rate, "total_active": total}
```

### 3. Update JD training data logging

In `create_application_from_export` (Task #13):

```python
# If application already exists as single-stage, still log JD URL for training
if existing and existing.stage_count < 2:
    await analytics.log_jd_for_training(
        user_id=current_user.id,
        job_url=job_url,
        job_title=job_title
    )
```

---

## Acceptance Criteria

- [ ] Analytics only count applications with ≥2 status updates
- [ ] Response rate requires ≥5 active applications before display
- [ ] Single-stage applications don't appear in analytics dashboard
- [ ] JD URLs from single-stage applications logged anonymously to jd_generation_logs
- [ ] PDPA: no user_id in jd_generation_logs entries

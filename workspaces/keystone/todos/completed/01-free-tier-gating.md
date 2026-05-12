# Task #7 — Free Tier Suggestion Gating

> Status: pending | Priority: CRITICAL | Depends on: none

---

## What

API-level enforcement of free tier suggestion limits:

- First JD for any user = unlimited suggestions
- Second+ JDs for Free users = first 3 suggestions only, rest gated
- Pro users = unlimited for all JDs

---

## Deliverables

### 1. Track analyzed JDs per user

**File**: `src/keystone/models/entities.py`

Add `UserAnalysisCount` model or extend `User` model to track:

```python
# Track which JDs a user has already analyzed (for gating)
class analyzed_job(Base):
    __tablename__ = "analyzed_jobs"
    id: int
    user_id: int  # FK to users
    job_url_hash: str  # SHA256 of normalized job URL
    job_title: str
    analyzed_at: datetime
```

Or simpler: add `analysis_count` field to a join table.

### 2. Check tier + count before returning suggestions

**File**: `src/keystone/api/job_seeker.py`

In `POST /api/analyze` or a new `GET /api/suggestions` endpoint:

- Check user's `subscription_tier`
- Check if this `job_url_hash` already exists in `analyzed_jobs` for this user
- If not analyzed before: mark as analyzed, return all suggestions
- If analyzed before AND tier == "free": limit suggestions to first 3
- If analyzed before AND tier == "pro": return all suggestions

### 3. Create analysis record on first analyze

**File**: `src/keystone/services/analysis_cache.py` (new file)

```python
async def mark_job_analyzed(user_id: int, job_url: str, job_title: str) -> None:
    url_hash = hashlib.sha256(job_url.encode()).hexdigest()
    # Upsert into analyzed_jobs
```

### 4. Gating logic in suggestions endpoint

**File**: `src/keystone/api/suggestions.py`

```python
# After suggestions are generated:
if user_tier == "free":
    url_hash = hashlib.sha256(job_url.encode()).hexdigest()
    is_first_analysis = not await db.analyzed_jobs.exists(
        user_id=user_id, job_url_hash=url_hash
    )
    if not is_first_analysis:
        suggestions = suggestions[:3]  # Gate to 3
```

---

## Acceptance Criteria

- [ ] Free user, first JD → all suggestions returned
- [ ] Free user, second JD → only first 3 suggestions returned
- [ ] Pro user, any JD → all suggestions returned
- [ ] Suggestion count is per-job (not per-session)
- [ ] `analyzed_jobs` table populated on each first analysis

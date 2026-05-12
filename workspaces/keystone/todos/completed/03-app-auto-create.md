# Task #13 — Application Auto-Creation After Resume Export

> Status: pending | Priority: CRITICAL | Depends on: none (can run in parallel with Task #7, #8, #12)

---

## What

When a user downloads a tailored resume (export), automatically create an Application record with status "auto_created". Then prompt the user: "Did you submit to [Company]?"

---

## Deliverables

### 1. New endpoint: POST /api/applications/from-export

**File**: `src/keystone/api/job_seeker.py`

```python
@router.post("/applications/from-export")
async def create_application_from_export(
    resume_id: int,
    job_url: str,
    job_title: str,
    company_name: str,
    current_user: User = Depends(get_current_user),
):
    # Check if application already exists for this user+job_url
    existing = await db.applications.exists(
        user_id=current_user.id,
        job_url_hash=hashlib.sha256(job_url.encode()).hexdigest()
    )
    if existing:
        return {"application_id": existing.id, "already_exists": True}

    # Create application with auto-created status
    application = await db.applications.create(
        user_id=current_user.id,
        job_url=job_url,
        job_title=job_title,
        company_name=company_name,
        resume_id=resume_id,
        status="auto_created",  # New status enum value
        source="resume_export",
    )

    return {"application_id": application.id, "already_exists": False}
```

### 2. Update Application model

**File**: `src/keystone/models/entities.py`

Add to `Application` model:

```python
status: str  # "auto_created" | "confirmed" | "withdrawn" | "auto_closed"
source: str  # "manual" | "resume_export"
```

### 3. Frontend: handleExport calls API then shows interstitial

**File**: `apps/web/src/app/(guest)/analyse/page.tsx`

Update `handleExport` function:

```typescript
const handleExport = async () => {
  // 1. Download resume (existing)
  await downloadResume(...)

  // 2. Create application record
  const res = await fetch('/api/applications/from-export', {
    method: 'POST',
    body: JSON.stringify({ resume_id, job_url, job_title, company_name })
  })
  const { application_id } = await res.json()

  // 3. Show "Did you submit?" interstitial
  if (application_id) {
    setPendingApplicationId(application_id)
    setShowSubmitPrompt(true)
  }
}
```

Add `ShowSubmitPrompt` component:

- "Did you submit to [Company]?"
- [Yes, I submitted] [Not yet] [Skip]
- "Yes" → update application status to "confirmed"
- "Not yet" → keep as "auto_created", remind later
- "Skip" → dismiss

---

## Acceptance Criteria

- [ ] Resume export triggers POST /api/applications/from-export
- [ ] Duplicate application (same user+job_url) returns existing record, doesn't create dup
- [ ] "Did you submit?" prompt appears after export
- [ ] User choice updates application status correctly

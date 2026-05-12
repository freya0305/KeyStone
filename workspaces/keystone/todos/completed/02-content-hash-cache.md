# Task #8 — Content Hash Caching

> Status: pending | Priority: CRITICAL | Depends on: none

---

## What

Resume analysis is expensive (LLM calls). If the same resume is analyzed against the same JD URL again within 7 days, return cached result instead of re-running LLM analysis. Cache key = `resume.content_hash + job_url`.

---

## Deliverables

### 1. Check cache before LLM analysis

**File**: `src/keystone/api/job_seeker.py`

In `POST /api/analyze`:

```python
async def analyze_resume(user_id: int, resume_id: int, job_url: str, ...):
    # 1. Get resume and its content_hash
    resume = await db.resumes.get(resume_id)

    # 2. Compute cache key
    cache_key = f"{resume.content_hash}:{hashlib.sha256(job_url.encode()).hexdigest()}"

    # 3. Check cache table
    cached = await db.analysis_cache.get(cache_key)
    if cached and (now - cached.created_at).days < 7:
        return cached.result  # Return cached analysis

    # 4. Run fresh LLM analysis
    result = await llm_analyze(resume, job_url, ...)

    # 5. Store in cache
    await db.analysis_cache.set(cache_key, result, ttl=7*24*3600)

    return result
```

### 2. AnalysisCache model

**File**: `src/keystone/models/entities.py`

```python
class AnalysisCache(Base):
    __tablename__ = "analysis_cache"
    cache_key: str  # PRIMARY KEY (resume_hash:job_url_hash)
    result_json: dict  # Serialized analysis result
    created_at: datetime
    expires_at: datetime
```

### 3. Cache invalidation

Cache entries expire automatically via `expires_at` check. No manual invalidation needed for MVP. For future: add invalidation when resume is re-uploaded.

---

## Acceptance Criteria

- [ ] Same resume + same JD URL within 7 days → cache hit, no LLM call
- [ ] Different JD URL → fresh analysis
- [ ] Cache entry older than 7 days → treated as cache miss
- [ ] Cache miss → LLM analysis runs normally

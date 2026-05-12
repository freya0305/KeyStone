# Task #17 — Add Industry Field to JD Generator

> Status: pending | Priority: HIGH | Depends on: none

---

## What

Recruiter JD Generator form is missing Industry field. Spec requires: job title, industry, company type, key requirements as inputs. Add industry selector to the form and pass to jd_generator.py.

---

## Deliverables

### 1. Add industry to JD Generator page form

**File**: `apps/web/src/app/(recruiter)/recruiter/jd/page.tsx`

Add industry selector:

```typescript
const INDUSTRIES = [
  "Finance & Accounting",
  "Technology & Software",
  "Healthcare & Medical",
  "Engineering & Manufacturing",
  "Marketing & Communications",
  "Sales & Business Development",
  "Human Resources",
  "Operations & Logistics",
  "Legal & Compliance",
  "Education & Training",
  "Consulting",
  "Other",
]

// Add to form state
const [industry, setIndustry] = useState("")

// Add selector in form
<select
  value={industry}
  onChange={(e) => setIndustry(e.target.value)}
  required
>
  <option value="">Select Industry</option>
  {INDUSTRIES.map((ind) => (
    <option key={ind} value={ind}>{ind}</option>
  ))}
</select>
```

### 2. Pass industry to API

```typescript
const handleSubmit = async () => {
  await fetch("/api/recruiter/jd/generate", {
    method: "POST",
    body: JSON.stringify({
      job_title: title,
      industry, // NEW
      company_type,
      seniority,
      key_requirements,
    }),
  });
};
```

### 3. Update backend to use industry

**File**: `src/keystone/api/jd_generator.py`

```python
@router.post("/recruiter/jd/generate")
async def generate_jd(
    job_title: str,
    industry: str,  # NEW
    company_type: str,
    seniority: str,
    key_requirements: str | None = None,
):
    # Pass industry to JD generation prompt
    jd = await jd_service.generate(
        job_title=job_title,
        industry=industry,
        company_type=company_type,
        seniority=seniority,
        requirements=key_requirements,
    )
    return jd
```

### 4. Update JD generation service

**File**: `src/keystone/services/jd_generator.py`

Include industry in skill frequency lookup:

```python
async def generate(job_title, industry, company_type, seniority, requirements):
    # Get skill frequency data filtered by industry
    skills = await skill_frequency.get_top_skills(
        job_title=job_title,
        industry=industry,  # NEW: filter by industry
        limit=15,
    )
    # Generate JD with industry-calibrated skills
    ...
```

---

## Acceptance Criteria

- [ ] Recruiter JD form has industry dropdown with 11 options
- [ ] Industry is a required field (no empty submission)
- [ ] Industry passed to /api/recruiter/jd/generate
- [ ] Backend JD generation uses industry for skill frequency filtering
- [ ] Generated JD reflects industry-specific skill expectations

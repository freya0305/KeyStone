# JD Generator — Architecture Decision Record

> Last updated: 2026-05-07
> All decisions are final and mutually consistent. Do not contradict.

---

## 1. Skill Normalization

### Scope: Hard Skills Only

Soft skills ("communication", "leadership", "teamwork") are excluded from skill_frequency.
**Reason**: Recruiters input hard skills; soft skills are generic and don't differentiate JDs.

**In scope**: Technical skills, tools, platforms, languages, frameworks, methodologies (e.g. Python, React, Agile, SQL, AWS, Project Management).

**Out of scope**:

- Degrees and certifications ("Bachelor's", "NUS", "NTU", "AWS Certified")
- Personal attributes ("detail-oriented", "self-motivated")
- Soft skills

### Normalization Pipeline (3-step)

**Step 1 — Clean**

```
- lowercase
- strip whitespace
- remove trailing "programming", "development", "skills"
- fix common typos (Sython → Python, etc.)
```

**Step 2 — Map to Standard Taxonomy**
Use LinkedIn Skills Taxonomy as canonical reference (~40K skills).

- Direct lookup: "ReactJS" → "React"
- If no match → enter manual mapping table

**Step 3 — Abbreviation Expansion**
Composite skills with common abbreviations:

```
"ML" → "Machine Learning"
"DL" → "Deep Learning"
"AI" → "Artificial Intelligence"
"PM" → "Project Management" (context-dependent, recruiter intent)
"FS" → "Financial Services" (context-dependent)
```

### Skill Hierarchy

All skill levels are kept as stated. "React" and "JavaScript" are separate skills — do NOT roll up.
Only abbreviations map to canonical forms; do NOT merge related-but-distinct skills.

---

## 2. Frequency Calculation — Section-Weighted

### JD Section Weights

| Section                   | Weight |
| ------------------------- | ------ |
| About the Role / Overview | 0.2    |
| Responsibilities          | 0.5    |
| Requirements / Must Have  | 1.0    |
| Nice to Have / Plus       | 0.3    |
| Benefits / Perks          | 0.05   |

### Formula

```
weighted_frequency = Σ(skill_weight_at_section × count_in_section) / total_JDs
```

### Example

```
Senior Python Engineer (100 JDs):
- Python: Requirements 73 times, Nice to Have 27 times
  = (73 × 1.0 + 27 × 0.3) / 100 = 0.811

- Docker: Requirements 12 times, Nice to Have 88 times
  = (12 × 1.0 + 88 × 0.3) / 100 = 0.384
```

**Result**: Same raw frequency → different weighted frequency → correctly ranked as Required vs Preferred.

---

## 3. JD Quality Filtering

### Deduplication

Duplicate if: same `company` + same `job_title_raw` + posted within 7 days.
Keep the most recent. Archive older.

### Staleness

JDs older than 180 days: weight = 0.5 (still counted, but half weight).
JDs older than 365 days: excluded from skill_frequency, kept in raw_jds for historical analysis.

### Spam Filter

Reject if:

- Word count < 50 (likely not a real JD)
- Contains "work from home" + "no experience needed" + "earn SGD 5000/day" patterns (obvious spam)
- Exact copy of another JD in same batch (dedup)

---

## 4. Cold Start — New Job Titles

### Fallback Strategy

When a `(title, industry, seniority)` tuple has < 30 JDs:

1. **Broaden title**: Try parent role
   - "Senior Software Engineer" → "Software Engineer" (drop seniority)
   - "Staff Engineer" → "Senior Software Engineer"

2. **Broaden industry**: Use "other" industry baseline
   - Tech skills apply across industries

3. **Ask recruiter**: If title has < 5 JDs even after broadening, prompt recruiter to input 3-5 required skills manually.

### Minimum Confidence Threshold

```
if total_JDs_for_tuple < 30:
    display_warning: "Based on {N} JDs — results may vary"
if total_JDs_for_tuple < 5:
    prompt for manual skills input
```

---

## 5. Data Freshness

### Skill_frequency Update Cadence

- **Real-time**: New user_submitted JDs go into raw queue
- **Nightly batch**: ETL runs overnight, rebuilds skill_frequency for affected (title, industry, seniority) tuples
- **Full rebuild**: Every 7 days, full recalculation

### Recency Weighting

Within ETL, JDs are weighted by age:

```
weight = 1.0 if posted < 90 days ago
weight = 0.7 if posted 90-180 days ago
weight = 0.5 if posted 180-365 days ago
weight = excluded if > 365 days
```

---

## 6. Scraping Legal Risk Mitigation

### Strategy: Respect ToS + Rate Limiting

1. **Rate limit**: max 1 request per 5 seconds per domain
2. **robots.txt**: respect `Disallow` rules
3. **User-Agent**: identify as research crawler (not commercial)
4. **IP rotation**: residential proxy pool for MyCareersFuture / JobStreet
5. **No LinkedIn**: Skip LinkedIn — ToS most aggressive, anti-scraping strongest

### Data Source Priority

```
P0 (easiest): MyCareersFuture — government platform, ToS relatively permissive, structured data
P0 (easiest): B2C user-submitted JDs — zero cost, already coming in via product
P1: JobStreet — larger volume, moderate anti-scraping
P2: Company career pages — high quality but scattered, one-off scrapes
Skip: LinkedIn — skip entirely until partnership
```

---

## 7. Consent for User-Submitted JDs

### Consent Text (B2C Signup Flow)

```
"I agree to share the job description URL I submit to help improve KeyStone's
job-market intelligence. Your JD data is used anonymously and never shared with
third parties. [Privacy Policy]"
```

- Consent is part of the main service consent (not separate training opt-in)
- User can delete their submitted JDs at any time
- Submitted JDs labeled `data_source: user_submitted`

---

## 8. JD Quality Feedback Loop

### Tracked Signals

Every generated JD records:

```
jd_id, generated_at, input_params (title, company, company_type, industry, seniority),
skills_used[], skills_from_frequency[]（哪些是market-data-driven）
recruiter_edits: boolean（recruiter改了AI选的技能吗）
saved: boolean
used_in_job_posting: boolean（recruiter真的发布了这个JD吗）
```

### Quality Metric

```
adoption_rate = JDs_saved / JDs_generated
edit_rate = JDs_edited / JDs_saved
usage_rate = JDs_used_in_posting / JDs_saved
```

If adoption_rate < 30%: investigate skill_frequency quality.
If edit_rate > 70%: the skill_frequency mapping may be wrong — recruiter keeps overriding.

---

## 9. GLC / Government Formatting

### Not in skill_frequency — Handled Separately

GLC and statutory board JDs have special requirements:

- NS/NSmen mention (for male candidates)
- Education level format (NUS/NTU/SMU hierarchy awareness)
- CITEX-registered company format
- Public service values language

**How it works**: skill_frequency generates the skills. A separate GLC-specific formatting layer applies after generation to add/modify these sections.

```
skill_frequency output → base JD text
↓
[GLC formatter] → adds NS framing, education hierarchy, public service language
↓
final JD
```

This is NOT part of skill extraction. Separate concern.

---

## 10. Database Schema (Final)

```sql
-- raw_jds: all JD sources
CREATE TABLE raw_jds (
    id UUID PRIMARY KEY,
    source_url TEXT,
    source_platform TEXT, -- mcf, jobstreet, linkedin, direct
    data_source TEXT NOT NULL, -- scraped, user_submitted, partner
    job_title_raw TEXT,
    company TEXT,
    company_type TEXT NOT NULL, -- glc, statutory_board, mnc, startup, banking, fintech, sme, other
    industry TEXT NOT NULL, -- fintech, technology, banking_finance, consulting, government_public, healthcare, retail_consumer, engineering, education, other
    seniority TEXT NOT NULL, -- junior, mid, senior, lead
    raw_text TEXT,
    posted_at TIMESTAMP,
    scraped_at TIMESTAMP DEFAULT NOW(),
    submitted_at TIMESTAMP, -- for user_submitted
    consent_given BOOLEAN DEFAULT FALSE, -- for user_submitted
    is_duplicate BOOLEAN DEFAULT FALSE,
    is_spam BOOLEAN DEFAULT FALSE,
    is_stale BOOLEAN DEFAULT FALSE
);

-- normalized_roles: job title normalization
CREATE TABLE normalized_roles (
    id UUID PRIMARY KEY,
    title_normalized TEXT NOT NULL,
    title_variants TEXT[], -- ARRAY['Software Engineer', 'SWE', 'Software Dev']
    industry TEXT NOT NULL,
    seniority TEXT NOT NULL,
    total_jds INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

-- role_skill_frequency: denormalized read table
CREATE TABLE role_skill_frequency (
    id UUID PRIMARY KEY,
    normalized_role_id UUID REFERENCES normalized_roles(id),
    title_normalized TEXT NOT NULL,
    industry TEXT NOT NULL,
    seniority TEXT NOT NULL,
    company_type TEXT NOT NULL, -- glc, statutory_board, mnc, startup, banking, fintech, sme, other, ANY
    skills_json JSONB NOT NULL, -- [{"skill": "Python", "raw_weighted_freq": 0.811, "required_count": 73, "preferred_count": 27, "total_jds": 100}]
    total_jds_analyzed INT NOT NULL,
    recency_weight FLOAT DEFAULT 1.0,
    last_updated TIMESTAMP DEFAULT NOW(),
    UNIQUE(title_normalized, industry, seniority, company_type)
);

-- jd_generation_logs: feedback loop
CREATE TABLE jd_generation_logs (
    id UUID PRIMARY KEY,
    input_title TEXT,
    input_industry TEXT,
    input_seniority TEXT,
    input_company_type TEXT,
    input_skills_user[], -- user-provided
    skills_from_frequency[], -- AI-selected from DB
    generation_source TEXT NOT NULL, -- skill_frequency, fallback_prompt
    adopted BOOLEAN, -- saved by recruiter
    edited BOOLEAN, -- recruiter changed AI skills
    used_in_posting BOOLEAN, -- actually posted
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## Summary of Decisions

| Decision             | Choice                                                      |
| -------------------- | ----------------------------------------------------------- |
| Skill scope          | Hard skills only (no soft skills, no degrees)               |
| Normalization        | Clean → LinkedIn Taxonomy → abbreviation map                |
| Frequency            | Section-weighted (Requirements=1.0, Nice to Have=0.3, etc.) |
| Deduplication        | Same company + same title + within 7 days                   |
| Staleness            | >180 days = 0.5 weight, >365 days = excluded                |
| Cold start threshold | <30 JDs = warning, <5 JDs = prompt for manual input         |
| Update cadence       | Nightly batch ETL + 7-day full rebuild                      |
| Scraping priority    | MCF P0, user_submitted P0, JobStreet P1, skip LinkedIn      |
| LinkedIn             | SKIP until partnership                                      |
| GLC formatting       | Separate post-processing layer, not in skill extraction     |
| Feedback             | Track adoption/edit/usage rates per generated JD            |

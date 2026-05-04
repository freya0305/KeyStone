# M3 — Job Analysis Engine

> Depends on: M0.1, M0.2, M1.5 (consent), M2.2 (resume parsing)
> Core AI pipeline for JD parsing + four-level match assessment.
> Implements: specs/product.md §Feature 2, specs/technical.md §AI Architecture

---

## M3.1 — JD URL fetcher + text extractor

**What**: Fetch and extract job posting content from URLs. Support MCF, JobStreet, LinkedIn Jobs, company career pages.

**Allowed URL sources** (allowlist — do not fetch arbitrary URLs):
- `mycareersfuture.gov.sg` — MCF jobs
- `jobstreet.com.sg` — JobStreet
- `linkedin.com/jobs` — LinkedIn job postings
- Any HTTPS URL from a corporate domain (user-submitted company career page)

**Technical approach**:
- HTTP fetch with 10s timeout, 1MB response cap
- User-agent: `KeyStoneBot/1.0 (+https://keystone.sg/bot)` — honest about being a bot
- Respect `robots.txt` for MCF and JobStreet (check before fetch)
- HTML→text extraction: BeautifulSoup, target: `<main>`, job description containers, ignore nav/footer
- If structured data present (JSON-LD `JobPosting`): prefer that over HTML extraction

**Cache**: URL → parsed JD JSON, TTL 7 days (per specs/technical.md §Caching)

**Failure handling**: If URL fetch fails for ANY reason (rate limit, robot block, parse failure, 403, redirect loop):
- Return `{success: false, reason: "url_parse_failed"}` — do NOT show error to user
- Frontend silently switches to text-paste input: "We couldn't read this job posting. Paste the text here instead — works just as well." (per Analysis 26 §Voice and Tone)

**Acceptance criteria**:
- MCF job URL returns structured JD in <5 seconds
- LinkedIn job URL returns structured JD
- Invalid URL / blocked URL: silently falls back (no 500, no error modal)
- Fetched URLs cached: second request for same URL returns cached result

**Implements**: specs/product.md §Feature 2 (URL Parsing), specs/mvp-scope.md §Feature 2

---

## M3.2 — JD parsing service (Claude Haiku)

**What**: Extract structured job requirements from JD text (from URL fetch or user paste).

**Input**: raw JD text (any format — URL-extracted HTML dump or user-pasted text)
**Output** (stored as `job_parsed_json`):
```json
{
  "job_title": "...",
  "company_name": "...",
  "company_type_hint": "GLC|MNC|SME|STARTUP|GOVERNMENT",
  "requirements": [
    { "id": "req_1", "text": "...", "category": "technical|experience|education|soft_skill", "years_required": null }
  ],
  "responsibilities": ["..."],
  "benefits": ["..."],
  "seniority_level": "entry|mid|senior|management",
  "industry": "..."
}
```

**Model**: Claude Haiku (structured extraction, no reasoning required)
**Prompt caching**: system prompt with extraction schema — static, cache per session

**NRIC Stage 2**: `assert_no_nric(text)` before sending JD text to Claude (JDs can contain contact names that look like NRICs)

**Acceptance criteria**:
- 20+ test JDs (MCF, JobStreet, company career pages) parsed correctly
- `requirements` array contains all stated requirements (not just the first 5)
- `company_type_hint` matches ground truth for GLCs (DBS, NTUC, Temasek) in test set

**Implements**: specs/product.md §Feature 2 (JD extraction), specs/technical.md §two-tier routing

---

## M3.3 — Company type detection + SG employer database

**What**: Classify employer as GLC / MNC / SME / Startup / Government / Statutory Board. Critical for suggestion tone and conventions.

**Two-pass approach**:

**Pass 1 — Known employer lookup** (zero LLM cost):
- Maintain a curated SG employer database (shipped as JSON config file, updatable without code deploy)
- GLCs: DBS, OCBC, UOB, SingTel, StarHub, M1, NTUC group, Temasek portfolio, Singapore Airlines, SIA Engineering, Changi Airport Group, CapitaLand, Keppel Corp, Sembcorp, SPH, Mediacorp, SMRT, ComfortDelGro, etc.
- Government/Statutory Boards: all Singapore ministries, agencies, and statutory boards
- MNCs: top 100 MNC Singapore operations (Google, Microsoft, Citi, HSBC, J.P. Morgan, McKinsey, etc.)
- Entry: `{company_name, normalized_name, type, notes}`

**Pass 2 — LLM classification** (for unknown employers):
- If not in database: Claude Haiku classifies based on company name + any JD context clues
- Output: `{type, confidence, reasoning}`

**Result cached per company name** (TTL: 90 days — company type is stable)

**Acceptance criteria**:
- DBS → `GLC`, Google Singapore → `MNC`, Ministry of Education → `GOVERNMENT`, Grab → `STARTUP`
- Test set of 50 SG employers: ≥90% accuracy
- Unknown employer classification works (with lower confidence flag)

**Implements**: specs/product.md §Feature 2 (Company Type Detection), specs/technical.md §AI Architecture (SG Intelligence System Prompt)

---

## M3.4 — Four-level match assessment (Claude Sonnet)

**What**: Assess each JD requirement against user's resume and classify as Strong / Transferable / Addressable / Fundamental.

**Input**: `parsed_resume_json` + `job_parsed_json` + `company_type` + `sg_flags`
**Output** (stored as `match_results_json`):
```json
{
  "summary": {
    "strong_count": 8, "transferable_count": 3,
    "addressable_count": 2, "fundamental_count": 1
  },
  "requirements": [
    {
      "id": "req_1",
      "text": "5+ years project management",
      "level": "strong",
      "rationale": "Led 3 cross-functional projects at OCBC; JD-aligned.",
      "sg_context": "GLC values structured project delivery methodology"
    }
  ]
}
```

**Classification definitions** (from specs/product.md §Feature 2):
- `strong`: demonstrably has the skill; resume makes this visible
- `transferable`: has relevant adjacent experience; resume doesn't make connection clear
- `addressable`: can legitimately claim this with reframing of existing experience
- `fundamental`: does not have this — honest assessment; cannot be resolved with resume work alone

**Model**: Claude Sonnet (nuanced judgment, SG context reasoning required)
**SG system prompt**: loaded from config file (updatable without code deploy), includes:
  - GLC entity list
  - MNC SG presence list
  - NS framing rules per vocation
  - Resume photo conventions per company type
  - SG education hierarchy
  - Common SG industry/role vocabulary

**Prompt caching**: SG system prompt is long + static → cache via Anthropic prompt caching API

**Acceptance criteria**:
- Assessment ≤15 seconds (p95) per specs/mvp-scope.md done criteria
- Rationale for every requirement includes: JD-specific reference OR company-type name OR SG market rule
- "Generic rationale" test: rationale must NOT contain ["be more specific", "add quantifiable", "improve your", "consider adding"] — these are failures (per Analysis 28 §Risk 1 Specificity test)
- Test: 10 known resume+JD pairs with ground-truth classifications → ≥80% accuracy

**Implements**: specs/product.md §Feature 2 (Four-level taxonomy), specs/technical.md §AI Architecture

---

## M3.5 — Job analysis endpoint (wire M3.1 + M3.2 + M3.3 + M3.4)

**What**: `POST /api/job-analyses` — accepts JD URL or text + resume_id → runs full pipeline → returns job_analysis_id + streaming progress.

**Flow**:
1. Accept: `{resume_id, jd_url?, jd_text?}` — one of jd_url or jd_text required
2. If `jd_url`: run M3.1 URL fetch → extract text (or use cached result)
3. Run M3.2 JD parsing (Haiku)
4. Run M3.3 company type detection (lookup + Haiku fallback)
5. Run M3.4 four-level match assessment (Sonnet) — most time-consuming
6. Store `job_analyses` record
7. Return result

**Streaming progress** (SSE):
```
data: {"step": "jd_fetch", "message": "Reading the job posting..."}
data: {"step": "jd_parse", "message": "Identified GLC employer type"}
data: {"step": "match_assess", "message": "Comparing your experience to 12 requirements..."}
data: {"step": "ready", "job_analysis_id": "..."}
```

**Free tier tracking**: this is the "second JD" trigger. After first JD (anon or free user): mark `first_jd_consumed = true` in session/user. On next JD: apply 3-suggestion gate.

**Acceptance criteria**:
- End-to-end: resume + JD URL → match results in ≤25 seconds (p95)
- SSE emits at least 3 progress events before final `ready`
- Cached results: same resume + same JD URL → returns cached job_analysis_id immediately
- Free-tier gate: first JD always unlimited; second JD sets gate

**Wire todo**: this endpoint connects M3.1 through M3.4 in sequence.

**Implements**: specs/product.md §Feature 2, specs/technical.md §Caching

---

## M3.6 — Rate limiting

**What**: Per-user + per-IP rate limiting on analysis endpoints. Required before public launch.

**Limits**:
- `POST /api/resumes/upload`: 10/hour per user (or IP for anon)
- `POST /api/job-analyses`: 20/hour per user (or IP for anon)
- SMS OTP send: 3/hour per phone number
- Auth endpoints: 10/hour per IP

**Implementation**: Redis sliding window counter (key: `ratelimit:{endpoint}:{user_id_or_ip}:{window}`)

**Response**: 429 with `{message: "Too many requests. Try again in X minutes.", retry_after: seconds}`

**Acceptance criteria**:
- 11th upload in 1 hour returns 429
- Rate limit resets correctly after window expires
- IP-based limiting works for anon users

**Implements**: specs/technical.md §Infrastructure (security), specs/mvp-scope.md §Technical done criteria


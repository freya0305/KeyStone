# Task #22 — LinkedIn URL Parsing

> Status: pending | Priority: MEDIUM | Depends on: none

---

## What

JD Fetcher currently supports MyCareersFuture and JobStreet. Add LinkedIn job page URL parsing. LinkedIn uses different HTML structure and may require Playwright for dynamic content.

---

## Deliverables

### 1. LinkedIn URL detection

**File**: `src/keystone/services/jd_fetcher.py`

```python
def detect_jd_source(url: str) -> str:
    """Detect which job site the URL is from."""
    if "linkedin.com/jobs/view" in url:
        return "linkedin"
    elif "mycareersfuture.gov.sg" in url:
        return "mycareersfuture"
    elif "jobstreet.com" in url:
        return "jobstreet"
    elif "careers-page.com" in url or "/careers/" in url:
        return "company_careers"
    else:
        return "unknown"
```

### 2. LinkedIn HTML extraction

**File**: `src/keystone/services/jd_fetcher.py`

LinkedIn requires JavaScript rendering for job descriptions. Options:

**Option A: Playwright (preferred for MVP)**

```python
async def fetch_linkedin_jd(url: str) -> dict:
    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, wait_until="networkidle")

        # Extract job title
        title = await page.locator(".topcard__title").text_content()

        # Extract company
        company = await page.locator(".topcard__org-name").text_content()

        # Extract job description (main content)
        description = await page.locator(".description__text").text_content()

        await browser.close()

        return {
            "title": title.strip() if title else None,
            "company": company.strip() if company else None,
            "description": description.strip() if description else None,
            "url": url,
        }
```

**Option B: LinkedIn API (requires OAuth)**
Not recommended for MVP — OAuth flow is complex.

### 3. Update fetch_jd endpoint

**File**: `src/keystone/api/jd_fetcher.py` OR `src/keystone/services/jd_fetcher.py`

```python
async def fetch_jd_from_url(url: str) -> dict:
    source = detect_jd_source(url)

    if source == "linkedin":
        return await fetch_linkedin_jd(url)
    elif source == "mycareersfuture":
        return await fetch_mycareersfuture_jd(url)
    elif source == "jobstreet":
        return await fetch_jobstreet_jd(url)
    elif source == "company_careers":
        return await fetch_generic_careers_jd(url)
    else:
        raise ValueError(f"Unsupported JD URL: {url}")
```

### 4. Fallback: text paste

**File**: `src/keystone/api/jd_fetcher.py`

If LinkedIn parsing fails (rate limited, blocked, etc.), fall back to text paste:

```python
# If Playwright fails or LinkedIn blocks, return error with guidance
raise HTTPException(
    422,
    "Could not parse LinkedIn URL. Please paste the job description text instead."
)
```

### 5. Tests with real LinkedIn job URLs

**File**: `tests/unit/test_jd_fetcher.py`

Add tests:

```python
async def test_linkedin_jd_parsing():
    # Use a real LinkedIn job URL (test environment)
    url = "https://www.linkedin.com/jobs/view/example-job"
    result = await fetch_linkedin_jd(url)

    assert result["title"] is not None
    assert result["company"] is not None
    assert result["description"] is not None
    assert len(result["description"]) > 100
```

---

## Acceptance Criteria

- [ ] LinkedIn job URL detected correctly by detect_jd_source()
- [ ] LinkedIn JD fetched with Playwright (headless Chrome)
- [ ] Title, company, description extracted correctly
- [ ] Graceful fallback if LinkedIn blocks/requires login
- [ ] Error message suggests text paste fallback
- [ ] Unit tests pass with real LinkedIn job URLs

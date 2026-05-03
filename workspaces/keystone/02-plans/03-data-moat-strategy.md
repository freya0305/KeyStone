# KeyStone — Data Moat Strategy

> Phase 02 Plan — 2026-04-29
> Question: How does every UX interaction build the proprietary database that creates technical and data barriers competitors cannot replicate?
> Integrates: Analysis 10, 14, 16, 17; User Flows 04, 05

---

## 1. What Makes a Data Moat

A data moat is not just "having data." It is:

1. **Proprietary**: The data cannot be scraped or purchased. It only exists because users took real actions in the product.
2. **Linked**: The value comes from correlations across tables — suggestion patterns linked to outcomes, employer types linked to suggestion effectiveness.
3. **Compounding**: Every user who joins makes the data more valuable for existing users, and for future users.

**The KeyStone moat is three layers:**

| Layer | What it is | Competitor can replicate? |
|---|---|---|
| **Suggestion Signals** | Accept/Skip/Edit patterns per suggestion type, employer type, role level | No — requires real users in real applications |
| **Outcome Labels** | Application → callback → interview → offer chain per employer/role | No — requires users to log outcomes over time |
| **Employer Fingerprints** | Aggregated patterns: which suggestion types correlate with offers at specific employers | No — requires outcome data + suggestion data linked |

---

## 2. The Suggestion Signals Table

### What Each Row Captures

```sql
suggestion_signals:
  suggestion_id           -- UUID
  user_id                -- UUID
  application_id         -- UUID (nullable for guest)
  suggestion_set_id       -- UUID (groups all suggestions for one JD match)

  -- The action
  action: accept | skip | edit

  -- The content
  original_text          -- text from user's resume
  suggested_text         -- what we proposed
  user_text             -- what user actually shipped (if edited)
  edit_distance         -- computed: levenshtein(suggested_text, user_text)

  -- The context (for segmentation)
  employer_type: GLC | MNC | Startup | Government | SME | Unknown
  role_level: entry | mid | senior | executive
  industry: string
  ns_related: boolean    -- does this suggestion involve NS framing

  -- The suggestion type (for per-type effectiveness)
  suggestion_type: Reframe | Strengthen | Quantify | Reorder | Add | Remove

  -- The match level of the requirement this suggestion addresses
  match_level: strong | transferable | addressable | fundamental

  created_at
  training_consent: boolean  -- from consent toggle 2
```

### What The Data Enables

**Per-suggestion-type effectiveness by segment:**
```python
# "Quantify" suggestions at GLC employers: 72% accept rate
# "Quantify" suggestions at MNC employers: 61% accept rate
# "Add" suggestions at any employer: 43% accept rate
# "Reorder" suggestions: 89% accept rate (low signal — almost always accepted)
```

**Edit distance as calibration:**
- Low edit distance (0–5): Our suggestion was almost exactly right → high quality signal
- Medium edit distance (6–20): User made meaningful adjustments → we inspired correct direction
- High edit distance (21+): Our suggestion was wrong direction → negative signal

**Time-to-decide as confidence:**
- Fast decisions (<3s): High confidence suggestion
- Slow decisions (10s+): User needed to think → suggestion requires more context in rationale

### Why This Cannot Be Scraped

A competitor can scrape LinkedIn for resume examples. A competitor can use ChatGPT to generate "typical suggestions." What they cannot get:
- Which suggestions were actually accepted vs skipped in real job applications
- How edit distance correlates with outcome quality
- Which suggestion types work at which employer types in Singapore

---

## 3. The Outcome Chain

### The Application → Offer Chain

```
Application created (suggestion_set_id linked)
         ↓
User logs: Applied (date)
         ↓
User logs: Got a response (date, response_type)
         ↓
User logs: Advanced to Phone Screen / Interview R1 / R2 / ...
         ↓
User logs: Offer received (date)
         ↓
User logs: Success factors (what helped — includes resume tailoring?)
```

### The Causal Link

The `suggestion_set_id` on the application is the critical linkage.

```
suggestion_set_id = uuid-abc123
  └── suggestion_signals (15 rows)
        ├── accept: 12
        ├── skip: 2
        └── edit: 1 (edit_distance: 8)

  └── application
        └── outcome: offer_received
        └── employer: DBS Bank
        └── role: Operations Manager
        └── time_to_offer: 23 days
```

This means: For DBS Bank / Operations Manager, the suggestion pattern that preceded an offer was: 12 accepts, 2 skips, 1 minor edit.

**This is what VMock cannot have.** VMock has outcome data OR suggestion data. KeyStone has them linked.

### Outcome Types and Their Signal Value

| Outcome | Signal Value | Frequency | How to Capture |
|---|---|---|---|
| Applied | Baseline | Every user | Post-download modal |
| Got a response | High | ~25% of applications | Batch update |
| Advanced (stage) | Very high | ~15% of applications | Stage progression |
| Offer received | Maximum | ~3–5% of applications | Offer celebration flow |
| Rejection (with stage) | High | ~20% of applications | Batch update |
| No response (30d) | Low | ~50% of applications | Auto-close |

---

## 4. The Employer Fingerprints Table (Derived)

Not a user-facing table — a derived data asset computed from the outcome chain.

```python
EmployerFingerprint:
  employer: str                    # "DBS Bank"
  employer_type: enum             # GLC | MNC | Startup | Government | SME

  cohort_stats:
    total_applications: int
    applications_with_outcome: int
    callback_rate: float           # applications with response / total
    stage_dropoff: dict           # {stage: dropoff_rate}
    offer_rate: float             # offers / applications_with_outcome

  suggestion_patterns:
    common_gaps: list[str]        # most frequent fundamental gaps
    effective_suggestion_types: dict  # {type: accept_rate}
    avg_accept_rate: float

  last_updated: datetime
```

**What this enables**:
- "DBS expects MAS regulatory licensing — this is a Fundamental gap we won't fake around"
- "Operations roles at GLCs: 72% of successful applicants had quantified outcomes in their bullets"
- "This employer type has 0% offer rate for applications without tailored resumes (n=47)"

The third example is the killer insight: proof that tailoring works, backed by real outcome data.

---

## 5. The Suggestion → Outcome Correlation Engine

### The Core Query

```sql
-- Which suggestion types correlate with offers at GLC employers?
SELECT
  ss.suggestion_type,
  COUNT(*) as total_count,
  SUM(CASE WHEN a.final_outcome = 'offer' THEN 1 ELSE 0 END) as offers,
  AVG(CASE WHEN a.final_outcome = 'offer' THEN 1.0 ELSE 0 END) as offer_rate
FROM suggestion_signals ss
JOIN applications a ON ss.application_id = a.id
JOIN employer_fingerprints ef ON a.employer = ef.employer
WHERE
  ef.employer_type = 'GLC'
  AND ss.action = 'accept'
  AND ss.training_consent = true
GROUP BY ss.suggestion_type
ORDER BY offer_rate DESC;
```

### What The Correlation Engine Produces

**Per employer, per role type:**
- Which suggestion TYPE has the highest offer-correlated accept rate
- Which suggestion TYPE users skip most often (and whether skips correlate with no-offer)
- Whether "Quantify" suggestions correlate with offers at specific employer types

**Per user segment:**
- Fresh graduates: Which suggestion types work best? (NS framing, quantified outcomes)
- Mid-career: Which suggestion types work best? (skill translation, relevance framing)
- PMET: Which suggestion types work best? (authority signals, industry language)

**For the Insights page (user-facing):**
```
Where to focus:
You skip "Quantify outcomes" suggestions 60% of the time,
but accepted ones correlate with 2.3× higher response rates.
Worth revisiting.
```

This is the data moat surfaced as user value.

---

## 6. How The UX Collects Each Signal

### Signal Collection Map

| UX Moment | Signal Captured | Table |
|---|---|---|
| User accepts suggestion | action=accept, suggestion_type, match_level, employer_type | suggestion_signals |
| User skips suggestion | action=skip, suggestion_type, match_level | suggestion_signals |
| User edits suggestion | action=edit, edit_distance, user_text, suggestion_type | suggestion_signals |
| User reads rationale | implicit: dwell time before decision | (analytics only) |
| User downloads resume | application.created, suggestion_set_id, employer | applications |
| User clicks "Yes — track" | opted_in=true | applications |
| User clicks "Just downloading" | opted_in=false (friction signal) | applications |
| User marks "Got a response" | stage=response, response_type | application_stages |
| User marks "Still no news" | stage=no_news | application_stages |
| User marks "Rejected" | stage=rejected, rejection_stage | application_stages |
| User advances a stage | stage_advanced, new_stage | application_stages |
| User receives offer | final_outcome=offer, success_factors[] | applications |
| User completes batch update | session_duration, apps_processed | batch_update_sessions |

### The Anti-Gaming Rules

**Preventing fake signal:**
1. **One account per user** — email verification required
2. **Training consent independent** — even if consent is off, outcomes are still tracked for the user's own dashboard; only training use is affected
3. **Edit distance floor** — an edit of 1 character is noise; minimum 3 characters to count as meaningful edit
4. **Stage progression minimum times** — "Applied to offer" in <7 days is suspicious (hiring processes take longer); flag for review

---

## 7. The Privacy/Utility Balance

### PDPA-Compliant Data Architecture

**Three-stage consent:**
1. Service operation (required for account)
2. AI improvement (default ON, can turn off)
3. Outcome correlation (default ON, can turn off)

**What each consent level means:**

| Consent | What Happens | What Doesn't Happen |
|---|---|---|
| All on | Signals feed training corpus, outcome correlations power suggestions, user sees own data | — |
| AI improvement off | No signals in training corpus | Suggestions still personalized, outcome tracking still works |
| Outcome correlation off | Suggestion patterns not linked to outcomes | User still sees own outcome stages |

**NRIC never enters the model context.** Masked at upload: `S****1234A`.

**Soft-delete with audit retention:**
- User deletes account: personal data purged, outcome data anonymized and retained for aggregate analysis
- Application records retain anonymized employer/role for employer fingerprint computation

---

## 8. Compounding Effects Over Time

### Month 1: Empty Corpus
- Suggestions are generic (based on prompt engineering + general SG context)
- Outcomes tracked but no correlation possible yet

### Month 3: First Patterns
- 500 applications with outcomes
- Early signal: "Quantify suggestions have 2× higher accept rate at GLCs"
- Suggestion engine updates: weight toward quantification at GLC match

### Month 6: Meaningful Fingerprints
- 2,000 applications, ~400 with outcomes
- DBS Bank fingerprint: n=23 applications, callback rate 34%, offer rate 12%
- Early employer-specific suggestions: "DBS operations roles: quantify programme scope over project scope"

### Month 12: Durable Moat
- 10,000+ applications, 1,500+ with outcomes across 200+ employers
- Suggestion engine: per-employer-type tuning
- Insights: "Users with 80%+ accept rate on Quantify suggestions have 3.1× higher offer rate at GLCs"
- B2B: "Students whose applications used KeyStone had 28% higher offer rate than cohort average"

### Why This Cannot Be Replicated

A competitor entering Month 12 would need:
- 12+ months of user acquisition
- Users willing to log real outcomes
- Suggestion-outcome linkage to train on
- Employer fingerprints requiring 200+ applications per employer

The moat compounds because the data is only generated through real use. There is no shortcut.

---

## 9. The Data Moat Metrics (What to Track from Day 1)

| Metric | Target | Why |
|---|---|---|
| Suggestion accept rate | 65–75% | Baseline quality indicator |
| Suggestion skip rate | 15–25% | Healthy — honest signal |
| Edit rate | 8–12% | High-value signal; users are engaging |
| Mean edit distance | 8–15 chars | "Almost right" is the sweet spot |
| Application → outcome logging rate | 25–35% | Target from pull-based system |
| Outcome → offer logging rate | 8–12% | Of applications that get response |
| Batch update completion rate | 70–80% | Of sessions started |
| Batch update avg duration | <60s for 20 apps | UX health |
| Training consent rate | >80% | Default on; most users stay on |
| Per-employer outcome coverage | >20 outcomes per employer | Minimum for fingerprint reliability |

---

## 10. What This Plan Does NOT Cover

- Database schema details (deferred to M0.2)
- Redis key design for per-user cost tracking (deferred to M0.5)
-具体的API endpoint设计 (deferred to M1–M6)
- Employer fingerprint computation pipeline (deferred to Phase 2)

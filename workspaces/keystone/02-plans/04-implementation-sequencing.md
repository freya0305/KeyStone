# KeyStone — Implementation Sequencing

> Phase 02 Plan — 2026-04-29
> Question: What order do we build in, and why?
> Principles: Moat-first (build the feedback loop before scaling), Validate before investing

---

## 1. The Sequencing Logic

**Rule 1: Build the loop before building the funnel.**

The most important product is not the landing page or the onboarding flow. It is the suggestion → outcome loop. Every build decision should ask: does this help the loop close faster or collect better signal?

**Rule 2: Validate the core loop before the interview prep module.**

Interview prep (Phase 2) depends on the same JD context already in the system. It doesn't make sense to invest in interview prep until the resume → application loop is validated.

**Rule 3: The moat is empty at launch. That's fine. But every feature should make the moat grow faster.**

---

## 2. Build Order

### Phase 0 — Foundation (M0)
**Goal**: Project scaffold, DB schema, auth, logging infrastructure

1. **M0.1** — Backend framework decision + scaffold
   - FastAPI vs Kailash Nexus evaluation
   - Entry point, router structure, dependency injection, env config
   - `docker-compose.yml` for local dev

2. **M0.2** — Database schema + migrations
   - All tables from `suggestion_signals` through `b2b_aggregate_reports`
   - PostgreSQL RLS policies (B2B ready)
   - Alembic setup

3. **M0.3** — Frontend scaffold
   - Next.js 14, TypeScript strict
   - Tailwind with design tokens (from Analysis 26)
   - shadcn/ui installed

4. **M0.4** — CI/CD
   - pytest + mypy + ruff (backend)
   - tsc --noEmit + ESLint + next build (frontend)

5. **M0.5** — Logging + token monitoring
   - structlog on every Claude API call
   - Redis counter per user/month
   - `/admin/costs` endpoint

### Phase 1A — Core Loop MVP (Months 1–2)
**Goal**: First users experience the full suggestion → outcome loop

```
User lands → uploads resume → pastes JD URL → sees match → reviews suggestions → downloads resume → logs outcome
```

**Priority order within 1A:**

1. **JD URL Parser** (P0)
   - MCF URL parsing
   - JobStreet URL parsing
   - Generic URL + free-text fallback
   - Employer type detection (GLC / MNC / Startup / Government / SME)

2. **Resume Uploader + NRIC Masking** (P0)
   - PDF / DOCX / plain text
   - Three-stage mask: upload → re-scan → AI input
   - Never full NRIC in context

3. **Four-Level Match Assessment** (P0)
   - Strong / Transferable / Addressable / Fundamental
   - Match panel with collapsible sections

4. **Suggestion Engine** (P0)
   - Six suggestion types: Reframe / Strengthen / Quantify / Reorder / Add / Remove
   - Rationale: 1 sentence, cites JD requirement OR company type
   - No suggestion generated when Strong match

5. **Suggestion Review Flow** (P0)
   - Suggestion card with Accept / Skip / Edit
   - Equal visual weight on all three
   - Keyboard shortcuts
   - Immediate DB write on every action

6. **Resume Preview** (P0)
   - Three-view toggle: Tailored / Original / Diff
   - Inline diff with strikethrough + green addition

7. **Resume Export** (P0)
   - PDF + DOCX generation
   - Filename suggestion: `[Name]_[Role]_[Employer].pdf`
   - Post-download outcome modal (NOT blocking)

8. **Application Creation** (P0)
   - suggestion_set_id linkage is the critical path
   - Post-download modal → Application created
   - Manual creation form for non-KeyStone applications

9. **PDPA Consent** (P0)
   - Six-type independent consent
   - Plain-language explanations
   - Toggle defaults: 1–4 on, 5–6 off

10. **Guest Flow** (P0)
    - `/try` path, no auth required
    - Gate at suggestion #4 on subsequent JDs
    - Watermarked export

### Phase 1B — Outcome Tracking MVP
**Goal**: Close the feedback loop — every application has an outcome record

11. **Stage Model** (P0)
    - Applied → Response → Screening → Interview R1..RN → Decision
    - Multi-round support (non-negotiable per Analysis 16)

12. **Batch Quick-Update** (P0)
    - One-at-a-time card stack
    - "Still no news" as default 1-tap action
    - "Mark all remaining" escape hatch
    - Target: 30 apps in <3 minutes

13. **Pull-Based Nudge System** (P0)
    - Nudge-eligible: 7/14/21 days with no activity
    - Dashboard banner when ≥3 nudge-eligible
    - Weekly digest email (max 1/week, only if no login that week)

14. **Auto-Close + Correction** (P1)
    - 30-day silence → auto_close_no_response
    - Toast on next login: "Update if needed"
    - Correction rate metric: if >20% corrected, window is too short

15. **Insights Dashboard** (P1)
    - Response rate, per-stage pass rate
    - Suggestion accept rate
    - Appears only after ≥3 applications with ≥1 outcome

### Phase 2 — Interview Prep (Months 3–6)
**Goal**: Extend LTV, close the interview stage of the loop

16. **JD-Specific Question Generation** (P0)
    - 8–10 questions from the JD already in the system
    - Categorized: competency / motivation / behavioral / situational
    - GLC competency framework mapping (Leadership, Integrity, etc.)

17. **Story Input + STAR Structuring** (P0)
    - Coach, not generator — ask questions, structure what user writes
    - Never auto-fill specifics user didn't provide
    - Flag if generated answer contains unprovided specifics

18. **Practice Answer Evaluation** (P0)
    - Text-based, Haiku for cost control
    - Evaluates: structural completeness, JD relevance, specificity, conciseness

19. **Callback-Triggered Entry** (P0)
    - When user marks "Got a response" → surface interview prep for that job
    - High-motivation moment

20. **Story Bank** (P1)
    - Persistent across applications
    - Reuse stories across different JDs
    - Maps stories to relevant questions automatically

### Phase 3 — Scale + B2B (Months 6–12)
**Goal**: Leverage the moat, unlock institutional revenue

21. **Suggestion → Outcome Correlation Engine** (P0)
    - Per employer, per role type
    - Which suggestion types correlate with offers
    - "Where to focus" insights generation

22. **Employer Fingerprints** (P1)
    - Aggregated from outcome chain
    - Surface in suggestion rationale as citations
    - "DBS hires 60% of Operations roles internally [source]"

23. **B2B Aggregate Dashboard** (P0)
    - Institution-level: cohort callback rates, common fundamental gaps
    - Per-student view for career advisors

24. **University SSO** (P0)
    - SAML/OIDC for NUS, NTU, SMU, SIT career portals
    - B2B consent model (institution vs individual)

---

## 3. What NOT to Build in MVP

| Feature | Why Not MVP |
|---|---|---|
| Voice input for interview prep | Phase 2 — text-first, validate before voice investment |
| LinkedIn auto-import | OAuth scope review needed; defer to Phase 2 |
| Cover letter generator | Phase 2 — resume is core, cover letter is secondary |
| Job board / job discovery | EAA legal risk; user brings the JD |
| In-app messaging / chat support | Opens support load before revenue; email only |
| Public profile / share resume | Out of scope — KeyStone tailors privately |

---

## 4. The One-Feature Decision Framework

When evaluating whether to add a feature, ask:

1. **Does it close the suggestion → outcome loop faster?**
   If yes: build it.
2. **Does it make the user more likely to log an outcome?**
   If yes: build it.
3. **Does it make the data more linkable (suggestion_set_id → outcome)?**
   If yes: build it.
4. **Does it expand the loop (new interaction type → new signal)?**
   If yes: evaluate carefully.

If none of the above, it can wait.

---

## 5. Moat Priming at Launch

The first 100 users are disproportionately valuable — they establish the initial signal quality. Design for this:

**Launch week priority:**
- Every early user gets full Pro features (no gate) in exchange for outcome logging participation
- Onboarding explicitly frames outcome logging as collaborative ("you're helping build something")
- First outcome logged → personal thank-you email from founders

**First-month priority:**
- Weekly digest to all users with nudge-eligible applications
- Personal outreach to users with 0 outcomes logged after 14 days
- First offer logged → case study (with permission)

---

## 6. Build vs Buy Decisions

| Component | Decision | Rationale |
|---|---|---|
| PDF generation | Buy (Puppeteer/Playwright) | Resume PDF must match preview exactly; complexity not worth building |
| DOCX generation | Buy (python-docx) | Resume formatting is complex; focus engineering on suggestions |
| URL parsing | Build (Scraping + NLP) | Core to moat; MCF/JobStreet have specific structures worth building for |
| LLM inference | API (Claude) | Haiku for extraction, Sonnet for analysis; no fine-tune at MVP |
| Auth | Clerk | Google OAuth + email; handles SSO for B2B later |
| Payments | Stripe | SGD billing, local payment methods, subscription management |
| Email | Resend or Postmark | Transactional email with consent management |
| Hosting | AWS ap-southeast-1 | PDPA compliance, Singapore region |

---

## 7. The 60-30-10 Heuristic for MVP Scope

For each feature, ask: is this:

- **60% feature**: The minimum version that delivers the core value (e.g., "accept a suggestion")
- **30% feature**: The version that makes it feel polished (e.g., "undo accept within 30 seconds")
- **10% feature**: The version that makes it excellent (e.g., "keyboard shortcuts for power users")

**MVP ships the 60% version of everything, not the 60% version of some things and 100% of others.**

Example — suggestion cards:
- 60%: Accept / Skip / Edit buttons, rationale text, card renders correctly
- 30%: Undo accept in toast, position indicator, edit distance captured
- 10%: Keyboard shortcuts, confidence calibration markers, per-suggestion feedback prompt

Ship 60% + 30%, hold 10% for post-MVP.

---

## 8. What This Plan Does NOT Cover

- Specific API endpoint design (deferred to M1–M6)
- Third-party API integration specs (deferred to individual M-tasks)
- Deployment infrastructure details (deferred to M0)
- Fine-tuning strategy for the suggestion engine (deferred to Month 6 when corpus is mature)

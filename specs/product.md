# Product Spec — KeyStone

> Last updated: 2026-04-29 (Phase 01 Analysis)

---

## Core Value Proposition

**Sharpest B2C pitch**: "Paste any Singapore job posting. KeyStone rewrites your resume for that exact role in under a minute — tuned for the way SG hiring managers actually read resumes."

**Sharpest B2B pitch (university buyer)**: "KeyStone gives every student in your career centre a personal resume coach for every application — so your team can focus on the 5% of students who need real intervention, not the 95% who need editing."

**Landing page headline**: "The resume tailoring tool built for the Singapore job market."
**Subhead**: "Paste a job. Get a resume tuned for that role, that company, this market. In under a minute."
**CTA**: "Try it on one job — free." (No signup gate for first use)

### What Users Pay For (Ranked by Importance)
1. **Job-specific line-by-line revision suggestions** — this is the product. Everything else supports it.
2. **Singapore-specific intelligence** — trust signal and credibility wedge; earns first-session confidence
3. **URL parsing / job extraction** — removes friction vs manual copy-paste
4. **Four-level match assessment** — helps users pre-qualify which jobs are worth full tailoring effort
5. **Application tracking / response rate / per-stage pass rate** — retention feature, not acquisition feature; cold-start until Month 3+

---

## Feature Specifications

### Feature 1: Resume Upload + Analysis

**Input**: PDF, Word (.docx), plain text
**Processing time**: ≤10 seconds target
**Output**:
- Overall strengths (2–4 bullet points)
- Weaknesses / gaps (2–4 bullet points)
- Singapore-specific flags:
  - NRIC detected → removal recommendation (one-time)
  - Professional photo present + company type → include/exclude advice
  - NS section detected → quality assessment (for male graduates)
  - Education format → SG conventions check

**Singapore intelligence rules (static, v1)**:
- NRIC pattern: `[STFGstfgMN]\d{7}[A-Za-z]` (S/T/F/G for citizens, M/N for permanent residents, FIN for foreigners)
- FIN pattern: `[KLPkpmn]\d{7}[A-Za-z]` (Foreign Identification Number)
- Photo: include recommendation for GLCs and statutory boards; exclude for MNCs and international firms
- NS framing: convert vocation-specific roles to civilian-equivalent competencies (leadership, logistics, operations, communications)
- Education: Singapore degree hierarchy awareness (NUS/NTU/SMU > SIT/SUTD/SUSS for certain employer types)

**PMET-specific intelligence (highest willingness-to-pay segment — must not be underserved)**:
- Career pivot narrative: reframe 15-20 year tenure in one industry for a different sector (e.g., "18 years DBS operations → how to position for fintech startup roles")
- Age-neutral language: remove implicit age signals (graduation years, early-career role descriptions that anchor seniority level)
- Seniority repositioning: adjust language for users targeting roles above or below their previous level
- Contract vs permanent framing: adjust expectations language for users entering the contract/freelance market for the first time

Note: NRIC detection and NS framing serve fresh grads (lower WTP). PMET intelligence serves the highest-WTP segment. Both must be scoped in MVP; PMET features are the stronger conversion driver for Pro.

**Caching**: Resume analysis cached by content hash (SHA-256 minimum). Re-running same resume against different jobs does NOT re-run full resume analysis.

---

### Feature 2: Job Match Assessment (Four-Level)

**Input**: Job posting URL (MCF, JobStreet, LinkedIn, company career pages) OR pasted JD text
**URL Parsing**: HTML extraction of job title, company name, requirements, responsibilities. Fallback to user-pasted text if parsing fails.
**Company Type Detection**: GLC vs MNC vs SME vs Startup vs Government/Statutory Board — drives suggestion tone and conventions

**Four-level taxonomy**:

| Level | Colour | Definition |
|-------|--------|-----------|
| Strong match | Green | User demonstrably has the skill/experience; resume makes this visible |
| Transferable | Amber | User has relevant adjacent experience; resume does not make the connection clear |
| Addressable gap | Orange | User can legitimately claim this with reframing of existing experience |
| Fundamental gap | Red | User does not have this; honest assessment; cannot be resolved with resume work alone |

**Output**: Per-requirement classification with one-sentence rationale for each level assignment.

---

### Feature 3: Line-by-Line Revision Suggestions (Core Feature)

**Trigger**: After job match assessment is completed
**Scope**: Existing resume bullets and sections that are Transferable or Addressable (NOT Fundamental gaps — those are flagged separately)
**Format per suggestion**:
- Original text (highlight in context)
- Suggested rewrite
- Rationale (one sentence, referencing the specific JD requirement and company type)

**Example**:
> **Original**: "Responsible for managing a team"
> **Suggested**: "Led an 8-person cross-functional team across 3 business units, improving reporting efficiency by 30%"
> **Because**: "This GLC values quantified team leadership; your current phrasing is vague and undersells the scale."

**User interaction**: Accept / Reject / Modify (inline edit of suggested text)
**Output**: Modified resume downloadable as PDF and/or DOCX, with accepted suggestions incorporated

**Free tier limit**: First job analysis: unlimited suggestions (full value demonstration). Subsequent jobs: first 3 suggestions visible; rest gated behind Pro.
**Pro**: Unlimited suggestions for all jobs.

**Anti-abuse (MUST — before launch)**: Phone number (SG mobile) verification required at signup. One phone number = one account. Prevents multi-account abuse of the unlimited-first-analysis gate. SMS verification cost ~SGD 0.05/user.

**Google OAuth enforcement**: Phone verification is required BEFORE the free tier entitlement is activated. Google OAuth bypasses email/password signup but NOT phone verification. Users who sign up via Google OAuth must complete phone verification before accessing the free tier. This prevents Google OAuth from being used to circumvent the one-phone-one-account rule.

**Batch mode (MVP+)**: Users applying to multiple jobs simultaneously can paste up to 5 job URLs against one resume — system generates 5 tailored versions in one session. Addresses the "spray-and-pray" application behavior that is the SG job seeker reality. Gate batch mode behind Pro.

**Learning loop (MUST architect from Day 1)**:
- Log every Accept/Reject/Modify signal with context: suggestion_id, user_segment, company_type, role_level, industry, outcome (linked to application if tracked)
- Purpose: future model fine-tuning on real SG user preference signal
- **PDPA training consent — B2C only**: Explicit separate consent at signup ("your feedback improves suggestions for all users"). B2B institutional (university) user signals are NEVER used for model training — only for aggregate dashboards. This separation is a hard architectural requirement.
- Pre-launch data sources: recruitment agency partnership data (historical placements) + design partner cohort (50-100 users, full consent) to bootstrap calibration before public launch

---

### Feature 4: Application Outcome Tracking

**Terminology correction**: SG job seekers receive responses via email, LinkedIn messages, phone, and SMS — not only phone calls. All references use "response rate" (回复率) and "per-stage pass rate" (各阶段通过率), not "callback rate".

**Data model — multi-stage (replaces simple status enum)**:

Each application record contains a `stages` array capturing every stage transition. SG professional roles typically have 2–4 interview rounds.

```
application_record {
  job_id, resume_version_id, applied_date
  status: applied | responded | screening | interviewing | decided | withdrawn
  
  stages: [
    {
      stage_type: response | screening | interview | final | offer | rejection | withdrawal
      round_number: null | 1 | 2 | 3 | 4 | 5
      date
      format: email | phone | video | in-person | assessment_centre | panel | technical | case
      outcome: passed | failed | pending | withdrawn
      notes (optional)
    }
  ]
  
  final_outcome: no_response | rejected | offer_received | withdrawn
}
```

**Why stage-based (not status enum)**: "Interview scheduled" conflates Round 1 with Round 4. Per-stage pass rates (e.g., R1→R2 conversion) are more predictive than overall response rate and are KeyStone's unique data asset. Analysis 16 has the full rationale.

**Dashboard metrics (stage-aware)**:
- Personal response rate: applications with any response / total logged (target: ≥5 applications before display)
- Per-stage pass rates: response → screen → R1 → R2 → final → offer
- Applications by stage, by month
- Job-match-level distribution (are Strong match applications more likely to reach R2+?)
- Trend line over time
- Benchmark comparison only after 15+ applications

**Outcome logging rate (realistic)**: 3–6% baseline (Teal/LinkedIn benchmark). Target after email reminders: 15–22%. Design treats 3–6% as baseline and optimises upward.

**UX framing (critical)**: Position as "your personal job search dashboard" — user utility first, not data collection. Per-stage breakdown surfaces insights users can act on ("you're getting to interviews but losing at R2 — here's what to prepare differently").

**Outcome logging incentive strategy — pull-based, not push-based**:

SG job seekers frequently mass-apply (20–50+ simultaneous applications). Per-application email sequences (Day 3 / Day 10 / Day 21 × N applications) cause inbox explosion, unsubscribes, and spam classification. The correct strategy: make logging low-friction at natural product re-entry points, not push reminders for each application.

**Primary mechanisms (MVP)**:

1. **Download-triggered capture** (highest conversion — always first): at resume download, prompt "Are you submitting this to [Company]?" → creates application record in one click. User is already in the product, already engaged.

2. **Batch quick-update UI — smart-default model** (pull, not push): when user returns to KeyStone, a persistent banner surfaces pending applications. **"No news" is the assumed state — no action required to confirm it.** The interface only asks users to flag exceptions (something happened). Design model:
   - Show grouped pending applications ("8 applications from last week — anything to report?")
   - Single primary action: [Nothing new — clear all] closes the batch with one click
   - Secondary action: [Something happened →] opens a mini-form for that specific application
   - User with 30 pending applications can complete the check-in in one click if nothing happened
   - Applications where something positive happened are the user's natural motivation to open and update

3. **Pre-prep interstitial**: when user enters Interview Preparation for any application, prompt to update status of other pending applications first: "You have 4 other pending applications — update them while you're here?" This captures the highest-motivation moment (user just got an interview invite, is already in a positive state).

4. **Gamification — tracking completeness score**: visible "tracking completeness: 72%" indicator showing user's ratio of logged vs unlogged applications, with percentile comparison ("top 30% of users"). Framed as "more complete tracking = more accurate insights for you", not "help us collect data".

5. **Single weekly digest email** (one email max per week, NOT per application): sent only if user has ≥5 pending applications AND did not log in that week. Subject: "Your job search this week". Contains count of pending applications + one deep link to the batch update screen. Maximum 1 email per 7 days regardless of application count. JWT-signed deep link opens batch update interface directly (no login required). SPF/DKIM/DMARC required before launch.

6. **Auto-close**: applications with no activity for 30 days are silently marked "no response (inferred)" and moved out of the active queue. At next login, a toast notification: "7 applications older than 30 days were marked 'no response' — [review and correct]". This keeps the active list clean without constant prompting.

**Explicitly NOT used**:
- Per-application email sequences (Day 3 / Day 10 / Day 21 per application) — causes inbox explosion for mass-applicants
- Any mechanism sending more than 1 email per week per user

**Phase 2**: Web Push API opt-in (Chrome/desktop, ~70% coverage). Supplement to in-product mechanisms.
**Phase 3**: Gmail/Outlook OAuth email parsing — automatically detect MCF/JobStreet/LinkedIn notification emails and update application status. Could increase logging rate from 20–25% to 45–60%.

**Cold-start mitigation**:
- Application record created at resume download (removes retroactive memory burden)
- Minimum 5 applications logged before response rate displayed (avoid 0% or 100% on small N)
- Dashboard unlocks incrementally: each logged application reveals more analytics (gamified completion)

**PDPA training separation**: B2B university student outcome data contributes ONLY to institutional aggregate dashboards. It is never part of the model training pipeline. Only B2C users with explicit training consent contribute signals to fine-tuning.

**B2B aggregate view** (university career centre dashboard):
- Cohort-level response rates and per-stage pass rates by industry, role level, application date
- Students with 0 applications (not using the tool → advisor outreach)
- Aggregate gap types (most common Fundamental gaps across the cohort)
- Privacy: individual student data not visible to advisors; only aggregate + anonymised

---

## Feature 5: Interview Preparation Module (Phase 2 — Post-MVP)

> Highest-priority next feature by pain matrix analysis (Score 80/125). Approved for Phase 2 design.

### Why Build This

From pain prioritisation analysis (acuity × frequency × coverage gap):
- "No JD-specific interview preparation" scores 80/125 — tied for 2nd highest underserved pain
- Directly extends from the existing tailoring workflow (JD context already loaded)
- Adds 3–5 high-value touchpoints per job search; extends subscription window by 4–6 weeks
- **No existing tool does the full combination**: JD-specific question generation + personal story synthesis + iterative practice with evaluation + SG company-type intelligence

### What No Competitor Does

| Tool | JD-Anchored Questions | Personal Story Input | Practice Loop | SG Company Type |
|------|-----------------------|---------------------|---------------|----------------|
| Glassdoor Q&A | No — crowd-sourced | No | No | No |
| ChatGPT | If prompted well | Partial | No | No |
| VMock STAR Coach | No | No | Delivery only | No |
| LinkedIn Interview Prep | No | No | No | No |
| Big Interview | Partial | Template-based | Yes (generic) | No |
| **KeyStone (proposed)** | **Yes** | **Yes (own stories)** | **Yes + JD evaluation** | **Yes** |

### Module Design

**Entry point**: Triggered at each interview stage transition in the application tracker — not only at first response. JD context is already loaded; no new input required.

Stage-specific triggers:
- Response received → prompt for screening/phone prep
- Phone screen passed → prompt for Round 1 prep
- Round N passed → prompt for Round N+1 prep (company-type adapted — e.g., GLC panel, startup culture-fit)
- Final round → dedicated senior-level / executive prep

This multiplies the interview prep engagement: a candidate with 4 interview rounds generates 4 prep sessions vs 1 under the old model. See Analysis 16 for LTV recalculation.

**Step 1 — Story Bank Input**
- Prompted mini-story collection: "Tell us about a time you led a team (2–3 sentences)," "Describe your biggest project (2–3 sentences)" etc.
- NS-specific prompts for male graduates: "Describe your NS role — what did you manage, how many people, what was the result?"
- Free-text input also accepted; system structures unstructured input into STAR components
- Story bank persists across job applications; user edits/expands over time

**Step 2 — Question Generation**
- Reads the JD (already parsed) and company type (already classified)
- Generates 5–8 highest-probability questions for this role/company type
- SG-specific question sets:
  - GLC: competency-based questions (Leadership, Integrity, Customer Focus, Innovation) per typical GLC framework
  - Civil service / statutory board: panel format, current affairs awareness, public service values
  - MNC: behavioural deep-dives, cross-functional examples, global context
  - Startup: practical assessment culture, culture-fit questions, "why this company specifically"
- Question confidence score: "This question is highly likely (asked in >60% of similar roles)" vs "possible (20–40% of similar roles)"

**Step 3 — Reference Answer Synthesis**
- Maps user's stories to each question: "For 'tell me about a leadership challenge', your NS section about platoon command is the right source material"
- Generates a STAR-structured reference answer drawing on the user's own stories
- **NOT writing the answer for the user** — synthesising and structuring THEIR material
- SG-specific framing adjustments: "For a GLC role, your answer should include a reference to team impact, not just individual achievement"

**Step 4 — Practice Loop**
- User writes or speaks their practice answer
- System evaluates: relevance to JD requirements, story quality, STAR structure completeness, appropriate framing for company type
- Returns specific, JD-calibrated feedback: "Your answer addresses Leadership but doesn't connect it to the Innovation competency this role requires"
- User iterates until they feel ready
- MVP scope: text-only practice. Voice input (async or real-time) deferred to Phase 3.

### Commercial Case

**LTV impact estimate (revised for multi-round)**:
- Without interview prep: user stays active for resume tailoring ≈ 2–3 months (until response or discouragement)
- With interview prep, single-trigger model: 50–67% LTV extension for users who receive responses
- With interview prep, multi-round model (per Analysis 16):
  - Fresh grad (avg 1.5 rounds): +0.8 months
  - PMET (avg 2.8 rounds): +1.6 months
  - Finance/consulting (avg 3.5 rounds): +2.3 months
  - Weighted average LTV extension: 75–90%
- Each stage transition to a new interview round is a natural re-engagement trigger
- Does NOT solve structural churn-at-offer; post-employment features deferred to Year 2+

**B2B value**:
- Adds a second module to the institutional pitch ("resume preparation + interview preparation" vs "resume only")
- Strong differentiation from VMock (whose STAR Coach doesn't do JD-specific preparation)
- Career directors can see "students who completed ≥3 prep sessions had X% higher interview-to-offer rate" — the metric that matters most

### Technical Feasibility

**Confirmed feasible with current LLM tier**:
- Question generation: Claude Sonnet, per-session (not cached; JD-specific)
- Answer evaluation: Claude Sonnet, per practice submission
- Story synthesis: Claude Haiku + Sonnet combo (extraction + structuring)
- SG company type intelligence: extends existing company-type classification already in data model

**Key design risk**: AI-generated answers that sound polished but feel hollow in real interviews. **Mitigation**: the module is designed as a coaching tool that structures the user's own stories, not a generation tool that writes answers from thin input. Users who provide rich story input get better answers. The system should prompt for richer input rather than generating filler.

### Success Metric

- Primary: interview-to-offer conversion rate for users who complete ≥3 prep sessions vs. those who don't
- Secondary: prep session completion rate (leading indicator of engagement)
- B2B: career director NPS after modules are used in pilot cohort

---

## What Is NOT in Scope (MVP)

- Cover letter generation
- Interview preparation (Phase 2 — see above)
- LinkedIn profile optimisation
- Salary benchmarking / offer evaluation
- Job recommendations (proactive "you should apply here")
- Two-sided recruiter platform
- Mobile app (web-first)
- Mandarin/Malay language UI (English-first; bilingual resume CONTENT handled by AI, but UI is English)
- Voice/real-time interview simulation (Phase 3)

---

## Value Proposition Audit (Red-Team Results)

| Claim | Status | Corrected Position |
|-------|--------|-------------------|
| "Per-job tailoring no competitor has done" | WRONG — Jobscan (2014), Teal do this | "The SG-localized version of per-job tailoring" |
| "SG intelligence is a moat" | Overstated — 90-day replication risk | "SG intelligence is a trust signal and wedge; learning loop is the actual moat" |
| "Outcome tracking = data moat" | Premature — cold-start until 5K+ events | "Applications dashboard (retention feature); data moat materializes Year 2" |
| "URL parsing = differentiator" | Table stakes, not moat | Feature, not USP. Remove from moat narrative. |
| "No feedback exists for SG job seekers" | Partially wrong — WSG/CC exist | "No instant, job-specific, 24/7, SG-contextualised feedback" |

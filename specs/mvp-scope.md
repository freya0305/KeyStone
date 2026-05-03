# MVP Scope — KeyStone v1.0

> Authority: this file defines what ships in v1.0 and what does not. Phase 03 (/implement) MUST NOT implement anything in the "excluded" section.
> Last updated: 2026-04-29

---

## What Is MVP v1.0

The minimum product that lets a SG job seeker experience measurable value — enough to justify SGD 12/month — AND begins accumulating the proprietary signal data that becomes the long-term defensibility moat.

**Decision criterion for any feature**: "If we don't ship this, will a SG job seeker pay SGD 12/month?" Yes → in. Maybe → Phase 2. Unlikely → cut.

---

## In Scope — v1.0

### Feature 1: Resume Upload + SG Analysis

- PDF, DOCX, plain text upload (max 5MB)
- Processing time: ≤10 seconds
- SG flags: NRIC detection (removal recommendation), NS section quality assessment (male graduates), professional photo include/exclude guidance (by company type), education format SG conventions
- PMET intelligence: career pivot narrative reframing, age-neutral language detection, seniority repositioning, contract/freelance framing
- Overall strengths (2–4 bullets) + gaps (2–4 bullets)
- Content hash caching (re-running same resume against different JDs does not re-trigger analysis)

### Feature 2: JD Input + Four-Level Match Assessment

- URL parsing: MCF, JobStreet, LinkedIn, company career pages
- Fallback: paste-in JD text
- Company type detection: GLC / MNC / SME / Startup / Government / Statutory Board
- Four-level taxonomy: Strong (green) / Transferable (amber) / Addressable (orange) / Fundamental (red)
- Per-requirement classification with one-sentence rationale
- Failure handling: if URL parse fails, silently offer text-paste fallback (no error state shown)

### Feature 3: Line-by-Line Revision Suggestions (Core Feature)

- Scope: Transferable and Addressable gaps only (Fundamental gaps flagged separately, not "fixed")
- Per suggestion: original text + suggested rewrite + one-sentence rationale (citing specific JD requirement + company type)
- Accept / Reject / Modify (inline edit) interaction
- Export: modified resume as PDF and/or DOCX with accepted suggestions incorporated
- Free tier: first JD = unlimited suggestions (full value demonstration); subsequent JDs = first 3 suggestions visible, rest gated
- Pro: unlimited suggestions for all JDs
- **Anti-abuse**: SG mobile phone number (SMS) verification at signup; one phone = one account; cost ~SGD 0.05/user
- **No signup required for first use**: user can complete first JD analysis before registration prompt

### Feature 4: Application Outcome Tracking + Reminder Emails

- Application record auto-created at resume download ("Did you submit to [Company]?")
- Stage-based tracking (not simple status enum): Applied → Response → Screening → Interview Round N → Final → Decision
- Dashboard: personal response rate, per-stage pass rates, applications by stage/month, trend line
- Minimum 5 applications before response rate shown; minimum 15 before benchmark comparison
- **Outcome logging incentive — pull-based (no per-application emails)**:
  - Batch quick-update UI: persistent banner when returning to product; card-per-application with [Got response] / [No news] / [Skip]; designed for 30 applications in <3 minutes
  - Pre-prep interstitial: prompt to batch-update pending applications before entering interview prep
  - Gamification: tracking completeness % visible to user with percentile ranking
  - Single weekly digest email (max 1/week/user, only if no login that week, deep link to batch update)
  - Auto-close: 30-day silent close with correction toast at next login
  - SPF/DKIM/DMARC on sending domain before launch (for the weekly digest)
- PDPA training separation: B2B university data → dashboards only, never training pipeline

### Architecture Requirements (Day 1, non-negotiable)

- **Suggestion signal logging**: every Accept/Reject/Modify logged to `suggestion_signals` table with `{suggestion_id, user_segment, company_type, role_level, industry, action, timestamp}`
- **B2C training consent**: separate opt-in checkbox at registration (distinct from service consent)
- **PDPA data separation**: B2B user data architecturally blocked from training pipeline

### Payments and Auth

- Stripe: monthly (SGD 9/month Basic, SGD 12/month Pro) and annual (SGD 144/year) plans
- Google OAuth as primary login option (lowest friction)
- Email + SG mobile phone verification as alternative
- Pro features gated immediately on subscription

### Annual Plan Upgrade Trigger

**The "Offer Received" moment is the primary Annual Plan conversion trigger.**

When a user logs "Decision: Offer Received" in the outcome tracker:
1. Show a congratulations interstitial ("You got the job!")
2. Present Annual Plan prompt: "Stay tracked for your next career move — SGD 144/year"
3. Include: 1× 30-min career advisor session (SGD 150+ value)
4. Post-hire tracking: skill gap monitoring, market intelligence, resume refresh

**Why this moment**: Users who just received an offer have the highest purchase intent and clearest understanding of product value. They are also the ideal Annual Plan target — employed, career-aware, willing to invest in tracking.

**Annual Plan is NOT**:
- A churn-reduction tool (job seekers won't prepay 12 months)
- A subscription lock-in
- Marketed as "save money" vs monthly

**Annual Plan IS**:
- A career ecosystem pass for post-hire tracking
- Differentiated by the included advisor session
- Positioned at the celebration moment, not the frustration moment

---

## Explicitly Excluded — v1.0

These are BLOCKED from implementation until the stated phase. If discovered partially implemented, remove them.

| Feature | Phase |
|---------|-------|
| Interview Preparation Module | Phase 2 |
| Batch mode (5 JDs simultaneously) | Phase 2 |
| Web Push API notifications | Phase 2 |
| Calendar ICS export | Phase 2 |
| Weekly digest email | Pro feature (v1.0 — implement with MVP, SPF/DKIM/DMARC required before launch) |
| B2B university dashboard | After first university contract signed |
| Cover letter generation | Never — not SG market priority |
| LinkedIn profile optimisation | Not confirmed |
| Salary benchmarking / offer evaluation | Year 2 |
| Job recommendations (proactive) | Year 2 |
| Two-sided recruiter platform | Never |
| Mobile app (iOS/Android) | Phase 3 |
| Mandarin / Malay UI | Year 2 |
| Voice interview simulation | Phase 3 |
| Email parsing integration (Gmail/Outlook OAuth) | Phase 3 |
| ATS score simulation | Never — not how SG hiring works |

---

## "Done" Criteria for v1.0 Launch

### User Experience

- [ ] New user completes full workflow (upload resume + paste JD + see suggestions) in ≤5 minutes
- [ ] First JD experience is gate-free (no signup required to see suggestions)
- [ ] Suggestions are specific: original → rewrite → rationale referencing company type + JD requirement
- [ ] PDF/DOCX export works with accepted suggestions incorporated
- [ ] Mobile-responsive (most SG users check on mobile first, even if they apply on desktop)

### Technical

- [ ] Resume analysis ≤10 seconds; suggestion generation ≤15 seconds (p95)
- [ ] LLM cost ≤SGD 5/user/month at full usage (Haiku + Sonnet routing)
- [ ] 99.5% uptime (single region acceptable for v1.0)
- [ ] Content hash caching functional (same resume + same JD = no duplicate LLM call)
- [ ] Suggestion signals 100% captured in `suggestion_signals` table

### Compliance

- [ ] PDPA-compliant privacy policy live (separate service consent vs training consent)
- [ ] B2C training consent checkbox present and wired to data pipeline gate
- [ ] B2B contract template includes "no AI training" clause
- [ ] Email sending domain has SPF/DKIM/DMARC
- [ ] EAA non-applicability written opinion letter from employment lawyer (not risk assessment — formal opinion letter for investor/bank/university use)

### Commercial

- [ ] Stripe payment accepting SGD (monthly + annual)
- [ ] SMS phone verification working (SG +65 numbers)
- [ ] At least 1 design partner providing written testimonial
- [ ] Founders able to monitor activation funnel daily (PostHog or equivalent)

---

## Design Partner Requirements (Pre-Launch)

50–100 design partner users needed before public launch:

- Source: 2–3 recruitment agency referrals + direct founder network
- Each partner: full Pro access (6 months free) + 1:1 resume review session
- Partners must: apply to ≥5 real jobs using KeyStone, agree to outcome tracking consent
- Target outcomes: 50 users × 5 applications × 35% logging rate = 87 outcome records at launch


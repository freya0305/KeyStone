# MVP Scope — KeyStone v1.0

> Authority: this file defines what ships in v1.0 and what does not. Phase 03 (/implement) MUST NOT implement anything in the "excluded" section.
> Last updated: 2026-05-07

---

## What Is MVP v1.0

The minimum product that serves two simultaneous user groups:

- **Job seekers**: Per-job resume tailoring with outcome tracking — enough value to justify SGD 12/month
- **Recruiters/employers**: AI JD generator — enough value to justify SGD 79–449/month

The two-sided data flywheel begins accumulating from Day 1 for skill frequency data (JDs written → skill patterns), but the bidirectional improvement loop (outcome-correlated skill patterns) activates Month 3+ once B2C application outcome data is flowing.

**Decision criterion for any B2C feature**: "If we don't ship this, will a SG job seeker pay SGD 12/month?" Yes → in. Maybe → Phase 2. Unlikely → cut.
**Decision criterion for any B2B feature**: "If we don't ship this, will a recruiter/employer pay SGD 79/month?" Yes → in.

---

## In Scope — v1.0

### Feature 1: Resume Upload + Analysis

- PDF, DOCX, plain text upload (max 5MB)
- Processing time: ≤10 seconds
- Overall strengths (2–4 bullets) + gaps (2–4 bullets)
- Content hash caching (re-running same resume against different JDs does not re-trigger analysis)

> **Note**: PMET intelligence (career pivot reframing, age-neutral language, seniority repositioning, contract/freelance framing) and SG-specific flags (NRIC, NS, photo, education format) are Phase 2 — requires SG PMET resume training data that is not available at launch. v1.0 ships with general resume analysis; PMET-specific features are the primary Phase 2 conversion driver for the highest-WTP segment.

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
  - Auto-close: 30-day silent close with correction toast at next login
- **Application tracking quality gate**: Only applications with ≥2 status updates are recorded as "active applications." Applications with only auto-created records (no user confirmation) are excluded from aggregate analytics and JD training data. This prevents false-positive application records from polluting outcome data.
- **JD training data from unconfirmed applications**: Even if an application record is not confirmed by the user, the job URL from that application is still logged to `jd_generation_logs` (anonymized, no user association) for skill frequency training data. User consent for this logging is collected at account creation.
- PDPA training separation: B2B university data → dashboards only, never training pipeline

### Feature 5: JD Generator for Recruiters / Employers (B2B Side — Phase 1 MVP)

- Input: job title, industry, company type, key requirements (free-text or structured)
- Output: AI-generated JD with skills, responsibilities, qualifications, tone calibrated for company type (GLC / MNC / SME / Startup)
- Based on: analysis of public job postings (MyCareersFuture, JobStreet, LinkedIn) — extracting skill frequency, required vs preferred patterns, industry-standard competency frameworks. NOT candidate profile data.
- Month 1–3 (MVP): JD tool helps recruiters write accurate JDs based on public JD analysis. Candidate quality data is not yet flowing back.
- Month 3+ (feedback loop): As B2C users log application outcomes (Applied → Interview → Offer), anonymized aggregate signal flows back: "JDs with skill pattern X attracted candidates who reached interview stage." This is NOT individual candidate profiles — it is aggregate outcome-correlated skill patterns, collected under PDPA-compliant consent. Recruiters see improved JD suggestions based on which skill combinations correlate with higher response rates across the platform.
- Pricing: Agency Team SGD 79/month (5 users, 100 JD) / Agency Pro SGD 199/month (10 users, 400 JD) / Agency Enterprise SGD 449/month (unlimited users, unlimited JD)
- Free tier: 10 JD generations/month for registered recruiters — lowers barrier to first use
- PDPA: no personal resume data stored; only aggregate market-skill pattern signal used

### Architecture Requirements (Day 1, non-negotiable)

- **Suggestion signal logging**: every Accept/Reject/Modify logged to `suggestion_signals` table with `{suggestion_id, user_segment, company_type, role_level, industry, action, timestamp}`
- **B2C training consent**: separate opt-in checkbox at registration (distinct from service consent)
- **PDPA data separation**: B2B user data architecturally blocked from training pipeline

### Payments and Auth

- Stripe: Free (SGD 0), Pro monthly (SGD 12/month). Annual Plan cancelled.
- No Basic tier — two tiers only (Free / Pro)
- Google OAuth as primary login option (lowest friction)
- Email + SG mobile phone verification as alternative
- Pro features gated immediately on subscription

### Post-Hire Retention (Future Feature)

**Note**: Annual Plan cancelled. "Offer Received" moment retained as future upsell trigger once post-hire features (career tracking, salary benchmarking) are built in Year 2.

---

## Explicitly Excluded — v1.0

These are BLOCKED from implementation until the stated phase. If discovered partially implemented, remove them.

| Feature                                         | Phase                                                                     |
| ----------------------------------------------- | ------------------------------------------------------------------------- |
| Interview Preparation Module                    | Phase 2                                                                   |
| Batch mode (5 JDs simultaneously)               | Phase 2                                                                   |
| Web Push API notifications                      | Phase 2                                                                   |
| Calendar ICS export                             | Phase 2                                                                   |
| Weekly digest email                             | Phase 2 (requires SPF/DKIM/DMARC infrastructure + email service provider) |
| B2B university dashboard                        | After first university contract signed                                    |
| Cover letter generation                         | Never — not SG market priority                                            |
| LinkedIn profile optimisation                   | Not confirmed                                                             |
| Salary benchmarking / offer evaluation          | Year 2                                                                    |
| Job recommendations (proactive)                 | Year 2                                                                    |
| JD generator for employers/recruiters           | IN MVP v1.0 — see Feature 5                                               |
| Mobile app (iOS/Android)                        | Phase 3                                                                   |
| Mandarin / Malay UI                             | Year 2                                                                    |
| Voice interview simulation                      | Phase 3                                                                   |
| Email parsing integration (Gmail/Outlook OAuth) | Phase 3                                                                   |
| ATS score simulation                            | Never — not how SG hiring works                                           |

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

- [ ] Stripe payment accepting SGD (monthly only; annual plan cancelled)
- [ ] SMS phone verification working (SG +65 numbers)
- [ ] At least 1 design partner providing written testimonial
- [ ] Founders able to monitor activation funnel daily (PostHog or equivalent)

---

## Design Partner Requirements (Pre-Launch)

**5–10 deep design partner engagements** before public launch — not 50-100. Focus on genuine activation over volume.

- Source: Application-based, not broad enrollment. Prioritize referral from existing founder network or warm intros.
- Each partner: full Pro access (3 months free) + optional 1:1 resume review session
- Partners must: apply to ≥5 real jobs using KeyStone, agree to outcome tracking consent
- Success criteria (each partner must produce at least ONE): written testimonial, referral call with prospective B2B buyer, case study data, or warm intro to career centre/agency decision-maker
- Design partner program is a B2B reference asset, NOT a subscription revenue driver. If partners do not produce reference assets within 3 months, do not renew.

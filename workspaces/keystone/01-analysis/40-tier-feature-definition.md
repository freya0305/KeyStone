# Feature Definitions by Pricing Tier — KeyStone v1.0

> Authority: This document defines what features each tier includes and how upgrade moments are designed.
> It supersedes the tier feature descriptions in `35-pricing-research-and-anti-abuse.md`.
> Last updated: 2026-04-30

---

## Executive Summary

The tier structure is designed around a single principle: **the upgrade to Pro must feel inevitable, not optional.** Basic exists to absorb price-sensitive users who would otherwise walk away; it is not a destination. Pro is where real job search momentum happens. Annual is not a subscription lock-in -- it is a post-hire career tracking package.

**Tier architecture**: Free (lead-gen) -> Basic (acquisition) -> Pro (core job search) -> Annual (ecosystem engagement post-hire)

**Critical note on Annual**: Annual Plan is NOT a churn-reduction tool. Job seekers find work in 2-4 months. They should NOT pay 12 months upfront. Annual exists for users who want to stay tracked in the KeyStone ecosystem after they get a job -- for their next career move.

---

## 1. Tier Structure

### 1.1 Free Tier -- "Try It Free"

**Entry condition**: No signup required for first use. User can complete their first full job analysis before being asked to register.

**Post-registration entitlement**: 3 job analyses per month

**First-job exception** (critical for conversion):
- The FIRST job analyzed after registration = UNLIMITED suggestions
- This is the full-value demonstration -- no gates, no limits
- After the first job, subsequent analyses fall under the 3/month limit

**Why this matters**: The first job analysis is the product's sales pitch. Showing limited suggestions on the first job kills conversion before the user understands what they are missing. Showing unlimited suggestions on the first job creates the "I need this" moment.

**What is NOT included in Free**:
- No resume storage (resume is session-only until registered)
- No outcome tracking
- No export
- No peer comparison
- No weekly digest

**Free tier purpose**: Data collection + lead generation. We are acquiring users at no cost and demonstrating value before asking for commitment.

---

### 1.2 Basic Tier -- SGD 9/month ("Try It")

**Target user**: Budget-conscious fresh grads (21-25) who are uncertain about committing to a paid tool. Price of a lunch in Singapore.

**What's included**:

| Feature | Detail |
|---------|--------|
| Resume upload | PDF, DOCX, plain text (max 5MB) |
| Job analyses | **UNLIMITED** |
| Match assessment | 4-level taxonomy per job (Strong / Transferable / Addressable / Fundamental) |
| Suggestions | Full suggestion list per analysis (all suggestions visible) |
| Suggestion interaction | Accept / Reject / Modify (inline edit) |
| Outcome tracking | Manual entry only. User records result for each application. |
| Resume storage | Up to 3 resumes stored |
| SG flags | NRIC detection, NS quality, photo guidance, SG education format |
| PMET intelligence | Career pivot framing, age-neutral language, seniority repositioning |
| Export | None |
| Analytics | None beyond basic match score |
| Peer comparison | No |
| Email digest | None |
| Career advisor session | No |

**What is explicitly NOT included**:
- Interview preparation module (Phase 2 feature)
- Stage-based application tracking (only manual outcome logging)
- Automated outcome capture
- PDF or DOCX export
- Peer comparison metrics

**Basic's value proposition**: Unlimited resume tailoring for SGD 9/month. Full product experience for the core use case. Pro users unlock interview preparation when they reach interview stage -- the highest-intent moment in the job search.

---

### 1.3 Pro Tier -- SGD 12/month ("Get Results")

**Target user**: Committed job seekers who have decided KeyStone is worth paying for. SGD 1/day pricing anchor makes it feel affordable.

**Everything in Basic, PLUS**:

| Feature | Detail |
|---------|--------|
| Job analyses | UNLIMITED |
| Suggestions | UNLIMITED for ALL jobs (no 3-suggestion cap) |
| Stage-based tracking | Applied -> Response -> Screening -> Interview Round N -> Final -> Decision |
| Automated outcome capture | Triggered by resume download -- system asks "Did you submit to [Company]?" and creates application record automatically |
| Weekly digest email | One email per week, max, only if no login that week. Deep link to batch update UI |
| Export | PDF and DOCX with accepted suggestions incorporated |
| Peer comparison | How user's match scores compare to similar job seekers in same industry/role level |
| Analytics dashboard | Response rate, per-stage pass rates, applications by stage/month, trend line |
| Minimum bar for benchmarks | 5 applications before response rate shown; 15 before peer comparison appears |
| **Interview preparation** | **Phase 2: Question generation + guidance for interview stages (R1, R2, Final)** |

**Pro upgrade trigger**: The real upgrade moment is NOT running out of analyses -- it is reaching the INTERVIEW STAGE. When a user logs "I have an interview," they have entered the highest-intent moment of their job search. They are willing to pay to prepare. That is when Pro converts.

**Why Interview Prep is the real upgrade trigger**:
- Interview stage users have 10-20× higher conversion intent than resume-tailoring-only users
- Interview prep is a one-time-per-job-search need that feels urgent
- "I have an interview tomorrow" is more compelling than "I ran out of analyses"
- Users who reach interview stage have already invested in the job search -- they will pay to win

---

### 1.4 Annual Tier -- SGD 144/year ("Stay Tracked")

**Annual is NOT a subscription lock-in. It is a career ecosystem pass.**

Annual exists for users who want to stay in the KeyStone ecosystem after they get a job: track their career progression, get skill gap alerts, and maintain calibrated suggestions for their next job search.

| Feature | Detail |
|---------|-------|
| All Pro features | Unlimited + interview prep |
| Post-hire career tracking | Outcome logging, skill gap tracking, market intelligence |
| Advisor session | 1x 30-minute session with partner coach network |
| Priority feature access | New features before Basic/Pro |

**Why Annual is NOT "lock-in"**: Job seekers find work in 2-4 months. They should NOT pay 12 months upfront for a product that served their job search. Annual is for users who WANT to stay tracked -- not a trap to capture users who no longer need the core product.

**Target Annual users**:
- Users who just logged "Offer Received" and want next-move preparation
- Users in passive career management mode (skill tracking, market intel)
- Users who want periodic resume refreshes as their career evolves

**Annual ≠ LTV maximization**. Annual = ecosystem engagement post-hire. This is qualitatively different from "annual as churn reduction."

**Pricing**: SGD 144/year = SGD 12/month equivalent. No discount framing. "Stay tracked for a year" not "save money vs monthly."

---

## 2. Upgrade Psychology

### 2.1 Why Basic -> Pro Is an Easy Sell

**The trigger moments**:

1. **Analysis ceiling hit**: "You've used 4 of 5 analyses this month. [Job they care about] requires a tailored resume tonight."
   - User has 1 analysis left but has applied to 6 jobs
   - The 6th job is the one they really want
   - Upgrade prompt: "Unlock unlimited analyses for SGD 12/month"

2. **Suggestion wall hit**: "3 of 12 suggestions shown. Upgrade to see the remaining 9 tailored suggestions for your [Target Role] application."
   - User sees that the tool has MORE to offer
   - The remaining suggestions are specific to their target role
   - Upgrade prompt: "See all suggestions. Pro plans start at SGD 12/month."

3. **The emotional moment**: User is about to apply to a job they care about. This is not a hypothetical -- this is their dream role, open for 3 more days. The upgrade is not a subscription decision; it is a "do I try for this job or not" decision.
   - Positioning: "Apply with full intelligence. Tonight."
   - NOT: "Compare Pro vs Basic features"

**The UX principle**: Upgrade prompts appear at the moment of frustration or desire -- never as a features comparison table. Users do not think "should I pay SGD 3 more for unlimited?" They think "I need to apply to that job tonight."

### 2.2 The Free -> Basic Upgrade

**This is a weaker conversion than Basic -> Pro.** Free users who have exhausted their 3 analyses and have not yet hit an urgent job application will often wait for the monthly reset rather than pay.

**When Free -> Basic does convert**:
- User has a job search underway and has been using KeyStone
- They have 0 analyses left
- They have at least one active job application in mind
- The monthly price (SGD 9) feels small relative to the job opportunity

**Free -> Basic is NOT the primary conversion event.** It is a safety net for users who need occasional analyses. The primary conversion is Free -> Pro, once the user has experienced unlimited suggestions on their first job and wants that full power back.

### 2.3 Annual Upgrade Moment

**Annual conversion is a post-hire retention event.** It happens when a user logs "Offer Received" and we prompt them to stay tracked.

**The moment**:
- User logs "Offer Received" -> Pro upgrade prompt
- "Congrats! Stay tracked for your next move. Annual = SGD 144/year. 1 advisor session included."
- User who just got a job is the ideal Annual candidate: they have career momentum, they understand the product's value, and they have a reason to stay engaged.

**Annual is NOT for users who are mid-search.** It is for users who FINISHED their search. The Annual moment is the "Offer Received" celebration moment -- not a "2-3 months of Pro usage" slow burn.

---

## 3. What Each Tier Optimizes For

| Tier | Price | Primary Goal | Target User | Conversion Event |
|------|-------|-------------|-------------|-----------------|
| Free | SGD 0 | Lead generation + data collection | Curious browsers, early-stage job seekers | First job analysis completed |
| Basic | SGD 9/month | Lower barrier, volume acquisition | Budget-conscious fresh grads | Analysis ceiling hit on a job they care about |
| Pro | SGD 12/month | Revenue driver | Committed job seekers | Emotional upgrade moment (dream job or interview stage) |
| Annual | SGD 144/year | Ecosystem engagement post-hire | Users who got a job and want to stay tracked | "Offer Received" moment + advisor session |

---

## 4. Feature Gating Table

| Feature | Free (Post-Register) | Basic (SGD 9/mo) | Pro (SGD 12/mo) | Annual (SGD 144/yr) |
|---------|---------------------|-----------------|-----------------|-------------------|
| Resume upload | Yes | Yes | Yes | Yes |
| Resume storage | No | Yes (3) | Yes (unlimited) | Yes (unlimited) |
| Job analyses/month | 3 | Unlimited | Unlimited | Unlimited |
| Suggestions visible | First 3 (first job: unlimited) | Full list | All unlimited | All unlimited |
| 4-level match assessment | Yes | Yes | Yes | Yes |
| SG flags (NRIC, NS, photo) | Yes | Yes | Yes | Yes |
| PMET intelligence | Yes | Yes | Yes | Yes |
| Suggestion accept/reject/modify | Yes | Yes | Yes | Yes |
| Manual outcome tracking | No | Yes | Yes | Yes |
| Stage-based application tracking | No | No | Yes | Yes |
| Automated outcome capture | No | No | Yes | Yes |
| Analytics dashboard | No | No | Yes | Yes |
| Peer comparison | No | No | Yes | Yes |
| Weekly digest email | No | No | Yes | Yes |
| PDF export | No | No | Yes | Yes |
| DOCX export | No | No | Yes | Yes |
| Career advisor session | No | No | No | Yes (1x 30-min) |
| Post-hire career tracking | No | No | No | Yes |
| Priority feature access | No | No | No | Yes |

---

## 5. Upgrade Trigger UX

### 5.1 Basic Tier Upgrade Prompts

**Trigger 1: Analysis limit approaching**
- Banner at 4/5 analyses: "You've used 4 of 5 analyses this month."
- Banner at 5/5 analyses: Full-screen interstitial on next app open
  - Copy: "You've reached your 5 analyses for this month."
  - "Unlock unlimited analyses for SGD 12/month -- apply to every job with full intelligence."
  - Primary CTA: "Upgrade to Pro"
  - Secondary: "Wait until [first of next month]"

**Trigger 2: Suggestion cap within analysis**
- After 3rd suggestion: Grey overlay on remaining suggestions
- Copy: "9 more suggestions hidden. See all tailored suggestions for your [Target Role] application."
- CTA: "Upgrade to see all suggestions"

**Trigger 3: Outcome tracking limit**
- After 10 manual outcomes logged: Prompt suggesting stage-based tracking
- Copy: "You're tracking your applications manually. Pro gives you stage-based tracking -- Applied, Interview, Offer -- so you can see where you're winning."

### 5.2 Free Tier Upgrade Prompts

**Trigger 1: Post-first-job, 3 analyses exhausted**
- Copy: "You've used all 3 free analyses. Get unlimited analyses with Basic -- or go Pro for interview prep."
- CTAs: "Start Basic (SGD 9/mo)" | "Get Pro (SGD 12/mo)"

**Trigger 2: Suggestion cap (Free sees 3 suggestions then hits wall)**
- Copy: "You've seen 3 of your tailored suggestions. Upgrade to see all suggestions -- or continue with Basic for unlimited analyses/month."
- Note: Free does NOT see "unlimited on first job" again. That is a one-time experience.

### 5.3 Pro Tier Retention -> Annual Prompt

**Trigger: User logs "Offer Received"**
- Banner: "Congratulations! You've got the job. Stay tracked for your next move -- Annual is SGD 144/year with a free advisor session."
- CTA: "Stay with KeyStone"
- Appears at the celebration moment, not as a random upgrade prompt

---

## 6. Free Tier Limit UX

### 6.1 Post-Registration Free

After a user registers (email + phone verification), they land on the dashboard with:
- "You have 3 analyses remaining this month"
- Empty state for saved applications
- Prompt to upload resume and start first analysis

### 6.2 Analyses Exhausted

When Free user hits 0 analyses:
- Dashboard shows: "You've used all 3 analyses this month. Upgrade to continue."
- All features remain accessible except job analysis
- Resume remains stored
- Previous analyses remain viewable

### 6.3 Monthly Reset

On the first of each month:
- Analyses reset to 3
- User receives email: "Your 3 free analyses are ready -- [Job they last analyzed] is still open. Continue where you left off."
- Deep link to last analyzed job or dashboard

---

## 7. Pricing Psychology

### 7.1 Price Anchoring

| Tier | Monthly | Effective Daily | Anchor |
|------|---------|----------------|--------|
| Basic | SGD 9 | SGD 0.30 | "Price of a lunch in Singapore" |
| Pro | SGD 12 | SGD 0.40 | "SGD 1 per day -- less than a coffee" |
| Annual | SGD 144 | SGD 0.40 | "Stay tracked for a year + advisor session" |

### 7.2 Annual Is NOT a Discount

**Do NOT position Annual as "save SGD 0 vs monthly."** Monthly Pro = SGD 12 × 12 = SGD 144. Annual = SGD 144. There is no discount.

**Position Annual as**:
- "Stay tracked after you get the job -- for your next career move"
- "1 advisor session included -- a SGD 150+ value"
- "Career tracking package for the full year"

---

## 8. Cross-Reference Audit

| Document | Section | Finding |
|----------|---------|---------|
| `specs/mvp-scope.md` | Feature 3 | States "Free tier: first JD = unlimited suggestions; subsequent = first 3 visible, rest gated" -- consistent |
| `specs/mvp-scope.md` | Feature 3 | States "Pro: unlimited suggestions for all JDs" -- consistent |
| `specs/mvp-scope.md` | Payments | States "Stripe: monthly (SGD 12/month) and annual (SGD 144/year)" -- consistent |
| `35-pricing-research-and-anti-abuse.md` | Tier Structure | Superseded by this document |

---

## 9. Implementation Notes

### 9.1 Stripe Configuration

| Plan | Amount | Interval | Features (metadata) |
|------|--------|----------|---------------------|
| Basic | SGD 9 | monthly | analyses:unlimited, export:false, tracking:manual |
| Pro | SGD 12 | monthly | analyses:unlimited, export:pdf_docx, tracking:stage_based |
| Annual | SGD 144 | yearly | analyses:unlimited, export:pdf_docx, tracking:stage_based, advisor_session:1, post_hire_tracking:true |

### 9.2 Feature Flag Keys

| Feature | Flag Key | Tiers where enabled |
|---------|----------|---------------------|
| Unlimited analyses | `feature.unlimited_analyses` | Pro, Annual |
| All suggestions visible | `feature.all_suggestions` | Pro, Annual |
| Stage-based tracking | `feature.stage_tracking` | Pro, Annual |
| Automated outcome capture | `feature.auto_outcome_capture` | Pro, Annual |
| Peer comparison | `feature.peer_comparison` | Pro, Annual |
| PDF export | `feature.export_pdf` | Pro, Annual |
| DOCX export | `feature.export_docx` | Pro, Annual |
| Weekly digest | `feature.weekly_digest` | Pro, Annual |
| Career advisor booking | `feature.advisor_session` | Annual only |
| Post-hire career tracking | `feature.post_hire_tracking` | Annual only |

### 9.3 Analytics Events

| Event | Properties | Trigger |
|-------|-----------|---------|
| `tier.upgraded` | `from_tier`, `to_tier`, `trigger` | Successful Stripe checkout |
| `analysis.counted` | `tier`, `analysis_number` | Each job analysis |
| `suggestion.gated` | `tier`, `job_id`, `gated_count` | Suggestion wall shown |
| `upgrade.shown` | `tier`, `trigger_type`, `position` | Upgrade prompt displayed |
| `upgrade.dismissed` | `tier`, `trigger_type` | Upgrade prompt dismissed |
| `outcome.offer_received` | `tier`, `company`, `role` | User logs offer received |
| `annual.upgrade_offer_received` | `tier`, `trigger` | Annual prompt shown at offer moment |

---

## 10. Out of Scope for v1.0

These features are NOT included in any tier for v1.0 launch:

| Feature | Reason |
|---------|--------|
| Batch mode (5 JDs simultaneously) | Phase 2 |
| Cover letter generation | Never -- not SG market priority |
| LinkedIn profile optimization | Not confirmed |
| Salary benchmarking | Year 2 |
| Proactive job recommendations | Year 2 |
| Mobile app | Phase 3 |
| Voice interview simulation | Phase 3 |
| Email parsing integration | Phase 3 |

# GTM Spec — KeyStone

> Last updated: 2026-04-29 (Phase 01 Analysis)

---

## Recommended Launch Sequence (B2B-First)

The brief proposes B2C first, B2B at Month 6. **This is inverted.** Recommended sequence:

| Month | Priority Action | Expected Output |
|-------|----------------|----------------|
| 0–1 | Approach 1–2 university career centres for free pilot commitment | Written pilot agreement (does not need to be paid) |
| 1–3 | Build MVP; begin 50–200 student free pilot at 1 university | First cohort data; product feedback at scale |
| 3–5 | Public B2C launch riding university co-branding | 1K–3K registered users; university logo as social proof |
| 5–9 | Convert pilot to paid contract; approach 2–3 more universities + agencies | First SGD 15–30K contract; 3–5 agency deals |
| 9–18 | Scale institutional pipeline; B2C grows as acquisition channel | 2–4 institutional contracts; 500–1,500 B2C paying users |

**Single highest-leverage Month 1 action**: lock ONE university pilot commitment before public launch.

---

## B2B Distribution

### University Targets (Priority Order — Revised Round 2)

**Priority ranking changed**: SIT is now ranked #1 (previously SUSS/SIT/UniSIM bundled). Reasoning below.

| Rank | Target | Why | Procurement Speed |
|------|--------|-----|-------------------|
| 1 | **SIT (Singapore Institute of Technology)** | Applied-degree focus; employment outcome pressure; low procurement overhead; no likely existing AI resume tool contract | Fast (director-level budget authority) |
| 2 | **SUSS (Singapore University of Social Sciences)** | Mid-career switcher student profile = ideal KeyStone user; less bureaucracy than NUS/NTU; career-transition focus matches KeyStone's mid-career value prop | Fast |
| 3 | **SUTD (Singapore University of Technology and Design)** | Small (~2K students), tech-forward culture, high early-adopter signal; lower revenue but high prestige reference per seat | Very fast (small institution) |
| 4 | **SMU (CCPD)** | Most sophisticated career centre, employer-focused, high KeyStone user quality; jump to #1 if founding team has SMU connection | Medium (structured CCPD procurement) |
| 5 | **Polytechnics (NYP, SP, TP)** | Volume play; ~80K students combined; career coordinators more accessible; fast decisions under SGD 20K | Fast |
| 6 | **NTU** | Large cohort valuable; medium procurement complexity; approach after 1–2 pilots complete | Slow |
| 7 | **NUS** | Most prestigious; most complex procurement; VMock may have some presence already | Very slow (18+ months to contract) |

**SMU Exception**: If any team member has a direct NUS/SMU alumni connection to CCPD staff, jump SMU to #1 immediately. Warm intro overrides institutional complexity every time.

### Critical Pre-Condition: Warm Network Access

Based on comparable company research, **every successful first B2B institutional client was won through a warm connection, not cold outreach**. No documented case of cold email winning first institutional client in edtech B2B.

**Before any outreach, the team must**:
1. Map full network for any 1st or 2nd-degree connection to SG career centre staff
2. Check NUS/NTU/SMU/SIT alumni networks for current career services employees
3. Check LinkedIn for career advisors or directors who follow or are connected to team members
4. Identify any faculty, mentor, or advisor who can provide a named introduction

If zero connections found: attend SG career sector events (NUS Career Fair, Singapore HR Institute functions, EnterpriseSG startup ecosystem events) to build the connection before pitching.

### Minimum Product State Before First University Meeting

Before any career director meeting, the product must have:

1. **20–30 tested SG job postings** — from MCF and JobStreet, across finance/tech/consulting/engineering/public sector; URL parsing confirmed working on each
2. **20–30 tested SG-style resumes** — synthetic but realistic (NUS CS + startup internship, SMU BBA + Big 4 internship, NTU Engineering with NS as SAF officer, SUTD Design); full output manually reviewed for quality
3. **5–8 selected best demo cases** — used in every meeting; never live-demo untested inputs
4. **Clean web UI with domain name** — not a Jupyter notebook; institution is lending its name to this
5. **PDPA one-pager** — where data is stored (AWS ap-southeast-1), what is collected, student rights
6. **MOU template (2 pages max)** — free service; one semester; exit clause (2 weeks notice, no obligations)

Pre-training a custom ML model is **NOT required** before the first meeting. Prompt engineering with SG context at inference time is sufficient for pilot-quality output.

### The Persuasion Narrative — What Actually Moves Career Directors

The one argument that reliably moves a career director to say yes to a meeting:

> "Your students need resume coaching at 11pm before application deadlines. Your advisors cannot be there. KeyStone is."

This works because: it is immediately relatable, undeniably true, addressable by the product on Day 1, framed in their operational language (not technology language), and makes no unverifiable AI quality claim.

Secondary argument (after the demo):
> "Your advisors spend 30–40% of their time on basic resume structure reviews. KeyStone handles the first pass. Same team, twice the throughput."

**Do NOT lead with**: outcome tracking data (requires 9 months to demonstrate), competitive comparisons to VMock (unverifiable at this stage), AI quality claims ("our AI is better"), or SG intelligence as the headline.

### Free-to-Paid Realistic Timeline (Based on Comparable Companies)

| Stage | Timeline | What Happens |
|-------|----------|-------------|
| MOU signed (pilot begins) | Month 0–3 | Pilot running; career centre staff using it |
| Semester ends | Month 6–9 | Partial outcome data visible |
| Renewal conversation begins | Month 9–12 | First data in hand for discussion |
| First paid contract signed | Month 18–24 | Realistic for most institutions |

**Aspirational**: "one semester free, then paid contract." **Realistic**: 18–24 months. Plan capital accordingly.

### Reasons Pilots Fail to Convert (Common Failure Modes)

1. No internal champion seeded during pilot — director who sponsored it moves on; successor has no relationship
2. Student adoption under 20% — tool was available but not embedded in workflow or mandatory touchpoint
3. No data to show at renewal conversation — outcome collection was not set up during the pilot
4. Procurement bureaucracy — VMock already has existing SG university relationships; new contracts require displacement argument, not greenfield pitch
5. Price shock — free-to-paid quote was unexpectedly high vs department budget

**Mitigations**:
- Identify two internal champions (director + a career advisor) at each pilot institution
- Design student access to require zero effort from career centre (one forwarded email = live access)
- Build outcome dashboard v1 before pilot starts so collection is automatic from Day 1
- Price the first paid contract below SGD 30K to keep it within director approval threshold

### Pilot offer 
- Free: 200–500 seats for one semester, full feature access, co-branded rollout
- In exchange: structured outcome data consent from students, aggregate reporting back to career centre, reference case study rights
- Commitment required: career centre sends one email to students introducing the tool

### Agency Targets
- Focus on boutique specialist agencies (finance, tech, healthcare) with 5–20 recruiters
- Decision by owner/director; no procurement process
- Value pitch: "Your candidates prepared better → faster placement → more fees per quarter"
- Pricing: SGD 10/seat/month, 3-month minimum; introduce at a career fair or cold LinkedIn outreach

### WSG / Government Channel
- Long-term play (Year 2–3 revenue)
- Monitor GeBIZ for AI career tools RFPs
- Position as the SG-native vendor with outcome data (by Year 2, credible)
- Defensive play if MCF builds competing feature: approach WSG as technology partner ("build it for us")

---

## B2C Acquisition Channels (Organic Only, Year 1)

| Channel | Leverage | Effort | Notes |
|---------|----------|--------|-------|
| University pilot spillover | VERY HIGH | Low (flows from B2B deal) | Students tell classmates; the best organic channel |
| Reddit (r/singapore, r/SGExams, r/askSingapore) | HIGH | Medium | Must be genuinely useful free tier; anti-marketing culture; one organic shot |
| SG career/NS-related Telegram groups | HIGH | Medium | SGX Job Sharing, NUS/NTU/SMU alumni groups; moderator relationship |
| HardwareZone / NS community forums | MEDIUM | Low | NS-framing content ("how to write SAF experience") earns organic shares |
| LinkedIn founder content | MEDIUM | High (ongoing) | Compound channel; slow start |
| Career fair physical presence | MEDIUM | Medium | Year 1 NUS/SMU career fair; direct fresh grad acquisition |
| SkillsFuture / NTUC / e2i partnerships | LOW (Year 1) | High | Government-adjacent; slow to close but real volume when live |
| SEO | LOW (Year 1) | High | 12–18 month payoff; not a Year 1 lever |
| TikTok / Instagram | LOW | High | Wrong ROI for Year 1 effort |
| Product Hunt / HN launch | VANITY | Low | US tech audience; no SG job-seeker conversion |

**What the brief should NOT count on**: paid Google/Facebook acquisition. CAC of SGD 40–80 against LTV of SGD 36–144 is structurally unprofitable for monthly Pro (SGD 36 LTV); viable only for Annual Plan (SGD 144 LTV).

---

## Product-Market Fit Gates (Month 6 Check)

Confirm three of four before scaling or raising capital:

1. **B2B signal**: One paid B2B contract signed OR one pilot with formal written commitment to convert
2. **B2C conversion**: 2–3% paid conversion among non-university users (4% is aspirational; 2–3% trending upward is the real signal)
3. **Engagement**: ≥60% of paid users use KeyStone for ≥3 sessions in their first month (predictor of retention through a full search)
4. **Outcome lift**: Pilot data shows any positive callback rate differential vs career centre's prior baseline (even if not statistically significant at Month 6)

**If only 1–2 gates are true**: do not raise growth capital. Iterate on product and B2B pitch. The SG career-tools market is too small to brute-force.

---

## Competitive Scenario Plans

### Scenario: VMock deepens SG university presence (HIGH probability — already in market)
- VMock is already present in SG universities. The scenario is not "if VMock arrives" but "if VMock adds outcome tracking to its SG deployments."
- Response: race to accumulate outcome data before VMock closes the architectural gap. Every month of delay in reaching 1,000 active users logging outcomes is a month where VMock can potentially start collecting outcomes too.
- Displacement pitch: anchor every university conversation on the one metric VMock cannot provide — "did students who used it get better callback rates?" VMock's ATS-scoring architecture has no answer. KeyStone's outcome tracking is the answer.
- If VMock discounts aggressively to keep a university: offer a dual-tool MOU ("your students use both; let the outcome data speak"). After one semester, outcome differential is the argument.
- Do NOT compete on SMART score or formatting rules — VMock wins the ATS-simulation frame.

### Scenario: LinkedIn ships SG resume AI (30–50% probability, 18 months)
- Response: double down on SG depth (LinkedIn won't localize for SG specifically) and B2B institutional lock-in (LinkedIn does not target career centres)
- Do NOT try to compete on generic AI writing quality — LinkedIn wins that

### Scenario: MCF ships free resume AI (20–40% probability, 24 months)
- Response: approach WSG / GovTech as B2B vendor BEFORE this happens
- Ideal outcome: KeyStone's engine powers MCF's feature (vendor contract, not competitive defeat)
- Fallback: B2B institutional contracts are MCF-independent; university channel is unaffected

### Scenario: Teal or Jobscan localises for SG (Low, 24–36 months)
- Response: institutional relationships and outcome data are not replicable by a US company localising overnight
- If Teal raises a Series B and announces Asia expansion, accelerate B2B signing as fast as possible

---

## Post-PMF Expansion (Year 2+)

Features that address the "what does KeyStone do when I'm employed" LTV problem:
1. **Accomplishment logger** — users log career wins continuously; resume auto-updates on demand
2. **Salary benchmarking** — SG market data by role/company/seniority
3. **Next-role planner** — given current role, what skills/experiences unlock the next jump
4. **Passive job alerts** — "a role matching your profile appeared at DBS, want to tailor your resume?"

These convert KeyStone from a 3–6 month job-search tool into a career-tenure product. Required for LTV > SGD 100. Not in MVP scope.

# AI Job Seeker Copilot — Product Brief

> **Note**: This brief is derived from early-stage analysis notes. Information has not been fully validated and may contain inaccuracies. Treat as a working reference, not a source of truth.

---

## One-Liner

**For job seekers**: An AI-powered resume optimization tool built for Singapore — match your resume to a specific job posting, receive line-by-line revision suggestions, and track your response rate over time.

**For employers & recruiters**: An AI-powered JD writer — generate precise, candidate-attracting job descriptions by learning from what successful candidates look like.

---

## The Problem

Singapore has approximately 300–400K active job seekers annually, including 30–40K fresh graduates. Three pain points remain unsolved by existing tools:

1. **No feedback on resume quality** — Most people write a resume, begin applying, and never learn what is wrong with it.
2. **No visibility into job-specific fit** — Applicants submit to dozens of positions, hear nothing back, and do not know why.
3. **No tool understands Singapore-specific context** — How to frame National Service (NS), whether to include a photo for GLC vs MNC roles, how to handle NRIC on a resume — generic AI tools (e.g., ChatGPT) do not carry this knowledge.

Existing tools are either generic resume templates (not tailored to specific jobs), foreign products (no Singapore context), or resume-only tools with no outcome tracking. No competitor has built **per-job resume optimization + outcome tracking** as a single, cohesive product.

---

## The Product

Users complete four core actions:

### 1. Upload Resume

Supports PDF, Word, and plain text. Analysis completes in approximately 10 seconds, surfacing strengths, weaknesses, and Singapore-specific issues (e.g., NRIC removal recommendation, photo advice per company type, NS description improvements).

### 2. Match Against a Target Job

Paste a job posting URL or description text. The system extracts requirements, compares them against the resume, and returns a four-level match assessment:

| Level           | Colour | Meaning                                  |
| --------------- | ------ | ---------------------------------------- |
| Strong match    | Green  | You have what they want                  |
| Transferable    | Amber  | You have it but have not written it well |
| Addressable gap | Orange | You can bridge it with reframing         |
| Fundamental gap | Red    | This requirement is genuinely missing    |

Supports URL parsing for MyCareersFuture, JobStreet, and other major platforms, plus free-text paste from any source.

### 3. Line-by-Line Revision Suggestions _(Core Value)_

Not generic "improve your resume" advice — suggestions are specific to the target job, presented one at a time. Example:

> _"Change 'responsible for managing a team' to 'led an 8-person cross-functional team across 3 business units, improving reporting efficiency by 30%' — because this role values quantified team leadership."_

> _"Expand your NS service into 'commanded a 200-person unit, responsible for operational planning and resource allocation' — because this is a GLC application where structured leadership experience matters."_

Users review each suggestion, accept / reject / modify, then download a resume tailored for that specific position.

### 4. Track Application Outcomes

Record results for each application — response received, interview stage reached. The system calculates: **"Your response rate is XX%."** The more the user applies through the platform, the more valuable their personal data becomes.

---

## Why Not ChatGPT

| Dimension           | ChatGPT                         | This Product                                                              |
| ------------------- | ------------------------------- | ------------------------------------------------------------------------- |
| Specificity         | Generic resume advice           | Tailored to a specific job posting, line-by-line                          |
| Singapore knowledge | No NS, GLC, MNC understanding   | Built-in Singapore hiring intelligence engine                             |
| Job source          | User describes the job manually | Direct URL parsing and job page extraction                                |
| Outcome tracking    | None                            | Tracks response rate, proves value over time                              |
| Retention           | Use once, leave                 | Data compounds — but value is near zero at launch (cold-start problem)    |
| Bilingual           | English-centric                 | EN / ZH toggle UI _(to be confirmed)_, understands mixed-language resumes |

---

## Why LinkedIn Cannot Do This

LinkedIn will likely add resume suggestions within 12–18 months. Three structural reasons this does not threaten the product:

1. **LinkedIn serves employers, we serve seekers.** 65% of LinkedIn's revenue comes from Talent Solutions (employer side). Helping seekers optimise resumes for non-LinkedIn applications has no commercial value for LinkedIn.
2. **LinkedIn will not send users to competitors.** The product tracks applications on MyCareersFuture, JobStreet, and company career pages — all LinkedIn competitors. LinkedIn will never build cross-platform application tracking.
3. **Singapore depth does not scale globally.** NS framing, GLC interview culture, Singapore education hierarchy — this knowledge is not worth investing in for a global product serving 200+ countries, but it is essential for the Singapore market.

**Bottom line**: LinkedIn will add resume tips, but will not build cross-platform tracking, will not integrate MyCareersFuture, and will not understand Singapore hiring culture. The moat is positioning, not features.

---

## The Market

- **Primary**: 30–40K fresh graduates per year + ~200K active job seekers in Singapore
- **Institutional**: All 6 public universities have career centres with dedicated budgets for employment tools; the government (WSG) invests heavily in career transition programmes
- **Willingness to pay**: Validated — this market is satisfying unmet demand, not creating it

---

## Business Model

### B2C — Individual Users

| Tier  | Price        | Features                                            |
| ----- | ------------ | --------------------------------------------------- |
| Guest | Free         | Upload resume + 1 job match preview                 |
| Free  | Free         | 3 matches/month, see 3 suggestions                  |
| Pro   | SGD 12/month | Unlimited matches, all suggestions, email reminders |

Paid conversion target: 2–5% of active registered users. Pro user gross margin: 82%.

### B2B — Employer / Recruitment Agencies _(Primary Revenue)_

| Client Type          | Pricing          | Description                                  |
| -------------------- | ---------------- | -------------------------------------------- |
| Recruitment agencies | SGD 79–449/month | AI JD generator + candidate quality insights |
| SME HR teams         | SGD 99–299/month | Unlimited JD generation for in-house hiring  |
| Enterprise           | Custom           | White-label JD engine + analytics dashboard  |

**B2B strategy**: Begin with boutique recruitment agencies (5–20 recruiters). Owner/director decides in 2–4 weeks — fastest B2B close cycle. Use agency JD pain ("write 10–50 JDs/day manually") as entry point.

### B2B — Institutional (Universities, WSG)

| Client Type               | Annual Contract   | Description                                                      |
| ------------------------- | ----------------- | ---------------------------------------------------------------- |
| University career centres | SGD 25,000–40,000 | Per-seat licence for graduating class, aggregate outcome reports |
| WSG government programmes | SGD 30,000–80,000 | Career conversion programme licensing                            |

**Note**: University procurement cycle is 9–18 months. B2C + agency revenue must cover burn until institutional contracts close (Month 18–24). Minimum SGD 40K reserves required to cover the B2B-first path to break-even with a 2-month safety buffer.

### Unit Economics

|         | Free User   | Pro User           | B2B Per Seat |
| ------- | ----------- | ------------------ | ------------ |
| Cost    | SGD 0.80/mo | SGD 2.16/mo        | SGD 1.90/mo  |
| Revenue | SGD 0       | SGD 12/mo          | SGD 3–8/mo   |
| Margin  | –SGD 0.80   | +SGD 9.84/mo (82%) | +SGD 1–6/mo  |

---

## Three-Year Projection

|                     | Year 1      | Year 2        | Year 3        |
| ------------------- | ----------- | ------------- | ------------- |
| Registered users    | 5K–8K       | 10K–15K       | 20K–30K       |
| Paying users        | 100–400     | 400–1K        | 1.2K–3K       |
| Institutional deals | 0–2         | 2–4           | 5–8           |
| Annual Revenue      | SGD 20K–72K | SGD 100K–250K | SGD 400K–800K |

**Break-even**: VC-funded path. Year 1 B2C ARR does not cover burn; institutional contracts + seed funding bridge to break-even.

---

## Competitive Moat

1. **Validated AI recommendations through real outcome data** — This is the core differentiator. Generic AI tools (ChatGPT, etc.) can suggest resume improvements, but have no way to know if those suggestions actually work. KeyStone tracks every application outcome (response received, interview reached, offer got), creating a feedback loop that validates which modification patterns lead to better results. By Month 3+, the model learns from aggregate outcome data — which suggestions correlated with higher response rates — and iteratively improves recommendation quality. No competitor can replicate this without actual market participation and PDPA-compliant outcome tracking infrastructure in place.

2. **Know exactly where every application stands** — Job seekers either manually track submissions (most give up after a week) or lose track entirely. KeyStone makes tracking effortless: see every application at a glance, update outcomes with one tap, and watch your response rate improve over time. Tangible value from day one — not an AI feature.

3. **Two-sided data flywheel** — Skill frequency data accumulates from Day 1 (JD writing → skill patterns). Outcome-validated model improvements compound on top of this. The flywheel: users receive suggestions → apply modifications → submit applications → outcomes are tracked → model learns what works → better suggestions → more engagement → richer outcome data. This bidirectional improvement loop activates Month 3+ once B2C application outcome data is flowing under PDPA-compliant consent.

4. **Institutional contracts** — B2B university/agency contracts create 3-year switching costs and lock in outcome data streams that individual competitors cannot access.

---

## Technical Architecture

| Component | Choice                                        | Rationale                                   |
| --------- | --------------------------------------------- | ------------------------------------------- |
| Frontend  | Next.js + Tailwind + shadcn/ui                | Performance, mature component library       |
| Backend   | Python FastAPI                                | AI ecosystem, async support                 |
| Database  | PostgreSQL 16+                                | Relational data, row-level security for B2B |
| AI Engine | Claude Haiku (extraction) + Sonnet (analysis) | Two-tier routing for cost control           |
| Auth      | Clerk                                         | Google OAuth, email, future university SSO  |
| Payments  | Stripe (Singapore)                            | SGD billing, local payment methods          |
| Hosting   | AWS ap-southeast-1                            | Singapore region, PDPA compliance           |

### AI Cost Control Strategy

- **Two-tier model routing**: Haiku for data extraction; Sonnet for deep analysis and suggestions only
- **Aggressive caching**: Resume analysis cached and reused; popular job extractions cached for 7 days
- **Hard cost ceiling**: Max SGD 5/user/month on LLM spend; degrade to cached results when exceeded
- **Measure from Day 1**: Token usage monitoring deployed from the first week

At current pricing, LLM spend represents 15–20% of Pro user revenue — sustainable.

---

## Compliance (PDPA)

Singapore PDPA (equivalent to EU GDPR) is a core design requirement, not an afterthought:

- **Three-stage NRIC masking**: Mask in uploaded files before S3 storage → re-scan before sending to AI API → sanitise AI output before database write
- **Six-type independent consent**: Registration, storage, AI processing, B2B sharing, outcome tracking, marketing — each independently revocable
- **Data stays in Singapore**: All user data on AWS ap-southeast-1; AI provider configured for zero data retention
- **External DPO**: Engage a Singapore-based Data Protection Officer before processing any real user data

---

## Roadmap — Parallel B2C + B2B

| Phase             | Timeline     | B2C (Job Seeker)                                    | B2B (Recruiter/Employer)                              |
| ----------------- | ------------ | --------------------------------------------------- | ----------------------------------------------------- |
| MVP Build         | Months 1–2   | Resume upload + JD match + line-by-line suggestions | JD generator for recruiters (Phase 1 MVP)             |
| Launch + Validate | Months 1–6   | 1.5K–3K registered, 100–250 paying                  | 1–3 agency deals signed, JD tool feedback loop starts |
| Grow              | Months 6–12  | 5K–10K registered, 400–1K paying                    | 5–10 agency deals, early university pilot             |
| Scale             | Months 12–24 | 15K–30K registered, 1.2K–3K paying                  | 3–5 institutional contracts, SGD 200K+ ARR            |

---

## Open Questions (To Be Resolved)

1. **Bilingual feature scope** — The original notes reference "EN/ffff UI", likely a placeholder. Is the second language Mandarin Chinese (EN/ZH)? Malay? Both?
2. **Backend framework** — Original report specifies Python FastAPI. Given the Kailash SDK environment, evaluate whether to use Kailash Nexus / Kaizen / DataFlow to replace some or all custom FastAPI code.

---

_Last updated: 2026-05-07. Pricing corrected to SGD 12/month Pro. Two-sided marketplace strategy confirmed._

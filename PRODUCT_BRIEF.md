# AI Job Seeker Copilot — Product Brief

> **Note**: This brief is derived from early-stage analysis notes. Information has not been fully validated and may contain inaccuracies. Treat as a working reference, not a source of truth.

---

## One-Liner

An AI-powered resume optimization tool built for Singapore job seekers — match your resume to a specific job posting, receive line-by-line revision suggestions, and track your callback rate over time.

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

| Level | Colour | Meaning |
|-------|--------|---------|
| Strong match | Green | You have what they want |
| Transferable | Amber | You have it but have not written it well |
| Addressable gap | Orange | You can bridge it with reframing |
| Fundamental gap | Red | This requirement is genuinely missing |

Supports URL parsing for MyCareersFuture, JobStreet, and other major platforms, plus free-text paste from any source.

### 3. Line-by-Line Revision Suggestions *(Core Value)*
Not generic "improve your resume" advice — suggestions are specific to the target job, presented one at a time. Example:

> *"Change 'responsible for managing a team' to 'led an 8-person cross-functional team across 3 business units, improving reporting efficiency by 30%' — because this role values quantified team leadership."*

> *"Expand your NS service into 'commanded a 200-person unit, responsible for operational planning and resource allocation' — because this is a GLC application where structured leadership experience matters."*

Users review each suggestion, accept / reject / modify, then download a resume tailored for that specific position.

### 4. Track Application Outcomes
Record results for each application — callback received, interview stage reached. The system calculates: **"Your callback rate is XX%."** The more the user applies through the platform, the more valuable their personal data becomes.

---

## Why Not ChatGPT

| Dimension | ChatGPT | This Product |
|-----------|---------|--------------|
| Specificity | Generic resume advice | Tailored to a specific job posting, line-by-line |
| Singapore knowledge | No NS, GLC, MNC understanding | Built-in Singapore hiring intelligence engine |
| Job source | User describes the job manually | Direct URL parsing and job page extraction |
| Outcome tracking | None | Tracks callback rate, proves value over time |
| Retention | Use once, leave | Data compounds — application history becomes a moat |
| Bilingual | English-centric | EN / ZH toggle UI *(to be confirmed)*, understands mixed-language resumes |

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

| Tier | Price | Features |
|------|-------|----------|
| Guest | Free | Upload resume + 1 job match preview |
| Free | Free | 3 matches/month, see 3 suggestions |
| Pro | SGD 12/month or SGD 144/year | Unlimited matches, all suggestions, email reminders |

Paid conversion target: 4–5%. Pro user gross margin: 75%.

### B2B — Institutional Clients *(Primary Revenue)*

| Client Type | Annual Contract | Description |
|-------------|----------------|-------------|
| University career centres | SGD 50,000–100,000 | Per-seat licence for graduating class, aggregate outcome reports |
| WSG government programmes | SGD 30,000–80,000 | Career conversion programme licensing |
| Recruitment agencies | SGD 5–15 / seat / month | White-label candidate preparation tool |

**B2B strategy**: Initiate university conversations from Day 1 (not Month 6). Offer 50 free accounts for one semester as a pilot, then use real outcome data to justify a formal contract. The 6–12 month university procurement cycle means B2C + agency revenue must cover burn until university contracts close (Month 18–24).

### Unit Economics

| | Free User | Pro User | B2B Per Seat |
|--|-----------|----------|--------------|
| Cost | SGD 0.80/mo | SGD 3/mo | SGD 1.90/mo |
| Revenue | SGD 0 | SGD 12/mo | SGD 3–8/mo |
| Margin | –SGD 0.80 | +SGD 9/mo | +SGD 1–6/mo |

---

## Three-Year Projection

| | Year 1 | Year 2 | Year 3 |
|--|--------|--------|--------|
| Registered users | 5K–8K | 20K–35K | 50K–80K |
| Paying users | 200–400 | 1K–2K | 3K–5K |
| Institutional deals | 0–1 | 2–4 | 5–8 |
| Annual Revenue | SGD 21K–50K | SGD 100K–250K | SGD 400K–800K |

**Break-even**: ~300 paying users (SGD 3,600/month) + 1–2 institutional contracts.

---

## Competitive Moat

1. **Proprietary Singapore outcome data** — Application tracking data compounds over time. Who applied where, whether they received callbacks, whether suggestions improved outcomes. This dataset cannot be acquired from public sources and grows more valuable with every user.
2. **Institutional contracts** — Once a university signs, switching costs are high (training, data migration, procurement process). Contracts typically run 1–3 years, providing stable, predictable revenue.
3. **Singapore intelligence engine** — NS framing, GLC/MNC/SME resume conventions, interview culture — this localisation knowledge requires deep understanding of the Singapore employment market and cannot be replicated by a generic global tool.

---

## Technical Architecture

| Component | Choice | Rationale |
|-----------|--------|-----------|
| Frontend | Next.js + Tailwind + shadcn/ui | Performance, mature component library |
| Backend | Python FastAPI | AI ecosystem, async support |
| Database | PostgreSQL 16+ | Relational data, row-level security for B2B |
| AI Engine | Claude Haiku (extraction) + Sonnet (analysis) | Two-tier routing for cost control |
| Auth | Clerk | Google OAuth, email, future university SSO |
| Payments | Stripe (Singapore) | SGD billing, local payment methods |
| Hosting | AWS ap-southeast-1 | Singapore region, PDPA compliance |

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

## Roadmap

| Phase | Timeline | Target |
|-------|----------|--------|
| Build MVP | Months 1–2 | Resume analysis + job matching + application tracking, launch |
| B2C validation | Months 1–6 | 2K–3K registered users, 100–200 paying users |
| B2B pilot | Months 6–12 | 1–2 university pilots, validate outcomes |
| Scale | Months 12–24 | 3–5 institutional contracts, SGD 200K+ ARR |

---

## Open Questions (To Be Resolved)

1. **Bilingual feature scope** — The original notes reference "EN/ffff UI", likely a placeholder. Is the second language Mandarin Chinese (EN/ZH)? Malay? Both?
2. **Backend framework** — Original report specifies Python FastAPI. Given the Kailash SDK environment, evaluate whether to use Kailash Nexus / Kaizen / DataFlow to replace some or all custom FastAPI code.
3. **MVP build sequence** — Which feature ships first: resume analysis only, or resume analysis + job matching together?

---

*Last updated: 2026-04-29. Source: initial project report (unvalidated). All figures are estimates pending market validation.*

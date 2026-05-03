# KeyStone — AI Job Seeker Copilot: Product Brief

> **Caveat**: Derived from early-stage analysis notes. Not fully validated. Treat as working context, not ground truth. All figures are estimates pending validation.

---

## Product

An AI-powered resume optimization tool built for Singapore job seekers. Users upload their resume, paste a job posting URL or description, and receive line-by-line revision suggestions specific to that job. The system tracks application outcomes and computes a personal callback rate over time. Differentiator: deep Singapore-specific hiring intelligence (NS framing, GLC/MNC conventions, NRIC handling) that no generic AI tool provides.

## Objectives

- Solve three unsolved pain points for SG job seekers: no resume feedback, no job-specific match visibility, no Singapore-specific guidance
- Build per-job resume optimization + outcome tracking as a single cohesive product (no competitor has done this)
- Reach break-even at ~800 paying B2C users + 2 university contracts
- Year 1: SGD 45–75K revenue; Year 3: SGD 685K–1.1M ARR

## Tech Stack

- Backend: Python FastAPI (evaluate Kailash Nexus/Kaizen as alternative — TBD)
- Frontend: Next.js + Tailwind + shadcn/ui
- Database: PostgreSQL 16+ (row-level security for B2B multi-tenancy)
- AI: Claude Haiku (data extraction) + Claude Sonnet (analysis + suggestions) — two-tier cost routing
- Auth: Clerk (Google OAuth, email, future university SSO)
- Payments: Stripe Singapore (SGD billing)
- Hosting: AWS ap-southeast-1 (Singapore region, PDPA compliance)

## Constraints

- Singapore PDPA compliance required: three-stage NRIC masking, six-type independent consent, data stays in SG region
- AI cost ceiling: max SGD 5/user/month LLM spend; degrade gracefully when exceeded
- Zero data retention with AI provider (Claude API config)
- External DPO must be engaged before processing real user data
- B2B row-level security: university/WSG/agency data must not cross tenant boundaries

## Users

### B2C Users
- **Job seeker (primary)**: Singapore resident actively applying for jobs — fresh graduate (22–28) or mid-career switcher (28–40). Uploads resume, targets specific jobs, reviews suggestions, tracks outcomes.
- **Guest**: One-time visitor. Can upload resume and see 1 job match preview. No account required.

### B2B Users
- **University career centre admin**: Purchases institutional licence. Manages student accounts, accesses aggregate outcome reports.
- **Student (B2B-provisioned)**: Same as job seeker but provisioned via university. May have extended Pro features.
- **WSG programme participant**: Career conversion candidate, provisioned via government contract.
- **Recruitment agency recruiter**: Uses white-label version to prepare candidates.

### Internal / System Roles
- **Platform admin**: Manages all tenants, billing, monitoring.

---

## Core Feature Set

### 1. Resume Upload + Analysis
- Supports PDF, Word, plain text
- ~10s analysis time
- Output: strengths, weaknesses, Singapore-specific flags
  - NRIC present → remove recommendation
  - Photo advice: include for GLC, omit for MNC (heuristic)
  - NS description quality assessment

### 2. Job Match (Four-Level Assessment)
- Input: URL (MyCareersFuture, JobStreet, company pages) or pasted JD text
- Extracts: required skills, experience level, company type, role type
- Output per requirement: Strong (green) / Transferable (amber) / Addressable (orange) / Fundamental gap (red)

### 3. Line-by-Line Revision Suggestions (Core Value)
- Specific to this job, this company type (GLC/MNC/SME)
- One suggestion at a time: original text → suggested rewrite + rationale ("because this GLC values structured leadership")
- User: accept / reject / modify each
- Download: tailored resume for this specific application

### 4. Application Outcome Tracking
- User records result per application: no response / callback / interview stage / offer
- System computes: callback rate, trend over time
- Data compounds — more applications = more accurate personal benchmark

---

## Business Model

### B2C Tiers
| Tier | Price | Features |
|------|-------|----------|
| Guest | Free | Upload + 1 match preview |
| Free | Free | 3 matches/month, 3 suggestions visible |
| Pro | SGD 19/mo or SGD 180/yr | Unlimited matches, all suggestions, email reminders |

Paid conversion target: 4–6%. Pro gross margin: 84%.

### B2B Tiers
| Client | Annual Contract |
|--------|----------------|
| University career centres | SGD 50–100K |
| WSG government programmes | SGD 30–80K |
| Recruitment agencies | SGD 5–15/seat/month |

B2B strategy: Day 1 university outreach. Free 50-seat pilot (1 semester). Outcome data justifies formal contract.

---

## Competitive Positioning

- **vs ChatGPT**: No job specificity, no SG knowledge, no URL parsing, no outcome tracking
- **vs LinkedIn**: Serves employers (65% Talent Solutions revenue); won't cross-track MCF/JobStreet; no SG depth at scale
- **vs Generic tools (Resume.io, Kickresume)**: No SG context, no job-specific suggestions, no outcome loop

Moat: (1) proprietary SG outcome data, (2) institutional lock-in, (3) Singapore intelligence engine irreplicable by global players

---

## Analysis Required

Perform full feasibility analysis across:
1. **Market size** — TAM/SAM/SOM with data and sources
2. **User pain points** — depth validation: is the problem real, acute, and underserved?
3. **Competitors** — direct, indirect, platform risk (LinkedIn, Indeed, JobStreet, government tools, MCF)
4. **How to win** — GTM strategy, distribution channels, defensibility timeline
5. **Pricing rationale** — Is SGD 19/mo correct? Are B2B tiers correctly sized? What does the market bear?
6. **Value proposition** — Sharpest version of the pitch. What is the one thing users will pay for?

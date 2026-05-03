# Market Size Analysis — KeyStone (Singapore AI Resume Copilot)

> **Data provenance**: All figures are from training data (knowledge cutoff August 2025) or estimated from public sources. Every number is labeled: [TRAINING DATA], [ESTIMATED], or [CONFIRMED — cite source]. No live data was fetched. Treat all figures as working estimates requiring validation before business decisions.

---

## Summary Verdict

The Singapore market is real, bounded, and accessible. The TAM is small by global standards (~SGD 15–25M addressable B2C and institutional spend), but the SAM is achievable and the SOM in Year 1 is realistic. The risk is not market size — it is conversion rate and churn. The SG-specific moat is defensible if institutional data compounds before a well-funded global player localizes.

---

## 1. Labor Market Context

### Active Job Seeker Pool (Primary Target)

| Metric | Figure | Source / Confidence |
|--------|--------|---------------------|
| Singapore resident labor force | ~3.6M | [TRAINING DATA — MOM 2023] |
| Annual job change rate (estimate) | ~15–18% of workforce | [ESTIMATED — based on MOM voluntary cessation data] |
| Annual active job seekers (all types) | ~540,000–650,000 | [ESTIMATED — derived above] |
| Fresh graduates entering workforce annually | ~30,000–35,000 | [TRAINING DATA — MOE 2023 graduate cohort] |
| Mid-career professionals in transition | ~80,000–100,000 | [ESTIMATED — extrapolated from MOM retrenchment + voluntary exit data] |
| Involuntary job seekers (retrenchment) | ~10,000–20,000/year | [TRAINING DATA — MOM retrenchment 2022-2023 range] |

**Critical: Not all job seekers are resume-optimizers.** The addressable pool is people who (a) are actively applying for jobs, (b) use digital tools, and (c) feel their resume is a bottleneck. That filter removes a large portion of the labor force — particularly blue-collar workers, hawker owners, and workers in labor-heavy sectors.

**Realistic digitally-engaged job seeker pool**: ~150,000–250,000/year
- This is the segment that would plausibly use an AI resume tool
- Basis: high SG internet penetration (~92%), but exclude sectors with minimal resume culture

---

## 2. TAM — Total Addressable Market

### B2C TAM

The theoretical upper bound: every digitally-engaged SG job seeker pays SGD 19/month for the full year.

| Scenario | Pool | Monthly Price | Duration | TAM |
|----------|------|---------------|----------|-----|
| Conservative | 150,000 seekers | SGD 19 | 3 months avg search | SGD 8.6M/year |
| Base | 200,000 seekers | SGD 19 | 3 months | SGD 11.4M/year |
| Optimistic | 250,000 seekers | SGD 19 | 4 months | SGD 19M/year |

**Data quality: [ESTIMATED]**. Duration of "active job search" in Singapore is not published. The 3–4 month figure is an estimate based on MOM vacancy fill times and anecdotal data from career counselor reports.

**Warning**: TAM figures for SaaS are often computed incorrectly. The 150,000–250,000 pool is people who ARE job seeking, not people who would necessarily pay SGD 19/month for resume help. That conversion is the real question.

### B2B TAM

| Segment | Institutions | Contract Range | TAM Estimate |
|---------|-------------|----------------|--------------|
| Local universities (NUS, NTU, SMU, SIT, SUTD, UniSIM) | ~8 | SGD 50–100K/year | SGD 400K–800K |
| Polytechnics (5 main polys) | ~5 | SGD 20–40K/year | SGD 100K–200K |
| ITEs | ~3 | SGD 10–20K/year | SGD 30–60K |
| WSG (Workforce Singapore) programmes | 1 (central) | SGD 30–80K/year | SGD 30–80K |
| Recruitment agencies (top-tier) | ~50–100 active agencies | SGD 5–15/seat/month | SGD 300K–900K/year at full penetration |

**Total B2B TAM: ~SGD 860K–2M/year** [ESTIMATED]

This is deliberately conservative. There are ~200+ registered employment agencies in Singapore but most are small (< 10 recruiters) and unlikely to adopt expensive per-seat software.

**Data quality: [TRAINING DATA]** for institution counts; [ESTIMATED] for contract values.

---

## 3. SAM — Serviceable Addressable Market

SAM = what KeyStone can realistically serve given its SG focus, feature set, and distribution strategy.

### B2C SAM

Constraints applied:
- English-language platform (excludes Mandarin-dominant users who would prefer Chinese-language tools) — reduces pool ~15–25%
- "Resume-obsessed" segment: people who are actively iterating on their resume, not passive browsers
- Digital payment capability (Stripe SGD) — eliminates fringe

**B2C SAM estimate: ~30,000–60,000 users/year** [ESTIMATED]

Reasoning: Empirically, 15–25% of active job seekers in English-proficient markets engage deeply enough with their resume to iterate on it digitally. That applied to 200,000 baseline gives ~30,000–50,000.

At 4–6% paid conversion (brief's target) → 1,200–3,000 paying users.

### B2B SAM

Constraints applied:
- Universities with active career centres and budget authority (NUS, NTU, SMU most likely; SIT, SUTD plausible; UniSIM uncertain)
- WSG: one contract but potentially large if programme-wide

**B2B SAM: 3–6 institutions Year 1, growing to 10–15 by Year 3** [ESTIMATED]

---

## 4. SOM — Serviceable Obtainable Market

What the brief claims to be targeting:

| Year | B2C | B2B |
|------|-----|-----|
| Break-even | ~800 paying users | ~2 university contracts |
| Year 1 Revenue | SGD 45–75K | Included |
| Year 3 Revenue | SGD 685K–1.1M ARR | Included |

### Stress Test: Is Break-Even Realistic?

**800 paying B2C users at SGD 19/month = SGD 182,400 ARR**
Plus 2 university contracts at SGD 50–100K each = SGD 100–200K

That's SGD 282–382K gross revenue — more than the brief's break-even figure implies. Either the break-even is referring to operational break-even at lower revenue, or the figure needs rechecking.

**[FLAG]**: The brief states "break-even at ~800 paying B2C users + 2 university contracts" but does not specify the cost structure. At SGD 19/month × 800 users = SGD 182K B2C ARR. If the two university contracts are at median (SGD 75K each), total = ~SGD 332K. Whether that's break-even depends entirely on infrastructure, salary, and LLM cost. This needs a cost model, not just a revenue figure.

### Year 1 Revenue Target (SGD 45–75K)

This implies:
- ~197–329 paying users at SGD 19/month for full year, OR
- A mix of paying users + partial B2B contract value recognized in Year 1

**This is an underperformance of the 800-user break-even target** — it may reflect a phased ramp (launch mid-year, end year at 400 paying users, average 200 for the year).

**[ESTIMATED]**: The Year 1 figure appears to assume launch around mid-2025 with slow Q1 ramp. If launch is Q1 2026, the full-year target of 800 paying users is achievable by Q4 2026 with a reasonable growth curve (~30 new paying users/month after Month 3).

---

## 5. Market Growth Dynamics

### Favorable Tailwinds

- **SG government push on upskilling**: SkillsFuture has normalized the idea of paid career support [TRAINING DATA — MOF Budget 2023, SkillsFuture credits]
- **Rising graduate unemployment anxiety**: NUS/NTU/SMU graduates increasingly report competitive entry-level market [TRAINING DATA — ST/CNA reporting 2023-2024]
- **AI awareness**: Singapore has among the highest AI tool adoption rates in Southeast Asia [TRAINING DATA — various digital economy reports]
- **MCF as national job board**: MyCareersFuture is mandated for Fair Consideration Framework roles — concentrated job listing surface makes scraping/parsing tractable [TRAINING DATA — MOM FCF 2023]

### Unfavorable Factors

- **Small absolute market**: Singapore has 3.6M workers. Even at best case, the B2C TAM is ~SGD 20M. A US product with 0.1% penetration of the US market would dwarf this.
- **Price sensitivity**: SGD 19/month is ~0.7% of median monthly income. Not prohibitive, but SG consumers are value-conscious for digital subscriptions.
- **Job search seasonality**: Concentrated graduation periods (July–August, December–January) mean demand spikes. A flat subscription model may not capture peak willingness-to-pay.
- **Government competition risk**: WSG's Careers Connect and SGUnited Careers programmes provide free career guidance. If they incorporate AI tools, the B2C segment could be undercut. [TRAINING DATA — WSG programme descriptions 2023]

---

## 6. Key Assumptions to Validate

| Assumption | Risk if Wrong | How to Validate |
|------------|---------------|-----------------|
| 4–6% paid conversion of free users | If < 2%, break-even recedes significantly | Early free-tier cohort data, pricing A/B test |
| Average job search duration 3–4 months | If < 2 months, LTV drops substantially | Interview 30 recent SG job seekers |
| Universities have budget authority to contract SGD 50–100K for software | Many NUS/NTU budget cycles are 9–12 months | Exploratory meeting with career centre director |
| MCF URL parsing is reliable and stable | MCF may change structure; not a public API | Prototype parser, test against 100 live listings |
| SGD 5/user/month LLM cost ceiling is sufficient for typical usage | Claude Sonnet per-token costs may exceed this for heavy users | Model actual Haiku/Sonnet cost per analysis run |
| NS framing heuristics are meaningfully better than ChatGPT | If users don't perceive quality difference, no SG moat | Blind comparison study with 20 SG male job seekers |

---

## 7. Revenue Projections — Annotated

The brief's figures (Year 1: SGD 45–75K; Year 3: SGD 685K–1.1M ARR) are credible IF:

- B2B contracts close within Year 1 (they take 6–12 months to negotiate for universities)
- Paid conversion holds above 4%
- Churn stays below 15%/month (job seekers churn fast — they get jobs or give up)

**The Year 3 upper-bound (SGD 1.1M ARR) requires:**
- ~2,000–2,500 B2C paying users at SGD 19/month = ~SGD 570K
- ~6–8 institutional contracts at SGD 50–80K = ~SGD 400–640K
- OR heavier weighting on B2B (fewer users, higher contract values)

This is achievable. It is not guaranteed. The B2B path is more capital-efficient but slower to close.

---

## Data Quality Scorecard

| Section | Confidence | Notes |
|---------|-----------|-------|
| Labor force figures | Medium | MOM data reliable but job-seeker subset is estimated |
| Paid conversion rate | Low | No SG-specific comparables found; US benchmarks may not apply |
| B2B contract values | Low | No public procurement data for SG university software contracts |
| LLM cost per user | Low-Medium | Depends heavily on usage patterns not yet observed |
| Market growth rate | Medium | Tailwinds real but timing uncertain |

---

*Analysis date: 2026-04-29. All figures require validation against live market data before fundraising or business plan finalization.*

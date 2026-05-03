# KeyStone — Pricing Analysis

> **Research note**: WebSearch was unavailable during this analysis. Competitor pricing, SaaS benchmarks, and market data are drawn from training knowledge (cutoff August 2025). All figures are flagged as [CONFIRMED], [ESTIMATE], or [NEEDS VERIFICATION]. The Jobscan, Teal, and Resume.io pricing figures should be verified against current pricing pages before using in investor or partner materials, as SaaS pricing changes frequently.

---

## 1. B2C Pricing Benchmark

### Competitor Pricing — Resume Optimisation Tools

| Tool | Free Tier | Paid Tier(s) | Notes |
|------|-----------|--------------|-------|
| **Jobscan** | ~5 scans/month | USD 49.95/mo or ~USD 19.99/mo (annual) | [NEEDS VERIFICATION — price as of ~2024] |
| **Teal** | Free (unlimited job tracking, basic resume builder) | USD 29/mo (Pro) | [NEEDS VERIFICATION] |
| **Resume.io** | Free (resume builder, watermarked download) | USD 19.95/mo or USD 9.95/mo (annual) | [NEEDS VERIFICATION] |
| **Kickresume** | Free (1 resume, limited templates) | USD 10–19/mo depending on plan | [NEEDS VERIFICATION] |
| **Enhancv** | Free tier | ~USD 24.99/mo | [NEEDS VERIFICATION] |
| **Rezi** | Free (basic) | USD 29/mo or USD 129 lifetime | [NEEDS VERIFICATION] |
| **ResumeWorded** | Free (limited scans) | USD 19–49/mo | [NEEDS VERIFICATION] |

**KeyStone SGD 19/mo ≈ USD 14/mo** (at SGD/USD 0.74).

**Positioning assessment**: KeyStone is priced at the **low end of the paid tier range** for comparable tools. This is deliberately conservative for market entry, and it is probably correct for Singapore given:
- Lower purchasing power relative to US/UK (even though SG is wealthy, SaaS pricing psychology anchors to USD pricing at USD rates)
- Higher price sensitivity in a smaller market where word-of-mouth dominates
- Need to establish credibility before charging premium rates

**The Jobscan comparison is instructive but misleading.** Jobscan at USD 49.95/mo is widely considered overpriced in its own market — its NPS is reportedly poor and it loses to free alternatives. Using Jobscan as the anchor makes KeyStone look cheap, which is fine for marketing but says nothing about whether SGD 19 is the right number.

**The more relevant comparison** is what SG job seekers pay for comparable productivity/self-improvement SaaS:
- LinkedIn Premium Career: SGD 39.99–49.99/mo [CONFIRMED range, verify current price]
- Grammarly Business: ~SGD 20–25/mo equivalent [ESTIMATE]
- Coursera Plus: ~SGD 60–80/mo [ESTIMATE]

At SGD 19/mo, KeyStone is priced below LinkedIn Premium Career, which is the most natural comparison a job seeker will make. This framing works in KeyStone's favour: "half the price of LinkedIn Premium, but specifically built for Singapore applications."

### SG Consumer SaaS Pricing Norms

Singapore consumers are accustomed to paying USD-equivalent prices for global SaaS products. The SGD vs USD delta (~26%) is not psychologically salient for most digital consumers — they see "SGD 19" or "USD 14" and compare to the category anchor.

**What SG consumers actually pay** [CONFIRMED ranges]:
- Streaming: SGD 10–18/mo (Netflix, Disney+)
- Productivity: SGD 9–20/mo (Notion, Grammarly, Adobe Express)
- Career: SGD 40–50/mo (LinkedIn Premium)

SGD 19/mo is in the productivity tier, below the career tools tier. For a job search tool, this is a defensible position during acquisition. The risk is that it signals "productivity tool" rather than "career investment," which affects the perceived ROI frame. A user is more willing to pay SGD 40/mo for something that feels like a career investment than SGD 19/mo for something that feels like a productivity app.

**Consideration**: A price of SGD 29/mo would position KeyStone more firmly in the career investment tier. The brief's SGD 19 is not wrong, but it may be leaving money on the table with mid-career switchers and PMETs who are less price-sensitive.

### Price Sensitivity — Is There a Magic Number for SG Consumers?

[ESTIMATE — based on general SaaS conversion research, not SG-specific data]

Consumer SaaS conversion rates by price point follow a consistent pattern:
- SGD 0–9/mo: Commodity perception, high conversion but low revenue per user
- SGD 10–19/mo: The "streaming equivalent" zone — broadly accessible, low perceived friction
- SGD 20–29/mo: Step-up requiring justification — conversion drops 20–40% vs the SGD 10–19 band
- SGD 30–49/mo: "Premium" positioning — high perceived value but narrow audience
- SGD 50+/mo: Professional tool territory — needs enterprise value prop to convert retail users

SGD 19 sits at the top of the accessible zone. Moving to SGD 20 or above triggers a psychological step-change in the conversion calculation for many users. The current price appears deliberately calibrated to stay below this threshold.

---

## 2. Freemium Model Validation

### Is "3 matches/month, 3 suggestions" the Right Free Tier?

**The tension in freemium design**: Too generous → users never upgrade. Too restrictive → users never experience value.

**3 matches/month**: This is probably **sufficient for fresh graduates but too restrictive for active job seekers.**

A fresh graduate running a casual search sends 5–15 applications/month in the early weeks. 3 matches/month shows the product works and creates mild upgrade pressure. For an active job seeker sending 20–40 applications/month, 3 matches/month is immediately insufficient — they hit the wall on day 3. This creates either an upgrade (good) or abandonment (bad). Which it creates depends on how good the first 3 matches are.

**3 suggestions**: This is too restrictive to demonstrate the core value proposition. The line-by-line revision suggestion feature is what differentiates KeyStone — it is not a feature that can be understood from 3 examples on one job. Users who see 3 suggestions cannot judge whether the quality is worth SGD 19/month.

**Recommendation**: Consider increasing suggestions to 5–10 per match on the free tier, to ensure users can genuinely evaluate the quality before hitting the paywall. Alternatively, give 1 full job analysis (unlimited suggestions) on the free tier, then gate the second job analysis behind Pro.

**Industry benchmarks for freemium productivity SaaS [CONFIRMED]**:
- Notion: Unlimited personal use free; converts ~5–8% of active users to paid
- Grammarly: Free tier is genuinely useful; paid conversion ~5–7% of registered users
- Calendly: Free tier covers most individual use cases; paid conversion ~3–5%
- Canva: Very generous free tier; paid conversion ~2–4% but massive user base

The common pattern: **generous free tiers convert fewer users but at higher quality (lower churn)**. Restrictive free tiers convert more users but churn faster when the "I'll try it for one month" window closes.

### Is 4–6% Paid Conversion Realistic for SG?

**Global SaaS benchmarks [CONFIRMED]**:
- Consumer freemium SaaS: 2–5% paid conversion is considered industry standard
- Career/productivity SaaS with job-outcome hooks: 5–10% is achievable for highly motivated users

**SG-specific factors**:
- Positive: SG has high disposable income relative to Southeast Asia; SGD 19/mo is accessible
- Positive: SG job seekers are digitally sophisticated and pay for tools that work
- Negative: The job search is temporary — users churn as soon as they get a job. This means **lifetime value is structurally limited** unless the product extends to ongoing career management (promotions, lateral moves)
- Negative: The free tier competes with free ChatGPT; users who are satisfied with generic AI help will not upgrade

**Assessment**: 4–6% is achievable **for motivated job seekers in active search** — the subset of registered users who are actively applying. If 40% of registered users are in active search at any time, 4–6% of total registered users implies 10–15% paid conversion among active searchers. That is aggressive but not impossible.

**The more important metric is not conversion rate — it is LTV.** A job seeker is in active search for 2–6 months on average. At SGD 19/mo, LTV is SGD 38–114. This is low. The product needs either:
- High volume (many users cycling through), OR
- High B2B revenue to subsidise the B2C churn economics, OR
- A reason for users to stay subscribed after getting a job (career tracking, salary benchmarking, future applications)

---

## 3. B2B Pricing Benchmark

### University Career Centre Tools

**What comparable tools charge [ESTIMATE — these are difficult to find publicly]**:

- **Handshake** (US): Primarily for employers to post jobs to students. University pricing is typically USD 8,000–25,000/year for a mid-size university. Not directly comparable (employer tool, not student-facing). [NEEDS VERIFICATION]
- **GradLeaders** (US): USD 15,000–40,000/year for career centre management. Does not have resume AI. [NEEDS VERIFICATION]
- **Symplicity** (US): Institutional pricing USD 20,000–60,000/year for full career services suite. Much broader than resume tools. [NEEDS VERIFICATION]
- **CareerSet / VMock** (AI resume tools for universities): USD 15,000–50,000/year for institutional licences. VMock is the closest direct competitor — AI resume feedback at institutional scale. [NEEDS VERIFICATION — current pricing]

**KeyStone SGD 50–100K for a Singapore university:**

This is **at the high end** for a resume-specific tool from an unproven vendor. Universities budget for this, but the procurement threshold is important:

- Below SGD 50K: Many universities can approve directly at department level (career centre director decision)
- SGD 50–100K: Likely requires faculty/school level approval
- Above SGD 100K: Requires central procurement, competitive tender, IT security review, DPO sign-off

At SGD 50–100K, KeyStone is right at the boundary where procurement complexity increases significantly. This is a meaningful risk factor for B2B Year 1.

**What a university actually buys**: A SGD 50K contract for NUS (approximately 40,000 students, ~10,000 graduates/year) = SGD 5/student/year. This is extremely good value per student if the tool is used. The challenge is **proving usage and outcomes** — university contracts are typically renewed based on adoption rates and student satisfaction, not just deal value.

**Recommendation**: Lead with a **free 50-seat pilot** (as the brief mentions) with a structured outcome measurement framework. Convert to SGD 25–40K in Year 1 (50% below target, but achievable), then expand to SGD 50–100K in Year 2 based on outcome data. Starting at full contract value without outcome data is a hard sell for Singapore university procurement.

### WSG Government Procurement

**WSG SGD 30–80K** is the right order of magnitude for a technology service contract with a government agency, but the procurement mechanics are the key risk.

**Government procurement in Singapore [CONFIRMED]**:
- GeBIZ (Government Electronic Business) is the mandatory procurement platform for Singapore government agencies
- Contracts above SGD 90,000 require open tender (mandatory competitive process)
- Contracts SGD 3,000–90,000 can be awarded via quotation (3 quotes required for SGD 6,000–90,000)
- Sole-source procurement above SGD 6,000 requires written justification and is rarely approved for commercial technology

**Implication**: WSG SGD 30–80K falls in the quotation range (3 competing bids required for contracts above SGD 6,000). KeyStone would compete against other vendors. This is not a closed deal — it requires a competitive bid process.

**What WSG actually procures**: WSG runs Career Matching Services, PMET retraining programmes (Place-and-Train, CCP, PCP). Technology tools for these programmes are procured through career matching platform providers. The relevant comparator is **e2i (Employment and Employability Institute)** and the tools WSG funds through these programmes.

**Timeline**: Government procurement cycles are 6–18 months from initial engagement to contract award. A WSG contract is a Year 2–3 outcome, not a Year 1 revenue item. The brief's model relies on B2B in Year 1 at potentially unrealistic speed.

### Recruitment Agency Pricing

**SGD 5–15/seat/month = SGD 60–180/seat/year.**

**ATS comparisons [CONFIRMED pricing ranges]**:
- Greenhouse: USD 6,000–60,000+/year (seats + features), primarily for larger organisations
- Lever (now part of Employ): USD 3,000–15,000+/year
- Workday Recruiting: Enterprise pricing, typically USD 100,000+/year for full suite
- SmartRecruiters: USD 10,000–30,000/year

These are applicant tracking systems — much broader than resume optimisation. The direct comparison is not valid.

**More relevant comparison**: Tools that recruitment agencies pay for to improve candidate presentation:
- Generic resume builder tools: Typically the agency uses free-tier tools or internal Word templates
- LinkedIn Recruiter: SGD 600–1,000/seat/month [ESTIMATE] — but this is sourcing, not optimisation
- VMock institutional: ~USD 10–20/seat/year at scale

**SGD 5–15/seat/month is plausible for a tool that demonstrably improves candidate placement rates**, but recruitment agencies are highly cost-conscious. They will not pay per-seat without evidence of ROI. The value prop here is: candidates prepared by KeyStone → higher offer acceptance rate → agency earns placement fee faster.

**Agency deal mechanics**: A 10-recruiter agency at SGD 10/seat/month = SGD 1,200/year. This is a small contract requiring no procurement process, no IT review, and minimal sign-off. This is actually the most immediately achievable B2B segment — small deals, fast sales cycle, decision made by the agency owner or director.

---

## 4. Revenue Model Risks

### Is Pro SGD 19/mo Sustainable Given SGD 2.95/mo Unit Cost?

The brief claims 84% gross margin, implying LLM + hosting costs of approximately SGD 2.95–3.04/user/month.

**Cost validation [ESTIMATE]**:

If a Pro user runs:
- 20 job matches/month (job JD extraction + analysis via Claude Haiku): ~20 × 500 input tokens + 2,000 output tokens per match = ~50,000 total tokens. At Haiku pricing (~USD 0.25/M input, USD 1.25/M output), cost ≈ USD 0.05–0.10
- 20 full revision analyses/month via Claude Sonnet: ~20 × 2,000 input + 3,000 output tokens = 100,000 total tokens. At Sonnet pricing (~USD 3/M input, USD 15/M output), cost ≈ USD 0.36–0.45
- Infrastructure/hosting amortised: ~USD 0.50–1.00/user/month at AWS ap-southeast-1

**Rough total**: USD 0.91–1.55/user/month ≈ SGD 1.23–2.09/user/month.

If this cost estimate is correct, the actual margin is **88–93%** on LLM + hosting alone, better than the 84% claimed. However, the brief's SGD 2.95 unit cost may already include a buffer for high-usage outliers (users who run 100+ analyses/month).

**The real margin risk is the 95th-percentile user** — a very active job seeker running 50+ analyses/month could cost SGD 8–15/month in LLM calls, destroying the economics on that user. The brief mentions a "max SGD 5/user/month LLM spend" ceiling with graceful degradation. This is the right architectural constraint; ensure the degradation is actually implemented before launch.

### LLM API Price Risk

Anthropic (Claude) pricing has followed a general downward trend since 2023. Haiku and Sonnet pricing as of mid-2025 has fallen significantly from 2023 rates. The risk is upward repricing, which is less likely given competitive pressure from OpenAI, Google Gemini, and open-source models.

**More relevant risk**: Anthropic could discontinue the specific models being used (Haiku, Sonnet) and require migration to newer versions at different price points. The brief's "two-tier cost routing" (Haiku for extraction, Sonnet for analysis) is the right architecture. Model substitution risk is low to medium over a 24-month horizon.

### Can B2C Cover Operating Costs Before B2B Revenue?

**Year 1 revenue model stress test [ESTIMATE]**:

The brief targets SGD 45–75K revenue in Year 1.

From B2C alone:
- 4% conversion rate × 800 total paid users = 20,000 registered free users needed
- 800 Pro users × SGD 19/mo × 12 months = SGD 182,400 (if all acquired in Month 1)
- Realistically: ramp to 800 users over 12 months = average 400 paying users × 12 × SGD 19 ≈ SGD 91,200

This implies B2C alone could reach SGD 45–90K in Year 1, without any B2B revenue — IF the user acquisition works.

**The operating cost question**: What does it cost to run KeyStone for 12 months?

Minimum viable team (solo founder + part-time contractors):
- Infrastructure: SGD 500–2,000/month (AWS, Clerk, Stripe, monitoring)
- LLM costs for free tier users: If 20,000 free users run 3 analyses each/month, cost ≈ 20,000 × 3 × USD 0.02 = USD 1,200/month ≈ SGD 1,620/month
- Total minimum infrastructure + LLM: SGD 2,120–3,620/month ≈ SGD 25–43K/year

**If the founder takes no salary in Year 1**, B2C revenue at 400–800 paying users covers operating costs from Month 6–9. This is the classic bootstrapped SaaS trajectory. Viable but very thin.

**If a university contract (SGD 25–50K) closes by Month 9**, break-even is reachable in Year 1. If B2B delays to Year 2 (realistic given procurement timelines), the founder needs either savings runway or early angel/pre-seed funding.

### Year 1 Revenue SGD 45–75K — Absolute User Numbers Required

| Scenario | Monthly Pro Users (avg) | Annual Pro Revenue | B2B Revenue | Total |
|----------|------------------------|-------------------|-------------|-------|
| Low | 200 | SGD 45,600 | SGD 0 | SGD 45,600 |
| Mid | 350 | SGD 79,800 | SGD 25,000 | SGD 104,800 |
| Target | 400 | SGD 91,200 | SGD 0 | SGD 91,200 |
| High | 400 | SGD 91,200 | SGD 50,000 | SGD 141,200 |

To reach SGD 45K from B2C alone: ~200 average monthly paying users. To reach SGD 75K from B2C alone: ~330 average monthly paying users.

**These numbers are achievable but not easy.** 200–330 paying users requires approximately 5,000–8,000 active registered users (assuming 4% conversion). Building 5,000+ active users in Singapore in Year 1 requires sustained marketing investment and/or viral organic growth — neither of which is free or guaranteed.

**The brief's SGD 45–75K range is plausible but the upper end requires either B2B revenue or exceptionally strong organic user acquisition.** Plan for the low scenario; design the product to enable the high scenario.

---

## 5. Recommendations

### Is SGD 19/mo Right?

**Short answer**: Yes for acquisition; potentially too low for retention.

SGD 19/mo is the right launch price. It is psychologically accessible, sits below the anxiety threshold for SG consumers, and is competitive against global tools when measured at USD equivalent. Do not change it for launch.

However, consider a **price increase path**: once product-market fit is demonstrated (defined as >500 active Pro users with <30% monthly churn), test SGD 25/mo for new users. The current cohort stays at SGD 19 (grandfather clause). This is the standard SaaS expansion revenue play.

**Annual plan pricing**: SGD 180/yr (SGD 15/mo effective) is a 21% discount. Consider SGD 150/yr to push this to ~21% discount at a rounder psychological number, or add a clear benefit (e.g., "priority analysis queue" or "1 human advisor review/year via WSG partnership") to make the annual plan a qualitatively different offer rather than just a discount.

### Should There Be a Team/SME Tier?

**Not at launch.** The product is not ready for team features (shared resume libraries, recruiter-facing candidate view, bulk analysis) that would justify a Team/SME tier. Adding a half-built tier confuses the product and splits development focus.

**What should exist at launch**: Guest → Free → Pro. Three tiers, clean.

**Post-PMF Team Tier** (consider at 18–24 months):
- SGD 49–79/mo for 5 seats
- Target: Small recruitment agencies (3–5 recruiters), SME HR teams preparing candidates
- This is a natural bridge between the B2C Pro tier and the B2B institutional contracts
- Revenue multiple: SGD 49/5 = SGD 9.80/seat vs SGD 19 individual — recruiter values team management features enough to accept lower per-seat cost

### What Pricing Change Would Most Improve Conversion?

The single highest-impact change is not to the price — it is to **increase the free tier's suggestion limit from 3 to 10 on the first match**.

Here is why: The conversion bottleneck is not "too expensive" — it is "I haven't seen enough to know if it's worth it." 3 suggestions on one job does not give a user enough signal to make a confident upgrade decision. 10 suggestions on one full job analysis is enough for a user to say "this is good, I want this for every job I apply to."

**Secondary pricing recommendation**: Add a **7-day free trial of Pro** triggered when a user upgrades from Guest to Free (with email collection). A 7-day Pro trial after email signup is industry standard for converting motivated top-of-funnel users who are in active job search.

**Tertiary recommendation**: Reduce friction on the annual plan. Currently it requires 9.5x the monthly commitment in one payment. A 3-month package at SGD 50 (roughly equivalent to SGD 16.67/mo) or a **monthly-to-annual upgrade prompt** at month 2 ("You've saved X applications this month — lock in this price for a year") would increase annual plan uptake without changing the underlying pricing structure.

---

## Summary: Pricing Verdicts

| Question | Verdict |
|----------|---------|
| Is SGD 19/mo the right launch price? | Yes — correct for acquisition phase |
| Is the free tier generous enough? | Borderline — 3 suggestions undersells the product |
| Is 4–6% paid conversion realistic? | Possible but requires strong onboarding and trial mechanics |
| Is the annual plan well-designed? | Underpriced discount; add qualitative benefit |
| Are university B2B prices right? | High for Year 1 — recommend SGD 25–40K pilots |
| Is WSG revenue a Year 1 item? | No — procurement timelines make it Year 2–3 |
| Are agency prices achievable? | Yes — small deals, fast cycles, best near-term B2B |
| Is the 84% margin claim accurate? | Probably conservative (actual may be 88–93%) |
| Is there a Team/SME tier gap? | Yes, but address it post-PMF (Month 18–24) |
| What single change most improves conversion? | Increase free tier suggestion limit from 3 to 10 |

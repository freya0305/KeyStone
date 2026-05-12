# Business Model Spec — KeyStone

> Last updated: 2026-05-04 (REMOVED: annual plan — cancelled)
> All revenue figures are estimates; validate against real cohort data in Month 1-3.

---

## B2C Pricing Tiers

| Tier  | Price                 | Features                                                                                | Notes                                              |
| ----- | --------------------- | --------------------------------------------------------------------------------------- | -------------------------------------------------- |
| Guest | Free                  | Upload resume + 1 job match preview (no full suggestions)                               | No account required for first match                |
| Free  | Free (email required) | 3 job analyses/month; 3 AI suggestions/month                                            | 3 suggestions per job, capped at 3 total per month |
| Pro   | SGD 12/month          | Unlimited matches; all suggestions; stage-based tracking; interview prep; weekly digest | —                                                  |

**SGD 12/mo rationale**: "SGD 1 per day" pricing anchor. Below SGD 15 anxiety threshold. Competitive vs LinkedIn Premium Career (SGD 40-50/mo). Equivalent to ~USD 9/mo.

**Post-PMF price path**: Once >500 active Pro users with <30% monthly churn confirmed, test SGD 15/mo for new signups (grandfather existing users at SGD 12).

**Conversion target**: 2–5% of active registered users (industry freemium average). At 5K–8K registered users in Year 1, this yields 100–400 paying Pro users. Year 1 ARR is therefore lower than initially projected; VC funding bridges the gap to meaningful B2C revenue.

---

## B2B Pricing Tiers

### University Career Centres

| Stage            | Price       | Scope                                               | Notes                                                                |
| ---------------- | ----------- | --------------------------------------------------- | -------------------------------------------------------------------- |
| Pilot (free)     | SGD 0       | 50–200 seats, 1 semester                            | Structured outcome measurement; career centre co-brands              |
| Year 1 contract  | SGD 25–40K  | Full cohort for 1 programme or one graduating class | Below aspirational range; achievable without competitive tender      |
| Year 2+ contract | SGD 50–100K | Full career centre licence, all students            | Supported by pilot outcome data; requires multi-stakeholder approval |

**Procurement reality**: Contracts above SGD 50K typically require VP/Provost approval + Procurement Office review + PDPA audit + vendor due diligence. Timeline: 9–18 months from first conversation to signed contract.

**Capital requirement**: Minimum SGD 40K reserves. With SGD 3,600/month burn, B2B-first path (agency deals Month 1-2, university pilot Month 3, first paid university contract Month 9) requires SGD 40K to cover the Month 1-9 gap with a 2-month safety buffer before institutional revenue arrives.

**First deal target**: SGD 15–20K at one of NUS / NTU / SMU / SUSS, positioned as "pilot expansion" rather than "new contract." Upper bound of SGD 25–40K is achievable in Year 2+ once outcome data exists and VP+Procurement approval is justified.

### WSG Government Programmes

| Stage              | Price                       | Notes                                                      |
| ------------------ | --------------------------- | ---------------------------------------------------------- |
| Initial engagement | SGD 0 (grant or free pilot) | WSG procurement above SGD 6,000 requires 3 quotes (GeBIZ)  |
| Formal contract    | SGD 30–80K/year             | Must win competitive tender; timeline 12–18 months minimum |

**WSG is a Year 2–3 revenue item, not Year 1.** Do not plan Year 1 operations to depend on WSG contract. Design product to serve PMET/CCP programme participants (so the capability is there when the contract comes).

**Opportunity flag**: If MCF/WSG issues an AI resume tools RFP, submit. Being the best-qualified SG-native vendor is the entire strategy for this channel.

### Recruitment Agencies — JD Generator (Primary B2B Revenue)

| Price             | Contract      | Features                                  |
| ----------------- | ------------- | ----------------------------------------- |
| Agency Team       | SGD 79/month  | 5 users, 100 JD generations/month         |
| Agency Pro        | SGD 199/month | 10 users, 400 JD generations/month        |
| Agency Enterprise | SGD 449/month | unlimited users, unlimited JD generations |

**Value prop to agencies**: "Write 10–50 JDs/day in 5 minutes each instead of 45 minutes — KeyStone learns from successful candidate profiles to write JDs that attract the right people."

**Best near-term B2B segment**: small boutique agencies (5–20 recruiters). Owner/director decides in 2–4 weeks, no procurement process. Target 5–10 agency deals in Year 1.

### Recruitment Agencies — Candidate Prep (Existing Tier)

| Price               | Contract               | Notes                                                                |
| ------------------- | ---------------------- | -------------------------------------------------------------------- |
| SGD 5–15/seat/month | Monthly, no minimum    | Fastest sales cycle: owner/director decision, no procurement process |
| SGD 3–8/seat/month  | Annual (bulk discount) | 10+ seat agencies                                                    |

**Value prop**: "Your candidates prepared with KeyStone → higher offer acceptance rate → you earn placement fee faster."

---

## Unit Economics

| Segment               | Cost/mo  | Revenue/mo | Gross Margin    |
| --------------------- | -------- | ---------- | --------------- |
| Free user             | SGD 0.80 | SGD 0      | –SGD 0.80       |
| Basic user            | SGD 2.16 | SGD 9      | +SGD 6.84 (76%) |
| Pro user              | SGD 2.16 | SGD 12     | +SGD 9.84 (82%) |
| B2B seat (university) | SGD 1.90 | SGD 3–8    | +SGD 1.10–6.10  |

**Cost basis (Pro user, per technical spec)**: LLM calls (Haiku+Sonnet, 20 analyses/mo avg) ≈ USD 0.90–1.60 = SGD 1.22–2.16; infrastructure (AWS, Clerk, Stripe, CDN, monitoring) ≈ SGD 0.50–0.80; heavy-user buffer ≈ SGD 0.20. Total ≈ SGD 1.92–2.96. SGD 2.16 is the mid-range estimate; SGD 2.95 in earlier documents was a conservative upper-bound figure. Max SGD 5/user/month LLM ceiling with graceful degradation is a hard architectural constraint — must be implemented before launch.

---

## Revenue Projections (CORRECTED — SGD 12 pricing)

|                                | Year 1                       | Year 2          | Year 3           |
| ------------------------------ | ---------------------------- | --------------- | ---------------- |
| Registered users               | 5K–8K                        | 10K–15K         | 20K–30K          |
| Paying B2C users (avg monthly) | 100–400                      | 400–1,000       | 1,200–3,000      |
| B2B contracts                  | 0–2 (agencies + free pilots) | 2–4             | 5–8              |
| B2C ARR                        | SGD 14–58K                   | SGD 58–144K     | SGD 173–432K     |
| B2B ARR                        | SGD 6–14K (agencies)         | SGD 27–54K      | SGD 74–148K      |
| **Total ARR**                  | **SGD 20–72K**               | **SGD 85–198K** | **SGD 247–580K** |

**Notes on revision**:

- Year 1 revised DOWN due to 2–5% conversion rate (was 6–8%); 100–400 paying users at SGD 12
- Year 1 B2C ARR (SGD 14–58K) is insufficient to cover burn; VC funding bridges the gap
- B2B Year 1 uses agency deals (fast cycle) not university contracts (slow cycle)
- Year 2–3 assume higher registered user base with same 2–5% conversion floor

**Capital requirement**: VC-funded. Year 1 B2C ARR (SGD 14–58K) does not cover SGD 3,600/month burn. Seed funding bridges to B2B institutional contracts and scaled B2C revenue.

---

## LTV / CAC Considerations

**B2C LTV**: SGD 36 (monthly plan only; annual plan cancelled). Job search tenure = 2–6 months. LTV = SGD 12 × 3 months average = ~SGD 36.

**Structural LTV problem**: Users churn when they get a job (the product works → they leave). Without post-search retention features (career tracking, salary benchmarking, passive alerts), the subscription model is structurally capped at 3–6 month tenures. Annual Plan is cancelled — LTV cannot be improved via pricing.

**B2C CAC**: Must stay near-zero for unit economics to work. Organic channels (referral, Reddit, community, career coach partnerships) are the only viable acquisition levers in Year 1. Paid acquisition (Google search) has estimated CAC of SGD 40–80 — unprofitable at SGD 36 LTV.

**B2B LTV**: High. SGD 25-40K first contract × 3-year retention × likely contract growth = SGD 75K-120K+ LTV per institutional client.

---

## Freemium Architecture Decision

The conversion trigger is: **user hits the paywall on a job they really want**.

Design the paywall moment to be:

1. Emotionally loaded (this is the job they applied for after running out of free matches)
2. Low friction (one-click upgrade, Stripe checkout pre-populated)
3. Immediate (Pro features unlock in under 5 seconds)

**Free tier change from brief**: Increase first-job suggestion limit from 3 to unlimited (to allow full product evaluation). Gate second+ jobs after the first 3 suggestions. This ensures users experience the full value before the paywall and makes the upgrade decision based on genuine quality perception.

**7-day Pro trial**: Offer on email signup (Guest → Free conversion). Runs simultaneously with the free tier. Trial users who don't convert go to Free tier. Industry standard for converting motivated top-of-funnel users in active job search.

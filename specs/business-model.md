# Business Model Spec — KeyStone

> Last updated: 2026-05-04 (REMOVED: annual plan — cancelled)
> All revenue figures are estimates; validate against real cohort data in Month 1-3.

---

## B2C Pricing Tiers

| Tier | Price | Features | Notes |
|------|-------|----------|-------|
| Guest | Free | Upload resume + 1 job match preview (no full suggestions) | No account required for first match |
| Free | Free (email required) | 3 job matches/month; first match: unlimited suggestions; subsequent matches: 3 suggestions each | Revised from brief (brief said "3 suggestions total" — undersells product) |
| Basic | SGD 9/month | Unlimited matches; all suggestions; manual outcome tracking | Target: budget-conscious fresh grads |
| Pro | SGD 12/month | Unlimited matches; all suggestions; stage-based tracking; interview prep; weekly digest | — |

**SGD 12/mo rationale**: "SGD 1 per day" pricing anchor. Below SGD 15 anxiety threshold. Competitive vs LinkedIn Premium Career (SGD 40-50/mo). Equivalent to ~USD 9/mo. Basic tier at SGD 9 captures price-sensitive users.

**Post-PMF price path**: Once >500 active Pro users with <30% monthly churn confirmed, test SGD 15/mo for new signups (grandfather existing users at SGD 12).

**Conversion target**: 4-6% of active registered users. Note: 4-6% of TOTAL registered users implies 10-15% of ACTIVELY-APPLYING users — the more relevant and achievable figure.

---

## B2B Pricing Tiers

### University Career Centres

| Stage | Price | Scope | Notes |
|-------|-------|-------|-------|
| Pilot (free) | SGD 0 | 50–200 seats, 1 semester | Structured outcome measurement; career centre co-brands |
| Year 1 contract | SGD 15–30K | Full cohort for 1 programme or one graduating class | Below aspirational range; achievable without competitive tender |
| Year 2+ contract | SGD 50–100K | Full career centre licence, all students | Supported by pilot outcome data; requires multi-stakeholder approval |

**Procurement reality**: Contracts above SGD 50K typically require VP/Provost approval + Procurement Office review + PDPA audit + vendor due diligence. Timeline: 9–18 months from first conversation to signed contract. Plan capital accordingly.

**First deal target**: SGD 15–30K at one of NUS / NTU / SMU / SUSS, positioned as "pilot expansion" rather than "new contract."

### WSG Government Programmes

| Stage | Price | Notes |
|-------|-------|-------|
| Initial engagement | SGD 0 (grant or free pilot) | WSG procurement above SGD 6,000 requires 3 quotes (GeBIZ) |
| Formal contract | SGD 30–80K/year | Must win competitive tender; timeline 12–18 months minimum |

**WSG is a Year 2–3 revenue item, not Year 1.** Do not plan Year 1 operations to depend on WSG contract. Design product to serve PMET/CCP programme participants (so the capability is there when the contract comes).

**Opportunity flag**: If MCF/WSG issues an AI resume tools RFP, submit. Being the best-qualified SG-native vendor is the entire strategy for this channel.

### Recruitment Agencies

| Price | Contract | Notes |
|-------|----------|-------|
| SGD 5–15/seat/month | Monthly, no minimum | Fastest sales cycle: owner/director decision, no procurement process |
| SGD 3–8/seat/month | Annual (bulk discount) | 10+ seat agencies |

**Best near-term B2B segment**: small deals, fast decisions, no tender requirement. A 10-recruiter agency at SGD 10/seat = SGD 1,200/year. Target 5–10 agency deals in Year 1 as "quick B2B wins" while university contracts are in procurement pipeline.

**Value prop to agencies**: "Your candidates prepared with KeyStone → higher offer acceptance rate → you earn placement fee faster." Track this metric for case studies.

---

## Unit Economics

| Segment | Cost/mo | Revenue/mo | Gross Margin |
|---------|---------|------------|-------------|
| Free user | SGD 0.80 | SGD 0 | –SGD 0.80 |
| Basic user | SGD 2.95 | SGD 9 | +SGD 6.05 (67%) |
| Pro user | SGD 2.95 | SGD 12 | +SGD 9.05 (75%) |
| B2B seat (university) | SGD 1.90 | SGD 3–8 | +SGD 1.10–6.10 |

**Note**: Actual Pro/Basic margin may be 88–93% at typical usage; the SGD 2.95 unit cost includes buffer for 95th-percentile heavy users. Max SGD 5/user/month LLM ceiling with graceful degradation is a hard architectural constraint — must be implemented before launch.

---

## Revenue Projections (CORRECTED — SGD 12 pricing)

| | Year 1 | Year 2 | Year 3 |
|--|--------|--------|--------|
| Registered users | 1.5K–3K | 5K–10K | 15K–30K |
| Paying B2C users (avg monthly) | 100–250 | 400–1,000 | 1,200–3,000 |
| B2B contracts | 0–2 (agencies + free pilots) | 2–4 | 5–8 |
| B2C ARR | SGD 14–36K | SGD 58–144K | SGD 173–432K |
| B2B ARR | SGD 6–14K (agencies) | SGD 27–54K | SGD 74–148K |
| **Total ARR** | **SGD 20–50K** | **SGD 85–198K** | **SGD 247–580K** |

**Notes on revision**:
- Year 1 revised DOWN due to SGD 12 pricing (was SGD 50-120K using SGD 19)
- B2B Year 1 uses agency deals (fast cycle) not university contracts (slow cycle)
- Year 2-3 reflect SGD 12 pricing + realistic B2C growth rates
- Break-even at SGD 3,600/month burn requires ~300 Pro-equivalent users = ~SGD 43K ARR

---

## LTV / CAC Considerations

**B2C LTV**: Low. Job search tenure = 2–6 months. LTV = SGD 12 × 3 months average = ~SGD 36 (monthly).

**Structural LTV problem**: Users churn when they get a job (the product works → they leave). Without post-search retention features (career tracking, salary benchmarking, passive alerts), the subscription model is structurally capped at 3–6 month tenures.

**B2C CAC**: Must stay near-zero for unit economics to work. Organic channels (referral, Reddit, community, career coach partnerships) are the only viable acquisition levers in Year 1. Paid acquisition (Google search) has estimated CAC of SGD 40–80 — unprofitable at SGD 36 LTV.

**B2B LTV**: High. SGD 15-30K first contract × 3-year retention × likely contract growth = SGD 50K-100K+ LTV per institutional client.

---

## Freemium Architecture Decision

The conversion trigger is: **user hits the paywall on a job they really want**.

Design the paywall moment to be:
1. Emotionally loaded (this is the job they applied for after running out of free matches)
2. Low friction (one-click upgrade, Stripe checkout pre-populated)
3. Immediate (Pro features unlock in under 5 seconds)

**Free tier change from brief**: Increase first-job suggestion limit from 3 to unlimited (to allow full product evaluation). Gate second+ jobs after the first 3 suggestions. This ensures users experience the full value before the paywall and makes the upgrade decision based on genuine quality perception.

**7-day Pro trial**: Offer on email signup (Guest → Free conversion). Runs simultaneously with the free tier. Trial users who don't convert go to Free tier. Industry standard for converting motivated top-of-funnel users in active job search.

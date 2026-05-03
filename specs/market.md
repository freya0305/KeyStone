# Market Spec — KeyStone

> Last updated: 2026-04-29 (Phase 01 Analysis)
> Confidence labels: [CONFIRMED] = from authoritative source; [ESTIMATE] = derived/inferred; [NEEDS VERIFICATION] = requires live research

---

## Singapore Job Seeker Market

### Size
- Resident labour force: ~3.6M [CONFIRMED — MOM 2023]
- Digitally-engaged active job seekers/year: ~150,000–250,000 [ESTIMATE]
- Fresh graduates entering workforce annually: ~30,000–35,000 [CONFIRMED — MOE GES 2023]
- Mid-career professionals in active transition: ~80,000–100,000 [ESTIMATE]
- PMET retrenchments: ~10,000–20,000/year [CONFIRMED — MOM 2022-2023]

### Application-to-Interview Conversion
- SG white-collar application-to-interview rate: ~3–6% [ESTIMATE — LinkedIn Southeast Asia Talent Insights 2023]
- Average applications before offer: fresh grads ~40–120; career changers ~80–150 [ESTIMATE]
- Median employment search duration: 8–12 weeks for PMETs; 3–4 months for fresh grads [CONFIRMED — MOM / MOE GES 2024]

---

## TAM / SAM / SOM

### TAM (Total Addressable Market)
- B2C: SGD 5.4M–12M/year (150K–250K seekers × SGD 12/mo × 3–4 month average search)
- B2B: SGD 860K–2M/year (universities, WSG, agencies at full penetration)

### SAM (Serviceable Addressable Market)
- B2C: ~30,000–60,000 users/year (English-proficient, digitally active, resume-iterating segment)
- B2B: 3–6 institutions in Year 1; 10–15 by Year 3

### SOM (Serviceable Obtainable Market)
- Year 1 paying B2C: 200–400 (at 4–6% conversion of 5K–8K registered users)
- Year 1 B2B: 0–1 contracts (realistic first contracts: SGD 15–30K, not SGD 50–100K)
- Year 3 paying B2C: 3,000–5,000

---

## Competitive Landscape

### Threat Tiers — Revised (Round 2: SG features are trust signals, not primary moat)

**Frame**: SG-specific features (NS framing, NRIC, GLC photo) are replicable in 4–8 weeks by any well-funded US team. All threats have been re-rated assuming SG localisation is NOT a defensible moat.

| Competitor | Type | Threat Level | Time to SG Parity | Primary Risk |
|------------|------|-------------|-------------------|-------------|
| LinkedIn AI | Platform + native JD data | **HIGH** | 3–6 months if prioritised | Owns distribution; users already there |
| ChatGPT/LLMs | Free floor | **HIGH** | Already at parity for power users | Free, increasingly capable; wrapper UX is weak moat |
| Jobscan | Direct B2C, JD matching | **HIGH** | 2–4 weeks SG features | Full JD workflow + URL parsing + brand |
| Teal | Direct B2C, outcome tracking | **MEDIUM-HIGH** | 4–8 weeks SG features | Outcome tracking + JD tailoring combo |
| VMock | B2B university incumbent | **MEDIUM** | 18–36 months for SG university entry | Well-resourced but NOT yet in SG universities |
| MCF (platform risk) | Government free tier | **MEDIUM** (long-term) | 2–4 years | If MCF ships free resume AI, B2C TAM collapses |
| Resume.io / builders | Format-only | LOW-MEDIUM | Not strategic | Template users, not tailoring users |
| Symplicity | Career centre CRM | LOW | Not relevant | Different product category; potential integration partner |

**VMock critical note**: VMock has ALREADY established relationships with Singapore universities. The "window period" framing is incorrect — KeyStone faces an existing incumbent, not an incoming one. The urgency driver is not timing but data depth: KeyStone must accumulate outcome-calibrated SG user data before VMock adds this capability to its existing SG deployments. See journal 0009 (correction) and 0010 (data moat strategy).

### SG Feature Replication Times (Honest Assessment)
- MCF URL parsing: 1–3 days of engineering
- NS framing rules: 1 week
- NRIC detection/masking: 30 minutes (regex)
- GLC/MNC employer database: 1–2 weeks
- SG resume conventions: 2–3 weeks of prompt engineering

**Total for a focused US team: 4–8 weeks.** The protection is competitor prioritisation (SG = 0.07% of global workforce), not technical complexity.

### What Is Genuinely Defensible

| Feature | Honest Assessment |
|---------|------------------|
| URL parsing | UX convenience, not a moat — replicable in days |
| Four-level gap assessment | Weak at launch, strengthens as outcome data validates it |
| Outcome tracking (B2C) | Moderate; Teal does this already; SG calibration adds value |
| B2B institutional contracts | **Genuine moat** — multi-year switching costs + outcome data + PDPA track record |
| SG user signal learning loop | **Most defensible long-term** — 12–18 months to accumulate meaningful signal |

**Honest conclusion**: At launch, defensibility is near zero. At Year 2 with 3–4 university contracts, B2B defensibility is real. B2C remains fragile unless learning loop produces measurably better outcomes than generic LLMs.

### Strategic Priority: Distribution Beats Features

This is a distribution and data accumulation race, not a technology race. A slightly inferior product with university contracts is more defensible than a superior product with no users. First 90 days: sign at least one university pilot. Do not spend the first 90 days on feature development.

### What Is NOT a Genuine Differentiator
- "Per-job tailored suggestions" — Jobscan (since 2014) and Teal do this; the brief's claim of "no competitor" is factually wrong
- URL parsing — replicable in <2 weeks
- SG intelligence (static) — replicable in 60–90 days via prompt engineering; only the LEARNING LOOP version is durable

---

## Moat Assessment

### Defensibility Timeline (Revised — 3–6% outcome logging rate, pre-launch data acquisition)
- Pre-launch: Secure 3–5 agency data partnerships (~1,500 outcome-linked pairs) + 50–100 design partners (~1,800 logged outcomes). Product launches with real SG calibration, not zero data.
- Month 0–6: Strong product with pre-launch calibration. B2C signal accumulation begins. At 3–6% logging rate, ~150–400 new outcomes/month at 1,000 active users.
- Month 6–12: First fine-tunable signal corpus (~10,000 accept/reject signals). Suggestion quality starts differentiating from generic LLM wrappers.
- Month 18–30: Outcome-calibrated scoring emerges (~1,000 logged outcomes from B2C). Callback lift demonstrable. B2B institutional lock-in deepens. (Previously Month 12–18 — revised down due to 3–6% real logging rate.)
- Year 3+: Employer fingerprints mature. Full fine-tuned SG model operational. Data moat reaches structural irreversibility. (Previously Year 2–3.)

**PDPA training separation (MUST):** B2B institutional (university) data is NEVER used for model training — aggregate dashboards only. Only B2C users with explicit training consent contribute to the fine-tuning pipeline.

### Actual Moat (vs Claimed Moat)
| Claimed | Actual Status |
|---------|--------------|
| SG intelligence engine | Marketing wedge (90-day replication) unless backed by outcome-calibrated learning loop |
| Outcome data | The primary long-term moat — zero value at launch; becomes irreproducible at Year 1.5+ |
| Suggestion signals (accept/reject corpus) | Real moat from Month 6+ — SG-specific preference data no competitor can buy |
| Institutional contracts | REAL moat — 3-year procurement inertia once signed + outcome data lock-in |
| URL parsing | Table stakes, not moat |

### The VMock Displacement Gap
VMock scores against an ATS simulation; it cannot show whether students who improved their VMock score got better callback rates. This is the single metric career directors must report upward. KeyStone's outcome tracking is not a nice-to-have — it is the structural answer to the question VMock's architecture cannot answer. This gap cannot be closed by VMock writing code; they need SG outcome data first, and they are not collecting it.

**Displacement pitch**: "VMock tells students how to pass an ATS. KeyStone tells students what actually gets callbacks from DBS, GovTech, and Accenture — calibrated on real SG outcomes. After one semester, you can show your Provost a callback rate differential."

### MCF Risk
20–40% probability MCF ships free resume AI within 24 months. Defensive play: approach WSG/MCF as technology vendor (white-label KeyStone's engine for MCF). This converts the existential threat into the largest possible B2B contract.

---

## Market Timing ("Why Now")
1. LLM cost cliff makes SGD 5/user/month AI ceiling viable; impossible in 2022
2. SG tech/finance retrenchments 2023–2025 raised active job-seeker count and search duration
3. AI literacy among SG job seekers is high; market is AI-receptive
4. Category is in land-grab year: Teal/Jobscan/Rezi have zero SG presence; 12–18 month window to establish SG-native brand before US incumbent localises
5. PDPA enforcement seriousness post-2022 amendments advantages SG-domiciled product for B2B procurement

Honest "why now": the competitive window, not consumer urgency. Job-seeking urgency is seasonal and episodic; competitive window is what's closing.

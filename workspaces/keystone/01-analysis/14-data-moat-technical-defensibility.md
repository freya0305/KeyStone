# Analysis 14 — How Customer Data Becomes Technical Defensibility

> Phase 01 Analysis — 2026-04-29
> Triggered by: founder correction that VMock is already in SG universities — window-period framing discarded; data moat is the only durable strategic answer.

---

## The Core Question

VMock is already an incumbent in SG universities. KeyStone cannot win on timing. The only viable long-term strategy is to build technical defensibility that VMock literally cannot replicate without rebuilding from scratch. What data does KeyStone collect, and how does each data type compound into a technical moat?

---

## The Fundamental Asymmetry: What VMock Does vs. What KeyStone Does

VMock scores resumes against an **ATS simulation model** — it predicts whether a resume will pass automated keyword filters. This model is trained on US/UK job posting data and generic resume corpora. It has no outcome feedback loop. It cannot answer: "Did the student who improved their VMock score actually get a callback?"

KeyStone's architecture, if built correctly from Day 1, scores resumes against **actual SG hiring manager behaviour** — calibrated on real callback outcomes from real SG users. This distinction is not a feature claim. It is an architectural one. VMock cannot add outcome calibration by writing more code. They need the data first. If KeyStone collects the data while VMock collects none, the data advantage compounds every month.

This is the moat: not the AI model itself (copyable), not the features (copyable in weeks), but the **training signal — SG-specific human preference data and outcome data that no competitor can acquire without starting over**.

---

## Data Types KeyStone Accumulates

### Type 1: Suggestion Signals (Fastest to Accumulate)

**What it is**: Every time a user accepts, rejects, or modifies a suggestion, that action is a labelled data point:

```
{
  suggestion_id: uuid,
  user_segment: "fresh_grad_ntu_cs" | "mid_career_finance" | ...,
  company_type: "GLC" | "MNC" | "Startup" | "StatBoard",
  role_level: "entry" | "mid" | "senior",
  industry: "finance" | "tech" | "consulting" | ...,
  original_text: "...",
  suggested_text: "...",
  action: "accept" | "reject" | "modify",
  modified_text: "..." (if action = modify),
  outcome_linked: boolean  # whether this application was later logged with an outcome
}
```

**Why this matters**: This is human preference data for SG job applications. It is the raw material for:
- Supervised fine-tuning of the suggestion model on SG user preferences
- Pattern identification: "Mid-career finance switchers applying to GLCs reject quantification suggestions at 3× the rate of fresh grads applying to MNCs" → model learns to suggest differently by segment
- Quality filtering: suggestions that get modified tell the model its output was directionally right but not quite there

**Accumulation rate**: 
- ~10 suggestions per job analysis session
- User does 3-5 sessions per job search (multiple jobs)
- 1,000 active users → ~30,000-50,000 signals/month
- Meaningful pattern detection at 10,000 signals per segment; ~6-12 months with university pilot

**Why VMock cannot replicate**: VMock's suggestion model (if it exists at all beyond keyword rules) is trained on generic corpora. It has no per-user action feedback. Even if VMock added a feedback button tomorrow, they would need 12-18 months of SG users to accumulate comparable signal volume.

---

### Type 2: Resume-JD Pair Corpus (Unique SG Training Data)

**What it is**: Every resume-JD analysis creates a structured pair:
```
{
  resume_summary: { skills, experience_years, degree_institution, industry_background },
  jd_requirements: { extracted_requirements, company_type, role_level, industry },
  gap_classification: { strong_match: [...], transferable: [...], addressable: [...], fundamental: [...] },
  suggestions_generated: [...]
}
```

**Why this matters**: This becomes a proprietary SG resume-JD paired corpus — the exact data needed to fine-tune a domain-specific model. US competitors have US-context pairs. No one has SG-context pairs at scale. After 50,000+ pairs, this corpus represents something that cannot be bought, synthesised, or scraped.

**Accumulation rate**: 1 pair per job analysis session. 1,000 active users × 5 analyses/month = 5,000 new pairs/month. 50,000 pairs in ~10 months with traction.

**Downstream uses**: 
- Fine-tune base LLM on SG-specific resume-JD matching patterns
- Build a proprietary embedding model for SG job requirements (outperforms generic embeddings on SG role classification)
- Enables offline batch scoring: given a resume, predict fit across 100 current SG openings without LLM inference

---

### Type 3: Application Outcome Data (Hardest to Collect, Highest Value)

**What it is**: When users log application outcomes (no response / callback / interview / offer), KeyStone can link the outcome back to:
- The specific suggestions accepted/rejected on that application
- The company, role, industry, and company type
- The user's segment and resume characteristics
- The match level assessment (Strong / Transferable / Addressable / Fundamental)

**Why this matters**: This is **calibration data for the prediction model**. After 5,000+ logged outcomes:
- Build a callback probability model: given a resume and JD, predict callback probability specifically calibrated on SG hiring manager behaviour
- Identify which suggestion types actually improve callback rates (some may have zero effect; some may hurt)
- Build the "SG hiring signal" — what resume signals actually trigger callbacks at GLCs vs MNCs vs startups in Singapore

This is categorically different from what VMock provides. VMock's SMART score predicts ATS pass probability (no outcome validation). KeyStone's score predicts actual callback probability (outcome-validated). The difference is the difference between "we think this is right" and "we measured this is right."

**Accumulation challenges**: 
- Users must voluntarily log outcomes; 15-20% logging rate is realistic
- Need 5,000+ logged outcomes for statistical significance across segments
- Timeline: 6,000-8,000 applications submitted by users → ~1,000-1,500 outcomes logged → meaningful patterns at 12-18 months
- University pilot dramatically accelerates: 500 students × 40-80 applications = 20,000-40,000 applications, with structured outcome consent from MOU

**Why this is non-replicable**: VMock does not collect outcomes. An LLM wrapper (ChatGPT) does not collect outcomes. Jobscan does not collect SG-specific outcomes. The only way to get this data is to have SG users who log results. First mover collects first data. The gap compounds monthly.

---

### Type 4: SG Employer Response Patterns (Network Effect on Data)

**What it is**: After enough applications to the same employer, patterns emerge:
```
Employer: DBS Bank
  - Quantified team leadership mentions: +12% callback lift
  - Singapore-centric project references: +8% callback lift  
  - NS leadership framing (for male candidates): +15% callback lift
  - Generic "responsible for" phrasing: -18% callback penalty
  Sample size: 847 applications, 312 outcomes logged
```

**Why this matters**: This is **employer-specific intelligence** no competitor can generate without the same employer-specific outcome data. Career directors can see "students applying to DBS who accept KeyStone suggestions have a 23% callback rate vs 8% baseline" — a verifiable, institution-specific outcome claim.

**Network effect**: More users applying to DBS → stronger DBS model → better DBS-specific suggestions → better outcomes for DBS-applying users → more users choose KeyStone. Repeat for every major SG employer. The network effect is on the data, not on the user base — it strengthens the product even when user growth slows.

**Threshold for first employer fingerprint**: ~500 applications with outcomes to the same employer. Achievable in 12-18 months for the top 10-20 SG employers (DBS, GovTech, Accenture, EY, McKinsey, MAS, NTUC, etc.).

---

## The Compounding Flywheel

```
More SG Users
      ↓
More Signal Data (accept/reject/modify)
More Resume-JD Pairs
More Outcome Logs
      ↓
Better Suggestion Model (fine-tuned on SG signals)
Better Match Calibration (outcome-validated)
Better Employer Fingerprints
      ↓
Better User Outcomes (higher callback rates)
Better B2B Data Story (cohort-level outcome reporting)
      ↓
More SG Users / More University Pilots
```

At each cycle, the gap between KeyStone (outcome-calibrated, SG-trained) and any new entrant (starting from zero SG data) widens. A competitor who enters SG in 2 years does not enter a level playing field — they enter a market where KeyStone has 24 months of accumulated SG signal data they cannot buy.

---

## Fine-Tuning Roadmap (When and What)

| Stage | Trigger | What to Fine-Tune | Method | Outcome |
|-------|---------|-------------------|--------|---------|
| Month 0-6 | Baseline | Nothing — use prompt engineering | N/A | Establish signal collection |
| Month 6-12 | 10K+ signals | Suggestion ranking model | Supervised fine-tune on accept/reject pairs | Better suggestion quality for SG context |
| Month 12-18 | 5K+ outcomes | Callback prediction | RLHF/DPO on outcome-linked signals | Outcome-calibrated scoring |
| Month 18-24 | 50K+ pairs | Domain embedding model | Contrastive training on SG resume-JD pairs | Proprietary SG job-fit embedding |
| Year 2+ | 500+ per employer | Employer-specific adapters | LoRA fine-tune per employer type | Employer-fingerprinted suggestions |

**Critical architecture decision**: The learning loop MUST be architecturally separate from the inference path. Signal collection and fine-tuning happen asynchronously; they improve the model but do not block real-time inference. See technical spec for the `suggestion_signals` schema and async processing queue.

---

## The B2B Pitch Reframed (For VMock Displacement)

The pitch to a university career centre that already uses VMock:

> "VMock tells your students how to pass an ATS. We tell them what actually gets callbacks from DBS, GovTech, and Accenture — calibrated on real SG outcomes. After one semester of your students using KeyStone, you can show your Provost: 'Students who completed at least 3 KeyStone analyses had a 23% callback rate vs 11% for students who didn't.' Can your current tool give you that number?"

The structural reason VMock cannot match this pitch: they don't have the outcome data. They cannot build this claim without starting over.

---

## What Has to Be Built From Day 1

The data moat requires specific architectural decisions at MVP. These cannot be retrofitted:

1. **`suggestion_signals` table** — every accept/reject/modify action logged with full context from the moment the product launches
2. **Application outcome logging** — built into the UX (prompt at resume download: "Did you submit this?"), not a bolt-on feature
3. **PDPA consent structure** — explicit consent for signal aggregation at signup ("your feedback improves suggestions for all users")
4. **Employer classification** — every JD tagged with employer identity at analysis time (not company_type alone — the actual employer, e.g., "DBS Digital Banking" not just "GLC")
5. **Outcome-suggestion linkage** — outcome log must reference the specific suggestion set used, enabling causality analysis (not just correlation)

If any of these are missing at launch, the first 6-12 months of user data is lost for the moat-building purpose. The moat starts accumulating the moment the first user accepts a suggestion. It cannot be rebuilt retroactively.

---

## Honest Assessment: Thresholds and Timelines

The data moat is real but deferred. Realistic milestones:

| Milestone | Required Volume | Realistic Timeline | What It Unlocks |
|-----------|----------------|-------------------|-----------------|
| First statistically significant segment preference | 2,000 signals | Month 3-4 (100+ active users) | Segment-specific suggestion tuning |
| Fine-tunable suggestion corpus | 10,000 signals | Month 6-8 (500+ active users) | First fine-tuning run |
| Outcome-calibrated scoring | 1,000 logged outcomes | Month 12-18 | "Our suggestions improve callbacks" claim |
| Major employer fingerprint | 500 outcomes per employer | Month 18-24 | Employer-specific suggestion lift |
| Full fine-tuned model | 50,000 high-quality pairs | Year 2+ | Model that outperforms generic LLM on SG matching |

**Critical implication**: At launch, KeyStone has NO data moat. The moat is being built from Day 1 — it does not exist yet. The honest position is: "We are building the first outcome-calibrated resume tool for SG. Today we have a strong product. In 12 months we will have a dataset no competitor can replicate."

This is why Year 1 strategy is **volume first** — not polishing features, not raising capital, but getting SG users using the product and logging outcomes. Every month of delay in reaching 1,000 active users is a month of moat-building the competitor can also use.

---

## Why VMock Cannot Close the Gap

VMock's architecture produces a score but doesn't collect outcomes. Their flywheel (if they have one) optimises against ATS pass rates — not human callback rates. To close the KeyStone gap, VMock would need to:

1. Add outcome tracking to their product (months of engineering)
2. Convince existing users to log outcomes (adoption problem)
3. Collect enough SG-specific outcomes to calibrate (12-18 months minimum)
4. Rebuild their scoring model against SG outcomes (full model retraining)

That sequence assumes they try. If they don't, the gap becomes permanent. If they do, KeyStone has a 24-36 month head start on SG outcome data — the one input the new VMock model would need.

**The only scenario where the data moat fails**: KeyStone does not reach meaningful user scale within 18 months. If KeyStone has fewer than 500 active users at Month 18, the data advantage is too small to matter and VMock can close the gap when they decide to. Volume is the strategy. The data moat is only as valuable as the data filling it.

---

## Summary: The Only Durable Answer

| Factor | Conclusion |
|--------|-----------|
| Is timing a moat? | No — VMock is already here |
| Are features a moat? | No — replicable in weeks to months |
| Is SG intelligence a moat? | No — prompt-engineering copyable in 60-90 days |
| Is outcome-calibrated data a moat? | **Yes** — requires SG users collecting outcomes; cannot be bought or synthesised |
| Is the fine-tuned SG model a moat? | **Yes** — but takes 12-24 months to build; starts at zero |
| What is the prerequisite? | Volume: 1,000+ active SG users logging outcomes within 12-18 months |
| What is the architectural prerequisite? | signal collection + outcome logging built at MVP launch, not added later |

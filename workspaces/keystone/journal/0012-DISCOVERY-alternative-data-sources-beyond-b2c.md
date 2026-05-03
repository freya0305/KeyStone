---
type: DISCOVERY
date: 2026-04-29
created_at: 2026-04-29T12:10:00Z
author: co-authored
session_id: 874f263b-1879-49b0-9e64-1f293538aedb
project: keystone
topic: Breaking the chicken-and-egg: pre-launch data acquisition via agency partnerships and design partner cohort
phase: analyze
tags: [data-moat, training-data, recruitment-agencies, design-partners, cold-start]
---

## The Problem

B2C growth at launch is slow because: (1) no data moat yet, (2) GPT and LinkedIn cover the same surface. But the data moat requires B2C users. Classic chicken-and-egg.

The PDPA constraint (0011) makes it worse: B2B university data is now excluded from training pipeline. Pure B2C accumulation at 3-6% logging rate = Year 3+ moat.

## Breaking the Loop: Pre-Launch Data Acquisition

The solution is to acquire calibration data BEFORE public launch through non-B2C channels — so the product launches with real SG signal quality, not just prompt engineering.

---

### Source 1: Recruitment Agency Data Partnerships (Best)

**What agencies have**: Real SG resume + job description + placement outcome data. When a recruiter places a candidate, they know: the candidate's resume, the JD, whether the candidate got the offer. This is exactly the calibration data KeyStone needs — outcome-linked, SG-specific, real.

**Why they'd share it**:
- Boutique agencies (5-20 recruiters) are already a KeyStone B2B revenue target
- Free seats in exchange for historical anonymized placement data is a credible trade
- Their data is their business data — no individual consent complication under PDPA (candidate personal data needs handling, but aggregate job-fit patterns are fine)
- They benefit from better-prepared candidates → faster placements

**Data volume estimate**: 5 boutique SG agencies (finance/tech/consulting) × 150 placements/year × 2 years history = ~1,500 real SG resume-JD-outcome pairs before launch. This is enough to calibrate initial suggestion quality beyond pure prompt engineering.

**Commercial structure**: Free KeyStone agency seats (SGD 0) for 12 months in exchange for anonymized historical placement data (CSV export). Both sides benefit. No cash exchange.

---

### Source 2: Design Partner Cohort (Fast, High Signal)

Recruit 50-100 SG job seekers currently in active search. Offer: free Pro access indefinitely. Require: (a) outcome logging for every application, (b) explicit model training consent, (c) 30-minute monthly feedback call.

**Why this works**:
- These are real users in real job searches — data is as authentic as any B2C user
- Full training consent removes PDPA complication
- High outcome logging rate (maybe 30-40%) because participants are invested in the program
- Design partner feedback directly improves UX before public launch

**Cost**: SGD 0 revenue from 100 users × 3 months = ~SGD 5,700 opportunity cost. Offset by product quality improvement before launch.

**Data volume**: 100 users × 3 months × 15 applications/month × 40% logging rate = ~1,800 logged outcomes before public launch.

---

### Source 3: Synthetic SG Context Bootstrapping (Immediate, Limited)

Use Claude/GPT to generate SG-specific resume-JD pairs with labeled quality assessments. Not a moat, but raises the baseline above a blank context window.

- Generate 5,000-10,000 SG-context pairs (NTU CS + SG tech internship, SMU BBA + Big 4, NTU Engineering + NS officer, etc.)
- Manually review a random 200-300 sample for quality
- Use for initial prompt context enrichment and system prompt calibration
- Cost: SGD 500-2,000 in API costs

This does NOT produce human preference signal. It produces better prompt calibration. Do not conflate with real training data.

---

## Revised Data Acquisition Sequence

```
Pre-launch (Month 0-3):
  ├── Secure 3-5 agency data partnerships → ~1,500 outcome-linked pairs
  ├── Recruit 50-100 design partners → ~1,800 logged outcomes
  └── Synthetic bootstrapping → improved prompt calibration

Public launch (Month 3-5):
  └── Product launches with already-calibrated SG intelligence
      Not "better than blank ChatGPT" — actually better for SG context

B2C growth (Month 5-18):
  └── Continues accumulating signal at 3-6% rate
      But starts from a meaningful baseline, not zero
```

The product now launches with ~3,300 real SG data points. The moat is thin but real.

## Honest Limitations

Agency data is retrospective (past placements, not current users). Design partner data is high-signal but small sample. Neither replaces the scale of real B2C accumulation at 1,000+ users.

The honest competitive position at launch: "A well-calibrated SG-context resume tool with real SG signal data, not just an LLM wrapper." Better than ChatGPT for SG users — but the gap is quality of SG context, not a structural moat.

The structural moat (outcome-calibrated model fine-tuning) still materialises at Year 2-3 with B2C scale. Pre-launch data acquisition compresses the cold-start problem, it does not eliminate the need for B2C growth.

## For Discussion

1. The 5 agency partnership model requires approaching agencies before the product is built. At what point in the development timeline should agency outreach begin — before MVP, or after a demo is ready?
2. Design partner recruitment: what is the right profile (fresh grad? mid-career? retrenched PMET?) and what channel reaches them most efficiently before the product has any brand recognition?
3. If agency data reveals patterns that contradict synthetic or prompt-engineered assumptions (e.g., "SG agencies consistently find that quantification hurts in civil service applications"), how does the team validate and act on this before B2C launch?

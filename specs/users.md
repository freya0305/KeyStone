# Users Spec — KeyStone

> Last updated: 2026-04-29 (Phase 01 Analysis)

---

## Primary B2C Personas

### Persona 1: Fresh Graduate (Highest Volume, Lower Yield)

**Profile**: 22–27 years old, recent Singapore university/polytechnic graduate, entering workforce for the first time
**Key characteristics**:
- Limited work history; resume is heavy on internships, CCAs, and NS (for males)
- High application volume (40–120 applications before first offer [ESTIMATE])
- Pain: volume without feedback ("I send applications and hear nothing back")
- Male-specific additional pain: NS experience framing (affects ~50% of this cohort)
- Low willingness to pay — psychologically expects free tools; BUT converts on emotional trigger ("I want this specific job")
- Average search duration: 3–4 months

**KeyStone use pattern**: Upload resume on Day 1, run 3–5 job matches in first week, hit paywall if engaged. Primary conversion trigger: a job they really want.
**Primary acquisition channel**: University pilot (B2B distribution) or Reddit/forum organic
**Best tier**: Monthly Pro during search period (3 months), then cancel
**LTV**: ~SGD 36 (3 months × SGD 12 Pro)

### Persona 2: Mid-Career Switcher (Highest Value, Best B2C Segment)

**Profile**: 28–40 years old, employed but seeking to switch industry or function
**Key characteristics**:
- Substantial work history; challenge is relevance, not volume
- Pain: "I have experience but it's in the wrong industry — how do I reframe it?"
- The four-level gap analysis is highly useful: Fundamental gaps tell them what to address via courses/projects
- High willingness to pay (more at stake financially; SGD 12/mo trivial vs potential salary impact)
- Longer search windows (6–12 months for career changes)
- Natural annual plan buyer
**LTV**: ~SGD 72–144 (6–12 months Pro) or SGD 144 annual

**KeyStone use pattern**: Uploads resume, creates multiple tailored versions for different target roles/industries, uses match assessment to prioritise applications, tracks outcomes carefully
**Primary acquisition channel**: Organic LinkedIn, Reddit mid-career advice threads, referral from employed users who already used KeyStone

### Persona 3: PMET Job Seeker (Best B2B via WSG, Lower Direct B2C)

**Profile**: 35–55 years old, retrenched professional/manager/executive/technician
**Key characteristics**:
- Outdated resume (years since last search); stale skills vocabulary
- Emotionally sensitive (retrenchment + application silence is psychologically damaging)
- Strong profile, poor keyword presentation for current ATS/MCF systems
- Time-pressured: severance running out
- Best served via WSG/e2i B2B contracts, not direct B2C

**KeyStone use pattern**: Heavy use during concentrated search period (3–6 months); less likely to discover organically; likely arrives via WSG programme referral
**Best acquisition**: WSG contract (B2B), not B2C organic

---

## B2B Buyer Personas

### Persona 4: University Career Centre Director

**Role**: Director of Career Services / Director of CCPD / VP Student Affairs (depending on university)
**Measured on**:
1. Graduate employment rate by graduation (primary KPI — appears in university rankings and MOE reports)
2. Employer NPS / employer attendance at career fairs
3. Student engagement with career services (workshop attendance, advising appointments)
4. Cost-per-student-served (budget pressure is real)
5. Defensible procurement narrative ("why did we buy KeyStone?")

**What they DO NOT care about** (despite the brief's pitch): callback rate as a metric. This is not on their dashboards. Do not lead with it.

**Right pitch**: "KeyStone scales your advisory team — every student gets resume coaching they currently can't afford to give. Your team focuses on the 5% who need real human intervention."

**Procurement reality**:
- Below SGD 30K: Director can usually approve
- SGD 30–100K: Requires VP Student Affairs + Procurement
- Above SGD 100K: Tender Board (rarely warranted for Year 1 deal)
- PDPA review adds 2–3 months
- AI ethics review is now real at SG universities post-2023

**Approval chain**: Director (sponsor) → Procurement Office → Finance → VP sign-off → Legal (contract)
**Timeline**: 9–18 months from first conversation to signed contract

### Persona 5: WSG Programme Manager

**Role**: Programme manager for Career Conversion Programme (CCP), Professional Conversion Programme (PCP), or Careers Connect
**Measured on**: Placement rates for programme participants; employer partner satisfaction; programme KPI dashboards to MOM
**Procurement**: GeBIZ mandatory; 3 quotes required for contracts above SGD 6,000; open tender above SGD 90,000
**Timeline**: 12–18 months minimum

### Persona 6: Recruitment Agency Owner / Director

**Profile**: Owner or senior director of a boutique specialist recruitment agency (5–20 recruiters)
**Pain**: Candidate quality is variable; time spent coaching candidates before submissions is unbillable
**Value prop**: "Candidates prepared with KeyStone → better match quality → faster placement → more fees earned"
**Decision process**: Owner decision; no procurement; no tender; can sign in days
**Pricing tolerance**: SGD 5–15/seat/month; high if ROI is demonstrated (one extra placement per month pays for 2 years of KeyStone)

---

## User Segmentation by Priority

| Segment | B2C Acquisition Priority | B2B Revenue Priority | Notes |
|---------|--------------------------|---------------------|-------|
| Fresh graduates | MEDIUM (high volume, low LTV) | HIGH (via university contracts) | Serve via B2B; don't build B2C acquisition campaigns for this cohort |
| Mid-career switchers | HIGH (best LTV B2C segment) | LOW direct | Primary B2C target; longer tenure, annual plan natural |
| PMETs / retrenched | LOW B2C direct | HIGH (via WSG contracts) | Reach via B2B channels; too hard to acquire in B2C |
| University career centres | — | HIGH (primary B2B target) | Longest cycle but highest data value |
| Recruitment agencies | — | MEDIUM-HIGH (fastest B2B cycle) | Best Year 1 B2B quick wins |
| WSG government | — | MEDIUM (Year 2–3) | Important long-term, slow short-term |

---

## Pain Point Validation Summary

| Pain Point | Validity | Recurring? | Primary Segment |
|-----------|---------|-----------|----------------|
| Low callback rates (3–6% application→interview) | CONFIRMED | Every search | All |
| No job-specific match visibility | CONFIRMED — strongest pain | Every application | All |
| Resume quality as ATS/MCF blocker | CONFIRMED (MCF keyword matching documented) | Every search | All |
| No feedback on resume quality | PARTIAL — WSG/CC exist but slow | Every search | Fresh grads |
| NS framing confusion | CONFIRMED | One-time per resume | Male fresh grads |
| NRIC on resume | CONFIRMED | One-time | All (especially older users) |
| GLC vs MNC photo confusion | REAL but minor | One-time | All |
| No SG-specific AI intelligence | CONFIRMED — but recurring value is in job-tailoring, not SG flags | Every application | All |

**Key reframe**: SG-specific intelligence (NS, NRIC, GLC) is a **trust signal** and credibility differentiator, not the recurring value driver. The recurring value is job-specific match + revision. Build marketing around trust ("built for Singapore"), product around job-tailoring ("for this role, at this company").

# Round 2 Analysis — Founder Inputs and Open Questions

> Written: 2026-04-29 after Phase 01 analysis review.
> These are founder corrections, new feature proposals, and deeper research requests.

---

## Founder Positions (Confirmed)

1. **SG-specific features are NOT the core value proposition.** NS/NRIC/photo advice are trust signals and differentiators, but not the reason users pay. Core value = per-job tailored resume revision + full-cycle outcome tracking.

2. **Agree with B2B-first GTM sequence.** Month 1 priority = lock one university pilot.

3. **USP to be redefined after full analysis** (deferred from this round).

---

## Question 1: Competitive Re-Analysis (Higher Threat Baseline)

Given that SG-specific features are NOT the core value prop, the threat level from all competitors increases. A competitor does not need SG localisation to replicate the core value (job-specific resume tailoring + outcome tracking).

**Specific request:**
- Re-assess all competitor threat levels under the assumption that SG intelligence is a secondary feature, not the primary defensibility
- Deep-dive on **VMock** — founder knows this is a university-partnered AI resume tool already operating in this space. Research: what does it do, which universities has it partnered with (especially SG/Asia), pricing, features, weaknesses
- Map the B2B university market: who else is in it, what agreements already exist, where is there space to enter

**Key question**: Given VMock and similar products, is there still an opening to enter the university B2B market? What would the pitch need to be?

---

## Question 2: Differentiation — URL Parsing + Full Cycle, and New Interview Prep Feature

**Founder's differentiation thesis:**
The true differentiation is:
1. **Direct URL paste → automatic JD keyword extraction → embedded in resume revision** — this is NOT what ChatGPT does natively. ChatGPT requires manual copy-paste of JD; KeyStone removes this friction and embeds job intelligence automatically.
2. **Full-cycle tracking + feedback** — from application submission to callback to outcome, with feedback loop. No current tool closes this loop.

**New feature proposal — Interview Preparation Module:**
- User inputs their own stories and experiences (in their own words, unstructured)
- System analyzes the JD and generates:
  - High-frequency interview questions likely to be asked for THIS specific role/company type
  - Customised reference answers drawing on the user's own stories
  - Practice flow: user answers, system evaluates fit with the JD, suggests refinements
  - Users can iterate repeatedly ("practice until ready")

**Research requested:**
- Does any current tool do this combination (JD-anchored question generation + personal story integration + practice loop)?
- Is this technically feasible (LLM capability assessment)?
- What is the commercial case? Does this increase LTV? Does it create an additional revenue tier?
- Does this extend the product's useful window BEYOND the resume stage (solving the "user gets a job and leaves" LTV problem)?

---

## Question 3: B2B-First SaaS — Comparable Products and Performance

Find products in a similar space (career tech, edtech, job-search AI) that have used a B2B-first (university/institution) go-to-market model. Analyse:
- What did they do right / wrong?
- What were their actual B2B contract sizes and timelines?
- What enabled them to stand out from competitors in the university procurement decision?
- What does KeyStone need to do differently to win over incumbents already in these institutions?

---

## Question 4: Early B2B Free Strategy — Feasibility

**Proposal**: In early B2B partnerships (Month 1–6), offer the service free to universities. Use this period to:
- Continuously improve and train the model on real SG user data
- Build outcome data
- Earn trust and case studies

**Core tension**: Why would a university partner with KeyStone (unproven) over VMock or a WSG-endorsed tool?
- Do we need some pre-training / pre-built capability BEFORE approaching universities?
- What is the minimum credible product that earns a university pilot commitment?
- What is the persuasion narrative for a career centre director who has never heard of KeyStone?

**Research requested:**
- What does a "minimum credible" AI resume product look like for a university buyer?
- Is there a strategy to get a first university partner without a track record?
- How have other early-stage edtech companies won their first institutional client?

---

## Question 6: User Pain Points and Behaviour — Deep Analysis

**Founder's goal**: Build a product that is truly useful to users AND commercially viable AND occupies a currently underserved space. To do this, we need to understand the COMPLETE user experience of a Singapore job seeker — not just resume writing.

**Research requested:**
- Map the full job search journey (from "I need a job" to "I accepted an offer") — every stage, every pain point
- At each stage: what tools exist, what is missing, what is the emotional state?
- Where is the pain MOST acute and MOST underserved simultaneously?
- What user behaviors (positive and negative) shape whether a job search succeeds?
- What does a successful SG job seeker do differently from an unsuccessful one? (behavioural differences)
- Given the full journey map, which parts does KeyStone currently address? Which high-value parts does it NOT address yet?
- Specific to the interview prep proposal: where does interview anxiety and preparation fit in the pain map? Is it high enough priority to build?

**Output wanted**: A comprehensive user journey map and pain point prioritisation framework that can drive future product feature decisions.

# Break-Even Optimization Risks and CAC Analysis

> Analysis date: 2026-04-29
> Phase: 01 Analysis
> Project: KeyStone — AI Resume Optimization SaaS

---

## Executive Summary

KeyStone's break-even path runs through three optimizations: free-tier first-job unlimited, annual plan with advisor benefit, and 8 agency deals. Each optimization carries distinct risks that could undermine the strategy if unaddressed. The CAC analysis reveals paid acquisition is only viable for annual plan conversions, and the core LTV challenge is churn management — users leave when they get a job, which is the product working as designed. The highest-leverage LTV extension is post-job outcome tracking, which is near-zero cost and keeps users in the ecosystem.

**Complexity: Moderate** — three independent risks, all manageable with pre-launch mitigations.

---

## 1. Risks of Each Break-Even Optimization

### Optimization 1: First-Job Unlimited Suggestions

**The strategy**: Give users unlimited AI suggestions on their first job match to enable full product evaluation before the paywall.

**Risk 1a: Users get full value on first job, never upgrade**
The product delivers complete value during the free evaluation. If a user's first job search ends successfully (they get an offer), they experience zero friction, zero cost, and the product worked. They have no reason to upgrade.

**Mitigation**: The upgrade trigger fires on the second job search — the moment they encounter their next job they want to apply for and hit the paywall. This is the intended design per `specs/business-model.md` § Freemium Architecture: "The conversion trigger is: user hits the paywall on a job they really want." Ensure the free tier's first-job unlimited does not extend to subsequent jobs.

**Risk 1b: "Unlimited" encourages excessive use, increasing LLM costs**
An unlimited offering on first job with no throttle could attract power users who generate 50+ suggestions per job, driving per-user LLM cost above the SGD 5/user/month ceiling noted in `specs/business-model.md` § Unit Economics.

**Mitigation**: Implement a suggestion-count soft cap at 20 suggestions per job match (above which a prompt suggests "you may be over-customizing — employers value authenticity"). Cap at 30. Monitor 95th-percentile usage at launch and adjust. The architectural constraint of SGD 5/user/month max must be implemented before launch.

**Risk 1c: Competitors offer the same model**
Teal HQ (and similar platforms) offer unlimited resume suggestions in their paid tiers. A competitor could match this offer at no cost, eroding the differentiation of "first job unlimited."

**Mitigation**: The first-job unlimited is a evaluation tool, not a value proposition. KeyStone's differentiation is the per-job tailoring depth and MCF job matching. If a competitor matches the same offer, the conversion rate impact is absorbed by the annual plan and agency channel diversification.

---

### Optimization 2: Annual Plan with Advisor Session

**The strategy**: Add a qualitative benefit (human advisor session) to the annual plan to differentiate it from a pure discount and increase LTV from SGD 180 to SGD 194–244 effective value.

**Risk 2a: No actual advisor partners lined up at launch**
The benefit is promised but no partner relationships exist. Launching with "1 advisor session" in the marketing and having no mechanism to book it creates a broken promise on day one — the worst possible first impression for paying customers.

**Mitigation (mandatory before launch)**: Partner with 3–5 career coaches or resume advisors before launch. Define the session format (30 min, video call, structured agenda). Build the booking flow (Calendly embed or equivalent). If partners are not confirmed 2 weeks before launch, remove the benefit from the annual plan description and replace with "priority analysis queue" or "early access to new features" — a real but undelivered benefit is worse than a modest替代.

**Risk 2b: Advisor sessions are hard to book, creating bad UX**
If the advisor calendar is full or the booking process has friction (email exchange, waitlist), paying customers feel their SGD 180 did not buy what was promised. The qualitative benefit becomes a complaint driver.

**Mitigation**: Define a maximum wait time (48 hours) and a direct backup (pre-recorded webinar) if advisors are unavailable. Include a satisfaction survey post-session. Treat advisor session NPS as a leading metric.

**Risk 2c: "Advisor session" feels like a gimmick**
SGD 180/year customers may have low expectations for a "free advisor session" from a startup. If the session quality is average, it reinforces the perception that the annual plan was just a discount with a token add-on.

**Mitigation**: Select advisors who are specific to Singapore job market (familiarity with MCF, Singapore CV norms, local employer expectations). Frame the session as "career strategy" not "resume review." Quality of the advisor matters more than the session existing.

---

### Optimization 3: 8 Agency Deals in Year 1

**The strategy**: Target 8 recruitment agencies at SGD 1,200/year each (SGD 10/seat/month × 10 seats × 12 months) for SGD 9,600 total B2B ARR, accelerating break-even.

**Risk 3a: Agency deals require personal outreach, not scalable**
Agency sales is a relationship business. Each agency deal requires a founder or sales person to cold outreach, demo, negotiate, and close. Eight deals in Year 1 means 20–40 conversations. This is time-intensive and does not scale linearly.

**Mitigation**: Start with 1–2 agencies in the first quarter to prove the model. Document the pitch, objections, and close process. Use the first deals to build a case study. Scale to 8 only after the sales motion is proven and can be handed off or templated. Per `specs/business-model.md` § Recruitment Agencies: "Target 5–10 agency deals in Year 1 as 'quick B2B wins' while university contracts are in procurement pipeline" — 5–10 is a range, start at the low end.

**Risk 3b: Agencies may not prioritize KeyStone referrals**
The value proposition to agencies is "candidates prepared with KeyStone → higher offer acceptance rate → you earn placement fee faster." If agencies do not see a direct revenue impact, they will not push KeyStone to candidates.

**Mitigation**: Track offer acceptance rate for candidates who used KeyStone vs. those who did not. Build a measurable case study: "Agencies using KeyStone referral saw 23% higher offer acceptance in Q2." Without data, the value prop is anecdotal. Define the metric before launching the channel.

**Risk 3c: Distribution channel model requires free seats, creating cost without immediate revenue**
Agencies need free seats for candidates to try KeyStone. This creates free users who consume LLM resources (SGD 0.80/user/month per `specs/business-model.md` § Unit Economics) with no immediate revenue offset.

**Mitigation**: Limit free seats per agency (max 5 per agency in pilot). Require agency point-of-contact to track candidate outcomes. If no measurable outcomes after 3 months, re-evaluate the arrangement. The free seat cost is justified only if it produces the offer-acceptance metric.

---

## 2. CAC Analysis: Paid Acquisition Viability

### Current LTV by Plan Type

| Plan | Revenue | Avg. Subscription Length | LTV |
|------|---------|--------------------------|-----|
| Monthly Pro | SGD 19/month | 3 months (job search tenure) | SGD 57 |
| Annual Pro | SGD 180/year | Annual | SGD 180 |
| Annual Pro + advisor | SGD 180 + coach value | Annual | SGD 194–244 effective |

*Source: `specs/business-model.md` § LTV/CAC Considerations*

### Paid Acquisition CAC Benchmarks

| Channel | Estimated CAC | Viability at SGD 57 LTV | Viability at SGD 180 LTV |
|---------|-------------|--------------------------|--------------------------|
| Google Search Ads | SGD 40–80 | No (CAC > LTV) | Yes (CAC < LTV) |
| Meta / Instagram | SGD 20–40 | Borderline | Yes |
| LinkedIn | SGD 60–120 | No | Borderline |
| Organic (SEO, community) | SGD 0–5 | Yes | Yes |

*Source: `specs/business-model.md` § "Paid acquisition has estimated CAC of SGD 40–80 — unprofitable at SGD 57 LTV"*

### CAC Viability Conclusion

**Paid acquisition ONLY viable for annual plan conversions.** At SGD 57 LTV (monthly), even the lowest estimated CAC (SGD 20–40) leaves little margin. At SGD 180 LTV (annual), paid acquisition becomes a viable channel with positive unit economics.

### When does paid acquisition become viable?

The break-even point for paid acquisition depends on two variables:

**Variable 1: Annual plan mix**
If 30% of signups choose annual, blended LTV rises to:
`(70% × SGD 57) + (30% × SGD 180) = SGD 39.90 + SGD 54 = SGD 93.90 blended`
Still below SGD 40–80 CAC range. Annual mix needs to reach 50%+ before paid search becomes marginally viable.

**Variable 2: Subscription length extension**
If average subscription extends from 3 months to 6+ months (through LTV extension features), monthly LTV rises to SGD 114+, making paid acquisition viable at lower CAC.

**Recommendation**: Do not run paid acquisition in Year 1. Focus on:
1. Annual plan conversion optimization (landing page, trial-to-annual upsell)
2. Organic acquisition channels (university spillover, Reddit r/singapore, SG career Facebook groups)
3. Agency channel (B2B, not CAC-dependent)

Introduce paid acquisition in Year 2 when:
- Annual plan mix > 40% of conversions
- LTV extension features keep users subscribed 5+ months
- CAC can be refined against real cohort data

---

## 3. Low-Cost LTV Extension Features

KeyStone's LTV problem is structural: users churn when they get a job. The product works, so users leave. LTV extension means keeping churned users engaged in the ecosystem through their next career move.

The features below cost near-zero to implement and extend subscription tenure by 2–6 months each.

### Feature A: Post-Job Outcome Logging (P0 — Near-Zero Cost)

**What it is**: After a user gets a job, prompt them to log the outcome: "I got the job at [Company]!" This is a celebration moment that also creates a retention hook.

**How it extends LTV**:
- User stays active to log the outcome (2–3 weeks of post-search engagement)
- "Track your new role" onboarding begins (30-day check-in, 90-day check-in)
- At 90 days: "Still at the same role?" → if left, re-activation offer

**Cost**: Near zero. Email sequence only. No LLM calls beyond the initial celebration prompt.

**Implementation**: Automated email sequence triggered when user hasn't logged in for 14 days after a job application milestone.

---

### Feature B: Passive Job Monitoring / Alert (P2 — Low Cost)

**What it is**: "Alert me when jobs matching my profile appear on MCF." User specifies target roles/industries. Weekly email digest when matching jobs appear.

**How it extends LTV**: Users stay subscribed "just in case" — they are employed but want to know if a better opportunity appears. Keeps them in the paid subscriber base without active job searching.

**Cost**: Low. Weekly email digest only. No app usage of LLM. Marginal infrastructure cost only.

**Risk**: Must not spam. Max 1 email per week. Relevance algorithm must be good enough that users do not unsubscribe.

---

### Feature C: Skill Gap Tracking (P3 — Low Cost)

**What it is**: "Based on jobs you're applying to, here's the skill gap." Shows users what skills appear in job postings they are targeting but are missing from their resume.

**How it extends LTV**: Keeps users engaged between active job searches. A user who finished one job search cycle but is "thinking about next move" stays subscribed to track skill development.

**Cost**: Low. Aggregated analysis of job posting skill requirements vs. user resume. Can be a pre-computed weekly report.

---

### Feature D: Referral Mechanic as LTV Extension (P2 — Near-Zero Cost)

**What it is**: "Refer a friend who gets a job = 1 month extended subscription." Every confirmed referral extends the referrer's subscription by 1 month.

**How it extends LTV**: Users who have referrred friends stay active to see if their friend succeeded. The referral reward creates a reason to remain subscribed even after the user's own job search ended.

**Cost**: Near zero. One month of subscription cost (SGD 19) vs. cost of new user acquisition (SGD 0 if organic). Net positive.

---

### Feature E: Post-Hire Career Check-In (P2 — Low Cost)

**What it is**:
- 30 days post-hire: "How's the new role going?" (short NPS survey)
- 90 days post-hire: "Still at the same role?" (if left → re-activation prompt; if stayed → promotion tracking)

**How it extends LTV**: The 90-day re-activation prompt converts a churned subscriber into an active one if they left the role. Even a 10% re-activation rate meaningfully extends average LTV.

**Cost**: Low. Automated email sequence. No LLM required.

---

## 4. LTV Extension Priority Matrix

| Feature | LTV Impact | Implementation Cost | Launch Priority |
|---------|-----------|---------------------|----------------|
| Post-job outcome logging | +2–3 months retention | Near zero | **P0** — launch with |
| Annual plan with advisor | 3× monthly LTV (SGD 57 → SGD 180) | Partner cost (recurring) | **P1** — before agency channel launch |
| Passive job alerts | +3–6 months (employed-but-watching) | Low (email only) | **P2** — Month 3 |
| Referral mechanic | +1–2 months per referral | Near zero | **P2** — Month 3 |
| Career check-in (30/90 day) | +1–2 months via re-activation | Low (email only) | **P2** — Month 3 |
| Skill gap tracking | +1–2 months (between searches) | Low | **P3** — Month 6+ |

---

## 5. The Key Insight on LTV

**KeyStone's LTV problem is churn, not revenue per user.**

The product works. Users get jobs. Users leave. The subscription ends. This is the intended outcome — but it means the business model cannot rely on sustained monthly subscription revenue from any individual user.

```
Monthly Pro LTV = SGD 19 × 3 months = SGD 57
Annual Pro LTV = SGD 180 × 1 year = SGD 180
```

The path to higher LTV is not raising prices. It is extending the subscription lifecycle beyond the job-search window.

**LTV extension = keeping churned users in the ecosystem**

```
User gets job → logs outcome → tracks new role → 90-day check-in → left role → re-activate
```

The user who would have churned after 3 months stays subscribed for 6–9 months through the post-hire engagement sequence. This doubles effective LTV without changing the price.

**The biggest risk of all three break-even optimizations combined**:

Optimizing for acquisition (unlimited free tier, annual plan, agency deals) while not solving the churn problem means spending resources to bring users in who leave after 3 months. The break-even optimizations are only sustainable if paired with LTV extension features that keep users through at least one career transition.

**Priority order**:
1. Solve churn first (post-job outcome logging, career check-ins)
2. Then optimize acquisition (annual plan, agency deals)
3. Then invest in paid acquisition (Year 2, when cohort data supports CAC model)

---

## 6. Cross-Reference Audit

| Document | Claim | Assessment |
|----------|-------|------------|
| `specs/business-model.md` § LTV/CAC | "Paid acquisition has estimated CAC of SGD 40–80 — unprofitable at SGD 57 LTV" | Confirmed. CAC > LTV for monthly plan. |
| `specs/business-model.md` § LTV/CAC | "Annual plan multiplies LTV 3× vs monthly" | Confirmed. SGD 180 vs SGD 57 = 3.16× |
| `specs/business-model.md` § Unit Economics | "Free user cost: SGD 0.80/user/month" | Confirmed. Used for agency free-seat cost estimate. |
| `specs/business-model.md` § Freemium | "First-job unlimited enables full product evaluation" | Confirmed. Mitigations noted for risk 1a (upgrade trigger on second job). |

---

## 7. Success Criteria

- [ ] Agency channel pilot launched with 1–2 agencies by end of Month 1, with offer-acceptance tracking defined
- [ ] Annual plan advisor benefit confirmed with 3–5 partners before any marketing mentions it
- [ ] Post-job outcome email sequence implemented before launch (P0 LTV feature)
- [ ] Paid acquisition NOT run in Year 1; budget directed to organic channels
- [ ] Monthly cohort churn rate tracked from Month 1 — target < 15% monthly churn for Pro users
- [ ] Annual plan mix tracked from launch — target > 30% annual by Month 6

---

## 8. Risks and Mitigations Summary

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Users get full value on first job, never upgrade | Medium | High | Upgrade trigger on second job; do not extend free tier beyond first job |
| Advisor sessions not bookable at launch | High | High | Confirm partners 2 weeks before launch; have backup benefit ready |
| Agency deals not scalable (personal outreach) | High | Medium | Start with 1–2, prove model, templatize sales motion before scaling |
| Paid acquisition burns budget on negative unit economics | High | High | No paid acquisition in Year 1; organic only |
| LTV capped by churn, not acquisition | High | High | Post-job outcome tracking and career check-ins (P0) before any acquisition spend |
| LLM cost ceiling exceeded by unlimited free tier | Medium | High | Soft cap at 20 suggestions per job; architectural SGD 5/user/month ceiling implemented before launch |

# B2C Acquisition Channels Analysis

> **Purpose**: Identify 3-5 practical, data-reliable B2C acquisition channels for KeyStone. Assess channels against practicality, data quality, expected volume, and cost. Produce a prioritised recommendation.
>
> **Context**: KeyStone is an AI resume optimization SaaS for Singapore job seekers. B2B-first strategy (university pilots + recruitment agencies) is the primary path. B2C channels are a secondary lever to build user volume and outcome data. No large marketing budget; startup with lean operations. The user specifically wants channels that produce users who complete the full workflow and log outcomes -- not vanity signups.
>
> **Assumes**: Product is functional (resume upload, job URL parsing, job-match assessment, suggestions). Free tier (3 analyses/month) is active. Pro tier at SGD 19/month or SGD 180/year exists.

---

## Executive Summary

KeyStone's B2C strategy should prioritise three channels: **(1) referral program from B2B pilot users**, **(2) career coach and interview coach partnerships**, and **(3) Reddit/r/singapore community presence**. These channels produce users with high intent who are likely to complete the full workflow and log outcomes. University career centre spillover (from the B2B-first strategy in file 13) is a fourth channel that becomes active once the first pilot launches.

Avoid: Carousell listings, Discord servers (for now), and cold LinkedIn outreach.

---

## Channel Assessment Framework

Each channel is assessed on:

- **Practicality (1-10)**: How quickly can this channel be activated with minimal resources?
- **Data Quality (High/Medium/Low)**: Does this channel produce users who actually use the product and log outcomes, or just vanity signups?
- **Volume estimate**: Realistic monthly user acquisition potential in SG context
- **Cost**: 0 = free, Low = <SGD 500/month, Medium = SGD 500-2000/month
- **Timeline to first users**: How fast can this channel produce the first signups?

**Data quality is the controlling criterion.** A channel that produces 50 users who complete the full workflow is more valuable than one that produces 500 signups who never return. KeyStone's moat is outcome data (suggestion_signals table, outcome logging per file 13), not user count.

---

## Channel 1: Referral Program (Existing User Referrals)

### Description
Existing free-tier or pilot users refer their network. Each referred user gets bonus analyses; referrer gets recognition or feature access. Structured referral mechanic with tracking links.

### Practicality: 8/10
- Technical implementation: minimal (tracking links, a "share" flow in the product, simple credit system)
- Can be live within 1-2 weeks of product having a shareable output
- No distribution building required -- leverages users who already have the product

### Data Quality: HIGH
- Referred users come with social proof from someone they trust
- The referrer is invested in the product working (their credibility is on the line)
- Referred users who come through a referrer have higher activation rates than cold signups
- Referred users are more likely to log outcomes because the referrer has set an expectation

### Expected Volume
- Month 1-3: Near zero (no user base yet)
- Month 4-6: 20-50 referred users/month (once B2B pilots are live with 200+ users)
- Month 6-12: 50-150 referred users/month (compounding as user base grows)
- Note: Volume is low initially but scales with B2B pilot success

### Cost
- 0 to Low: Developer time to build the referral mechanic (1-2 days)
- Ongoing cost: Free analyses credits (marginal cost near zero since边际 cost of AI analysis is low)
- No cash outlay required

### Execution
1. Build a "Share your results" flow in the product -- generates a unique referral link per user
2. Display the link after every successful analysis with copy button
3. When a referred user signs up and completes 3 analyses, credit the referrer
4. Send a notification to the referrer when their link converts ("Your friend just signed up!")
5. Do NOT require the referred user to pay -- free tier activation is sufficient

### Why This Works for KeyStone
Referral works when the product produces a shareable, visible output. KeyStone's job-specific resume suggestions are exactly that -- users want to show the suggestions to friends. The share mechanic should emphasise the output ("See how I improved my resume for the DBS role"), not the product.

---

## Channel 2: Community Partnerships (Career Coaches, Interview Coaches)

### Description
Partner with independent career coaches, interview prep coaches, and LinkedIn profile writers who already serve SG job seekers. They recommend KeyStone to clients as a complement to their coaching service. Revenue share or referral credit model.

### Practicality: 7/10
- Requires outreach to 10-20 coaches; 2-3 will convert
- Coaches are reachable via LinkedIn; no cold email required if founder has a network
- No formal contract needed initially -- informal referral arrangement
- Pitch is easy: "I give my clients resume advice; KeyStone gives them 24/7 second opinions between our sessions"

### Data Quality: HIGH
- Coaches send users who are actively job searching and motivated
- Coach-referred users complete the workflow because their coach set an expectation
- Outcome logging is higher because coaches can encourage clients to log results
- If coach tracks client outcomes (some do), KeyStone gets indirect outcome data
- This channel produces the highest-quality users per acquisition

### Expected Volume
- Month 1-3: 10-30 users/month from 2-3 active coach partners
- Month 4-6: 30-80 users/month from 5-8 active coach partners
- Month 6-12: 80-200 users/month from 10+ active coach partners
- Each coach serves 5-20 active clients at any time

### Cost
- Low: SGD 200-500/month in referral credits or modest revenue share (e.g., 15% of referred Pro subscriptions)
- Founder time: 3-5 hours/month managing coach relationships

### Execution
1. Identify 20 career coaches/interview prep coaches on LinkedIn in SG
2. Send personalised LinkedIn message: "I built an AI tool that gives job-specific resume suggestions -- I'm looking for coaches who'd want to recommend it to clients as a complement to your service. Would you be open to a 20-minute call?"
3. Give each coach a unique referral link and a one-pager to share with clients
4. Offer coaches a dashboard showing their referred clients' usage (engagement lever for them)
5. Set up a simple revenue share for Pro conversions: e.g., SGD 5 per referred user who upgrades to Pro

### What Coaches Need to See
- The product produces job-specific suggestions (not generic advice)
- Their clients can use it between sessions without the coach losing control
- It reflects well on the coach (the tool enhances the coach's advice, doesn't replace it)

### Why This Works for KeyStone
Career coaches are a trusted intermediary. Their recommendation carries weight. A user who signs up because their interview coach recommended it arrives with intent, activation cost is low, and outcome logging is more likely because the coach is tracking their progress.

---

## Channel 3: Reddit (r/singapore, r/NTU, r/NUS, rjobs)

### Description
Organic presence in SG Reddit communities. Post useful, non-promotional content that demonstrates the product's value. Answer resume questions when they come up. Build karma and trust before any promotion.

### Practicality: 7/10
- Zero cash cost
- Requires consistent time investment (2-3 hours/week for 2-3 months before meaningful traction)
- Account needs karma-building period (2-4 weeks of non-promotional participation first)
- SG Reddit communities are active and responsive to career content

### Data Quality: MEDIUM-HIGH
- Reddit users who find KeyStone organically are self-selecting for resume help
- However: Reddit signups skew toward younger users (21-26) who are earlier in career
- Outcome logging rates on Reddit referrals are lower than coach referrals (no intermediary accountability)
- Data quality is acceptable but not the highest of all channels

### Expected Volume
- Month 1-3: 10-30 signups/month (karma-building period)
- Month 4-6: 30-80 signups/month (consistent presence, occasional viral posts)
- Month 6-12: 50-150 signups/month (established presence, content compounds)
- Quality: primarily fresh grads and early-career PMETs; lower proportion of mid-career switchers

### Cost
- 0: Time investment only
- If running Reddit ads (optional): Low-Medium (SGD 200-1000/month for targeted ads in r/singapore)

### Execution
**Phase 1 (Weeks 1-4): Karma building**
1. Create a new Reddit account (or use existing)
2. Spend 2-4 weeks participating in r/singapore, r/NTU, r/NUS, rjobs with non-promotional content
3. Comment on resume/CV threads offering genuine advice
4. Do NOT mention KeyStone yet

**Phase 2 (Month 2): Soft presence**
5. Create a post about "How I improved my resume for a Singapore job" using real (anonymised) KeyStone output
6. Do not pitch the product directly; show the output and let readers draw conclusions
7. Respond to every comment with genuine engagement

**Phase 3 (Month 3+): Value-first promotion**
8. Answer every resume question in SG subreddits with KeyStone-backed suggestions
9. Create a subreddit-quality FAQ post about common SG resume mistakes
10. Include a link to KeyStone only if it genuinely adds value

**What NOT to Do**
- Do not post "Check out my AI resume tool!" posts -- community will reject
- Do not mention KeyStone in the first 4 weeks of account activity
- Do not astroturf (fake engagement) -- Reddit communities detect this immediately

### Reddit Content Ideas
- "What got me the interview at [SG company]: resume breakdown" (anonymised KeyStone output)
- "Common resume mistakes I see from Singapore job seekers" (drives from KeyStone's pattern analysis)
- "How to tailor your resume for a Singapore Government Scholarship" (SG-specific, high-value)
- "Before and after: resume improvement using AI" (real output, anonymised)

### Why This Works for KeyStone
SG Reddit communities are active, engaged, and suspicious of corporate accounts. A value-first approach builds trust. The product's SG-specific output (NS framing, MCF job-tailored suggestions) is genuinely differentiated from generic tools and Reddit will notice. The compounding effect of good content is real -- one well-received post can drive 200+ signups over 6 months.

---

## Channel 4: University Career Centre Spillover

### Description
Students who use KeyStone through a university pilot share it with friends outside the university. Also: students who don't use VMock or the university career centre find KeyStone through organic search or peer sharing.

### Practicality: 6/10
- Depends entirely on the B2B-first pilot strategy (file 13) succeeding first
- Cannot be directly executed -- it emerges from pilot success
- However: the referral mechanic (Channel 1) should be active within the pilot to capture spillover
- If the pilot is running, spillover happens organically within 2-3 months

### Data Quality: HIGH
- Students referred by peers have similar profile to coach referrals (social proof, trusted source)
- Peer-referred users complete the workflow at higher rates than cold signups
- Outcome logging is higher when the referrer has set expectations
- However: peer spillover users tend to be same cohort (fresh grads), limiting demographic diversity

### Expected Volume
- Month 1-3: 0 (pilot not launched yet)
- Month 4-6: 20-50 spillover users/month from first pilot
- Month 6-12: 50-150 spillover users/month as pilot scales across institutions

### Cost
- 0: No incremental cost -- emerges from B2B pilot execution
- However: requires the referral mechanic (Channel 1) to be live

### Execution
1. Prioritise the B2B pilot strategy from file 13 -- this channel depends on it
2. Ensure the referral mechanic (Channel 1) is built before the pilot launches
3. Ask pilot students to share KeyStone with friends (explicitly frame as "help your friends")
4. Track which university cohorts produce the most spillover -- double down on those

### Why This Works for KeyStone
University spillover is the most natural B2C activation path from a B2B-first strategy. When 200 students at SIT are using KeyStone, their friends at NUS, SMU, and polytechnics will hear about it. The peer-to-peer trust transfer is powerful.

---

## Channel 5: SG Job Fairs and Career Events

### Description
Physical presence at SG job fairs (National Career Fair, university career fairs, industry-specific events). Free or low-cost booth presence. Demo the product live. Collect signups via QR code to the product.

### Practicality: 6/10
- Moderate execution effort: 2-3 days of event staff time per major fair
- Most SG job fairs have low booth costs (SGD 500-2000 for small startups) or are free
- Events are frequent: National Career Fair, university career fairs (NUS, NTU, SMU, SIT, SUSS each have their own), industry-specific fairs (FinTech, Tech, Healthcare)
- Requires physical presence -- not scalable remotely

### Data Quality: MEDIUM
- Job fair attendees are actively job searching (high intent)
- However: conversion from booth visit to signup to activated user is low (10-20% of signups actually activate)
- Outcome logging rates are lower than coach or peer referrals
- Job fair users tend to be in acute job-search mode (more motivated than average)

### Expected Volume
- Per major event: 50-200 signups, 10-40 activated users (20% activation rate is realistic)
- 4-6 events per year is realistic for a lean startup
- Annual potential: 200-800 signups, 40-160 activated users from events

### Cost
- Medium: SGD 500-2000 per event for booth/table
- Founder time: 1-2 days per event
- Material cost: SGD 200-500 (pop-up banner, flyers)
- Total per event: SGD 700-2500

### Execution
1. Target university career fairs first (lower cost, more targeted audience than National Career Fair)
2. Prepare a laptop/tablet running a live demo -- never just flyers
3. Have a "try it now" moment at the booth: user uploads a resume, pastes a job URL, sees output in 60 seconds
4. QR code to sign-up page; offer a bonus analysis (4th free analysis) for signing up at the event
5. Collect business cards or WhatsApp contacts for follow-up (with consent)
6. Follow up within 48 hours of the event with a personalised message

### What Makes Event ROI Positive
Event ROI is positive only if the cost per activated user is below SGD 20. With a 20% activation rate and SGD 1000 booth cost, that means 100 signups at the event. University fairs with 200-300 attendees can produce this. National Career Fair (10,000+ attendees) can produce 500+ signups but requires more investment.

---

## Channel 6: LinkedIn Organic (Founder's Personal Network)

### Description
The founder publishes LinkedIn posts about resume advice, job search tips, and KeyStone's SG-specific insights. Builds personal brand as a SG career-tech voice. Drives signups from the founder's network and their network's network.

### Practicality: 5/10
- Easy to start (founder already has LinkedIn)
- Hard to scale (dependent on one person's network and content output)
- Algorithm rewards consistency; 3 posts/week minimum for traction
- SG LinkedIn community is smaller but engaged

### Data Quality: MEDIUM
- Network-effect users (friends of friends) have moderate intent
- LinkedIn users skew older and more senior (mid-career PMETs) -- valuable demographic for KeyStone
- However: LinkedIn signups from organic posts have lower activation rates (people click, don't return)
- Outcome logging rates are lower than coach or peer referrals

### Expected Volume
- Month 1-3: 20-50 signups/month (network effect from founder's 500+ connections)
- Month 4-6: 30-80 signups/month (if content is consistent)
- Diminishing returns without paid amplification

### Cost
- 0: Time investment only
- Founder time: 3-5 hours/week for content creation and engagement

### Execution
1. Post 2-3x per week on LinkedIn -- not product promotion, career advice
2. Content pillars: (a) SG resume mistakes, (b) MCF/JobStreet job analysis insights, (c) NS experience framing, (d) case studies (anonymised)
3. Engage with every comment and DM within 24 hours
4. After 4-6 weeks of building content, include a soft CTA ("If you want to try the tool I mention, here's a link")
5. Repurpose content for Reddit and Telegram (Channels 3 and note below)

### Why This Works for KeyStone
The founder is the product's best salesperson. LinkedIn personal brand builds credibility that a company account cannot match. SG mid-career PMETs (the Pro tier target) are on LinkedIn daily. The content strategy should focus on demonstrating SG expertise, not generic resume advice.

---

## Channel 7: Telegram Groups (SG Jobs, Grad Jobs)

### Description
Presence and participation in Telegram groups focused on Singapore jobs, graduate jobs, and career discussion. Examples: "SG Jobs & Job Search", "NUS Careers", "SG Graduate Exchange".

### Practicality: 4/10
- Telegram groups are notoriously resistant to promotional content
- Most groups have explicit rules against self-promotion; violating = immediate ban
- Requires long-term community participation (months) before any promotion is acceptable
- Groups are often moderated by volunteers who may be hostile to commercial products

### Data Quality: MEDIUM
- Telegram users who discover KeyStone organically are self-selected job seekers
- However: Telegram group dynamics reward attention-seeking content, not genuine value
- Users from Telegram tend to have lower engagement depth than Reddit or coach referrals
- The risk of being banned is high if approach is perceived as spam

### Expected Volume
- Month 1-6: 5-20 signups/month (community building period)
- Month 6-12: 20-50 signups/month (if community trust is established)
- Not a high-volume channel

### Cost
- 0: Time investment only
- Risk: reputation damage if perceived as spam

### Execution (If Pursued)
1. Join 5-10 relevant Telegram groups
2. Spend 2-3 months participating genuinely (answering questions, sharing insights)
3. Never post a link in the first 3 months
4. Only share KeyStone when someone asks a direct question that the product answers
5. Frame sharing as "I built a tool that might help with your question" -- not a promotion
6. Do NOT mass-post or send DMs to group members

### Why Practicality Is Low
Telegram groups are a high-risk, low-return channel for KeyStone. The community participation requirement (months of unpaid engagement) and ban risk make this inefficient relative to Reddit or coach partnerships. Reddit (Channel 3) offers similar audience reach with lower risk and better content permanence.

**Verdict: Low priority. Pursue only if Reddit (Channel 3) is producing insufficient volume after Month 3.**

---

## Channel 8: Carousell Listings (People Selling Job Search Services)

### Description
Listing resume writing, CV优化, or job search services on Carousell. Positioning KeyStone as part of the service offering, or advertising alongside complementary services.

### Practicality: 3/10
- Carousell is a consumer marketplace; users are looking for services, not AI tools
- Competing with resume writers who charge SGD 50-200 for a full resume rewrite
- KeyStone's free tier is hard to communicate on Carousell (users expect to pay for services)
- Carousell has high transaction fees for promoted listings

### Data Quality: LOW
- Carousell users looking for resume services have high purchase intent but expect a human deliverable
- They are not looking for an AI self-service tool
- KeyStone's free tier does not match the Carousell paid-service expectation
- Users who sign up via Carousell expect a different product than what KeyStone delivers

### Expected Volume
- Low: 10-30 signups/month
- Conversion to Pro: lower than other channels (users expect a completed resume, not suggestions)

### Cost
- Medium: Carousell promoted listings or seller fees
- Time cost: Creating and managing listings, responding to enquiries

### Why Avoid
Carousell attracts users who want someone else to do the work (resume writing service). KeyStone is a self-service tool that makes users better at writing their own resumes. This is a fundamental product-market fit mismatch. The users who buy resume services on Carousell are not KeyStone's users.

**Verdict: AVOID. Poor data quality, high cost, product-market fit mismatch.**

---

## Channel 9: Discord Servers (Tech/Finance Career Seekers)

### Description
Presence in Discord servers focused on tech careers, finance careers, or SG job searching. Discord servers exist for SG tech job seekers (e.g., SG Tech Jobs, SG Developers) and finance careers.

### Practicality: 4/10
- Discord servers are communities with their own norms and gatekeeping
- Requires being invited or building reputation over time
- Most servers have channels for job postings, resume feedback, interview prep
- Self-promotion is usually restricted to designated channels

### Data Quality: MEDIUM
- Discord users in career-focused servers are actively job searching
- However: Discord skews younger (18-25) and more tech-oriented
- Data quality is acceptable but demographic is narrower than other channels
- Discord communities are harder to reach without existing relationships

### Expected Volume
- Month 1-3: 5-15 signups/month (building presence)
- Month 4-6: 15-40 signups/month (established presence)
- Lower volume than Reddit but potentially higher per-user quality in tech-focused servers

### Cost
- 0: Time investment only
- Requires finding and joining servers (often invite-only)

### Execution
1. Find relevant Discord servers via Google ("SG tech jobs Discord server") or mutual connections
2. Request an invite; join servers focused on SG tech/finance careers
3. Participate genuinely for 4-6 weeks before sharing any product
4. Contribute to resume feedback channels with genuine advice
5. When appropriate, share KeyStone as a tool you've found useful

### Comparison to Reddit
Discord and Reddit have similar audiences (young, tech-adjacent job seekers) but Discord requires invite access and has smaller communities. Reddit (Channel 3) has larger reach and better content permanence. Reddit should be prioritised first; Discord is a supplement.

**Verdict: Low priority. Pursue only after Reddit (Channel 3) is established.**

---

## Channel 10: Government Programs (WSG, SkillsFuture Credited Courses)

### Description
Align KeyStone with WSG (Workforce Singapore) or SkillsFuture programmes. Explore whether KeyStone can be offered as part of a SkillsFuture Credit-eligible course, or partnered with WSG's career services.

### Practicality: 2/10
- SkillsFuture Credit is for approved courses, not individual SaaS tools
- Getting KeyStone approved as a SkillsFuture Credit-eligible course requires 6-12+ months of government process
- WSG partnerships require formal procurement processes
- This channel is too slow for a startup that needs traction in months, not years

### Data Quality: HIGH (if achieved)
- Government-referred users have high intent (using SkillsFuture Credit = motivated)
- However: government processes move slowly and the relationship would take 6-12 months to establish
- Not feasible as an early channel

### Expected Volume
- Month 1-6: 0 (process takes 6-12+ months)
- Month 12+: Potentially high volume if partnership is established

### Cost
- Low upfront, but requires significant founder time navigating government processes
- May require legal/compliance overhead for SkillsFuture certification

### Why Avoid (For Now)
Government channels are high-potential but long-lead-time. A startup that needs B2C traction in Month 1-6 cannot spend 6 months navigating SkillsFuture approval processes. This channel should be revisited in Year 2 when KeyStone has outcome data to demonstrate effectiveness.

**Verdict: AVOID for now. Revisit in Year 2.**

---

## Recommended Priority Order

### Tier 1: Execute Immediately (Month 1-2)

**1. Referral Program (Channel 1)**
- Reason: Lowest cost, fastest to build, highest quality users
- Prerequisite: Product must have shareable output
- Build time: 1-2 days
- Owner: Founder (technical build)

**2. Career Coach Partnerships (Channel 2)**
- Reason: Produces the highest-quality users; leverages founder's network
- Prerequisite: Product demo that works reliably
- Startup time: Week 1 outreach to 10 coaches
- Owner: Founder (outreach and relationship management)

### Tier 2: Build in Parallel (Month 2-3)

**3. Reddit Presence (Channel 3)**
- Reason: Compounds over time; zero cost; builds SG credibility
- Prerequisite: Reddit account with karma-building period (start Week 1)
- Content strategy: SG resume advice, not product promotion
- Owner: Founder (content creation)

**4. LinkedIn Organic (Channel 6)**
- Reason: Targets mid-career PMETs (Pro tier demographic); founder is the channel
- Prerequisite: Consistent content output (3 posts/week minimum)
- Startup time: Start posting Week 1
- Owner: Founder (personal brand)

### Tier 3: Activate When B2B Pilot Launches (Month 3-4)

**5. University Spillover (Channel 4)**
- Reason: Depends entirely on B2B pilot success
- Prerequisite: First pilot MOU signed and live
- Owner: Activates automatically if referral mechanic (Channel 1) is live

### Tier 4: Selective Events (Month 3-6)

**6. Job Fair Presence (Channel 5)**
- Reason: Moderate volume, moderate cost; good for product feedback
- Selection criteria: University career fairs only (lower cost, better fit)
- Target: 2-3 events in first year
- Owner: Founder (event attendance)

---

## Channels to Avoid

### AVOID: Carousell (Channel 8)
**Reason**: Product-market fit mismatch. Carousell users want resume writing services (someone else does the work). KeyStone is a self-service AI tool. The channel will produce low-quality users who expect a different product. Spend the time on coach partnerships instead.

### AVOID: Government Programs (Channel 10) -- For Now
**Reason**: Lead time is 6-12+ months for SkillsFuture/WGS partnerships. A startup that needs traction in Month 1-6 cannot allocate founder time to government procurement processes. Revisit in Year 2.

### AVOID: Telegram Groups (Channel 7) -- As Primary Channel
**Reason**: High ban risk, long community-building period (months), lower reach than Reddit. Pursue only if Reddit is producing insufficient volume after Month 3.

### AVOID: Discord (Channel 9) -- As Primary Channel
**Reason**: Smaller audience than Reddit, invite-only access, similar demographic. Reddit (Channel 3) should be prioritised first.

---

## Summary: Channel Comparison Table

| Channel | Practicality | Data Quality | Monthly Volume (Month 6) | Cost | Timeline to First Users |
|---------|-------------|--------------|--------------------------|------|------------------------|
| Referral Program | 8/10 | HIGH | 50-150 | 0 | 2-4 weeks (once base users exist) |
| Career Coach Partnerships | 7/10 | HIGH | 30-80 | Low (SGD 200-500/mo) | 2-4 weeks |
| Reddit (r/singapore) | 7/10 | MEDIUM-HIGH | 30-80 | 0 | 4-8 weeks |
| University Spillover | 6/10 | HIGH | 50-150 | 0 | Depends on B2B pilot |
| LinkedIn Organic | 5/10 | MEDIUM | 30-80 | 0 | 2-4 weeks |
| Job Fairs | 6/10 | MEDIUM | Event-based | Medium (SGD 700-2500/event) | 2-4 weeks |
| Telegram | 4/10 | MEDIUM | 20-50 | 0 | 2-3 months |
| Discord | 4/10 | MEDIUM | 15-40 | 0 | 2-3 months |
| Carousell | 3/10 | LOW | 10-30 | Medium | 2-4 weeks |
| Government Programs | 2/10 | HIGH | 0 ( Month 12+) | Low | 6-12 months |

---

## Risk Considerations

### Referral Program Risk
- If B2B pilots fail, referral program has no base to grow from
- Mitigation: Do not invest heavily in referral mechanic until first pilot is live

### Career Coach Risk
- Coaches may feel threatened by KeyStone (it reduces dependence on them for basic resume advice)
- Mitigation: Position KeyStone as a complement to coaching, not a replacement; emphasise that coaches save time on basic reviews

### Reddit Risk
- Account can be banned for perceived spam
- Mitigation: Strict karma-building period; value-first content; never mention product in first 4 weeks

### Job Fair Risk
- High cost per activated user if activation rate is low
- Mitigation: Target university career fairs first; always have a live demo at the booth; follow up within 48 hours

---

## Next Steps

**Week 1-2**:
1. Build referral mechanic (Channel 1) -- tracking links, share flow, credit system
2. Identify 10 career coaches on LinkedIn and send outreach messages (Channel 2)
3. Create Reddit account and begin karma-building (Channel 3)
4. Begin LinkedIn content cadence (Channel 6)

**Month 2-3**:
5. Activate coach partnerships; aim for 2-3 active coaches referring clients
6. Publish first Reddit content (non-promotional; demonstrate product value)
7. Begin B2B pilot conversations (file 13) to activate university spillover

**Month 3-4**:
8. Sign first pilot MOU; launch referral mechanic to pilot students
9. Identify 1-2 university career fairs to attend
10. Review channel performance; de-prioritise low-performing channels

---

*Analysis date: 2026-04-29. Volume estimates are based on Singapore market context, typical early-stage startup conversion rates, and the SG job seeker demographic. All estimates should be validated through actual channel execution and updated based on real data. Government program timelines (SkillsFuture, WSG) should be verified with current SG government digital services before any formal approach.*

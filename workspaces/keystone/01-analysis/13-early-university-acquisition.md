# Early University Acquisition Strategy — How to Win Without a Track Record

> **Purpose**: A concrete playbook for securing KeyStone's first Singapore university partner before the product has any track record, revenue, or case studies. Builds on the comparable analysis in `12-b2b-first-comparables.md`.

---

## The Core Question

How does an unproven early-stage product convince a Singapore university career centre to partner on a free pilot, when VMock and other established players already exist?

The honest answer: mostly, you cannot win on product quality. You win on relationship access, operational framing, and removing all risk from the decision. Everything below is about how to do those three things.

---

## 1. The University Decision-Maker's Calculus

### What risk does a career centre director actually take?

A career centre director who endorses a free KeyStone pilot is taking three distinct risks:

**Risk 1: Professional reputational risk.** If the product fails publicly (students complain, data leaks, outcomes worsen), the director's name is on the decision. In a small, collegial SG higher-education community, word travels. A bad pilot with an unproven startup is a career-damaging anecdote.

**Risk 2: Student trust risk.** Students share their resumes, job applications, and career anxieties. If that data is mishandled or the product gives bad advice that harms a student's application, the trust the career centre has built with students is damaged.

**Risk 3: Time and administrative overhead risk.** Running a pilot requires staff time: communicating to students, troubleshooting problems, collecting feedback, writing a report. For a team of 8-15 advisors serving 5,000-30,000 students, a 20-hour administrative burden is not trivial.

### What upside does the career centre director actually see?

The upside is almost entirely operational and KPI-linked. It is NOT "better AI than VMock" or "students get more callbacks." Those are outcomes the director cannot measure in a semester and cannot attribute clearly.

The actual upside, in descending order of what moves the director:

1. **Reduce the resume-review queue.** Most SG university career centres report that 30-50% of advisor-student interactions are basic resume reviews — formatting, structure, content. These are high-volume and low-skill relative to what a trained advisor can offer. If KeyStone handles the basic pass, advisors can serve more students or do deeper-value work. This is a measurable operational gain the director can report to their VP.

2. **Serve students who never come to the career centre.** A persistent pain point for career directors is the students who most need help (shy students, international students, lower-confidence first-gens) are the least likely to book an appointment. An always-available AI tool lowers the access barrier. This is a student-equity argument directors genuinely care about — and it shows up in their institutional reports.

3. **Analytics they don't currently have.** Most career centres have anecdotal data on where students apply. A KeyStone dashboard showing "this semester, 340 students applied to finance roles; their most common gap was quantification of achievements" gives the director insight to design better workshops. This is new operational intelligence.

4. **A story to tell in their annual report.** University career centres write annual reports to the VP of Student Affairs. "We piloted an AI career tool with 200 students" is a modern, forward-looking story. Career directors with innovation mandates value this.

### What makes a new product worth the administrative overhead of a pilot?

The pilot must be nearly zero-friction for the career centre team. Specifically:

- Students self-sign-up (career centre sends one email with a link; they do not manage accounts)
- No IT integration required (no SSO, no API, no integration with existing systems — at pilot stage, standalone is fine)
- KeyStone handles all student support enquiries directly (career centre staff are not first-line support)
- Structured mid-pilot and end-pilot feedback template provided by KeyStone (career centre does not have to design evaluation)
- Founder availability for a 30-minute mid-pilot check-in (personal accountability)

If the pilot requires the career centre to do anything beyond "send one email to students," you have made it too hard.

### What is the table-stakes quality threshold below which no university pilot is possible?

Below this line, no SG university career centre will agree to any pilot, regardless of relationship or pitch:

1. **PDPA-compliant data handling**: a written one-pager explaining what data is collected, where it is stored (SG region), who can access it, and the student deletion process. Without this, the conversation ends at the first question.

2. **Professional UX on a real domain**: the product must look like a real product, not a prototype. A domain name (keystone.sg or equivalent), a homepage that explains what it does, a functional login flow, and a working core feature. If it looks like a hackathon project, the career centre is not lending it institutional credibility.

3. **Working core functionality with SG examples**: the demo must show the product processing a real SG-style resume against a real SG job posting. Not: "here's what it will do." Yes: "here, I'll upload this SMU Finance graduate's resume and this DBS job posting right now."

4. **A named founder who can be contacted**: not an anonymous tool. The director needs to know who is responsible if something goes wrong. A LinkedIn profile, a clear email address, and a phone number are minimum credibility.

5. **Basic terms and conditions**: a simple Service Agreement or MOU that states the pilot is free, what KeyStone will provide, what data will be collected, and an exit clause. The absence of any formal document is more alarming to institutions than a simple one-page document.

---

## 2. Pre-Approach Requirements

### What the product must be able to do before any university contact

This is the absolute minimum product state before approaching any university:

1. **Resume upload and analysis**: accepts PDF, extracts content, returns structured feedback with at least 5-8 dimensions (formatting, quantification, action verbs, contact section, work experience quality). Ideally SG-specific flags (NS description quality, NRIC removal advice).

2. **Job URL parsing**: paste a MyCareersFuture or JobStreet URL, system extracts the job requirements (at minimum: required skills, role type, industry). This is KeyStone's primary differentiation from VMock and must be demonstrable.

3. **Job-match assessment**: a clear output showing how the resume aligns to the specific job. The four-level assessment (Strong / Transferable / Addressable / Gap) is compelling visually. Even if it works on 70% of job types, it must work flawlessly on the types you will demo.

4. **At least 3-5 line-by-line suggestions**: specific to the job being applied to, not generic. The career director should read one suggestion and think "that's actually good advice." If the suggestions sound like ChatGPT on generic settings, you lose the demo.

5. **A basic dashboard or reporting view**: even a simple export or summary showing "here's what your cohort used the product for." This addresses the operational-intelligence upside that directors care about.

### What proof points should exist before approach?

You do not need a track record with other universities. You need evidence that the product works on real SG examples. Specifically:

1. **20-30 tested SG resumes**: gather these from friends, LinkedIn connections, alumni networks — anyone willing. Run them through the product and document 5-10 cases where the output was genuinely useful. Screenshot the best examples. These become your demo materials.

2. **10-20 tested SG job postings**: pull real postings from MyCareersFuture and JobStreet across the target industries (finance, tech, consulting, engineering). Verify the URL parsing works on at least 80% of them. Have 3-4 showcased examples where the resume-job match output is clearly useful.

3. **One or two informal user testimonials**: find 3-5 SG job seekers (not the founding team) willing to try the product and give a candid quote. A statement like "the suggestion to reframe my SAFOS scholarship as stakeholder management experience was something my advisor never mentioned" is worth more than any feature list.

4. **A brief internal accuracy test**: compare KeyStone's suggestions against what a human career advisor would say for the same resume and job. Document cases where the AI's suggestions align with professional advice. This becomes your "it works" claim in the meeting.

### Is a prototype demo with 20 real SG resumes + 20 real SG job postings sufficient?

Yes — if the demo works reliably on those 20 cases and you only demo those cases.

The risk is demoing a live product that breaks on an unexpected input. Never run a live demo with a job posting you have not pre-tested. Always have 3-4 pre-loaded, pre-tested demo sessions ready to show.

For the career director's perspective: seeing 20 well-chosen examples where the product gives genuinely useful, SG-specific advice IS credible enough to agree to a free pilot. They are not expecting a finished enterprise product.

### What collateral is required before the first meeting?

Non-negotiable before any meeting:

1. **One-page product overview** (A4, printable): what KeyStone does, who uses it, how the pilot works, what data is collected, what the career centre needs to do (very little). Not a VC pitch deck — a one-page operational brief.

2. **PDPA compliance statement**: one page. Where data is stored (AWS ap-southeast-1), what data is collected (resumes and job postings submitted by students; no NRIC collected, NRIC flagged for removal), who can access it (no third parties; aggregates only shared with institution), student rights under PDPA (access, correction, deletion).

3. **Pilot terms letter or MOU template**: two pages maximum. Free service. Duration (one semester). What KeyStone provides. What the university provides (access to willing students; one feedback session). Exit clause (either party can end with 2 weeks notice, no obligations).

4. **Contact page or LinkedIn**: the director will Google the founder before or after the meeting. Make sure what they find is professional and consistent with the pitch.

Nice-to-have before the meeting, not blocking:
- A brief FAQ document anticipating the 10 most common questions
- A sample student consent notice (shows you have thought through the PDPA implications)
- A draft outcome metrics report template (shows what data you will share with the institution at semester end)

---

## 3. The Persuasion Narrative

### The ONE argument that makes a director want to try KeyStone

The argument is not about AI quality, Singapore specificity, or competitive positioning. It is this:

**"Your students need resume coaching at 11pm before a deadline. Your advisors are not available at 11pm. KeyStone is."**

This is the access-to-advice gap argument. It is:
- Immediately relatable to any career director (they know this problem)
- Undeniably true (no career centre has 24/7 advising)
- Addressed by KeyStone's product on Day 1 (no outcome data needed)
- Framed in the career centre's language (service-to-students, not technology)
- Not a claim about being better than VMock (avoids the comparison problem)

The secondary argument (for follow-up or if the director asks for more):

**"Your advisors spend 30-40% of their time on basic resume formatting and structure reviews. KeyStone handles the first pass; your advisors handle the hard conversations. Same team, twice the throughput."**

### Draft cold outreach email to a NUS/NTU career centre director

Subject: AI resume tool pilot — built specifically for Singapore students

---

Dear [Name],

I'm [Founder], the founder of KeyStone — an AI resume tool built for Singapore job seekers. I'm writing to ask whether you'd consider a free pilot with a group of students next semester.

The pitch is simple: your students need resume coaching at 11pm before application deadlines. Your team cannot be available then. KeyStone is.

What makes it different from generic tools: it parses real job postings directly from MyCareersFuture or JobStreet, and gives students feedback tailored to that specific role — not generic advice they could get from ChatGPT. A student applying to a DBS Management Associate role gets different suggestions from a student applying to an IMDA scholarship. We also give your career centre an aggregate dashboard so you can see where students are applying and what their most common gaps are.

For the pilot: we offer 200 seats, free for one semester, zero administrative overhead for your team. Students self-register via a link you send; we handle all support queries directly. At semester end, we give you a full report of usage and aggregate outcomes.

I'd like 20 minutes to show you a live demo with a real NUS student resume and a real SG job posting. If it's not obviously useful to your students in those 20 minutes, there's no further conversation needed.

Would a call next week work?

[Name] | [Email] | [LinkedIn] | keystone.sg

---

Notes on why this email works (for revision reference):
- Subject line states the offer without being promotional
- Paragraph 1: specific ask, not vague "partnership interest"
- Paragraph 2: the ONE argument, in plain language
- Paragraph 3: the differentiation without a competitor comparison claim
- Paragraph 4: zero-friction pilot terms, defined
- Paragraph 5: the demo ask — small and reversible (20 minutes, not a commitment)
- No VC deck attached; no buzzwords (AI-powered, cutting-edge, etc.)
- No ask for a decision — ask only for a meeting

### Draft 10-minute pitch deck outline

This is for the in-person meeting, not a cold pitch. The career director has already agreed to 20 minutes.

**Slide 1 (1 min): The problem in one question**
"How many students on your campus submitted a job application last night at 11pm without any feedback on their resume?"
[No answer needed — it's rhetorical. Move on.]

**Slide 2 (1 min): What KeyStone does — one sentence**
"KeyStone gives every student instant, job-specific resume coaching — at any hour, for any role they're applying to."
[One sentence. Do not expand here. The demo is the expansion.]

**Slide 3 (5 min): Live demo**
[This is the heart of the pitch. Walk through a real SG resume against a real SG job posting. Show the job-specific suggestions. Show one suggestion that is obviously correct and non-obvious — something the advisor might have said themselves but had never written down as a rule. Let the director react.]

**Slide 4 (1 min): What the pilot looks like**
- 200 student seats, free for one semester
- One email from your team to self-register students
- KeyStone handles all student support
- Mid-pilot check-in call; end-of-semester report with aggregate data
- No commitment beyond the pilot

**Slide 5 (1 min): What we ask in return**
- Access to willing students (via one email from you)
- Permission to use aggregate (not individual) outcome data to improve our model
- Your candid feedback at semester end — what worked, what didn't
- A quote for our website if you think it merited it (no obligation)

**Slide 6 (1 min): Data and privacy**
- Student data stays in Singapore (AWS ap-southeast-1)
- We do not collect NRICs; we flag them for removal
- Individual student data is not shared with anyone
- PDPA-compliant; I'll share our data notice for your review before any pilot starts

[No venture funding slide. No market size slide. No competitor comparison. The director does not care. They care about three things: does it work, does it cost them effort, does it protect their students. Every slide answers one of those.]

---

## 4. Who to Approach First and Why

### The ideal first partner profile

The best first university partner has these characteristics:

1. **Career director who is new to role (0-3 years)**: new directors have an incentive to bring in new initiatives; they are building their tenure story and "I piloted an AI resume tool" is a good chapter.

2. **No existing AI resume tool contract**: if VMock already has a multi-year contract, the pilot must compete for contract space. Institutions with no existing AI tool have no switching cost.

3. **Graduate employment rate pressure**: institutions where employment outcomes are under visible scrutiny — either below the industry average, or where the director has recently been asked by university leadership to improve the numbers — have more urgency for new tools.

4. **Lower procurement bureaucracy**: smaller institutions, institutions with less formalized procurement, or directors who have operational budget discretion under SGD 30K can approve a paid contract without a tender process.

5. **Innovation-friendly culture**: universities that have public statements about "digital transformation," "student-centered innovation," or similar signals are more willing to take a calculated risk on a new vendor.

6. **Accessible leadership**: if the founder can get to the right director through two degrees of separation (mutual connection), the cold outreach becomes a warm introduction.

### SG University Rankings — First Partner Recommendation

Ranked from BEST to WORST first-partner target, with reasoning:

**1. SIT (Singapore Institute of Technology) — BEST FIRST TARGET**

SIT focuses on applied degree programmes in partnership with overseas universities (Glasgow, Coventry, DigiPen, etc.). Their career centre serves a student population that is largely returning polytechnic graduates — practical, job-focused, not overly prestigious. SIT has:
- Smaller institutional bureaucracy than NUS/NTU
- A public mandate around industry-readiness and employment outcomes
- Less likely to have existing AI resume tool contracts (VMock targets elite business schools first)
- Career centre team small enough that a single energetic director can run a pilot without multi-stakeholder sign-off
- Published employment outcome reports that create public accountability pressure

**2. SUSS (Singapore University of Social Sciences) — STRONG SECOND**

SUSS serves a high proportion of adult learners, working professionals, and part-time students. Their career centre's primary challenge is helping mid-career students navigate job changes and transitions — which is exactly where KeyStone's outcome-tracking and job-specific tailoring is most valuable. SUSS also:
- Has a smaller, less bureaucratic procurement process than NUS/NTU
- Has a student body highly motivated to apply KeyStone (career switchers, not just fresh grads)
- Has fewer existing digital career tool contracts to displace
- Has a public focus on lifelong learning and career upskilling that aligns with KeyStone's narrative

**3. SMU (Singapore Management University) — VIABLE BUT HARDER**

SMU has a career-oriented student body (BBA, accountancy, law, economics, information systems) with very high job placement rates. The career centre is well-resourced and sophisticated. Harder reasons:
- More likely to already have VMock or similar tools
- Procurement is more formalized (single-source justification is harder)
- The career centre team is experienced and will probe harder on product claims
- BUT: SMU students are among the most career-focused and would be the best data source

If KeyStone has a connection to anyone at SMU (alumni, faculty, career advisory board), SMU jumps to first target.

**4. SUTD (Singapore University of Technology and Design) — NICHE WIN**

SUTD is small (~2,000 students), focused on engineering and design, with high employment rates. Less relevant for volume but:
- Small institution = very fast decision-making
- SUTD has a culture of early-adopter experimentation
- A SUTD partnership has outsized prestige signal relative to the institution's size

Best approached as a second or third institution once the pitch is refined.

**5. Polytechnics (NYP, SP, TP, RP, NP) — HIGH VOLUME, LOW PRESTIGE**

The five polytechnics collectively serve ~80,000 students. Career services at polys are:
- Less resourced than university career centres
- More transactional about student outcomes (they need employability numbers, not sophisticated career advice)
- Much faster in procurement decisions (directors have more operational autonomy, contracts under SGD 20K can be director-approved)
- Less likely to have existing AI tool contracts

Polys are the BEST fallback if university approach stalls (see Section 6). They are also potentially the highest-volume first pilot if the goal is data collection.

**6. NTU (Nanyang Technological University) — LATER**

NTU has a large, well-resourced career centre with existing tech tools. Procurement is significant and slow. NTU should be approached once one or two smaller institutions have completed pilots and can provide case studies.

**7. NUS (National University of Singapore) — LAST**

NUS is the most prestigious target but the hardest procurement environment. NUS career services (CELC — Centre for English Language Communication; OCA — Office of Career Action) has existing relationships with major employers and established programmes. VMock appears to have some NUS presence already. NUS requires the most formal procurement process (tender board for contracts above SGD 70K). Approach NUS second-year with case studies from SIT/SUSS in hand.

---

## 5. The "Free Service + Data" Exchange — Legal and Ethical Framing

### Is exchanging free service for student data legal under PDPA?

Yes, under the right structure. The answer depends on HOW the data relationship is constructed.

**The correct structure**:

1. **KeyStone is the data controller for student data**, not the university. Students consent directly to KeyStone's Data Protection Notice (DPN) when they create their account on the KeyStone platform. The university is simply a distribution channel — they send a link to students. They do not transfer data to KeyStone.

2. **The university does not provide student data to KeyStone**: the university provides access to students (via email / announcement). Students then choose to sign up on KeyStone's platform and consent directly. This is legally straightforward under PDPA — the student is giving their own data voluntarily to a third party.

3. **What KeyStone collects from students** under its own DPN:
   - Resume content (uploaded by student)
   - Job postings they run against their resume (URL + extracted content)
   - Self-reported application outcomes (if student chooses to log them)
   - Usage data (which features they use, how often)

4. **What KeyStone provides to the university**:
   - Aggregate anonymised cohort data: "X% of students from your institution used the product, here are the aggregate usage patterns and the most common gap types identified"
   - NO individual student records are shared with the university unless the student specifically requests this (e.g., a downloadable personal report they can share with their advisor)

5. **The data improvement clause** in KeyStone's student DPN:
   - "KeyStone may use anonymised, aggregated data from your usage to improve its services." This is standard language used by essentially every edtech platform and is consistent with PDPA's legitimate business purpose exception.
   - KeyStone does NOT need to say "we share your data with the university in exchange for a free service" because that is not what is happening.

### The institution's consent framework concerns

The questions every SG university procurement officer will ask about data:

**Q: Where is the data stored?**
A: AWS ap-southeast-1 (Singapore region). Data does not leave Singapore. This is the strongest possible answer and directly addresses the post-2022 PDPA amendments' emphasis on cross-border transfer restrictions.

**Q: Who has access to individual student data?**
A: No one externally. KeyStone employees with direct access are limited to engineering for support and debugging. Aggregate data (not individual records) is shared with the institution's career centre.

**Q: What happens if KeyStone closes or is acquired?**
A: Documented deletion protocol — all student personal data is deleted within 30 days of service termination. In event of acquisition, student data handling transitions under the same PDPA obligations. This clause in the MOU gives the institution a contractual right to demand deletion.

**Q: Can students request deletion of their data?**
A: Yes, at any time, via the PDPA access and erasure right. The product interface will include a "delete my account" button that purges all personal data. Residual anonymised aggregate data may be retained.

**Q: Does using KeyStone create any vendor lock-in for the university?**
A: No — it is a free pilot with no contract. The university can stop at any time. There is no integration with university systems, so there is no switching cost.

### Precedent for this model in SG academic/government context

The "free service + right to use aggregate anonymised data for product improvement" model is used by:

- **Coursera for Campus**: free or subsidised institutional access; Coursera uses aggregated learning data to improve its platform
- **LinkedIn Learning for institutions**: institutional contracts include data about employee/student learning patterns used to improve recommendations
- **Government-linked education platforms** (Student Learning Space operated by MOE): MoE's Student Learning Space explicitly uses anonymised student interaction data for educational research

The precedent is clear: institutional edtech in Singapore routinely uses this model, and universities have established procurement language for it. KeyStone is not inventing a new legal structure — it is adopting the structure already used by platforms the institution already has contracts with.

---

## 6. What If No University Says Yes in Month 1?

### Fallback sequence

If three separate university contacts have been approached and none has agreed to a pilot within 30 days of the demo meeting, escalate through this fallback sequence:

**Fallback 1: Polytechnics**

NYP, SP, TP, RP, NP collectively serve ~80,000 diploma students annually. Career services at polytechnics are:
- More accessible (career coordinators are easier to reach than university directors)
- Less process-bound (operational budget decisions can be made faster)
- More focused on employability metrics (they are evaluated on whether students get jobs)
- Less likely to have existing AI resume tool contracts

The trade-off: a polytechnic pilot has less prestige signalling than NUS/NTU/SMU. But the data is equally valuable and the growth curve from poly → university is clear ("we ran a pilot with NYP, here's the data, we'd like to do the same at SMU").

Target polytechnics: NYP (strong in health sciences, engineering, design), SP (strong in business and IT), TP (strong in applied science and engineering).

**Fallback 2: Private education institutions (PEIs)**

MDIS, Kaplan Singapore, PSB Academy, JCU Singapore, Curtin Singapore. These serve students who tend to have HIGHER anxiety about employability (private degrees have more scrutiny from employers). Benefits:
- Significantly less procurement overhead (private institutions, no government tender rules)
- Career coordinators are more commercially oriented and can make faster decisions
- Students are highly motivated users (they feel more pressure to differentiate themselves)
- Smaller institutions = faster decisions, more flexibility

A Kaplan or MDIS pilot is not as prestigious as NUS but it is a real case study with real outcome data.

**Fallback 3: Recruitment agencies**

One or two smaller SG recruitment agencies (not the large multinationals — Hays, Michael Page, Robert Walters are too process-heavy) could be approached for a white-label or small pilot. Benefits:
- Recruitment agencies have direct financial incentive in candidate quality
- They measure candidate placement rates — outcome data is inherently tracked
- A small agency (5-20 recruiters) can make a decision in days, not months
- The case study is different ("used by [agency] to prepare candidates") but still a real reference

This does not produce university credibility, but it produces logos, case study language, and outcome data that can be used in the university pitch ("we have been used to prepare candidates placed at DBS, Singtel, and EY through [agency name]").

**Fallback 4: Direct-to-student B2C with deferred B2B**

If all institutional approaches stall in Month 1-2, consider a brief B2C-only launch to accumulate 100-200 real users and real usage data before returning to the university conversation. The pitch changes from "here is what we can do" to "here is what 200 students have done with this product, here are their results." This compresses the credibility gap.

The risk: B2C launch without institutional distribution is slow. But 100 real users with logged outcomes is a stronger university pitch than any demo.

### At what point does B2B-first need to be reconsidered?

If by Month 3 none of the following has occurred:
- One university or polytechnic has agreed to a pilot (MOU signed)
- One private institution has agreed to a pilot
- One recruitment agency is using the product with candidates

Then run a structured root-cause analysis before spending more time on B2B outreach. The possible root causes are:

1. **Product not ready**: the demo is not compelling enough to override procurement inertia. Fix: more demo refinement, more tested SG examples, better UX polish.

2. **Network access problem**: the founding team does not have the right introductions. Fix: targeted LinkedIn outreach to anyone in the team's extended network connected to SG university career services; attend SG career-related events; approach NUS/NTU alumni associations (large alumni networks often have informal connections to career centre staff).

3. **Narrative not landing**: the pitch is not connecting with the career director's actual KPIs. Fix: spend 5 office-hours sessions shadowing a career adviser (even informally) to understand their actual workflow before re-pitching.

4. **Product-category resistance**: universities are in a freeze on new AI tools for policy or AI ethics review reasons. Fix: adjust approach to frame KeyStone as a "student productivity tool" (not "AI") or wait for institutional AI policies to mature (likely by mid-2026 across SG universities).

If Month 3 passes with none of the above root causes addressable, the B2B-first timing is wrong — not the strategy. In that case: build B2C user base to 200-500 real users, collect outcome data, and return to the university conversation in Month 6-9 with real evidence.

---

## 7. Model Training Before University Approach

### Must KeyStone do pre-training before approaching universities?

The short answer: no, but the product must be "good enough to demo well on 20-30 pre-tested cases."

The nuance: "pre-training" in the sense of fine-tuning an AI model on SG-specific data is NOT a prerequisite for the pilot conversation. The demo only needs to show that the product gives useful, relevant advice on real SG resumes and job postings. If the LLM (Claude Haiku + Sonnet) produces high-quality suggestions with well-engineered prompts and good SG context injected at inference time, that is sufficient for the demo and for the pilot.

What IS required before approaching universities:

1. **Prompt engineering with SG context**: the LLM calls need to understand the SG hiring context — what MCF/JobStreet jobs look like, what NS experience represents, what the difference is between GLC and MNC hiring preferences. This is a prompt engineering and context-injection task, not a training task. It can be done in 2-4 weeks with a small set of SG job examples and resume examples.

2. **Edge-case reliability**: the product should handle the full range of SG student resume formats without breaking. This means testing on 30-50 diverse resumes (different industries, different formats, fresh grad vs experienced, with and without NS experience) and fixing the edge cases that produce bad output.

3. **URL parsing reliability on MCF and JobStreet**: these two sites are the primary SG job boards. URL parsing must work reliably on both before demo. Test 50+ URLs across job categories, fix the parsing failures.

### What minimum AI capability is required?

The AI must clear these bars before any university demo:

1. **Suggestions must be specific to the job, not generic**: "Consider adding metrics to your work experience bullet" is generic. "For this Singapore Government Scholarship position at MOE, your bullet about your project team should mention the number of stakeholders you coordinated with, as MOE values documented leadership scale" is specific. The demo must show the specific version.

2. **Suggestions must not be harmful**: any suggestion that would embarrass the product in a live demo (suggesting the student include their NRIC, suggesting they lie about experience, producing grammatically broken output) must be caught and prevented in pre-launch testing.

3. **NS experience framing must work**: male Singaporean candidates with NS experience are a large portion of the target population. The product must handle NS experience meaningfully — extracting leadership, operational, and logistics skills from military service descriptions and framing them appropriately for civilian roles. This should be explicitly tested before university demos.

### Is it feasible to build a demo using publicly available SG job postings and synthetic resumes?

Yes, and this is exactly the right approach for the pre-university phase.

Practically:
- Pull 20-30 real job postings from MyCareersFuture and JobStreet across 5-6 industry categories (finance, tech, consulting, engineering, public sector/GLC)
- Create 20-30 synthetic SG-style resumes — these can be constructed from common SG graduate experience patterns (NUS Computer Science with internship at a local tech startup; NTU Accountancy with internship at one of the Big 4; SUTD Engineering with NS as SAF officer; SMU Business with NS as NSF PC)
- Run each resume against the relevant job postings and manually review every output for quality, accuracy, and relevance
- Select the 5-8 best examples as demo cases
- Document the edge cases that fail and either fix them or exclude those resume/job types from demos

This is 2-4 weeks of engineering and manual review work. It does not require real student data. By the time a university pilot starts, you will have real student data within the first week.

### How many real examples do you need before the product is "good enough to show"?

For the university demo: zero real user examples, if synthetic examples are high quality.

For the university pilot commitment (MOU): zero real user examples required. The MOU is based on the demo.

For the renewal conversation (converting to paid contract): data from the pilot itself. The pilot IS the evidence.

For a second university: case study from the first pilot.

The progression is: synthetic demo → pilot data → case study. You do not need real users before the first pilot, because the first pilot IS where you get real users.

---

## Summary: The Critical Path

The single most important execution sequence for Month 1-2:

1. **Identify one warm connection to any SG career centre** (university, poly, or private institution). If none exists on the founding team, find one through alumni networks, LinkedIn, or mutual connections within 2 weeks. Do not cold-email without at least one degree of separation.

2. **Build demo-quality product on 20-30 pre-tested SG examples**. Not full production quality. Demo quality: works reliably on the specific cases you will show, with clean UX and SG-specific output.

3. **Prepare the PDPA one-pager and the MOU template** before the first meeting. These are not complex documents. One page each. Their presence signals professionalism and removes the "I need to check with our DPO" delay.

4. **Book the demo meeting**. The goal of the first meeting is not a signed MOU. It is a second meeting. The goal of the second meeting is the MOU.

5. **Set student intake live before semester starts**. Once the MOU is signed, the founder personally emails the career director a ready-to-forward student link. Make it as easy as forwarding an email.

If these five steps happen in Month 1-2, the B2B-first strategy works. If Step 1 is blocked (no warm connection anywhere in the network), that is the most important problem to solve before building anything else — relationship access is the constraint, not product quality.

---

*Analysis date: 2026-04-29. Recommendations based on edtech B2B comparable analysis (see file 12) and SG market context from training data up to August 2025. University-specific details (existing tool contracts, director names, procurement thresholds) should be verified with current market research before acting.*

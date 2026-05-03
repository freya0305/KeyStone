# Analysis 27 — Value Proposition Design Coherence Audit

> Phase 01 Analysis — 2026-04-29
> Question: Screen-by-screen, does the design deliver the core value proposition? What does the B2B buyer need to see? How does the design make SG-native intelligence tangible vs abstract?
> Method: Value-Auditor walkthrough applied to the spec'd screens (no live UI to crawl yet — audit is conducted against the activation flow in Analysis 21 and the MVP feature spec).

---

## Core Value Proposition (Restatement)

**B2C**: "Paste any Singapore job posting. Get a resume rewritten for that exact role in under a minute — by an AI that understands how SG hiring managers think."

**B2B**: "Every student in your career centre gets a personal resume coach for every application — so your team can focus on the 5% of students who need real intervention, not the 95% who need editing."

The audit asks the same five questions at every surface:

1. What is this FOR?
2. What does it LEAD TO?
3. Why do I NEED this?
4. How do I USE this?
5. Where's the PROOF?

A surface that fails any of these is a value drain — it costs context (cognitive + visual) without buying the user closer to the value moment.

---

## Part 1 — Screen-by-Screen Audit

### Screen 1: Landing Page (`/`)

**Purpose per spec**: Get the visitor to start the workflow without registering.

**What the design must show**:
- Headline: "The resume tailoring tool built for the Singapore job market."
- Subhead: "Paste a job. Get a resume tuned for that role, that company, this market. In under a minute."
- Primary CTA: "Try it on one job — free." opening directly to the workflow (NO "Sign up to continue").
- ONE proof element above the fold (a real example, not a mock testimonial).
- Trust signals in the footer: PDPA-compliant badge, "Built in Singapore" line, real founder photo + LinkedIn link.

**Value Assessment**:
- Purpose clarity: **CLEAR** *if* the example proof is above the fold. **VAGUE** if the page is a generic-SaaS hero+features+CTA stack.
- Data credibility: **AT RISK**. Most SaaS landing pages show fake testimonials with stock-photo headshots. SG buyers (Reddit-acquired users especially) detect these instantly. Use a real worked example: a (consented, anonymized) before/after of one bullet rewrite, with the JD requirement and company type cited.
- Value connection: **CONNECTED** if the CTA goes directly to the upload flow. **DEAD END** if it goes to a signup wall.
- Action clarity: **OBVIOUS** if there is exactly one CTA above the fold. SaaS landing pages with 3 CTAs ("Sign up free", "Watch demo", "See pricing") split intent and reduce conversion.

**Specific design recommendations**:
- The hero should embed a **live demo widget**: a JD URL input field on the right, a "what this would look like" preview on the left that updates as the user pastes. This is the single highest-impact landing-page decision — turns the abstract claim into a concrete demo before the user even clicks.
- NO carousel of features. Carousels are dead conversion.
- The "Built for Singapore" claim must be visually substantiated: a single line under the hero like "Recognises GLC vs MNC vs startup. Knows how SG hiring managers read resumes." with real example labels.

**Client Questions a CTO/buyer would ask**:
- "Is this just GPT-4 with an SG-themed prompt?" → answer this on the page with one specific SG-only feature stated concretely (NRIC removal, NS framing, photo guidance by company type).
- "Why should I trust this with my resume?" → answer with the privacy-first language ("Your resume never trains the AI without your explicit opt-in") visible on the landing page, not buried in privacy policy.

**Verdict**: VALUE ADD if the live demo + one-CTA + concrete-SG-claim discipline holds. NEUTRAL if it becomes a typical SaaS hero/features/CTA layout. VALUE DRAIN if the CTA gates behind signup.

---

### Screen 2: First-Use Workflow — JD Input

**Purpose**: Capture the JD in <30 seconds with zero friction.

**Per Analysis 21 the order is: JD first, then resume.** The design implication: the first input the user touches must be the JD URL field, prominent, generously sized, with paste-detection.

**Value Assessment**:
- Purpose clarity: **CLEAR** if a single input dominates the screen. **VAGUE** if the design tries to "guide" the user with multi-step wizards.
- Action clarity: **OBVIOUS** if paste-into-the-box just works. **HIDDEN** if the user has to click "Analyse" after pasting (they will paste and stare).

**Design recommendations**:
- Auto-trigger parsing on paste — show a loading state for the URL fetch within 500ms of paste detection. Do NOT require an "Analyse" button click after URL paste.
- Show the parsed company name + job title within 2 seconds of paste, in a confirmation chip beneath the input: "✓ Parsed: Senior Product Manager at DBS Bank · GLC". This is the **first proof of intelligence** the user sees — confirms the URL was understood AND demonstrates company-type detection in one stroke. This single moment is where the user first thinks "oh this actually understands SG."
- If parse fails, the input transforms into a textarea labelled "Paste the job posting text here" with NO error state shown (per Analysis 21 / MVP spec: silent fallback).

**SG-native intelligence proof point #1**: the company-type chip ("GLC" / "MNC" / "Startup") is the first place where the product distinguishes itself from a generic "AI resume tool." Make it visually prominent — match-level color treatment isn't right here (those are for skills); use the brand-primary tint with a subtle border.

**Verdict**: VALUE ADD if paste auto-triggers AND company type displays within 2s of parse. NEUTRAL if the user has to click a button. VALUE DRAIN if there's a visible error on parse failure.

---

### Screen 3: First-Use Workflow — Resume Upload

**Purpose**: Get the resume uploaded within 30 seconds, no friction.

**Value Assessment**:
- Purpose clarity: **CLEAR** with a single drop zone.
- Action clarity: **OBVIOUS** with drag-or-click.

**Design recommendations**:
- Drop zone full-width, dashed border, generous padding (h-48 minimum). Accepts drag, click-to-browse, OR paste-text alternative.
- On successful parse, immediately show the SG flags as positive feedback: "✓ NRIC detected — we'll recommend removing this" / "✓ NS section found — we'll help reframe this for civilian competencies" / "✓ Photo detected — we'll advise based on company type." THIS IS THE SECOND PROOF POINT — instant, specific, SG-native. The user sees the AI **acting** on their resume before any suggestion is generated.
- Caching: if the resume hash matches a cached analysis, show "Welcome back — using your saved resume analysis" — small touch but signals "this product remembers you" and respects time.

**Anti-pattern to avoid**: showing the parsed resume content as a wall of plain text. Most SaaS resume tools do this and it looks broken — like the OCR wasn't quite right. Better: show a structured summary ("8 work experience entries, 3 education, 12 skills detected") with an "edit if anything's wrong" affordance.

**Verdict**: VALUE ADD if the SG flags surface immediately after parse. The flags are the single most differentiated moment in the activation flow — they prove SG-nativeness before the user has invested any effort. NEUTRAL if the upload just shows the file name. VALUE DRAIN if it shows a wall of unparsed text.

---

### Screen 4: Analysis Wait (Loading State)

**Purpose**: Hold the user's attention for up to 60 seconds without losing them.

This is the highest-risk screen in the activation flow. Per Analysis 21, ">30s wait" is a top-3 user-loss moment.

**Value Assessment**:
- Purpose clarity: **CLEAR** if progress is shown.
- Data credibility: **AT RISK** if a fake-progress bar is used. AT RISK if "AI is thinking…" with no specifics.

**Design recommendations** (these MUST ship):
- Streaming, not batched: as soon as resume analysis is done (typically 5-8s), show it. Don't wait for suggestions.
- Progress is **stage-based**, not percentage: "✓ Parsed JD requirements" → "✓ Identified company type: GLC" → "⟳ Comparing your experience to requirements" → "⟳ Generating suggestions."
- A rotating SG-market insight in a sidebar during the wait (curate ~30 of these, plain text, no flourish): "GLC hiring managers typically look at the first 8 lines of your work experience before deciding to read further." / "Singapore MNC roles weight cross-functional collaboration evidence more than direct authority." / "Most fresh grad applicants in SG over-list internships and under-quantify each one."
- The insight sidebar is the **third major SG-native proof point**: the user is seeing the product's domain knowledge while waiting for their result.

**What NOT to do**:
- A spinner with "Analysing…" — generic, betrays no intelligence.
- A fake percentage bar — destroys trust the moment it stalls.
- A "fun fact" that's not SG-specific — wastes the proof opportunity.
- An ad for Pro during the wait — looks desperate; user hasn't seen value yet.

**Verdict**: VALUE ADD if streaming + stage-based progress + SG insight sidebar are all present. NEUTRAL if streaming is in but the sidebar is generic. VALUE DRAIN if it's a spinner with no information.

---

### Screen 5: First Result — The Aha Moment

**Purpose**: Deliver at least one specific, SG-contextualised suggestion within view of the first scroll. This is THE moment the activation either succeeds or fails.

**Per Analysis 21 the layout is dual-pane**: left side shows the resume bullet (original), right side shows the suggestion card with rewrite + rationale + actions.

**Value Assessment**:
- Purpose clarity: **CLEAR** if the user sees the original/rewrite side-by-side immediately.
- Data credibility: **REAL** only if the rationale cites *the specific JD requirement and company type*. **EMPTY** if it cites generic best practice ("Use action verbs" / "Quantify your achievements").
- Value connection: **CONNECTED** when the suggestion card has Accept/Skip/Edit and the action carries forward into the resume.
- Action clarity: **OBVIOUS** with the three-action pattern.

**The single most important design decision in the entire product** is what the rationale text says. If the rationale reads "Quantifying achievements is a resume best practice," the value prop dies — the user could get that from any AI tool. If the rationale reads "This GLC weights quantified team leadership; your phrasing 'responsible for' reads as ambiguous ownership in SG public-sector hiring," the value prop is delivered.

**Design enforcements**:
- The rationale field has a **minimum 2 information facets** rule, enforced at the prompt-engineering level: facet 1 = JD requirement reference, facet 2 = company-type-specific reasoning. If the LLM can't produce both facets for a suggestion, suppress that suggestion rather than ship a generic one. **Better to show 8 specific suggestions than 14 mixed.**
- Match-level chip displayed prominently on every suggestion card (from the four-level system). The chip color is the user's at-a-glance signal of how much rewriting is happening.
- The first card auto-expands on render. Subsequent cards are collapsed (just title + match-level chip) for the user to expand at their pace.

**SG-native intelligence proof points 4 through N**: every rationale that cites GLC/MNC/startup/government convention is a small proof point. Aim for 3+ such citations in the first 5 suggestions. This is what earns the SGD 19/mo conversion.

**Free-tier handling**: per the freemium architecture, the FIRST JD shows unlimited suggestions. The user sees the full product on their first run. Pro-gating kicks in on the second JD. The design implication: **do not visually flag free-vs-paid on the first JD**. Show every suggestion. The user must finish their first session believing "this works." Pro pitching happens at the start of the second JD, not the middle of the first.

**Verdict**: VALUE ADD if every visible rationale cites JD requirement + company type. NEUTRAL if half the rationales are generic. VALUE DRAIN if ANY rationale is something a free ChatGPT could produce.

---

### Screen 6: Resume Export ("Download tailored version")

**Purpose**: Let the user leave with a real, polished output. This is the value moment they came for.

**Per Analysis 23 (outcome logging redesign)**: the download moment is the highest-conversion application-tracking trigger — "Are you submitting this to [Company]?" → one-click application creation.

**Value Assessment**:
- Purpose clarity: **CLEAR**.
- Action clarity: **OBVIOUS** with one primary download action.
- Value connection: **CONNECTED** because download is also the application-tracking trigger.

**Design recommendations**:
- Single primary CTA "Download tailored resume" with a dropdown for PDF/DOCX format choice.
- Inline preview of the changed bullets (a "what changed" summary) before download — gives the user confidence the suggestions actually applied.
- **Application-tracking prompt**: appears immediately after download as a non-modal toast/banner: "Submitting to DBS? Track this application — takes 5 seconds." with a [Yes, track it] [Not yet] action. Critically: the [Not yet] dismissal must not be punished or repeated — log the dismissal and move on.

**Anti-pattern**: do NOT modal-block the user post-download asking them to track. They already got their value (the resume); blocking that moment with a modal demanding "track this application now" is the data-extractive UX that kills trust.

**The "did this make the resume better?"** confidence question — many resume tools ship the wrong file (lost formatting, broken layout). The export must preserve the original structure with surgical replacements, NOT regenerate from scratch. Show a 1-page-thumbnail preview before the download confirms.

**Verdict**: VALUE ADD if the application-tracking prompt is non-blocking AND the export preserves formatting. NEUTRAL if formatting is preserved but tracking is modal-blocked. VALUE DRAIN if the export regenerates the resume from scratch and loses the user's formatting.

---

### Screen 7: Signup Prompt (Post-Aha)

**Purpose**: Convert anonymous Aha-moment users into registered accounts.

**Per Analysis 21**: triggered AFTER value is seen (accept first suggestion, view third suggestion, attempt download).

**Value Assessment**:
- Purpose clarity: **CLEAR** if framed as "save your work" not "sign up to continue."
- Action clarity: **OBVIOUS** with Google OAuth as primary, email + SG mobile as alternative.

**Design recommendations**:
- Modal title: "Save your work" — present-tense, action-led. Not "Create an account" (transactional) and not "Join KeyStone" (cult-y).
- Body: "We've saved your analysis for the next 24 hours — sign in to keep it forever."
- Two options: Google (one click) and Email + SG mobile (two-step, minor friction). Phone verification is anti-abuse per the spec.
- A small clarification line: "Free tier covers 3 jobs/month. No credit card needed." — sets expectations honestly.
- DO NOT: ask for first name, last name, role, target industry, etc. ALL secondary data collection happens AFTER the user is signed in. The signup form has 1-2 fields, max.

**Trust micro-element**: a single line "Your resume never trains the AI without your separate opt-in." with a "Why?" tooltip. This addresses the latent SG concern about AI + personal data, makes it explicit that consent is granular.

**Verdict**: VALUE ADD if the prompt is post-Aha AND Google OAuth is the primary path. NEUTRAL if it's post-Aha but signup form has >2 fields. VALUE DRAIN if it's a wall encountered before the user sees a suggestion.

---

### Screen 8: Application Tracking Dashboard

**Purpose**: Make outcome tracking feel like personal benefit, per Analysis 23.

**Per spec**: framed as "your personal job search dashboard" — user utility first, not data collection. Per-stage breakdown surfaces actionable insights.

**Value Assessment**:
- Purpose clarity: **CLEAR** if framed as personal insight.
- Data credibility: **AT RISK** until the user has 5+ applications logged (avoid 0%/100% on small-N — per spec).
- Value connection: **CONNECTED** if pass-rate insights link back to "what to do about it."

**Design recommendations**:
- The dashboard headline metric is **per-stage pass rate**, NOT total response rate. SG users care about "I'm getting interviews but not offers" or "I'm not even getting screening calls" — different problems, different fixes.
- Visual: a horizontal funnel with five stages — Applied → Responded → Screened → Interviewed → Offered. Each segment shows count + percentage transition. The funnel is the most important visual in the product after the suggestion card.
- Below the funnel: an insight card. "Your response rate (12%) is above the SG market median (~8%) — your resume's getting attention. Focus next on the response→screen step (where you're at 25% vs market 40%)." This is the **personal insight** that makes the dashboard feel like utility, not surveillance.
- Tracking-completeness gauge in the corner: "72% complete · top 30% of users." Per Analysis 23 — gamification framed as "more complete = better insights for you," NOT "help us collect data."
- Cold-start handling: if <5 applications logged, show "Log 3 more applications to unlock your response-rate analytics." with a clear count to the unlock. NEVER show fake/empty charts during cold-start — they look broken.

**Anti-pattern**: a typical "applications" CRM-style table view as the primary surface. SG users won't maintain a CRM-style log; they'll abandon. The funnel + insight is the value; the table is secondary access.

**Per Analysis 23 — the batch-update UI** is the supporting surface. Not the main dashboard. When the user lands on the dashboard, if there are ≥3 pending applications, show a banner at the top: "8 applications pending — 30 seconds to update them all" with a CTA opening the batch UI.

**Verdict**: VALUE ADD if the funnel + per-stage insight + cold-start handling are all in. NEUTRAL if the funnel is there but no insight cards. VALUE DRAIN if the dashboard surfaces 0% callback-rate to a user with 0 applications.

---

### Screen 9: Paywall / Pro Upgrade Moment

**Purpose**: Convert engaged free users to Pro at SGD 19/mo.

**Per Business Model**: emotionally loaded (this is a job they really want), low friction (one click), immediate (Pro features unlock <5s).

**Value Assessment**:
- Purpose clarity: **CLEAR** if the paywall arrives at the natural friction point.
- Action clarity: **OBVIOUS** with a single Stripe-checkout flow.

**Design recommendations**:
- Trigger: at the start of the second JD analysis (NOT mid-flow on the first JD), the user sees: "You've used your first analysis — looking strong! Free tier shows 3 suggestions per additional job; Pro is unlimited." with [See suggestions] (free, capped) and [Go Pro — SGD 19/mo] (CTA).
- The paywall is **opt-out friendly** — the user CAN see the first 3 suggestions free, even on the second JD. Hard-block paywalls trigger refund-rage churn from frustrated users.
- The "Pro features include" list is short and concrete: "Unlimited suggestions on every job. Application tracking dashboard. Single weekly digest email if you want." — three bullets, no kitchen sink.
- Annual plan offer is presented inline ("SGD 180/yr — 21% off — $15/mo") not as a separate upsell modal.
- **Re-trigger placement**: if the user analyses the second JD with the free 3-suggestion cap and reaches suggestion 3, a soft non-blocking banner says "11 more suggestions ready when you upgrade." NEVER an interrupting modal.

**Anti-patterns** (these will tank conversion):
- A countdown timer — looks scammy.
- Strikethrough fake "original price" — looks scammy.
- Hard paywall before any suggestion is shown on the second JD.
- Asking for credit card before showing the cap.

**Per Persona tonal variation**:
- Fresh grad: emphasis on "$5 less than Spotify, for the job that pays back 100×."
- Mid-career: emphasis on "Annual plan — for serious career changers; covers your full search."
- PMET: emphasis on respect for time — "Single payment annual covers your full search; cancel any time."

**Verdict**: VALUE ADD if the paywall is at the second-JD start with 3 free suggestions, and Pro features are listed concretely. NEUTRAL if it interrupts the first JD. VALUE DRAIN if it's a hard wall before any suggestion is visible on the second JD.

---

## Part 2 — Value Flow Audit (End-to-End)

### Flow 1: First-Time User → Aha Moment → Signup

**Steps Traced**:
1. Landing → Click "Try it on one job" → JD input
2. JD input → Paste URL → Auto-parse → Company-type chip displays (proof point 1)
3. Resume upload → SG flags surface (proof point 2)
4. Analysis wait → Streaming progress + SG insight sidebar (proof point 3)
5. First result → Suggestion cards with JD-cited rationales (proof points 4-N)
6. Accept first suggestion → "Save your work" prompt → Signup

**Flow Assessment**:
- Completeness: **COMPLETE** if all proof points fire.
- Narrative coherence: **STRONG** — every step adds a piece of "this product knows SG" before the user is asked to commit.
- Evidence of value: **DEMONSTRATED** at each proof point.

**Where it could break**:
- Step 2 if the URL parser fails and shows an error instead of silently falling back.
- Step 3 if no SG flags fire (resume has no NRIC, no NS, no photo) — design needs a fallback "we read your resume and it looks clean — let's see how it lines up against the JD" message that maintains the proof-point cadence even when there's nothing to flag.
- Step 5 if any rationale is generic.
- Step 6 if signup form has more than 2 fields.

### Flow 2: First-Time User → Download → Application Tracking → Return

**Steps Traced**:
1. Suggestions accepted → Download tailored resume
2. Post-download → "Submitting to DBS?" banner → Application created
3. User leaves site
4. User returns 2 weeks later (got an interview invite)
5. Pre-prep interstitial: "You have 4 other pending applications — update?" → Batch update UI
6. Interview prep entry (Phase 2)

**Flow Assessment**:
- Completeness: **THEORETICAL** until interview prep ships in Phase 2; for MVP, COMPLETE through step 5.
- Narrative coherence: **STRONG** if the dashboard's insight cards make the tracking feel like personal benefit.
- Evidence of value: **DEMONSTRATED** at the dashboard insight; **PROMISED** for interview prep.

**Where it could break**:
- Step 2 if the tracking prompt blocks the download flow.
- Step 5 if the batch-update UI requires more than 1 click per application.

### Flow 3: Second JD → Paywall → Pro Conversion

**Steps Traced**:
1. User starts second JD analysis
2. After analysis completes, a banner notes: "Free tier — 3 suggestions per job. See unlimited with Pro."
3. User views 3 free suggestions
4. After suggestion 3, soft banner: "11 more ready with Pro — SGD 19/mo"
5. Click → Stripe checkout (pre-filled from signup data)
6. Payment success → Pro features unlock immediately

**Flow Assessment**:
- Completeness: **COMPLETE**.
- Narrative coherence: **STRONG** — user is converting because they hit the cap on a real second job, not because of a manipulative pop-up.
- Evidence of value: **DEMONSTRATED** — they've seen the product work on TWO real jobs (one full, one capped) before the conversion ask.

**Where it could break**:
- Step 2 if the cap is communicated as a wall rather than as information.
- Step 4 if the banner is interrupting rather than persistent.

---

## Part 3 — B2B Buyer Design Requirements

The B2B buyer (university career-centre director, per Persona 4) sees a demo before signing a SGD 15-30K contract. Procurement reviewers will examine the product before funding.

### 3.1 Visual Quality Threshold

A SGD 15-30K contract puts the demo in front of:
- The director (sponsor, has seen 5-10 vendor demos this year)
- A procurement officer (compares against VMock, JobTeaser, locally-developed alternatives)
- A PDPA / data governance reviewer
- Possibly an AI ethics committee member (now real at SG universities post-2023)

**Threshold for visual quality**: same level as a Stripe Atlas, Linear, or Notion product. Below that, the procurement officer will silently downgrade KeyStone vs VMock (which has 10 years of polish). Specifically:
- No placeholder content visible in any demo screen.
- No console errors.
- Zero broken images, broken links, or "Coming soon" tags.
- All text in a final voice — no Lorem ipsum, no "TODO: rewrite this."
- A genuine pre-populated demo account with realistic Singapore student data (anonymised).

### 3.2 Career-Centre Dashboard (B2B Admin Surface)

This is the screen that wins or loses the contract. The director must see, on first load:

**Top section — cohort scorecard**:
- Total students enrolled / active this month / activated (completed first workflow)
- Aggregate response rate across the cohort
- Aggregate per-stage pass rates (the differentiated metric vs VMock)

**Middle section — actionable insights**:
- "12 students have 0 applications logged — recommend advisor outreach" (this is the "concentrate on the 5%" pitch made literal)
- "Most common Fundamental gaps in your cohort: SaaS product experience (47%), People management (38%), Data engineering tooling (29%)"  — gives the director something to brief the curriculum team about.
- "Top employer types your students are targeting: GLC (52%), MNC (28%), Startup (12%)"

**Bottom section — usage analytics**:
- Tracking completeness percentile
- NPS rolling average for the cohort
- Engagement over time

**What it MUST NOT show**:
- Individual student data (privacy + PDPA + the institutional pitch literally says "we don't surveil your students")
- Raw suggestion text from any student's resume
- Any data that cuts across institutions (the procurement reviewer will ask about data segregation; the answer must be "your cohort is yours alone")

**Visual design treatment**: this dashboard must look like an enterprise admin tool, not a B2C product with admin features bolted on. Specific cues:
- Denser typography (`text-sm` body), more table-heavy.
- Export-to-CSV affordances on every aggregate (procurement officers love CSV exports).
- A clear "Powered by KeyStone" footer + version number — looks professional, supports vendor management.
- A "Privacy mode" toggle that's defaulted ON: hides any view that could be construed as individual-student-identifying. The toggle existing IS the trust signal; it doesn't need to be off ever.

### 3.3 Trust Signals for Institutional Procurement

The product needs to surface these explicitly, NOT bury them in the privacy policy:

1. **PDPA compliance summary page** linked from footer + B2B admin sidebar. Plain-language summary of what data is collected, how long it's retained, who has access, how to delete. No legalese on this page — that's separate.
2. **Data Processing Agreement template** downloadable from the B2B sales page (PDF). Procurement officers ask for this in week 2 of evaluation.
3. **AI ethics statement** — separate page, separate from privacy policy. Topics: training data sources, model selection rationale, bias-mitigation, override mechanisms (the user can always edit any suggestion). Universities post-2023 expect this; not having it is a procurement red flag.
4. **Sub-processor list** (Stripe, OpenAI/Anthropic, the LLM provider, hosting region). One page, kept current.
5. **Status page** at `status.keystone.sg` — uptime + incident history. SG procurement loves a status page; it signals operational maturity.
6. **Founder identity verifiable** — LinkedIn-linked About page with real photos. Anonymous teams lose deals at SG universities.
7. **"Your data does not train our AI"** clearly stated in the B2B contract template AND in the dashboard UI. Per spec: B2B user data is architecturally blocked from training.

### 3.4 The B2B Demo Story (UI-Centric)

The demo runs in this order (60 minutes typical):

1. **5 min — Aggregate dashboard**: "This is what your career centre would see — cohort scorecard, common gaps, students needing outreach." (This is the screen that converts the director.)
2. **15 min — Student-side workflow**: walk through a fresh-grad demo account uploading a resume, pasting an MCF JD, getting suggestions. (This proves the product actually works.)
3. **10 min — Application tracking + outcomes**: dashboard funnel + insights. (This proves measurability.)
4. **10 min — PDPA + data governance**: dedicated page walkthrough. (This unblocks procurement.)
5. **20 min — Q&A**.

The design implication: each of these surfaces must hold up to a 15-minute walkthrough. No "and then we'd build…" — every claim must be visible in product.

### 3.5 The Career-Centre Director's Five Questions

A skeptical director will ask:
1. "How is this different from VMock?" → **Design answer**: SG-native intelligence visible in suggestions; per-stage tracking visible in dashboard. NOT just "our slides say so."
2. "What does my staff need to do to deploy this?" → **Design answer**: SSO + roster import; admin dashboard with 1-click cohort creation. Need a self-service admin surface, not "we'll set it up for you."
3. "How do I prove ROI to my dean?" → **Design answer**: a one-page "Cohort Outcomes Report" exportable as PDF, with the key metrics. Dean-presentable.
4. "What happens if a student says you've leaked their data?" → **Design answer**: visible audit log of every data access, plain-language privacy controls per student, 1-click student data export and deletion.
5. "What's your roadmap?" → **Not a design question**, but the demo should feel like a product that has months of polish ahead, not a startup MVP held together with tape.

---

## Part 4 — Competitive Differentiation Through Design

### 4.1 Jobscan (ATS-Focused, Feature-Dense, Utilitarian)

**Their design language**: dense feature tables, ATS-score-as-headline-metric, optimisation-checklist UI, lots of percentages and scores everywhere. Looks like a tool for SEO professionals, not job seekers.

**KeyStone's differentiation**: replace "ATS score" (a metric SG hiring DOES NOT use per the MVP spec) with **per-stage pass rate** as the headline. Replace optimisation checklists with **rewriting suggestions**. The visual is calmer, fewer numbers per square inch, more text per square inch. Reads as advisory, not diagnostic.

**Specific UI tactics**:
- KeyStone has NO score-out-of-100 anywhere in the product. Scores trigger "gaming the score" behavior; KeyStone's value is in qualitative improvement.
- KeyStone shows ONE primary metric per surface; Jobscan shows 12.

### 4.2 Teal (Clean, Outcome-Focused, Career OS Positioning)

**Their design language**: soft-rounded everything, generous whitespace, friendly tone, single-color (literal teal). Looks calm and competent. Closer to KeyStone's target than Jobscan.

**KeyStone's differentiation**: similar visual calmness, BUT
- KeyStone's color is teal-blue, not Teal's literal teal-green — avoids accidental brand collision (and avoids a name+color match that would make KeyStone look derivative).
- KeyStone's content is denser and more directive — Teal's "career OS" pitch keeps suggestions soft and optional; KeyStone's "senior SG colleague" voice is more opinionated.
- KeyStone's per-stage pass-rate funnel is sharper than Teal's resume score. Funnel as a visual carries more institutional weight than a score.
- KeyStone's SG-native rationales are concrete in a way Teal's generic suggestions aren't — the design must let those rationales breathe (more vertical space per suggestion, more text per card).

### 4.3 VMock (B2B, Dashboard-Heavy, Institutional)

**Their design language**: corporate enterprise aesthetic, dense charts, lots of shields and badges, a "professional certification" vibe. Heavy on dashboards. The student-side experience feels like a compliance tool.

**KeyStone's differentiation**: the consumer-side product is a delight to use; the institutional dashboard is enterprise-grade. KeyStone wins B2B not by being more institutional than VMock, but by being **dramatically better on the student side** — and the director sees that in the demo. The pitch becomes: "your students will actually use this."

**Specific UI tactics**:
- KeyStone's student-facing surface has zero university branding by default (universities can co-brand on signed contracts, but the default is clean).
- KeyStone doesn't use shield icons, certificate aesthetics, or "certified" language anywhere — VMock owns that. KeyStone's aesthetic is editorial-professional, not certification-professional.
- KeyStone's STAR Coach equivalent (Phase 2 interview prep) is conversation-driven, not video-recording-driven — distinct from VMock's STAR coach.

### 4.4 The Visual Differentiation in One Sentence

| Competitor | Their visual identity | KeyStone's contrast |
|---|---|---|
| Jobscan | "Your resume scored 73/100 — fix these issues." | "Here's how to rewrite this for the GLC you're applying to." |
| Teal | "Track your career like a CEO." | "Tailor every application to the SG market." |
| VMock | "AI-powered resume certification." | "AI that knows how SG hiring managers read resumes." |

KeyStone's design must make these one-sentence differences visible WITHIN the product, not just on the marketing site. Every surface has at least one detail that proves the contrast — the company-type chip, the SG-rationale text, the per-stage funnel, the calm professional voice.

---

## Part 5 — Cross-Cutting Findings

### 5.1 Design Asymmetry Risk

Several screens are critical to value delivery (suggestion card, analysis wait, dashboard funnel, paywall) and several are supporting (settings, privacy page, account management). The risk: spending equal design effort on all surfaces dilutes the critical ones.

**Recommendation**: explicit design-priority tiering before /implement.
- Tier 1 (production-quality polish): suggestion card, JD input, resume upload, analysis wait, dashboard, paywall, B2B cohort dashboard, landing page hero.
- Tier 2 (functional quality): settings, account, privacy page, login/signup, billing.
- Tier 3 (utility): admin surfaces beyond the B2B dashboard, internal tooling.

A SaaS product wins on Tier 1 polish. Tier 2 just has to not embarrass.

### 5.2 The "SG Intelligence" Risk

The single biggest design risk (echoed in Analysis 28) is that the product's SG-nativeness fails to register visually. If the product looks like generic SaaS with English copy mentioning "Singapore" twice, the value prop dies on contact.

**Mitigation visible in design**:
- The company-type chip (GLC / MNC / Startup) — first proof, visible within 5 seconds.
- The SG flags after resume parse (NRIC / NS / photo) — second proof, visible within 30 seconds.
- The streaming progress with SG insight sidebar — third proof, visible during wait.
- Every rationale citing SG context — Nth proof, throughout the workflow.

Without these, the design becomes generic. With these, the design is the value prop.

### 5.3 The Tone Risk

The voice doctrine ("senior SG colleague") is fragile. One generic-AI rationale breaks the spell for the rest of the session. One emoji in a toast undermines the calm professional aesthetic. One countdown timer at the paywall makes the whole product feel scammy.

**Mitigation**: a published voice-and-tone document, banned-phrase list at the LLM-prompt level, design review at every PR that touches user-facing copy. This is not optional polish — it's what differentiates KeyStone from "another AI resume tool."

---

## Summary

The design coherence audit, in three findings:

1. **The Aha moment lives in the suggestion rationale.** If the rationale cites JD requirement + company-type, the product earns its SGD 19/mo. If it cites generic best practice, the product loses to ChatGPT. Every other design decision supports this one.
2. **The B2B demo is won on the cohort dashboard, not on the student surface.** Design the cohort dashboard to be presentable in an institutional procurement meeting — clean aggregates, actionable insights, audit-ready privacy controls, exportable reports. The student experience must be excellent to clear the threshold; the cohort dashboard is what closes the contract.
3. **Visual SG-nativeness must be tangible by minute 1, not promised.** The company-type chip, the SG flags, the rationale citations — these are the design's job to make visible. A SaaS that "supports the Singapore market" is generic; a SaaS where the user sees "GLC" on the screen 30 seconds in is differentiated.

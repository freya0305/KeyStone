# Analysis 42 — Interview Preparation Module (Phase 2)

**Date**: 2026-04-30
**Question**: User wants to explore the Interview Preparation Module for Phase 2. Based on JD + resume, predict high-frequency questions, provide mock interview or preparation advice, reference answers.

---

## Executive Summary

The Interview Preparation Module is the highest-LTV feature in the roadmap. It extends user engagement from weeks (resume tailoring) to months (interview prep), creates the most differentiated moat, and is triggered at every stage transition — not just once.

**Core insight**: We already have the JD and resume. We can generate questions and guidance without additional user input.

---

## Part 1: What The Feature Does

### The Core Loop

```
User reaches "Interview Stage" →
System generates:
  1. High-frequency questions for THIS JD + THIS user's resume
  2. Why this question is asked (context)
  3. How to approach an answer using THIS resume
  4. Sample strong answer (based on resume content)
  5. Red flags to avoid

User can:
  - Practice in mock interview mode (async, not live)
  - Record themselves answering
  - Get AI feedback on their answer
```

### Trigger Points

The module activates at ANY stage transition where interview is involved:

| Trigger | What Happens |
|---------|-------------|
| User logs "Interview R1" | Interview prep for R1 questions |
| User logs "Interview R2" | R2-specific questions (usually harder/deeper) |
| User logs "Final Round" | Executive/partner round questions |
| User logs "Offer Received" | Offer negotiation prep |
| Any stage | User can manually request interview prep |

---

## Part 2: Question Generation

### Input Data (We Already Have)

From the JD analysis:
- Job title and level (entry/mid/senior)
- Required skills and qualifications
- Company type (GLC/MNC/Startup)
- Industry
- Key responsibilities from JD

From the user's resume:
- Past experience with achievements
- Skills (extracted)
- Education
- Career narrative (fresh grad / career switcher / PMET)

### Output: Question Types

**Level 1 — Questions for ALL candidates** (generic)
- "Tell me about yourself"
- "Why this role/company?"
- "What are your strengths and weaknesses?"
- "Where do you see yourself in 5 years?"

**Level 2 — Questions CALIBRATED to this JD** (our moat)
- "This JD emphasizes team leadership in financial analysis. Tell me about your leadership experience." → Generated because JD has "team leadership" keyword
- "This role requires stakeholder management. What's your experience managing senior stakeholders?" → Generated because JD mentions "stakeholder management"
- "DBS Digital Banking focuses on digital transformation. What's your experience with digital transformation projects?" → Generated because employer = DBS

**Level 3 — Questions CALIBRATED to this user's RESUME** (our moat)
- "Your resume shows a career switch from finance to tech. What motivated this switch?" → Generated because resume shows career pivot
- "I see you have NS experience. How does NS leadership apply to this role?" → Generated because SG male + NS in resume
- "You quantified outcomes at your last job (increased efficiency by 30%). Walk me through that." → Generated because resume has quantified achievements

### Question Generation Prompt (for reference)

```
Given:
- JD: [job description text]
- Employer: [company name]
- Company type: [GLC/MNC/Startup]
- User resume: [resume text]
- User segment: [fresh_grad/mid_career/senior]
- Interview round: [R1/R2/Final]

Generate:
1. 5-8 questions likely to be asked in this interview
2. For each question:
   a. Why this question is asked (context)
   b. How to approach using THIS user's resume
   c. A sample strong answer based on their experience
   d. Red flags (what NOT to say)
3. Company-specific questions if employer is known (DBS, GovTech, etc.)
```

---

## Part 3: The Mock Interview Mode

### How It Works

1. User selects a generated question
2. User records their answer (video or audio, async)
3. System transcribes + analyzes
4. AI provides feedback:
   - Content: Did they answer the question? Did they use resume examples?
   - Structure: STAR format used? Clear and concise?
   - Red flags: Listed to avoid but mentioned anyway?
   - SG-specific: Did they mention NS appropriately? Did they use quantified achievements?

### What Makes This Different from Competitors

| Competitor | Approach |
|-----------|----------|
| Pramp | Live peer-to-peer practice (no AI feedback) |
| InterviewBuddy | Human coaches (expensive, not scalable) |
| Teal | No interview prep feature |
| VMock | Score-based feedback on video, generic questions |

**KeyStone's differentiation**:
- Questions are GENERATED from the specific JD + resume combination
- Feedback references specific resume content
- SG-specific context (NS framing, GLC culture, SG employer norms)
- Triggered by actual interview stage, not user-initiated

---

## Part 4: SG-Specific Interview Intelligence

This is where we add SG market knowledge that Teal/Pramp cannot replicate:

### GLC Interview Norms
- DBS: "Digital transformation" and "stakeholder management" are frequent themes
- GovTech: "Public sector experience" and "policy compliance" questions
- Singtel: "Telecom industry knowledge" and "customer-facing experience"
- MRT/federal roles: "NS experience" framing (positive for leadership/operations)

### MNC Interview Norms
- US MNCs: Direct, achievement-focused answers appreciated
- European MNCs: Teamwork and cultural fit emphasized
- Japanese MNCs: Hierarchy respect and long-term commitment valued

### Cultural Considerations
- "Tell me about a time you disagreed with your manager" → In SG, this needs careful framing (respect hierarchy but show independence)
- "What's your expected salary?" → SG-specific negotiation norms
- "Any questions for me?" → In SG, asking about career progression is appropriate; asking about salary too early is not

---

## Part 5: LTV Impact

### Without Interview Prep
- User gets job offer → logs outcome → churns
- Engagement: 1-3 months

### With Interview Prep
- User gets interview → interview prep activates → user practices → user gets to next round
- User gets R2 → R2 prep activates → user practices → user gets offer
- Engagement extends to 3-6 months per job search

### LTV Extension Calculation

| Without Interview Prep | With Interview Prep |
|----------------------|-------------------|
| Avg subscription: 3 months | Avg subscription: 5-7 months |
| LTV: SGD 36 (monthly) | LTV: SGD 60-84 |
| Annual LTV: SGD 144 | Annual LTV: SGD 144 + sessions |

**Estimated LTV increase**: +60-130% on engaged users who reach interview stage

---

## Part 6: Implementation Complexity

### Phase 2 MVP Scope

For MVP of interview prep module, ship only:

1. **Question generation** (static, no video)
   - Given JD + resume → generate 5-8 questions
   - Show: question + why asked + how to approach + sample answer
   - No: recording, transcription, AI feedback

2. **Text-based guidance** (expandable)
   - STAR format guide
   - SG-specific norms per employer type
   - Common red flags for SG interviews

### Phase 3 Full Feature

- Video/audio recording
- Transcription
- AI feedback on answer content + delivery
- Mock interview simulation (timed, structured)

---

## Part 7: The Moat Angle

Interview prep generates the HIGHEST quality data because:

1. **Stage-specific outcomes**: "User practiced R2 questions, then got R2 → offer" is a labeled success
2. **Question-level granularity**: We know WHICH questions were practiced and what happened
3. **Content correlation**: We can correlate specific answer patterns with outcomes

This data is the deepest moat because:
- No competitor has question-level outcome data
- No competitor knows which questions predict offers at which employers
- After 1,000+ interview outcomes: "Users who practiced R2 DBS questions had 2.3× higher offer rate"

---

## Part 8: Free vs Pro Tier for Interview Prep

| Feature | Free | Basic | Pro | Annual |
|---------|------|-------|-----|--------|
| Question generation for user's JD+resume | No | No | Yes | Yes |
| Sample answers | No | No | Yes | Yes |
| SG employer-specific norms | No | No | Yes | Yes |
| Mock interview (video) | No | No | No | Yes |
| AI feedback on answers | No | No | No | Yes |

**Logic**: Interview prep is a deeper engagement feature. Free/Basic tiers get resume tailoring. Pro+ tiers get interview prep. Annual gets the full practice suite.

---

## Recommendation

**Ship Phase 2 interview prep as text-first MVP**:
1. Question generation (JD + resume → 5-8 questions with full context)
2. Text-based guidance (STAR, SG norms, red flags)
3. This is low engineering cost, high user value, high LTV impact

**Do NOT delay for video feature** — video recording and AI feedback can come in Phase 3.

---

## Summary: Interview Prep Module

| Aspect | Decision |
|--------|----------|
| Trigger | Every interview stage transition (R1, R2, Final) |
| MVP scope | Text-based question generation + guidance |
| Question types | Level 1 (generic) + Level 2 (JD-calibrated) + Level 3 (resume-calibrated) |
| Moat | Question-level outcome data (which questions predict offers) |
| LTV impact | +60-130% on engaged users |
| Tier placement | Pro+ only |
| Phase 2 priority | HIGH — highest LTV feature |

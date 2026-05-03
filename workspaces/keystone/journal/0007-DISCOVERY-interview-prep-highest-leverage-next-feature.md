---
type: DISCOVERY
date: 2026-04-29
created_at: 2026-04-29T09:35:00Z
author: agent
session_id: 874f263b-1879-49b0-9e64-1f293538aedb
project: keystone
topic: Interview preparation module scores as the highest-priority next feature by pain × coverage gap
phase: analyze
tags: [product, interview-prep, ltv, user-journey, pain-points]
---

## Discovery

The user journey pain matrix identifies three pains scoring 80+ priority (Acuity × Frequency × Coverage Gap, scale 125 max):

1. **No feedback on why applications fail** — Score 125 (universal, unserved, most acute)
2. **No JD-specific interview preparation** — Score 80 (tied)
3. **Waiting / silence — no signal** — Score 80 (tied)

The "no application feedback" pain (125) is partially addressed by KeyStone's outcome tracking. The "waiting / silence" pain requires external platform integrations (MCF, LinkedIn, email parsing) that add significant technical complexity.

**Interview preparation is the highest-leverage buildable next feature because**:
- It operates entirely on data KeyStone already has (the JD, the resume, the tailored application), plus user-supplied story input. No new data pipelines.
- It directly follows the tailoring workflow: user tailors resume, submits application, then needs interview prep for the same job. Natural handoff — the JD context is already loaded.
- The pain is high-intensity and high-willingness-to-pay. Interview anxiety is qualitatively different from resume uncertainty. Users will pay to feel prepared.
- LTV impact: adds 3–5 distinct high-value touchpoints per job search (one per interview round), extending active product engagement by 4–6 weeks beyond resume tailoring.

## No Existing Tool Does This Combination

The gap is specific: **JD-anchored high-frequency question prediction + personal story synthesis + iterative practice with evaluation**. 

Current tools:
- Glassdoor Q&A: crowd-sourced but not JD-anchored, no personal story integration
- ChatGPT: capable if prompted well, but requires significant prompting skill, no SG company type context, no iterative practice framework
- VMock STAR Coach: evaluates verbal delivery mechanics, not whether the answer fits the specific JD competencies; no personal story input
- LinkedIn Interview Prep: generic question banks, no JD anchoring, no company-type differentiation

The SG-specific gap is especially large: GLC competency frameworks (Leadership, Integrity, Customer Focus) versus MNC behavioral deep-dives versus startup culture-fit conversations require meaningfully different preparation. No tool currently differentiates on SG company type. KeyStone already has company type classification in its data model.

## Proposed Module Architecture

1. **Input**: User story bank (free-text, unstructured — user writes "tell me about yourself" content, key experiences, NS stories if applicable)
2. **Processing**: System reads JD (already parsed), classifies company type (already classified), generates the 5–8 highest-probability questions for this specific role/company type
3. **Answer synthesis**: System generates reference answers drawing on the user's own stories + JD requirements, structured in STAR format
4. **Practice loop**: User submits a practice answer → system evaluates fit with the JD + story relevance + structure → suggests refinement → repeat
5. **SG-specific layer**: company-type-specific tips (e.g., "For GLC interviews, your answer should include a component about your contribution to Singapore/team/organisation" or "For PSB/MOH, reference your civil service values alignment")

## For Discussion

1. The module assumes users will invest time writing their story bank. What fraction of users will actually do this (high effort, front-loaded)? Is there a design pattern that makes story input feel lighter (e.g., prompted mini-stories: "Tell us about a time you led a team — 2-3 sentences")?
2. Is the practice loop with evaluation sufficient for LTV extension, or does the "iterative" value require human feedback at some point? At what point does AI evaluation of interview answers feel credible vs. hollow?
3. Does adding interview prep as a feature change the product's positioning from "AI resume tool" to "AI job search coach"? Is that positioning upgrade net positive or does it create confusion?

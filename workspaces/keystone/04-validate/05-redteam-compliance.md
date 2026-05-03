# Red Team Report: KeyStone PDPA Compliance Risks

> Phase 04 Validation — 2026-04-30
> Reviewer: quality-reviewer
> Scope: NRIC handling, consent architecture, data residency, third-party processors, jurisdiction

---

## Executive Summary

KeyStone's PDPA compliance architecture is well-structured in its design intent but has significant gaps in enforceability, edge case handling, and third-party risk management. Three HIGH findings require resolution before any real user data is processed. Three MEDIUM findings should be resolved before launch. Four LOW findings are improvements for post-launch.

---

## HIGH Findings (Must Fix Before Launch)

### Finding H1: NRIC Masking Failure = Direct S3 Storage of Sensitive Data

**Risk:** If Stage 1 regex `[STFGstfg]\d{7}[A-Za-z]` fails to detect an NRIC (unusual spacing, mixed case, hyphenated format, or the digit-within-letters variant), the unmasked NRIC is written directly to S3. This is a PDPA breach of sensitive personal data with no recovery path — S3 objects are immutable, and the raw NRIC is now in persistent storage.

**Specific failure modes not addressed:**

1. **Spacing variants**: `S1234567A` vs `S 1234567 A` vs `S1234567 A` (with trailing space)
2. **Hyphenated**: `S-1234567-A` — the hyphen breaks the `\d{7}` sequence
3. **Lowercase letters**: `[STFGstfg]` covers 8 formats but NRIC validation letters can be any A-Z; lowercase-only check misses some valid NRICs
4. **Digit substitution**: OCR errors could turn `0` into `O`, `1` into `I` — detection logic should fuzz or use a validation checksum (NRIC has a valid checksum algorithm)
5. **Copy-paste artifacts**: Users may paste with zero-width spaces or other invisible Unicode that break string matching

**Evidence:** The regex is stated in `specs/compliance.md` § Stage 1 with no fallback mechanism. There is no stated checksum validation, no mention of whitespace normalization, and no Stage 1A re-validation after masking.

**Required fix:**
- Add NRIC checksum validation (Singapore NRIC uses a weighted checksum algorithm) as a second verification layer after regex match
- Normalize all whitespace and common punctuation before matching
- Implement a Stage 1A: read back masked file from S3 before confirming success, assert no raw NRIC patterns survive
- Document the masking failure as a security event triggering immediate user notification and S3 object re-write

---

### Finding H2: Data Residency Is Not Enforceable With Claude API Calls

**Risk:** The spec states all data stays in `ap-southeast-1` and Claude API is configured with "zero data retention." This does NOT mean data processing occurs in Singapore. Data is transmitted to Claude's servers (currently us-east-1 or eu processing regions by default). "Zero data retention" only means the data is not stored after processing — it is still processed outside Singapore.

**PDPA s26(1) cross-border transfer implication:** PDPA prohibits transfer of personal data outside Singapore unless the destination has "a standard of protection comparable to Singapore's." The PDPC has not confirmed the US has comparable protection. Anthropic's "zero data retention" is a processing agreement, not a data residency guarantee.

**Evidence:** `specs/compliance.md` § Data Residency states "Anthropic Claude API: configure for zero data retention" — zero retention ≠ processing in Singapore. This is a fundamental misunderstanding of the control.

**Required fix:**
- Either: (a) Use a Claude API deployment with explicit Singapore/EU data residency (Anthropic offers this for enterprise customers with explicit DPA), OR (b) acknowledge in the privacy notice that resume data is processed outside Singapore for AI analysis, and obtain explicit consent for this cross-border transfer
- Remove the claim "all data stays in ap-southeast-1" unless it is technically enforced
- The PDPA s26 consent exception requires the user to be informed of the cross-border transfer — the current consent architecture does not include this disclosure

---

### Finding H3: No DPO Engaged — Hard Launch Block

**Risk:** The spec explicitly states: "Do not launch with real user data without a DPO engaged." This is a mandatory PDPA requirement. An external DPO is required to review the DPIA, validate the consent architecture, and be named in the privacy policy. Without a DPO, there is no PDPA-compliant accountability structure for data protection decisions.

**Evidence:** `specs/compliance.md` § External DPO states the DPO is "Required before processing any real user data" and gives an estimated cost of SGD 2,000–5,000. No DPO is listed in the current team or project contacts.

**Required fix:**
- Engage a Singapore-based qualified DPO before any real user data is processed
- Have DPO review and sign off on the DPIA before launch
- Name the DPO in the privacy policy (required under PDPA)
- Document DPO engagement in the compliance file trail

---

### Finding H4: Agency "We Have Consent For Everything" Creates KeyStone Liability

**Risk:** Under Model A, the agency claims it has consent from candidates. If an agency represents it has consent for KeyStone's AI processing and outcome tracking, but that consent was collected for a different purpose (job placement, not AI resume analysis), the consent is not valid for KeyStone's use. KeyStone processes data based on the agency's representation, making KeyStone potentially liable for processing without valid consent.

**PDPA s20 exception (purpose limitation):** Consent must be for the specific purpose at the time of collection. Consent for "job placement services" does not cover "AI resume optimization and training data collection."

**Evidence:** Analysis 34 § Model A states agencies refer candidates who "give their own consent" — but if an agency has already told candidates "we'll share your data with partners," candidates may believe they are consenting to a previously-arranged arrangement rather than making a fresh, informed choice.

**Required fix:**
- KeyStone must collect its own direct consent from each candidate at registration, regardless of any agency representation
- Contractual clause in all agency agreements: "Agency represents that any candidate referral is made with candidate's informed consent for KeyStone's data practices; Agency shall indemnify KeyStone for any breach of this representation"
- Consent flow must clearly state: "Your data will be processed by KeyStone (company), stored in Singapore, and used for [purposes]. This is independent of any previous consent you may have given [Agency Name]."

---

### Finding H5: University Outcome Data Boundary Is Not Defined

**Risk:** Students submit resumes to KeyStone. Universities want outcome data (are students getting jobs?). The PDPA boundary is unclear: if KeyStone shares outcome data with universities, it becomes a data processor for the university's purposes. If universities can identify individual students from aggregate data, it is not truly anonymized under PDPA's re-identification standard.

**Specific gaps:**
1. **What data does the university actually receive?** If university receives "50 of 100 design partner students received offers," this is aggregate but may be re-identifiable if cohort is small
2. **What is the legal basis for sharing outcome data with university?** Student consent only covers KeyStone's purposes; sharing with university requires separate legal basis (either student consent for university disclosure, or university has its own independent legal basis)
3. **Who is the data controller for university-shared data?** If KeyStone shares individual outcome data, KeyStone and university may be joint controllers, requiring a joint controller agreement

**Evidence:** Analysis 34 § University MOU describes outcome tracking but does not define the data sharing boundary. Specs/compliance.md § B2B University has "aggregate-only data sharing protocol" but no technical or legal definition of "aggregate."

**Required fix:**
- Define technically what "aggregate" means for PDPA purposes (minimum cohort size of 10, no single individual can be identified directly or indirectly, no small-cell suppression issues)
- Execute a Data Processing Agreement with university before any data sharing
- Consent flow must explicitly disclose: "Your outcome data (anonymized in aggregates of 10+) may be shared with [University Name] for careers program evaluation"
- Implement row-level security ensuring no individual student's outcome is visible to university — only aggregate statistics

---

## MEDIUM Findings (Should Fix Before Launch)

### Finding M1: Consent Revocation Leaves Processed Data In AI Pipeline

**Risk:** If a user revokes AI Processing consent (type 3) after data has been sent to Claude API, the revocation does not recall the data from Claude's processors. The data has already been processed. The revocation only prevents future processing.

**PDPA inconsistency:** The spec says users "can revoke anytime" and revocation "stops AI features." It does not address the data already processed. If a user revokes consent for AI processing but their resume was already analyzed, the revocation is backward-looking in effect only.

**Edge case:** User signs up, uploads resume, opts out of AI processing in settings, but resume was already sent to Claude API before the opt-out was processed. What is the data retention obligation? The spec says data is "retained" (implying stored) after opt-out, but does not address what happens to data already processed by Claude.

**Recommended fix:**
- Add a processing delay (e.g., queue-based) so consent can be registered before data leaves KeyStone's systems
- In privacy notice, disclose: "Once data is transmitted to our AI processor, revocation of AI processing consent prevents future processing but cannot recall processed data. We retain your data for [X period] in accordance with our data retention policy."
- Implement a processing window flag: data marked "awaiting AI processing" stays in queue for a consent check before being sent to the API

---

### Finding M2: Stripe Payment Data — What Does KeyStone Store?

**Risk:** Stripe handles PCI-DSS compliance for card data. However, KeyStone may store transaction metadata (amount, date, plan tier, user ID) which is not PCI-DSS relevant but is PDPA-relevant personal data. Stripe's own DPA covers the card data; it does not cover the transaction records KeyStone creates.

**Specific gap:** The compliance spec does not address what payment data KeyStone stores. If KeyStone stores any record linking a user identity to a payment (even a Stripe subscription ID), this is personal data under PDPA and must be included in the data inventory, consent architecture, and retention policy.

**Recommended fix:**
- Document exactly what Stripe data KeyStone stores: subscription ID, plan, billing cycle, amount — all of these are personal data linked to identity
- Include payment consent (storage of transaction records) in the six-type consent architecture or as a separate seventh type
- Define retention period for payment records (minimum: duration of subscription + any legal hold period)

---

### Finding M3: Clerk OAuth — No DPA On File

**Risk:** Google OAuth data (email, name, profile picture URL) is processed by Clerk. Clerk's standard terms may not meet Singapore PDPA requirements for data processing agreements. Under PDPA s24, when a data controller uses a data processor, there must be a contract ensuring the processor acts only on the controller's instructions.

**Specific questions without answers:**
- Does Clerk have a DPA addendum for Singapore PDPA compliance?
- Where is Google OAuth user data actually processed/stored?
- What is Clerk's data retention policy for OAuth tokens?

**Recommended fix:**
- Request Clerk's DPA addendum for PDPA compliance (most enterprise SaaS vendors have this)
- Document the countries where Clerk/Google process OAuth data
- If Clerk's DPA does not meet PDPA standards, implement a workaround: email/password authentication as primary with Google OAuth as optional alternative, and move Google OAuth to a later phase after DPA is confirmed

---

### Finding M4: International Users — Malaysian Jurisdiction

**Risk:** A Malaysian job seeker uses KeyStone. Malaysia has its own PDPA (PDPA 2010, amended 2020). Singapore PDPA does not apply to Malaysian residents. KeyStone's privacy notice is written for Singapore PDPA. If KeyStone stores Malaysian user data in Singapore, it may be subject to Malaysia's cross-border transfer restrictions (PDPA s43A — transfer outside Malaysia requires the destination to have comparable protection).

**Evidence:** No mention of international user handling in any compliance document. No jurisdiction selection in signup flow. No Malaysia-specific consent language.

**Recommended fix:**
- Add jurisdiction detection at signup: "Are you currently residing in Singapore?" (required for PDPA applicability)
- For non-SG users: either (a) apply Singapore PDPA voluntarily as a comparable standard, or (b) implement a geographically-restricted rollout
- Privacy notice must disclose where Malaysian user data is stored and processed
- Consider Malaysia's PDPA in the DPA with Clerk and Stripe

---

### Finding M5: Six Consent Types — Implementation Complexity Underestimated

**Risk:** Each of six consent types must be independently tracked, enforced at every data processing boundary, and correctly implemented. The spec describes the architecture but not the implementation. Real-world complexity:

1. **Consent type 3 (AI Processing)** gates data being sent to Claude — must be checked at the API call site, not just at the upload endpoint
2. **Consent type 4 (B2B Sharing)** gates aggregate data being visible to institutional clients — must be enforced at the query layer, not just at dashboard display
3. **Consent type 5 (Outcome Tracking)** gates whether outcome data is written to the database — must be enforced at every outcome submission

**Edge case — consent ambiguity:** User uploads resume (consent type 1 = yes, type 2 = yes), immediately goes to settings and opts out of AI Processing (type 3 = no). Resume is already in S3 (type 2 covered). But what about the suggestion signals generated from the pre-upload resume analysis that ran on signup? Or if the user later re-enables AI Processing — can KeyStone retroactively process the stored resume?

**Recommended fix:**
- Implement consent as a claims token in the JWT or as a server-side flag checked at every processing boundary, not as a UI checkbox state
- Document the processing decision tree: "If consent type 3 = no at time of API call, API call is blocked, no data transmitted"
- Address retroactive processing: once opted-out, stored resume cannot be AI-processed without re-obtaining consent

---

## LOW Findings (Post-Launch Improvements)

### Finding L1: DPIA Not Completed

The spec requires a DPIA before launch covering three risk areas (NRIC handling, AI processing, B2B data sharing). No DPIA is documented. This should be completed by the DPO once engaged.

### Finding L2: Breach Response Protocol — Internal Contact Is Single Point of Failure

The breach response protocol lists "founder/CTO (sole operator initially)" as internal contact. If the CTO is unavailable during a breach (overnight, weekend), 3-day PDPC notification deadline may be missed. Assign a backup contact.

### Finding L3: Audit Log Retention — 12 Months May Be Insufficient

PDPA does not specify a minimum retention period for audit logs. 12 months is stated but may not be sufficient for demonstrating compliance if a complaint is filed months after an incident. Consider 3 years (aligned with common statute of limitations for civil claims in Singapore).

### Finding L4: Marketing Consent Default — Spec Correct, Implementation Must Verify

The spec correctly states marketing consent must NOT be pre-ticked. This is a PDPA requirement. Implementation must verify that no pre-ticked checkboxes exist in any signup or settings flow. Add automated test to catch pre-ticked marketing consent.

---

## Summary Table

| Finding | Severity | Category | Owner | Fix Before Launch |
|---------|----------|----------|-------|-----------------|
| H1: NRIC masking gaps | HIGH | NRIC | Engineering | Yes |
| H2: Data residency / Claude API | HIGH | Data Residency | Engineering + Legal | Yes |
| H3: No DPO engaged | HIGH | Governance | Founder | Yes |
| H4: Agency consent liability | HIGH | Third-Party | Legal | Yes |
| H5: University data boundary | HIGH | University | Legal + Engineering | Yes |
| M1: Consent revocation data | MEDIUM | Consent | Engineering | Recommended |
| M2: Stripe metadata | MEDIUM | Payment | Engineering | Recommended |
| M3: Clerk DPA | MEDIUM | Auth | Legal | Recommended |
| M4: Malaysia jurisdiction | MEDIUM | International | Legal + Engineering | Recommended |
| M5: Consent implementation | MEDIUM | Consent | Engineering | Recommended |
| L1: DPIA incomplete | LOW | Governance | DPO | Post-launch |
| L2: Breach contact backup | LOW | Operations | Founder | Post-launch |
| L3: Log retention period | LOW | Operations | Engineering | Post-launch |
| L4: Pre-ticked marketing | LOW | Consent | Engineering | Verify pre-launch |

---

## Priority Sequence for Launch Clearance

Before any real user data is processed, the following must be completed in order:

1. **Engage DPO** (Finding H3) — unblocks DPIA and consent architecture review
2. **Complete DPIA** (Finding L1, after DPO engagement) — validates all three risk areas
3. **Fix NRIC masking** (Finding H1) — prevents immediate data breach risk
4. **Define Claude API cross-border disclosure** (Finding H2) — ensures PDPA s26 compliance
5. **Contractual protections for agency referrals** (Finding H4) — prevents third-party consent fraud
6. **Define university data sharing protocol** (Finding H5) — prevents inadvertent PDPA violation with first university partner

Items M1–M5 and L1–L4 should be completed before public launch but are not hard blocks on internal testing with synthetic data.

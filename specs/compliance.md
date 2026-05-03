# Compliance Spec — KeyStone (PDPA)

> Last updated: 2026-04-29 (Phase 01 Analysis)
> Singapore PDPA (Personal Data Protection Act 2012, amended 2021) compliance is a core design requirement, not an afterthought.

---

## PDPA Obligations

### Data Classification
| Data Type | Sensitivity | Handling |
|-----------|-------------|---------|
| Resume content (general) | Medium | Encrypted at rest; masked before AI API calls |
| NRIC number | HIGH — sensitive personal data | Three-stage masking (see below); never stored in plaintext |
| Name, email, phone | Medium | Standard encrypted storage; consent required |
| Job application URLs | Low | Stored; no PDPA sensitivity |
| Application outcomes (callback/interview/offer) | Medium | Linked to user account; consent required |
| AI suggestion accept/reject signals | Low-Medium | Anonymised before aggregate analysis; consent required |
| B2B cohort aggregate data | Low (aggregate, anonymised) | Accessible to institutional buyer only; no individual visibility |

---

## NRIC Handling — Three-Stage Pipeline

### Stage 1: Upload → S3 Storage
- Detect NRIC pattern on upload: `[STFGstfgMN]\d{7}[A-Za-z]` (citizen + PR) and FIN pattern: `[KLPkpmn]\d{7}[A-Za-z]`
- Mask NRIC in document before writing to S3: replace with `[NRIC_REDACTED]`
- Log detection event (not the NRIC value)
- Notify user: "We detected an NRIC number in your resume. We've recommended removing it. Your stored copy has been masked."

### Stage 2: Before AI API Call
- Re-scan masked document before sending to Claude API
- If any NRIC pattern survived Stage 1 masking (edge cases, unusual formatting): re-mask
- Assert zero NRIC patterns in outbound payload before API call — raise if assertion fails

### Stage 3: AI Output → Database Write
- Sanitise AI-generated suggestions for any reconstructed NRIC patterns (edge case: AI might generate NRIC-like strings)
- Write sanitised output to database

**Implementation note**: Masking logic must be a shared utility function used at all three stages. Inline masking at individual call sites is BLOCKED.

---

## Consent Architecture — Six Types

Each consent is independently revocable. Revoking one does not affect others.

| Consent Type | Required For | Default | User Can Revoke |
|-------------|-------------|---------|----------------|
| Registration | Account creation | Mandatory | Account deletion only |
| Storage | Storing resume + application data | Opt-in at signup | Delete data anytime |
| AI Analysis | Sending data to Claude API for resume/job analysis | Opt-in at first analysis | Stops AI features; data retained |
| AI Training Data | Using anonymised suggestion/outcome data to improve KeyStone analysis models | Opt-in (separate checkbox, NOT pre-ticked) | Opt-out anytime; deletion removes data from training pipeline |
| B2B Sharing | Sharing anonymised aggregate data with institutional client | Opt-in separately | Opt-out anytime |
| Outcome Tracking | Storing application outcomes + callback rate calculation | Opt-in in dashboard | Opt-out deletes history |
| Marketing | Newsletters, product updates, promotional emails | Opt-in (NOT pre-ticked) | Unsubscribe at any time |

**Implementation**: Consent state stored per user per type. Every data processing pipeline must check consent state before processing. Pipeline that processes data without valid consent is a PDPA breach.

---

## Data Residency

All user data must remain within Singapore:
- AWS ap-southeast-1 (Singapore region) for all storage, compute, and database
- No cross-region replication to non-SG regions
- Anthropic Claude API: configure for zero data retention (per Anthropic's data processing agreement options)
- Stripe: Singapore-region data processing where available

**B2B data**: University cohort data stored in dedicated RLS (row-level security) tenant partition. No cross-tenant data access.

---

## Data Retention Schedule

| Data Type | Retention Period | Deletion Trigger |
|-----------|----------------|-----------------|
| Resume files (S3) | 2 years from last login OR account deletion | Account deletion OR 24 months inactivity |
| Application outcomes | 3 years from last login OR account deletion | Account deletion OR 36 months inactivity |
| Suggestion signals (anonymised) | 5 years | No individual deletion (anonymised, no PII) |
| AI Training Data (if consented) | Until user revokes consent OR 3 years | User opt-out deletes within 30 days |
| Auth logs | 12 months | Auto-purge at 12 months |
| Payment records | 7 years | PDPA financial record requirement |
| Audit logs | 12 months minimum | Auto-purge |

**Deletion process**: User-initiated deletion = immediate flag + 30-day grace period + permanent removal. Inactivity deletion = 30-day warning email before deletion.

---

## External Data Protection Officer (DPO)

- **Required before processing any real user data**
- Must be a Singapore-based, qualified DPO
- Role: review DPIA (Data Protection Impact Assessment), advise on consent architecture, be named in privacy policy
- Estimated cost: SGD 2,000–5,000 for initial engagement + annual retainer
- **Do not launch with real user data without a DPO engaged**

---

## Data Protection Impact Assessment (DPIA)

A DPIA is required before processing sensitive personal data (NRIC, employment status, salary expectations). Key risk areas:
1. NRIC handling in uploaded resumes (high risk — sensitive data)
2. AI processing of resume content (medium risk — personal data leaving SG systems)
3. B2B aggregate data shared with institutional clients (medium risk — aggregate, but must ensure non-re-identification)

DPIA to be completed by DPO before launch.

---

## Breach Response Protocol

As per PDPA 2021 mandatory breach notification:
- Breaches affecting ≥500 users OR involving NRIC data: notify PDPC within 3 calendar days
- All data breaches: notify affected users within 3 calendar days of assessment

Incident response contacts:
- Internal: founder/CTO (sole operator initially)
- External: DPO
- Regulatory: PDPC (Personal Data Protection Commission)

Logging: all data access events must be logged for audit trail. Minimum retention: 12 months.

---

## B2B University PDPA Requirements

Universities will conduct their own PDPA / data residency review before signing contracts. Prepare:
- Data Processing Agreement (DPA) template
- Confirmation of AWS ap-southeast-1 data residency
- Zero data retention confirmation from Anthropic
- Description of NRIC masking pipeline
- Student consent flow documentation
- Aggregate-only data sharing protocol

PDPA review adds 2–3 months to university procurement timeline. Start preparing documentation at Month 1; do not wait until a deal is near-close.

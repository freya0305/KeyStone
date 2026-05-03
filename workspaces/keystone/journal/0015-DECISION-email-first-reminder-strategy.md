---
type: DECISION
date: 2026-04-29
created_at: 2026-04-29T14:10:00Z
author: co-authored
session_id: 874f263b-1879-49b0-9e64-1f293538aedb
project: keystone
topic: Email-first reminders replace push notifications for browser-only users
phase: analyze
tags: [reminders, email, outcome-logging, browser, push-notifications]
---

## Decision

**Outcome logging reminders will use email as the primary channel** (not push notifications). The product is web-only; no native app exists. Push notifications require either native app or Web Push API opt-in — neither is available at launch.

## What Changes

Previous spec: "Day-7 and Day-21 nudges" (channel unspecified, implying push notifications)

New spec:
- **Day 3 / Day 10 / Day 21 email reminders** per application, containing a JWT-signed deep link that opens the status update modal directly (no login required for the update action)
- **Weekly Sunday digest** of all open applications ("any updates?")
- **Download-triggered record creation** remains the highest-conversion logging point (no change)

Web Push API is deferred to Phase 2 as an opt-in supplement for Chrome/desktop users.

## Email Parsing (Phase 3 flag)

Identified a high-value Phase 3 feature: Gmail/Outlook OAuth integration to auto-detect MCF/JobStreet/LinkedIn notification emails and automatically update application status. This could increase outcome logging rate from 15–22% (with email reminders) to 40–60% (fully automated). Architecture should reserve an integration point for this.

## Projected Outcome Logging Rate

| State | Projected rate |
|-------|---------------|
| No reminders (baseline) | 3–6% |
| Download-triggered capture only | 8–12% |
| + Email sequence (MVP) | 12–18% |
| + Weekly digest (MVP) | 15–22% |
| + Web Push (Phase 2) | 18–28% |
| + Email parsing (Phase 3) | 40–60% |

Target for MVP: 15–22%. This is a 3–4x improvement over the 3–6% baseline, significantly accelerating data flywheel.

## Technical Requirements

- JWT-signed deep links (7-day TTL) in every reminder email
- SPF/DKIM/DMARC on sending domain before launch (email deliverability)
- Maximum 3 reminder emails per application (anti-harassment)
- Unsubscribe link required (PDPA)

## For Discussion

1. The JWT deep link approach means unauthenticated users can update application status via email click. This is convenient but creates a trust question: should a one-click email update require confirmation ("Are you sure you want to mark this as 'responded'?") or should it be single-action? What's the tradeoff between friction and data accuracy?
2. The "auto-mark no response after Day 21 unanswered" logic will affect benchmark accuracy. If users don't respond because they're busy (not because there's no response), auto-close will skew the "no response" category upward. What's the right default: auto-close or leave open indefinitely?
3. Should the weekly digest email aggregate ALL open applications in one email, or send separate emails per application? Separate emails have higher per-application open rates but risk feeling like spam if users have 20 open applications.

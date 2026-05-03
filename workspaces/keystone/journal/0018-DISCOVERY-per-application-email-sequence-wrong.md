---
type: DISCOVERY
date: 2026-04-29
created_at: 2026-04-29T15:00:00Z
author: human
session_id: 874f263b-1879-49b0-9e64-1f293538aedb
project: keystone
topic: CORRECTION of 0015 — per-application email sequences cause inbox explosion for mass-applicants; replace with pull-based batch logging
phase: analyze
tags: [outcome-logging, email, reminders, ux, correction]
---

## Correction to Journal Entry 0015

Entry 0015 proposed email sequences per application (Day 3 / Day 10 / Day 21). This is wrong for SG job seekers who mass-apply (海投).

User correction: "每个岗位都发送邮件那样收件箱会爆炸，一般用户可能会集中海投"

A user with 30 active applications × 3 reminder emails = 90 emails over 3 weeks. The strategy would cause unsubscribes, spam classification, and reputational damage to the email sending domain. Per-application email sequences are explicitly BLOCKED.

## Correct Strategy

**Pull-based, not push-based**. The goal is to capture outcome logging at moments the user is already in the product, not to push reminders to their inbox.

Four mechanisms (MVP):
1. **Download-triggered capture** — at resume export, one-click application record creation
2. **Batch quick-update UI** — persistent in-product banner + card swipe interface to update all pending applications in one session (designed for 30 apps in <3 min)
3. **Pre-prep interstitial** — before interview prep, surface other pending applications for batch update
4. **Single weekly digest email** (max 1/week/user, only if no login that week) — not per-application, aggregated

Auto-close: 30-day silence → auto-mark "no response (inferred)" + correction toast at next login.

## Updated Outcome Logging Rate Projection

| Strategy | Projected rate |
|---------|---------------|
| Baseline (no mechanisms) | 3–6% |
| + Download-triggered capture | 8–12% |
| + In-product batch update (pull) | 15–20% |
| + Pre-prep interstitial + gamification | 20–25% |
| + Weekly digest email | 22–28% |
| + Email parsing (Phase 3) | 45–60% |

Target for MVP: **20–25%** (vs old target 15–22% with per-application emails)

## For Discussion

1. The batch update UI requires users to return to KeyStone voluntarily. For users who only visit when they need to prepare a new application, the capture rate is high. For users who don't return between applications, we have limited visibility. Is there any mechanism besides email that could surface the batch update at the right moment?
2. The auto-close at 30 days means that if a GLC processes applications slowly (sometimes 6–8 weeks for government roles), applications get auto-closed before receiving a response. Should the auto-close threshold be different by employer type (GLC/government: 45 days; startup: 21 days)?
3. The gamification "tracking completeness" metric only motivates users who care about the analytics. New users with <5 applications have no analytics to motivate them. What's the value framing for tracking completeness BEFORE the dashboard has anything meaningful to show?

# Task 21: Pre-prep interstitial for application updates

**Status**: pending
**Priority**: P2
**Created**: 2026-05-11
**Source**: Original todo

## Description

Add an interstitial/page that prompts users to update application status before interview stages. Drives return visits and outcome updates.

## Requirements

1. When user is about to update an application to "Interview" stage, show interstitial
2. Prompt to add interview prep notes or update previous outcome
3. Remind to record outcome after interview
4. Drives return visits + outcome updates that feed VP2

## Value Proposition

Supports VP2: drives outcome event capture and reminder flow

## Files to examine

- src/keystone/api/job_seeker.py
- apps/web/src/app/(app)/applications/page.tsx

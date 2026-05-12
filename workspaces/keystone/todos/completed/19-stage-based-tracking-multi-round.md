# Task 19: Full stage-based tracking with multi-round support

**Status**: pending
**Priority**: P1
**Created**: 2026-05-11
**Source**: Original todo

## Description

Implement complete stage-based application tracking that supports multiple interview rounds. This is the core "where it stands" UI for VP1.

## Requirements

1. Full application lifecycle: Applied → Response → Screening → Interview Round N → Final → Decision
2. Support multiple interview rounds (not just single interview stage)
3. Stage transitions are the key outcome events that feed VP2
4. UI shows current stage clearly for each application

## Value Proposition

VP1 core: "Know exactly where every application stands" — this IS the tracking UI.

## Files to examine

- src/keystone/api/job_seeker.py
- src/keystone/models/entities.py
- apps/web/src/app/(app)/applications/page.tsx

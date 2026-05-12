# Task 18: Auto-close 60-day stale applications

**Status**: pending
**Priority**: P1
**Created**: 2026-05-11
**Source**: Original todo

## Description

Implement auto-close for applications that have had no status update in 60 days. This keeps the dashboard accurate and prevents stale applications from cluttering the user's tracking view.

## Requirements

1. Create a background job or scheduled task that runs daily
2. Query applications with no status update in 60 days
3. Auto-update their status to "Closed" or "Stale"
4. Do not delete data — just mark as closed

## Value Proposition

Supports VP1: "Know exactly where every application stands" — keeps dashboard clean and accurate.

## Files to examine

- src/keystone/api/job_seeker.py
- src/keystone/models/entities.py
- src/keystone/workers/celery_app.py (for scheduling)

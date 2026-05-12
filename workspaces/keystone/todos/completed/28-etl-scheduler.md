# Task 28: Fix ETL scheduler for skill frequency pipeline

**Status**: pending
**Priority**: P0
**Source**: /redteam audit

## Description

skill_etl.py has run_nightly_etl() but no cron/Celery Beat trigger.

## Requirements

1. Add Celery Beat schedule in celery_app.py for nightly ETL
2. Verify skill_frequency table gets populated from real JD data
3. Test the pipeline end-to-end

## Files to examine

- src/keystone/services/skill_etl.py
- src/keystone/workers/celery_app.py

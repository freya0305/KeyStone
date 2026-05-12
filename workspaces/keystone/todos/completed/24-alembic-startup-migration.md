# Task 24: Add Alembic migration to production startup

**Status**: pending
**Priority**: P0
**Created**: 2026-05-11
**Source**: /redteam audit

## Description

Create entrypoint script that runs `alembic upgrade head` before uvicorn/celery start. Fix docker-compose.yml:

1. Add volumes section to cache service mounting redis_data
2. Add startup script that waits for postgres then runs migrations

## Blockers

Fresh deploy fails because database tables don't exist.

## Files to modify

- docker-compose.yml
- Create: entrypoint.sh or startup script

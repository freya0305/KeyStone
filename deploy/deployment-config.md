---
type: application
platform: docker-compose
---

# KeyStone Application Deployment Configuration

## Application Overview

- **Name**: KeyStone
- **Type**: Full-stack web application (Next.js frontend + FastAPI backend)
- **Description**: AI-powered Job Seeker + Recruiter JD Tool (Singapore market)

## Infrastructure

### Backend (FastAPI)
- **Port**: 8000
- **Health endpoint**: `/health`
- **Dockerfile**: `./Dockerfile` (root)
- **Entry**: `keystone.main:app`

### Frontend (Next.js)
- **Port**: 3000 (default Next.js)
- **Build**: `npm run build` in `apps/web/`
- **Dockerfile**: `apps/web/Dockerfile` (needs creation)

### Database
- **PostgreSQL**: 16-alpine
- **Redis**: 7-alpine

## Production Paths

```yaml
production_paths:
  - "src/keystone/**"
  - "apps/web/src/**"
  - "pyproject.toml"
  - "apps/web/package.json"
```

## Deploy Command

```bash
# Build and start production services
docker compose -f docker-compose.yml up -d --build

# Or with explicit image tag
GIT_HASH=$(git rev-parse --short HEAD) docker compose -f docker-compose.yml build && docker compose -f docker-compose.yml up -d
```

## Deploy Check Command

```bash
# Get current deployed commit (from container label or git hash in env)
docker compose ps --format json | jq -r '.[].Labels."com.docker.compose.service"' 2>/dev/null || echo "unknown"
```

## Smoke Test

```bash
# Health check
curl -f http://localhost:8000/health || exit 1

# API endpoint check
curl -f http://localhost:8000/api/health || exit 1
```

## User-Facing URL

- **Frontend**: `http://localhost` (nginx) or direct `http://localhost:3000`
- **API**: `http://localhost:8000`

## Pre-Deploy Gates

1. **Backend tests**: `uv run pytest tests/ -x`
2. **Frontend build**: `cd apps/web && npm run build`
3. **Lint**: `cd apps/web && npm run lint`

## Post-Deploy Checks

1. Health endpoint responds 200
2. API responds 200
3. Frontend loads without errors

## Deployment Steps

1. Run pre-deploy gates
2. Build Docker images with git hash
3. Deploy with docker compose
4. Run smoke tests
5. Verify health endpoints

## Environment Variables (Production)

Required in `.env`:
- `DEBUG=false`
- `DATABASE_URL`
- `REDIS_URL`
- `ANTHROPIC_API_KEY`
- `STRIPE_SECRET_KEY`
- `JWT_SECRET` (min 32 chars)
- `CLERK_SECRET_KEY`
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `S3_BUCKET`
- `INTERNAL_API_KEY` (required when debug=false)
- `APP_CORS_ORIGINS` (comma-separated domains)

## Notes

- Frontend Dockerfile needs to be created at `apps/web/Dockerfile`
- Consider nginx reverse proxy for production
- Set up SSL/TLS termination at load balancer

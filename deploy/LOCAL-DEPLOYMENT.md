# KeyStone Local Deployment Guide

This guide covers how to run KeyStone locally using Docker Compose.

## Prerequisites

- Docker with Colima context installed
- Docker Compose v2+

## Starting the Application

1. Copy the environment template and configure:

```bash
cp .env.example .env
# Edit .env and add your API keys (CLERK keys are required)
```

2. Start all services in detached mode:

```bash
docker --context colima compose up -d
```

This starts all services: web, api, db, cache, localstack, and worker.

3. Create the local S3 bucket for resume uploads:

```bash
# Wait for LocalStack to be ready (about 10 seconds)
sleep 10

# Create the bucket using awslocal (or aws with --endpoint-url)
docker --context colima compose exec localstack bash -c "awslocal s3 mb s3://keystone-resumes-dev"
```

## Local S3 (LocalStack)

For local development, LocalStack provides a mock S3 service. This is required for resume upload functionality.

- **Endpoint**: http://localhost:4566
- **Bucket**: keystone-resumes-dev
- **Credentials**: test / test

To use AWS CLI with LocalStack:

```bash
# List buckets
aws --endpoint-url=http://localhost:4566 s3 ls

# List objects in bucket
aws --endpoint-url=http://localhost:4566 s3 ls s3://keystone-resumes-dev/

# Upload a file
aws --endpoint-url=http://localhost:4566 s3 cp resume.pdf s3://keystone-resumes-dev/resumes/
```

**For production**: Set `AWS_ENDPOINT_URL=` (empty) and use real AWS credentials in `.env`.

## Checking Status

To view the status of all containers:

```bash
docker --context colima compose ps
```

Expected output shows all services as "Up" with healthy status indicators:

| Service    | Description              |
| ---------- | ------------------------ |
| web        | Next.js frontend         |
| api        | FastAPI backend          |
| db         | PostgreSQL database      |
| cache      | Redis cache              |
| localstack | LocalStack S3 emulator   |
| worker     | Celery background worker |

## Viewing Logs

View logs for all services:

```bash
docker --context colima compose logs
```

View logs for a specific service:

```bash
docker --context colima compose logs web      # frontend logs
docker --context colima compose logs api      # backend API logs
docker --context colima compose logs worker   # background worker logs
docker --context colima compose logs db       # database logs
docker --context colima compose logs cache    # redis cache logs
```

Tail logs in real-time:

```bash
docker --context colima compose logs -f web
```

## Stopping the Application

To stop all services (preserves data volumes):

```bash
docker --context colima compose down
```

To stop and remove volumes (deletes database data):

```bash
docker --context colima compose down -v
```

## Access URLs

| Service  | URL                        |
| -------- | -------------------------- |
| Web UI   | http://localhost:3000      |
| API      | http://localhost:8000      |
| API Docs | http://localhost:8000/docs |

## Environment Variables

For production deployments, set these required variables:

```bash
INTERNAL_API_KEY=<your-api-key>       # Internal API authentication key
APP_CORS_ORIGINS=<origins>            # Allowed CORS origins (e.g., http://localhost:3000)
```

Without these variables, Docker Compose issues warnings but services start with default (insecure) values.

## Rebuilding Services

After code changes, rebuild and restart affected services:

```bash
docker --context colima compose up -d --build [service-name]
```

Rebuild everything:

```bash
docker --context colima compose up -d --build
```

## Database Migrations

Run database migrations:

```bash
docker --context colima compose exec api python -m alembic upgrade head
```

Create a new migration:

```bash
docker --context colima compose exec api python -m alembic revision --autogenerate -m "description"
```

## Troubleshooting

### Resume Upload Not Working

If resume uploads fail with S3 errors:

1. Check LocalStack is running: `docker --context colima compose ps localstack`
2. Verify bucket exists:
   ```bash
   docker --context colima compose exec localstack bash -c "awslocal s3 ls"
   ```
3. If bucket doesn't exist, create it:
   ```bash
   docker --context colima compose exec localstack bash -c "awslocal s3 mb s3://keystone-resumes-dev"
   ```
4. Check API logs for S3 errors:
   ```bash
   docker --context colima compose logs api | grep -i s3
   ```

### Worker Unhealthy

If the worker service shows unhealthy status:

```bash
docker --context colima compose logs worker
```

Common issues:

- Missing environment variables
- Database connection failures
- Redis connection failures

### API Connection Refused

If the web app cannot connect to the API:

1. Check API is running: `docker --context colima compose ps api`
2. Check API logs: `docker --context colima compose logs api`
3. Verify port 8000 is not blocked: `lsof -i :8000`

### Database Connection Issues

```bash
docker --context colima compose exec db psql -U postgres -d keystonedb
```

## Quick Reference

```bash
# Start all services
docker --context colima compose up -d

# Create local S3 bucket (first time only)
docker --context colima compose exec localstack bash -c "awslocal s3 mb s3://keystone-resumes-dev"

# Status
docker --context colima compose ps

# Logs
docker --context colima compose logs -f api

# Stop
docker --context colima compose down

# Rebuild after code changes
docker --context colima compose up -d --build
```

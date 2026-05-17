FROM python:3.11-slim

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Install system deps for psycopg2 and pdfplumber
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy source first (needed for package discovery)
COPY src/ ./src/

# Copy startup scripts (entrypoint for alembic migrations)
COPY startup/ ./startup/
RUN chmod +x startup/entrypoint.sh

# Copy alembic configuration
COPY alembic.ini ./
COPY alembic/ ./alembic/

# Install Python deps
COPY pyproject.toml uv.lock* ./
RUN uv sync --frozen --no-dev --no-editable

# Run API
CMD ["uvicorn", "keystone.main:app", "--host", "0.0.0.0", "--port", "8000"]

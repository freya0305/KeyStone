"""KeyStone FastAPI Application."""
import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from keystone.core import get_settings
from keystone.api import health, webhooks, jd_generator, job_seeker, b2b_onboarding

settings = get_settings()

# Structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer(),
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

app = FastAPI(
    title="KeyStone API",
    description="AI-powered Job Seeker + Recruiter JD Tool",
    version="0.1.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router)
app.include_router(webhooks.router)
app.include_router(jd_generator.router)
app.include_router(job_seeker.router)
app.include_router(b2b_onboarding.router)


@app.on_event("startup")
async def startup():
    logger.info("keystone_starting", app_name=settings.app_name, debug=settings.debug)


@app.on_event("shutdown")
async def shutdown():
    logger.info("keystone_shutting_down")

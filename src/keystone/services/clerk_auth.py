"""Clerk JWT authentication for KeyStone.

Verifies Clerk-issued JWTs and extracts user identity.
Supports both B2C (job seeker) and B2B (recruiter) users.

Uses PyJWT for JWT verification against Clerk's JWKS endpoint.
No external SDK dependency - uses standard JWT verification.
"""
import uuid
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

import structlog
import httpx
from jose import jwt
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from keystone.core import get_settings
from keystone.models.base import get_db
from sqlalchemy.ext.asyncio import AsyncSession

logger = structlog.get_logger()

# HTTP Bearer scheme for FastAPI
bearer_scheme = HTTPBearer(auto_error=True)


@dataclass
class AuthUser:
    """Authenticated user from Clerk JWT."""

    id: str  # Clerk user ID (clerk_xxx)
    job_seeker_id: Optional[uuid.UUID] = None  # Internal user ID (if B2C)
    b2b_user_id: Optional[uuid.UUID] = None  # Internal B2B user ID (if B2B)
    tenant_id: Optional[uuid.UUID] = None  # B2B tenant (if recruiter)
    access_level: Optional[str] = None  # "admin" or "member" (if B2B)

    @property
    def is_b2b(self) -> bool:
        return self.b2b_user_id is not None

    @property
    def is_b2c(self) -> bool:
        return self.job_seeker_id is not None


def _fetch_jwks_sync(clerk_secret_key: str) -> dict:
    """Synchronous JWKS fetch - runs in thread pool."""
    import httpx

    jwks_url = "https://api.clerk.dev/v1/jwks"
    with httpx.Client(timeout=10.0) as client:
        response = client.get(
            jwks_url,
            headers={"Authorization": f"Bearer {clerk_secret_key}"},
        )
        response.raise_for_status()
        return response.json()


def get_clerk_jwks_cached() -> dict:
    """Get cached JWKS dict - call this from async context with run_in_executor."""
    return _fetch_jwks_sync(get_settings().clerk_secret_key)


async def verify_clerk_token(token: str) -> dict:
    """Verify a Clerk JWT and return its payload.

    Uses Clerk's JWKS for verification.

    Args:
        token: The JWT string from Clerk

    Returns:
        Decoded JWT payload

    Raises:
        HTTPException: If token is invalid or expired
    """
    settings = get_settings()

    try:
        # Get the unverified header to find the key ID
        unverified_header = jwt.get_unverified_header(token)
        kid = unverified_header.get("kid")

        if not kid:
            raise HTTPException(status_code=401, detail="Invalid token header")

        # Get JWKS in thread pool to avoid blocking event loop
        import asyncio
        jwks = await asyncio.to_thread(get_clerk_jwks_cached)
        rsa_key = None

        for key in jwks.get("keys", []):
            if key.get("kid") == kid:
                rsa_key = jwt.algorithms.RSAAlgorithm.from_jwk(key)
                break

        if not rsa_key:
            raise HTTPException(status_code=401, detail="Token signing key not found")

        # Verify and decode the token
        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=["RS256"],
            audience=settings.clerk_publishable_key,
            issuer="https://clerk.dev/",
        )

        return payload

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError as e:
        logger.warning("clerk_token_invalid", error=str(e))
        raise HTTPException(status_code=401, detail="Invalid token")


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db),
) -> AuthUser:
    """Extract and verify user from Clerk JWT.

    Auto-provisions B2C users on first authentication.
    Looks up B2B user record if user is a recruiter.

    Use as a FastAPI dependency:
        @app.get("/protected")
        async def protected(user: AuthUser = Depends(get_current_user)):
            ...
    """
    from keystone.models.entities import User, B2BUser

    token = credentials.credentials

    try:
        payload = await verify_clerk_token(token)

        clerk_id = payload.get("sub")
        if not clerk_id:
            raise HTTPException(status_code=401, detail="No user_id in token")

        # Look up internal user ID by clerk_id
        result = await db.execute(select(User).where(User.clerk_id == clerk_id))
        user = result.scalar_one_or_none()

        # Auto-provision new B2C users
        if user is None:
            email = payload.get("email", f"{clerk_id}@clerk.dev")
            name = payload.get("name", email.split("@")[0])
            user = User(
                clerk_id=clerk_id,
                email=email,
                name=name,
            )
            db.add(user)
            await db.commit()
            await db.refresh(user)
            logger.info("auth.user_provisioned", clerk_id=clerk_id, user_id=str(user.id))

        job_seeker_id = user.id

        # Check if user is also a B2B user (recruiter)
        b2b_result = await db.execute(
            select(B2BUser).where(B2BUser.user_id == user.id)
        )
        b2b_user = b2b_result.scalar_one_or_none()

        if b2b_user:
            logger.debug("auth.user_verified", user_id=clerk_id, job_seeker_id=str(job_seeker_id), b2b_user_id=str(b2b_user.id), tenant_id=str(b2b_user.tenant_id))
            return AuthUser(
                id=clerk_id,
                job_seeker_id=job_seeker_id,
                b2b_user_id=b2b_user.id,
                tenant_id=b2b_user.tenant_id,
                access_level=b2b_user.access_level.value if b2b_user.access_level else None,
            )

        logger.debug("auth.user_verified", user_id=clerk_id, job_seeker_id=str(job_seeker_id))

        return AuthUser(id=clerk_id, job_seeker_id=job_seeker_id)

    except HTTPException:
        raise
    except Exception as e:
        logger.warning("auth.token_verification_failed", error=str(e))
        raise HTTPException(status_code=401, detail="Authentication failed")


async def get_current_b2b_user(
    user: AuthUser = Depends(get_current_user),
) -> AuthUser:
    """Get current user, requiring B2B (recruiter) access.

    Use for recruiter endpoints:
        @app.get("/recruiter/...")
        async def recruiter_only(user: AuthUser = Depends(get_current_b2b_user)):
            ...
    """
    if not user.is_b2b:
        raise HTTPException(
            status_code=403,
            detail="Recruiter access required"
        )
    return user


def require_tenant_access(tenant_id: uuid.UUID):
    """Dependency factory for tenant-scoped B2B access.

    Usage:
        async def endpoint(
            user: AuthUser = Depends(get_current_user),
            tenant = Depends(require_tenant_access(tenant_id_from_request))
        ):
            # user.tenant_id == tenant_id is verified
    """
    async def _check_tenant(user: AuthUser = Depends(get_current_user)) -> AuthUser:
        if user.tenant_id is None or user.tenant_id != tenant_id:
            raise HTTPException(
                status_code=403,
                detail="Access denied to this tenant"
            )
        return user
    return _check_tenant

"""SMS phone verification endpoints for anti-abuse.

Implements: M1-auth-pdpa.md § M1.3
- POST /api/auth/phone/send-otp — send 6-digit OTP to SG +65 number
- POST /api/auth/phone/verify — validate OTP and mark phone verified
"""
import asyncio
import hashlib
import random
import re
import time
from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
import redis
import structlog

from keystone.core import get_settings
from keystone.models.base import get_db
from keystone.services.consent import hash_phone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from keystone.models.entities import User
from keystone.services.clerk_auth import get_current_user, AuthUser

logger = structlog.get_logger()

router = APIRouter(prefix="/api/auth/phone", tags=["auth-phone"])

# OTP config
OTP_TTL_SECONDS = 600  # 10 minutes
OTP_MAX_ATTEMPTS = 3
OTP_LOCKOUT_SECONDS = 600  # 10 minute lockout after max attempts
OTP_LENGTH = 6

# SG phone pattern: +65 followed by 8 digits
SG_PHONE_PATTERN = re.compile(r"^\+65[89]\d{7}$")


def _get_redis() -> redis.Redis:
    settings = get_settings()
    return redis.from_url(settings.redis_url, decode_responses=True)


def _generate_otp() -> str:
    """Generate a cryptographically weak but human-readable 6-digit OTP."""
    return f"{random.randint(0, 999999):06d}"


def _validate_sg_phone(phone: str) -> bool:
    """Validate Singapore mobile number format."""
    return bool(SG_PHONE_PATTERN.match(phone.strip()))


class SendOtpRequest(BaseModel):
    phone: str  # +65XXXXXXXX


class SendOtpResponse(BaseModel):
    message: str


class VerifyOtpRequest(BaseModel):
    phone: str  # +65XXXXXXXX
    otp: str  # 6-digit code


class VerifyOtpResponse(BaseModel):
    verified: bool
    message: str


@router.post("/send-otp", response_model=SendOtpResponse)
async def send_otp(
    req: SendOtpRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: AuthUser = Depends(get_current_user),
):
    """Send OTP to a Singapore mobile number.

    Rate limited: 1 OTP per phone per 60 seconds.
    """
    phone = req.phone.strip()

    if not _validate_sg_phone(phone):
        raise HTTPException(
            status_code=400,
            detail="Invalid Singapore mobile number. Format: +65XXXXXXXX",
        )

    phone_hash = hash_phone(phone)
    r = _get_redis()

    # Rate limit: 1 OTP per 60 seconds per phone
    rate_key = f"otp:rate:{phone_hash}"
    if r.exists(rate_key):
        ttl = r.ttl(rate_key)
        raise HTTPException(
            status_code=429,
            detail=f"Too many requests. Try again in {ttl}s.",
        )

    # Check lockout
    lockout_key = f"otp:lockout:{phone_hash}"
    if r.exists(lockout_key):
        ttl = r.ttl(lockout_key)
        raise HTTPException(
            status_code=429,
            detail=f"Phone locked due to too many failed attempts. Try again in {ttl}s.",
        )

    # Generate and store OTP
    otp = _generate_otp()
    otp_key = f"otp:code:{phone_hash}"

    # Store OTP with 10-minute expiry
    r.setex(otp_key, OTP_TTL_SECONDS, otp)

    # Set rate limit key (1 per 60 seconds)
    r.setex(rate_key, 60, "1")

    # Send via Twilio (async to not block response)
    settings = get_settings()
    if settings.twilio_account_sid and settings.twilio_auth_token:
        try:
            await _send_twilio_sms(
                settings.twilio_account_sid,
                settings.twilio_auth_token,
                settings.twilio_phone_number,
                phone,
                f"Your KeyStone verification code is: {otp}",
            )
            logger.info("otp.sent", phone_hash=phone_hash[:8], user_id=str(current_user.job_seeker_id))
        except Exception as e:
            logger.error("otp.send_failed", phone_hash=phone_hash[:8], error=str(e))
            # Don't expose Twilio errors to client
    else:
        # Development mode: log OTP to console (NOT for production)
        logger.warning("otp.dev_mode", phone=phone, otp=otp)
        logger.info("otp.sent_dev", phone_hash=phone_hash[:8])

    return SendOtpResponse(message="OTP sent successfully")


@router.post("/verify", response_model=VerifyOtpResponse)
async def verify_otp(
    req: VerifyOtpRequest,
    db: AsyncSession = Depends(get_db),
    current_user: AuthUser = Depends(get_current_user),
):
    """Verify OTP and mark phone as verified on user record."""
    phone = req.phone.strip()
    otp = req.otp.strip()

    if not _validate_sg_phone(phone):
        raise HTTPException(status_code=400, detail="Invalid phone number format")

    if len(otp) != OTP_LENGTH or not otp.isdigit():
        raise HTTPException(status_code=400, detail="Invalid OTP format")

    phone_hash = hash_phone(phone)
    r = _get_redis()

    # Check lockout
    lockout_key = f"otp:lockout:{phone_hash}"
    if r.exists(lockout_key):
        raise HTTPException(
            status_code=429,
            detail="Phone locked due to too many failed attempts.",
        )

    # Get stored OTP
    otp_key = f"otp:code:{phone_hash}"
    stored_otp = r.get(otp_key)

    if not stored_otp:
        raise HTTPException(status_code=400, detail="OTP expired or not requested")

    # Check attempt count
    attempts_key = f"otp:attempts:{phone_hash}"
    attempts = int(r.get(attempts_key) or "0")

    # Constant-time comparison to prevent timing attacks
    if not _constant_time_compare(otp, stored_otp):
        attempts += 1
        r.setex(attempts_key, OTP_TTL_SECONDS, str(attempts))

        if attempts >= OTP_MAX_ATTEMPTS:
            r.setex(lockout_key, OTP_LOCKOUT_SECONDS, "1")
            r.delete(otp_key)
            r.delete(attempts_key)
            logger.warning("otp.locked", phone_hash=phone_hash[:8], attempts=attempts)
            raise HTTPException(
                status_code=429,
                detail="Too many failed attempts. Phone locked for 10 minutes.",
            )

        logger.warning("otp.wrong_attempt", phone_hash=phone_hash[:8], attempt=attempts)
        raise HTTPException(status_code=400, detail="Invalid OTP")

    # OTP correct — clear all OTP keys
    r.delete(otp_key)
    r.delete(attempts_key)

    # Check phone hash uniqueness (exclude current user)
    result = await db.execute(
        select(User).where(
            User.phone_hash == phone_hash,
            User.id != current_user.job_seeker_id,
        )
    )
    existing_user = result.scalar_one_or_none()
    if existing_user:
        logger.warning("otp.duplicate_phone", phone_hash=phone_hash[:8])
        raise HTTPException(
            status_code=409,
            detail="This phone number is linked to an existing account.",
        )

    # Update user record
    user_id = current_user.job_seeker_id
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user:
        user.phone_hash = phone_hash
        user.phone_verified = True
        user.phone_verified_at = datetime.utcnow()
        await db.commit()
        logger.info("otp.verified", user_id=str(user_id), phone_hash=phone_hash[:8])

    return VerifyOtpResponse(verified=True, message="Phone verified successfully")


def _constant_time_compare(a: str, b: str) -> bool:
    """Constant-time string comparison to prevent timing attacks."""
    if len(a) != len(b):
        return False
    result = 0
    for x, y in zip(a, b):
        result |= ord(x) ^ ord(y)
    return result == 0


async def _send_twilio_sms(account_sid: str, auth_token: str, from_: str, to: str, body: str) -> None:
    """Send SMS via Twilio REST API."""
    import httpx

    url = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json"
    data = {
        "To": to,
        "From": from_,
        "Body": body,
    }
    auth = (account_sid, auth_token)

    async with httpx.AsyncClient() as client:
        response = await client.post(url, data=data, auth=auth, timeout=10.0)
        if response.status_code not in (200, 201):
            logger.error(
                "twilio.send_failed",
                status=response.status_code,
                response=response.text[:200],
            )
            raise Exception(f"Twilio error: {response.status_code}")

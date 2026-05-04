"""S3 service for resume storage.

Handles uploading and retrieving resumes from S3 with proper bucket naming.
"""
from datetime import datetime
import boto3
from botocore.exceptions import ClientError
import structlog

from keystone.core import get_settings

logger = structlog.get_logger()


def get_s3_client():
    """Get configured S3 client."""
    settings = get_settings()
    return boto3.client(
        "s3",
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key,
        region_name=settings.aws_region,
    )


def get_resume_bucket() -> str:
    """Get the resume bucket name for the current environment.

    Bucket naming: keystone-resumes-{env}
    where env is 'dev', 'staging', or 'prod' (derived from app_name or explicit env var).
    """
    settings = get_settings()
    env = getattr(settings, "environment", "dev")
    return f"keystone-resumes-{env}"


async def upload_resume_to_s3(
    content: bytes,
    content_hash: str,
    user_id: str | None,
    filename: str,
    anon_session_id: str | None = None,
) -> str:
    """Upload resume content to S3.

    Args:
        content: Raw file bytes
        content_hash: SHA-256 hash of content for unique identification
        user_id: User ID if authenticated, None for anonymous
        filename: Original filename
        anon_session_id: Anonymous session ID if not authenticated

    Returns:
        S3 key where the file is stored

    Raises:
        Exception: If upload fails
    """
    settings = get_settings()
    bucket = get_resume_bucket()

    # Determine the S3 key path
    if user_id:
        s3_key = f"resumes/{user_id}/{content_hash}/{filename}"
    elif anon_session_id:
        s3_key = f"resumes/anonymous/{anon_session_id}/{content_hash}/{filename}"
    else:
        # Fallback to a hash-based path
        s3_key = f"resumes/anon/{content_hash}/{filename}"

    s3_client = get_s3_client()

    try:
        s3_client.put_object(
            Bucket=bucket,
            Key=s3_key,
            Body=content,
            ContentType=_get_content_type(filename),
            Metadata={
                "content-hash": content_hash,
                "original-filename": filename,
                "uploaded-at": datetime.utcnow().isoformat(),
            },
        )
        logger.info(
            "resume_uploaded_to_s3",
            bucket=bucket,
            key=s3_key,
            size_bytes=len(content),
            user_id=user_id[:8] if user_id else None,
            anon_session_id=anon_session_id[:8] if anon_session_id else None,
        )
        return s3_key
    except ClientError as e:
        logger.error("s3_upload_failed", bucket=bucket, key=s3_key, error=str(e))
        raise


def _get_content_type(filename: str) -> str:
    """Infer content type from filename extension."""
    ext = filename.lower().split(".")[-1]
    content_types = {
        "pdf": "application/pdf",
        "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "doc": "application/msword",
    }
    return content_types.get(ext, "application/octet-stream")


async def get_resume_from_s3(s3_key: str) -> bytes:
    """Retrieve resume content from S3.

    Args:
        s3_key: S3 object key

    Returns:
        Raw file bytes

    Raises:
        Exception: If download fails
    """
    bucket = get_resume_bucket()
    s3_client = get_s3_client()

    try:
        response = s3_client.get_object(Bucket=bucket, Key=s3_key)
        content = response["Body"].read()
        logger.info("resume_downloaded_from_s3", bucket=bucket, key=s3_key, size_bytes=len(content))
        return content
    except ClientError as e:
        logger.error("s3_download_failed", bucket=bucket, key=s3_key, error=str(e))
        raise

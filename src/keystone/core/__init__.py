"""Core configuration and settings."""
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # App
    app_name: str = "KeyStone"
    debug: bool = False

    # Database (no default - must be set in .env)
    database_url: str

    # Redis (no default - must be set in .env)
    redis_url: str

    # Claude AI
    anthropic_api_key: str
    anthropic_model_haiku: str = "claude-haiku-4-20250514"
    anthropic_model_sonnet: str = "claude-sonnet-4-20250514"
    anthropic_max_tokens_haiku: int = 4096  # Prevent overflow truncation

    # Stripe
    stripe_secret_key: str
    stripe_webhook_secret: str
    stripe_price_solo: str = "price_solo"
    stripe_price_pro: str = "price_pro"
    stripe_price_team: str = "price_team"

    # Auth
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 1440  # 24 hours

    # Clerk
    clerk_secret_key: str
    clerk_publishable_key: str = ""

    # AWS S3
    aws_access_key_id: str
    aws_secret_access_key: str
    s3_bucket: str
    aws_region: str = "ap-southeast-1"

    # Cost control
    llm_cost_ceiling_sgd: float = 5.0  # SGD 5/user/month
    llm_cost_warning_threshold: float = 0.8  # 80% before warning


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()

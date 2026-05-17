"""Core configuration and settings."""
from pydantic import model_validator
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
    stripe_price_pro_monthly: str = "price_pro_monthly"
    stripe_price_pro_annual: str = "price_pro_annual"
    # B2B Stripe price IDs
    stripe_price_b2b_basic: str = "price_b2b_basic"  # Agency Team: SGD 79/mo, 5 users, 100 JD/month
    stripe_price_b2b_pro: str = "price_b2b_pro"  # Agency Pro: SGD 199/mo, 10 users, 400 JD/month
    stripe_price_b2b_team: str = "price_b2b_team"  # Agency Enterprise: SGD 449/mo, unlimited users, unlimited JD

    # App
    app_base_url: str = "http://localhost:3000"
    app_cors_origins: str = ""  # Comma-separated list of allowed origins for production

    # Twilio (SMS OTP)
    twilio_account_sid: str = ""
    twilio_auth_token: str = ""
    twilio_phone_number: str = ""

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
    aws_endpoint_url: str | None = None  # For LocalStack/local development

    # Cost control
    llm_cost_ceiling_sgd: float = 5.0  # SGD 5/user/month
    llm_cost_warning_threshold: float = 0.8  # 80% before warning

    # Internal API (for admin/cron endpoints)
    internal_api_key: str = ""

    @model_validator(mode="after")
    def validate_production_security(self):
        """Ensure security-critical fields are set in production (debug=False)."""
        # Handle both bool False and string "false" from env var conversion
        is_production = self.debug is False or str(self.debug).lower() == "false"
        if is_production:
            if not self.internal_api_key:
                raise ValueError(
                    "internal_api_key must be set in production (debug=False). "
                    "Generate a secure key: python -c \"import secrets; print(secrets.token_urlsafe(32))\""
                )
            if not self.jwt_secret or len(self.jwt_secret) < 32:
                raise ValueError(
                    "jwt_secret must be set and at least 32 characters in production. "
                    "Current value length: " + str(len(self.jwt_secret) if self.jwt_secret else 0)
                )
            if not self.twilio_account_sid and not self.twilio_auth_token and not self.twilio_phone_number:
                raise ValueError(
                    "Twilio credentials are required for SMS OTP in production. "
                    "Set TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER."
                )
        return self


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Supabase
    supabase_url: str
    supabase_anon_key: str
    supabase_service_key: str
    supabase_jwt_secret: str

    # Stripe
    stripe_secret_key: str
    stripe_webhook_secret: str

    # Resend
    resend_api_key: str
    from_email: str = "noreply@sourcingelf.com"

    # App
    app_env: str = "development"
    app_url: str = "http://localhost:8000"
    frontend_url: str = "http://localhost:3000"

    # Credits pricing (USD)
    credits_single_price_usd: float = 138.00
    credits_triple_price_usd: float = 368.00
    credits_five_pack_price_usd: float = 498.00


settings = Settings()

from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Lokalize AI Translator"
    API_HOST: str = "0.0.0.0"
    API_PORT: str = "8000"

    # Security settings
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: str = "30"

    # CORS settings
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:5173"]
    ALLOWED_ORIGINS: str = "http://localhost:5173,http://localhost:80,http://localhost"

    # API Keys
    GEMINI_API_KEY: str | None = None
    LOKALISE_API_TOKEN: str | None = None

    # Environment
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"

    class Config:
        case_sensitive = True
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    """Get cached settings."""
    return Settings()


def validate_api_keys(settings: Settings) -> bool:
    """Validate that all required API keys are present."""
    missing_keys = []

    if not settings.GEMINI_API_KEY:
        missing_keys.append("GEMINI_API_KEY")
    if not settings.LOKALISE_API_TOKEN:
        missing_keys.append("LOKALISE_API_TOKEN")

    if missing_keys:
        if settings.ENVIRONMENT == "development":
            print("\n⚠️  Missing API Keys:")
            for key in missing_keys:
                value = input(f"Please enter your {key}: ").strip()
                if value:
                    setattr(settings, key, value)
                else:
                    print(f"❌ {key} is required!")
                    return False
            return True
        else:
            print("\n❌ Missing required API keys in production environment:")
            for key in missing_keys:
                print(f"  - {key}")
            return False

    return True

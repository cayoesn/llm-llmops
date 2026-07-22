from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configurações do Pipeline Industrial Unificado LLMOps."""
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    APP_NAME: str = "LLMOps Industrial Unified Gateway"
    ENV: str = "development"
    PORT: int = 8000

    # Cache Semântico
    SEMANTIC_CACHE_THRESHOLD: float = 0.88

    # Guardrails SLAs
    MAX_PROMPT_LENGTH: int = 2000

    # Langfuse Observability
    LANGFUSE_PUBLIC_KEY: str = "pk-lf-demo"
    LANGFUSE_SECRET_KEY: str = "sk-lf-demo"
    LANGFUSE_HOST: str = "http://localhost:3000"


settings = Settings()

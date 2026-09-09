from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    admin_username: str = "admin"
    admin_password_hash: str

    database_url: str = "sqlite:///./cc_admin.db"

    cors_allow_origins: str = ""

    llm_model_path: str = "models/qwen2.5-3b-instruct-q4_k_m.gguf"
    llm_n_ctx: int = 4096
    llm_n_threads: int = 4

    # Cloud tier (tier 3) for POST /api/v1/admin/generate -- used only when
    # the local tier is unavailable or explicitly requested. Empty key means
    # this tier is disabled; see app/core/llm.py.
    anthropic_api_key: str = ""
    cloud_llm_model: str = "claude-sonnet-5"

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_allow_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()

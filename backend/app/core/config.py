from functools import lru_cache

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    project_name: str = "Asterix Consultoria Imobiliaria API"
    environment: str = "development"
    database_url: str = "sqlite:///./asterix_local.db"
    jwt_secret_key: str = Field(min_length=32)
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    backend_cors_origins: str = "http://localhost:4200,http://127.0.0.1:4200"
    upload_dir: str = "uploads/imoveis"
    admin_name: str = "Administrador"
    admin_email: str = "admin@asterix.com.br"
    admin_password: str = Field(min_length=8)
    integration_token: str | None = None

    @model_validator(mode="after")
    def validate_production_secrets(self) -> "Settings":
        if self.environment.lower() == "production":
            forbidden = {"change-me-in-production", "local-development-secret", "change-me-in-local-dev"}
            if self.jwt_secret_key in forbidden:
                raise ValueError("JWT_SECRET_KEY insegura para producao")
            if self.admin_password in {"admin123", "change-me"}:
                raise ValueError("ADMIN_PASSWORD insegura para producao")
        return self

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.backend_cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

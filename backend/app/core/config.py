from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    project_name: str = "Asterix Consultoria Imobiliaria API"
    database_url: str = "postgresql+psycopg://asterix:asterix@localhost:5432/asterix"
    jwt_secret_key: str = Field(default="change-me-in-production")
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 120
    backend_cors_origins: str = "http://localhost:4200"
    upload_dir: str = "uploads/imoveis"
    admin_name: str = "Administrador"
    admin_email: str = "admin@asterix.com.br"
    admin_password: str = "admin123"

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.backend_cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()


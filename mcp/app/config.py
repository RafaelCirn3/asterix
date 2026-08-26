from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # MCP -> FastAPI. Credencial interna, nunca deve ser entregue ao cliente MCP.
    asterix_api_url: str = "http://backend:8000/api"
    integration_token: str

    # Cliente MCP -> MCP. Credencial independente da API interna.
    mcp_access_token: str

    # Host publico aceito pelo mecanismo anti-DNS-rebinding do SDK MCP.
    mcp_public_host: str = "mcp.asterixconsultoria.com.br"

    mcp_host: str = "0.0.0.0"
    mcp_port: int = 8000


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

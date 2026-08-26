from typing import Any

import httpx

from app.config import settings


class AsterixAPIError(RuntimeError):
    pass


class AsterixClient:
    def __init__(self) -> None:
        self.base_url = settings.asterix_api_url.rstrip("/")
        self.headers = {"Authorization": f"Bearer {settings.integration_token}"}

    async def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.request(
                    method,
                    f"{self.base_url}{path}",
                    headers=self.headers,
                    params=params,
                    json=json,
                )
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            detail = exc.response.text
            raise AsterixAPIError(
                f"Asterix API retornou HTTP {exc.response.status_code}: {detail}"
            ) from exc
        except httpx.HTTPError as exc:
            raise AsterixAPIError(f"Falha ao comunicar com a API do Asterix: {exc}") from exc

        return response.json()

    async def listar_imoveis(
        self,
        *,
        cidade: str | None = None,
        bairro: str | None = None,
        tipo: str | None = None,
        destacado: bool | None = None,
        preco_min: float | None = None,
        preco_max: float | None = None,
        busca: str | None = None,
        pagina: int = 1,
        tamanho: int = 20,
    ) -> dict[str, Any]:
        params = {
            "cidade": cidade,
            "bairro": bairro,
            "tipo": tipo,
            "destacado": destacado,
            "preco_min": preco_min,
            "preco_max": preco_max,
            "search": busca,
            "page": pagina,
            "size": tamanho,
        }
        return await self._request(
            "GET",
            "/integrations/imoveis",
            params={key: value for key, value in params.items() if value is not None},
        )

    async def ver_imovel(self, imovel_id: int) -> dict[str, Any]:
        return await self._request("GET", f"/integrations/imoveis/{imovel_id}")

    async def criar_imovel(self, payload: dict[str, Any]) -> dict[str, Any]:
        return await self._request("POST", "/integrations/imoveis", json=payload)

    async def editar_imovel(self, imovel_id: int, payload: dict[str, Any]) -> dict[str, Any]:
        return await self._request("PATCH", f"/integrations/imoveis/{imovel_id}", json=payload)


client = AsterixClient()

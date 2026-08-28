import hmac
from typing import Any, Literal

from mcp.server import MCPServer
from mcp.server.transport_security import TransportSecuritySettings

from app.client import client
from app.config import settings


class BearerAuthMiddleware:
    """ASGI middleware simples para proteger toda a entrada HTTP do servidor MCP."""

    def __init__(self, app: Any, token: str) -> None:
        self.app = app
        self.expected = f"Bearer {token}"

    async def __call__(self, scope: dict[str, Any], receive: Any, send: Any) -> None:
        if scope.get("type") != "http":
            await self.app(scope, receive, send)
            return

        headers = {key.lower(): value for key, value in scope.get("headers", [])}
        authorization = headers.get(b"authorization", b"").decode("utf-8")

        if not hmac.compare_digest(authorization, self.expected):
            body = b'{"detail":"MCP access token invalido"}'
            await send(
                {
                    "type": "http.response.start",
                    "status": 401,
                    "headers": [
                        (b"content-type", b"application/json"),
                        (b"content-length", str(len(body)).encode("ascii")),
                        (b"www-authenticate", b"Bearer"),
                    ],
                }
            )
            await send({"type": "http.response.body", "body": body})
            return

        await self.app(scope, receive, send)


mcp = MCPServer(
    "Asterix Imoveis",
    instructions=(
        "Ferramentas administrativas do Asterix para consultar, listar, criar e editar imoveis. "
        "Campos ausentes representam informacao nao fornecida. Em campos numericos, zero representa "
        "explicitamente que o imovel nao possui aquele item, enquanto null representa nao informado. "
        "O tipo de anuncio, quando informado, deve ser Aluguel ou Venda. O campo numero representa "
        "o WhatsApp do corretor responsavel pelo imovel. Nao ha ferramentas de exclusao neste servidor."
    ),
)


@mcp.tool()
async def listar_imoveis(
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
    """Lista imoveis do Asterix, opcionalmente filtrando por localizacao, tipo, destaque, preco ou nome."""
    return await client.listar_imoveis(
        cidade=cidade,
        bairro=bairro,
        tipo=tipo,
        destacado=destacado,
        preco_min=preco_min,
        preco_max=preco_max,
        busca=busca,
        pagina=pagina,
        tamanho=tamanho,
    )


@mcp.tool()
async def ver_imovel(imovel_id: int) -> dict[str, Any]:
    """Retorna todos os dados disponiveis de um imovel pelo ID, incluindo a galeria cadastrada."""
    return await client.ver_imovel(imovel_id)


@mcp.tool()
async def criar_imovel(
    nome: str,
    descricao_curta: str | None = None,
    descricao: str | None = None,
    preco: float | None = None,
    cidade: str | None = None,
    bairro: str | None = None,
    endereco: str | None = None,
    tipo: str | None = None,
    tipo_anuncio: Literal["Aluguel", "Venda"] | None = None,
    numero: str | None = None,
    area: int | None = None,
    quartos: int | None = None,
    banheiros: int | None = None,
    garagem: int | None = None,
    status: str = "Disponivel",
    destacado: bool = False,
) -> dict[str, Any]:
    """Cria um imovel. numero e o WhatsApp do corretor; tipo_anuncio aceita Aluguel ou Venda."""
    payload = {
        "nome": nome,
        "descricao_curta": descricao_curta,
        "descricao": descricao,
        "preco": preco,
        "cidade": cidade,
        "bairro": bairro,
        "endereco": endereco,
        "tipo": tipo,
        "tipo_anuncio": tipo_anuncio,
        "numero": numero,
        "area": area,
        "quartos": quartos,
        "banheiros": banheiros,
        "garagem": garagem,
        "status": status,
        "destacado": destacado,
    }
    return await client.criar_imovel(payload)


@mcp.tool()
async def editar_imovel(
    imovel_id: int,
    nome: str | None = None,
    descricao_curta: str | None = None,
    descricao: str | None = None,
    preco: float | None = None,
    cidade: str | None = None,
    bairro: str | None = None,
    endereco: str | None = None,
    tipo: str | None = None,
    tipo_anuncio: Literal["Aluguel", "Venda"] | None = None,
    numero: str | None = None,
    area: int | None = None,
    quartos: int | None = None,
    banheiros: int | None = None,
    garagem: int | None = None,
    status: str | None = None,
    destacado: bool | None = None,
) -> dict[str, Any]:
    """Edita somente os campos fornecidos de um imovel existente."""
    values = {
        "nome": nome,
        "descricao_curta": descricao_curta,
        "descricao": descricao,
        "preco": preco,
        "cidade": cidade,
        "bairro": bairro,
        "endereco": endereco,
        "tipo": tipo,
        "tipo_anuncio": tipo_anuncio,
        "numero": numero,
        "area": area,
        "quartos": quartos,
        "banheiros": banheiros,
        "garagem": garagem,
        "status": status,
        "destacado": destacado,
    }
    payload = {key: value for key, value in values.items() if value is not None}
    return await client.editar_imovel(imovel_id, payload)


transport_security = TransportSecuritySettings(
    allowed_hosts=[
        settings.mcp_public_host,
        f"{settings.mcp_public_host}:*",
        "127.0.0.1:*",
        "localhost:*",
    ],
    allowed_origins=[],
)

mcp_app = mcp.streamable_http_app(transport_security=transport_security)
app = BearerAuthMiddleware(mcp_app, settings.mcp_access_token)

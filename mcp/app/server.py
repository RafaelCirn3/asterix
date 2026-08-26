from typing import Any

from mcp.server import MCPServer

from app.client import client


mcp = MCPServer(
    "Asterix Imoveis",
    instructions=(
        "Ferramentas administrativas do Asterix para consultar, listar, criar e editar imoveis. "
        "Campos ausentes representam informacao nao fornecida. Em campos numericos, zero representa "
        "explicitamente que o imovel nao possui aquele item, enquanto null representa nao informado. "
        "Nao ha ferramentas de exclusao neste servidor."
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
    area: int | None = None,
    quartos: int | None = None,
    banheiros: int | None = None,
    garagem: int | None = None,
    status: str = "Disponivel",
    destacado: bool = False,
) -> dict[str, Any]:
    """Cria um imovel. Use null para informacao desconhecida e 0 quando souber que nao possui o item."""
    payload = {
        "nome": nome,
        "descricao_curta": descricao_curta,
        "descricao": descricao,
        "preco": preco,
        "cidade": cidade,
        "bairro": bairro,
        "endereco": endereco,
        "tipo": tipo,
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
        "area": area,
        "quartos": quartos,
        "banheiros": banheiros,
        "garagem": garagem,
        "status": status,
        "destacado": destacado,
    }
    payload = {key: value for key, value in values.items() if value is not None}
    return await client.editar_imovel(imovel_id, payload)


app = mcp.streamable_http_app()

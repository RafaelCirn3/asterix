from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy import select

from app.api.router import api_router
from app.core.config import settings
from app.core.security import get_password_hash
from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.models.imovel import Imovel
from app.models.usuario import Usuario
from app.services.files import ensure_upload_dir

app = FastAPI(title=settings.project_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ensure_upload_dir()
app.mount("/uploads/imoveis", StaticFiles(directory=Path(settings.upload_dir)), name="imoveis")
app.include_router(api_router)

DEMO_IMOVEIS = [
    {
        "nome": "Apartamento Vista Mar no Cabo Branco",
        "descricao_curta": "Apartamento ventilado com varanda gourmet e vista lateral para o mar.",
        "descricao": (
            "Planta inteligente, sala integrada, cozinha planejada e localizacao privilegiada "
            "a poucos metros da orla de Cabo Branco."
        ),
        "preco": 820000,
        "cidade": "Joao Pessoa",
        "bairro": "Cabo Branco",
        "endereco": "Av. Cabo Branco, 1820",
        "tipo": "Apartamento",
        "area": 94,
        "quartos": 3,
        "banheiros": 3,
        "garagem": 2,
        "status": "Disponivel",
    },
    {
        "nome": "Casa Familiar no Altiplano",
        "descricao_curta": "Casa ampla com jardim, suite master e area social integrada.",
        "descricao": (
            "Imovel ideal para familias que buscam conforto, seguranca e espacos generosos "
            "em um dos bairros mais valorizados de Joao Pessoa."
        ),
        "preco": 1380000,
        "cidade": "Joao Pessoa",
        "bairro": "Altiplano",
        "endereco": "Rua Bancario Sergio Guerra, 455",
        "tipo": "Casa",
        "area": 238,
        "quartos": 4,
        "banheiros": 5,
        "garagem": 4,
        "status": "Disponivel",
    },
    {
        "nome": "Studio Executivo em Tambau",
        "descricao_curta": "Studio mobiliado, compacto e pronto para morar ou investir.",
        "descricao": (
            "Localizacao estrategica perto da praia, de restaurantes, servicos essenciais "
            "e areas de lazer da cidade."
        ),
        "preco": 390000,
        "cidade": "Joao Pessoa",
        "bairro": "Tambau",
        "endereco": "Av. Almirante Tamandare, 612",
        "tipo": "Studio",
        "area": 39,
        "quartos": 1,
        "banheiros": 1,
        "garagem": 1,
        "status": "Disponivel",
    },
]

OLD_DEMO_NAMES = {
    "Apartamento Vista Parque",
    "Casa Jardim Privativo",
    "Studio Executivo",
}


@app.on_event("startup")
def startup() -> None:
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        admin = db.scalar(select(Usuario).where(Usuario.email == settings.admin_email))
        if admin is None:
            db.add(
                Usuario(
                    nome=settings.admin_name,
                    email=settings.admin_email,
                    senha_hash=get_password_hash(settings.admin_password),
                    ativo=True,
                )
            )
            db.commit()
        old_demo_items = db.scalars(select(Imovel).where(Imovel.nome.in_(OLD_DEMO_NAMES))).all()
        for item in old_demo_items:
            db.delete(item)

        for payload in DEMO_IMOVEIS:
            imovel = db.scalar(select(Imovel).where(Imovel.nome == payload["nome"]))
            if imovel is None:
                db.add(Imovel(**payload))
            else:
                for field, value in payload.items():
                    setattr(imovel, field, value)
        db.commit()


@app.get("/health", tags=["Sistema"])
def health() -> dict[str, str]:
    return {"status": "ok"}

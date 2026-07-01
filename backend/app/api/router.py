from fastapi import APIRouter

from app.api.routes import auth, contato, dashboard, imagens, imoveis, usuarios

api_router = APIRouter(prefix="/api")
api_router.include_router(auth.router)
api_router.include_router(imoveis.router)
api_router.include_router(imagens.router)
api_router.include_router(usuarios.router)
api_router.include_router(contato.router)
api_router.include_router(dashboard.router)


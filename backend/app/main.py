from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.router import api_router
from app.core.config import settings
from app.services.files import ensure_upload_dir

app = FastAPI(
    title=settings.project_name,
    docs_url="/api/docs" if settings.environment.lower() != "production" else None,
    openapi_url="/api/openapi.json" if settings.environment.lower() != "production" else None,
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

ensure_upload_dir()
app.mount("/uploads/imoveis", StaticFiles(directory=Path(settings.upload_dir)), name="imoveis")
app.include_router(api_router)


@app.get("/health", tags=["Sistema"])
def health() -> dict[str, str]:
    return {"status": "ok"}

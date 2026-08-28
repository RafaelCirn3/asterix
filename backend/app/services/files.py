from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from app.core.config import settings

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
MAX_IMAGE_SIZE_BYTES = 10 * 1024 * 1024
MAX_IMAGES_PER_PROPERTY = 20


def ensure_upload_dir() -> Path:
    upload_dir = Path(settings.upload_dir)
    upload_dir.mkdir(parents=True, exist_ok=True)
    return upload_dir


async def save_upload(file: UploadFile) -> str:
    extension = Path(file.filename or "").suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError("Formato de imagem invalido. Use JPG, JPEG, PNG ou WEBP")

    content = await file.read()
    if not content:
        raise ValueError("A imagem enviada esta vazia")
    if len(content) > MAX_IMAGE_SIZE_BYTES:
        raise ValueError("Cada imagem pode ter no maximo 10 MB")

    filename = f"{uuid4().hex}{extension}"
    destination = ensure_upload_dir() / filename
    destination.write_bytes(content)
    return filename


def delete_upload(filename: str) -> None:
    path = ensure_upload_dir() / filename
    if path.exists():
        path.unlink()

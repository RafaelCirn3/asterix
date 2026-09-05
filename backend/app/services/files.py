from io import BytesIO
from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile
from PIL import Image, UnidentifiedImageError

from app.core.config import settings

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
ALLOWED_FORMATS = {"JPEG", "PNG", "WEBP"}
MAX_IMAGE_SIZE_BYTES = 10 * 1024 * 1024
MAX_IMAGES_PER_PROPERTY = 20
READ_CHUNK_SIZE = 1024 * 1024


def ensure_upload_dir() -> Path:
    upload_dir = Path(settings.upload_dir)
    upload_dir.mkdir(parents=True, exist_ok=True)
    return upload_dir


async def _read_limited(file: UploadFile) -> bytes:
    chunks: list[bytes] = []
    total = 0
    while True:
        chunk = await file.read(READ_CHUNK_SIZE)
        if not chunk:
            break
        total += len(chunk)
        if total > MAX_IMAGE_SIZE_BYTES:
            raise ValueError("Cada imagem pode ter no maximo 10 MB")
        chunks.append(chunk)
    return b"".join(chunks)


def _validate_image_content(content: bytes) -> str:
    try:
        with Image.open(BytesIO(content)) as image:
            detected_format = image.format
            image.verify()
    except (UnidentifiedImageError, OSError, ValueError) as exc:
        raise ValueError("O arquivo enviado nao e uma imagem valida") from exc
    if detected_format not in ALLOWED_FORMATS:
        raise ValueError("Formato de imagem invalido. Use JPG, JPEG, PNG ou WEBP")
    return detected_format


async def save_upload(file: UploadFile) -> str:
    extension = Path(file.filename or "").suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError("Formato de imagem invalido. Use JPG, JPEG, PNG ou WEBP")

    content = await _read_limited(file)
    if not content:
        raise ValueError("A imagem enviada esta vazia")

    detected_format = _validate_image_content(content)
    expected_formats = {".jpg": "JPEG", ".jpeg": "JPEG", ".png": "PNG", ".webp": "WEBP"}
    if expected_formats[extension] != detected_format:
        raise ValueError("A extensao do arquivo nao corresponde ao conteudo da imagem")

    filename = f"{uuid4().hex}{extension}"
    destination = ensure_upload_dir() / filename
    destination.write_bytes(content)
    return filename


def delete_upload(filename: str) -> None:
    base_dir = ensure_upload_dir().resolve()
    path = (base_dir / Path(filename).name).resolve()
    if path.parent != base_dir:
        raise ValueError("Nome de arquivo invalido")
    if path.exists():
        path.unlink()

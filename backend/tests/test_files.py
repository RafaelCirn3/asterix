from io import BytesIO

import pytest
from fastapi import UploadFile
from PIL import Image

from app.services.files import save_upload


@pytest.mark.asyncio
async def test_rejects_fake_image_extension(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr("app.services.files.settings.upload_dir", str(tmp_path))
    upload = UploadFile(filename="fake.jpg", file=BytesIO(b"not-an-image"))
    with pytest.raises(ValueError):
        await save_upload(upload)


@pytest.mark.asyncio
async def test_accepts_valid_png(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr("app.services.files.settings.upload_dir", str(tmp_path))
    data = BytesIO()
    Image.new("RGB", (2, 2)).save(data, format="PNG")
    upload = UploadFile(filename="valid.png", file=BytesIO(data.getvalue()))
    filename = await save_upload(upload)
    assert (tmp_path / filename).exists()

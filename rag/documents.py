from pathlib import Path

from fastapi import UploadFile
from pypdf import PdfReader

from rag.config import UPLOAD_DIR


async def save_and_load(file: UploadFile) -> list[dict]:
    path = UPLOAD_DIR / Path(file.filename).name
    path.write_bytes(await file.read())

    suffix = path.suffix.lower()
    if suffix == ".pdf":
        return _load_pdf(path)
    if suffix in {".txt", ".md"}:
        return [{"text": path.read_text(encoding="utf-8"), "source": path.name}]
    raise ValueError("Only PDF, TXT, and Markdown files are supported.")


def _load_pdf(path: Path) -> list[dict]:
    reader = PdfReader(path)
    docs = []
    for index, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        if text.strip():
            docs.append({"text": text, "source": f"{path.name}, page {index}"})
    return docs


def split_text(text: str, size: int = 900, overlap: int = 150) -> list[str]:
    chunks = []
    start = 0
    while start < len(text):
        chunks.append(text[start : start + size])
        start += size - overlap
    return [chunk.strip() for chunk in chunks if chunk.strip()]


from typing import Dict, Optional

from fastapi import HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.extractors.file_extractors import (
    extract_text_from_csv,
    extract_text_from_doc,
    extract_text_from_docx,
    extract_text_from_pdf,
    extract_text_from_pptx,
    extract_text_from_txt,
)
from app.extractors.generate_text_title import generate_text_title
from app.extractors.models import TextOrm
from app.extractors.schemas import FileExtractor
from app.extractors.url_extractors import (
    extract_text_from_url_content,
    extract_text_from_url_pdf_content,
)
from app.extractors.utils import fetch_url, get_file_extension

FILE_EXTRACTORS: Dict[str, FileExtractor] = {
    ".doc": FileExtractor(extract_text_from_doc, "DOC"),
    ".docx": FileExtractor(extract_text_from_docx, "DOCX"),
    ".pptx": FileExtractor(extract_text_from_pptx, "PPTX"),
    ".pdf": FileExtractor(extract_text_from_pdf, "PDF"),
    ".txt": FileExtractor(extract_text_from_txt, "TXT"),
    ".csv": FileExtractor(extract_text_from_csv, "CSV"),
}

SUPPORTED_FILE_TYPES = ", ".join(extractor.file_type for extractor in FILE_EXTRACTORS.values())


async def extract_text_from_file(file: UploadFile) -> str:
    try:
        content = await file.read()

        extension = get_file_extension(file.filename)
        extractor = FILE_EXTRACTORS.get(extension)

        if extractor:
            text = extractor.fn(content, extension)
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Непідтримуваний формат файлу. Підтримуються: {SUPPORTED_FILE_TYPES}",
            )

        return text

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Помилка обробки файлу: {str(e)}")


async def extract_text_from_url(url: str) -> str:
    response = fetch_url(url)
    content_type = response.headers.get("Content-Type", "").lower()

    if "application/pdf" in content_type or url.lower().endswith(".pdf"):
        return extract_text_from_url_pdf_content(response.content)

    return extract_text_from_url_content(response.content)


async def get_or_save_text(session: AsyncSession, content: str, source_type: str) -> int:
    text_id = await get_text_id_by_content(session, content)

    if text_id is None:
        text_id = await save_text(session, content, source_type)

    return text_id


async def get_text_id_by_content(session: AsyncSession, content: str) -> Optional[int]:
    text_result = await session.execute(select(TextOrm).where(TextOrm.content == content))
    text_entity = text_result.scalar_one_or_none()

    if text_entity:
        return text_entity.id


async def save_text(session: AsyncSession, text: str, source_type: str, language: str = "uk") -> int:
    if not text or not text.strip():
        raise HTTPException(status_code=400, detail="Текст не може бути порожнім")

    title = await generate_text_title(text)

    text_entity = TextOrm(
        title=title,
        content=text,
        language=language,
        source_type=source_type,
    )

    session.add(text_entity)
    await session.commit()

    return text_entity.id

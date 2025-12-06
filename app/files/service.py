from typing import Dict

from fastapi import HTTPException, UploadFile

from app.files.extractors import (
    extract_text_from_csv,
    extract_text_from_doc,
    extract_text_from_docx,
    extract_text_from_pdf,
    extract_text_from_pptx,
    extract_text_from_txt,
)
from app.files.schemas import ExtractTextResponse, FileExtractor
from app.files.utils import get_file_extension

FILE_EXTRACTORS: Dict[str, FileExtractor] = {
    ".doc": FileExtractor(extract_text_from_doc, "DOC"),
    ".docx": FileExtractor(extract_text_from_docx, "DOCX"),
    ".pptx": FileExtractor(extract_text_from_pptx, "PPTX"),
    ".pdf": FileExtractor(extract_text_from_pdf, "PDF"),
    ".txt": FileExtractor(extract_text_from_txt, "TXT"),
    ".csv": FileExtractor(extract_text_from_csv, "CSV"),
}

SUPPORTED_FILE_TYPES = ", ".join(extractor.file_type for extractor in FILE_EXTRACTORS.values())


async def extract_text(file: UploadFile) -> ExtractTextResponse:
    try:
        content = await file.read()

        extension = get_file_extension(file.filename)
        extractor = FILE_EXTRACTORS.get(extension)

        if extractor:
            text = extractor.fn(content, extension)
        else:
            raise HTTPException(
                status_code=400, detail=f"Непідтримуваний формат файлу. Підтримуються: {SUPPORTED_FILE_TYPES}"
            )

        return ExtractTextResponse(filename=file.filename, text=text, char_count=len(text))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Помилка обробки файлу: {str(e)}")

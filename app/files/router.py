from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.files.schemas import ExtractTextResponse
from app.files.service import extract_text, get_text_id_by_content, save_text

router = APIRouter(prefix="/files", tags=["Файли 🗂️"])


@router.post("/upload", response_model=ExtractTextResponse, summary="Отримати текст з файлу")
async def upload_file(
    file: UploadFile,
    session: AsyncSession = Depends(get_session),
):
    text = await extract_text(file)
    text_id = await get_text_id_by_content(session, text)

    if text_id is None:
        text_id = await save_text(session, text, "upload")

    return ExtractTextResponse(text_id)

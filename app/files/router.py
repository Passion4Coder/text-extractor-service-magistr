from fastapi import APIRouter, UploadFile

from app.files.schemas import ExtractTextResponse
from app.files.service import extract_text

router = APIRouter(prefix="/files", tags=["Файли 🗂️"])


@router.post("/upload", response_model=ExtractTextResponse, summary="Отримати текст з файлу")
async def upload_file(file: UploadFile):
    response = await extract_text(file)

    return response

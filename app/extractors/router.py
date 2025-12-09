from typing import Annotated

from fastapi import APIRouter, Depends, Query, UploadFile
from pydantic import HttpUrl
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.extractors.schemas import ExtractTextResponse, ProcessInputRequest
from app.extractors.service import (
    extract_text_from_file,
    extract_text_from_url,
    get_or_save_text,
)

router = APIRouter(prefix="/extractors", tags=["Витягувачі тексту 📄"])


@router.post("/file", response_model=ExtractTextResponse, summary="Отримати текст з файлу")
async def process_file(
    file: UploadFile,
    session: AsyncSession = Depends(get_session),
):
    text = await extract_text_from_file(file)
    text_id = await get_or_save_text(session, text, "upload")

    return ExtractTextResponse(text_id)


@router.post("/url", response_model=ExtractTextResponse, summary="Отримати текст по посиланню")
async def process_url(
    url: Annotated[HttpUrl, Query()],
    session: AsyncSession = Depends(get_session),
):
    text = await extract_text_from_url(url.encoded_string())
    text_id = await get_or_save_text(session, text, "url")

    return ExtractTextResponse(text_id)


@router.post("/input", response_model=ExtractTextResponse, summary="Отримати текст з вводу користувача")
async def process_input(
    request: ProcessInputRequest,
    session: AsyncSession = Depends(get_session),
):
    text_id = await get_or_save_text(session, request.input, "input")

    return ExtractTextResponse(text_id)

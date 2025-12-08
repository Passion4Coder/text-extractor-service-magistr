from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class TextOrm(Base):
    __tablename__ = "texts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    language: Mapped[str] = mapped_column(String(10), default="uk")
    source_type: Mapped[str] = mapped_column(String(50), default="upload")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

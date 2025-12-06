from typing import Callable

from pydantic import BaseModel


class ExtractTextResponse(BaseModel):
    filename: str
    text: str
    char_count: int


class FileExtractor:
    fn: Callable[[bytes, str], str]
    file_type: str

    def __init__(self, fn: Callable[[bytes], str], file_type: str):
        self.fn = fn
        self.file_type = file_type

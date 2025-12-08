from typing import Callable

from pydantic import BaseModel


class ExtractTextResponse(BaseModel):
    text_id: int

    def __init__(self, text_id: int):
        super().__init__(text_id=text_id)


class FileExtractor:
    fn: Callable[[bytes, str], str]
    file_type: str

    def __init__(self, fn: Callable[[bytes], str], file_type: str):
        self.fn = fn
        self.file_type = file_type

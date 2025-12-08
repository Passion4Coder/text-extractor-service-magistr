import io
import re
from typing import Optional

import PyPDF2
from bs4 import BeautifulSoup

from app.extractors.utils import fetch_url_content


def extract_text_from_url_page(content: bytes) -> str:
    text = BeautifulSoup(content, "html.parser").get_text(separator="\n", strip=True)

    text = extract_text_from_pdf_js_viewer(text)

    return text


def extract_text_from_url_pdf(content: bytes) -> str:
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
    text = []

    for page in pdf_reader.pages:
        text.append(page.extract_text())

    return "\n".join(text)


def extract_text_from_pdf_js_viewer(raw_text: str) -> Optional[str]:
    match = re.search(r"\.getDocument\(['\"](.*?)['\"]\)", raw_text)

    if match:
        pdf_url = match.group(1)
        response = fetch_url_content(pdf_url)

        return extract_text_from_url_pdf(response.content)

    return raw_text

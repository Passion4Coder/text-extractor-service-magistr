import io
import re
from typing import List

import PyPDF2
from bs4 import BeautifulSoup

from app.extractors.utils import fetch_url


def extract_text_from_url_content(content: bytes) -> str:
    text = extract_text_from_html(content)
    text = extract_text_from_pdf_js_viewer(text)

    return text


def extract_text_from_url_pdf_content(content: bytes) -> str:
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
    text = []

    for page in pdf_reader.pages:
        text.append(page.extract_text())

    return "\n".join(text)


def extract_text_from_html(content: bytes) -> str:
    soup = BeautifulSoup(content, "html.parser")

    decompose_tags(soup, ["style", "noscript", "header", "nav", "footer"])
    text = soup.get_text(separator="\n", strip=True)

    decompose_tags(soup, "script")
    main_text = "\n".join([main.get_text(separator="\n", strip=True) for main in soup.find_all("main")])

    if main_text.strip():
        return main_text

    return text


def decompose_tags(soup: BeautifulSoup, name: str | List[str]) -> None:
    for tag in soup.find_all(name):
        tag.decompose()


def extract_text_from_pdf_js_viewer(raw_text: str) -> str:
    match = re.search(r"\.getDocument\(['\"](.*?)['\"]\)", raw_text)

    if match:
        pdf_url = match.group(1)
        response = fetch_url(pdf_url)

        return extract_text_from_url_pdf_content(response.content)

    return raw_text

import io
import tempfile

import docx
import pandas as pd
import PyPDF2
import textract


def textract_process(content: bytes, extension: str) -> str:
    with tempfile.NamedTemporaryFile(suffix=extension) as fp:
        fp.write(content)
        return textract.process(fp.name).decode()


def extract_text_from_doc(content: bytes, extension: str) -> str:
    return textract_process(content, extension)


def extract_text_from_docx(content: bytes, _: str) -> str:
    doc = docx.Document(io.BytesIO(content))
    text = []

    for paragraph in doc.paragraphs:
        text.append(paragraph.text)

    return "\n".join(text)


def extract_text_from_pptx(content: bytes, extension: str) -> str:
    return textract_process(content, extension)


def extract_text_from_pdf(content: bytes, _: str) -> str:
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
    text = []

    for page in pdf_reader.pages:
        text.append(page.extract_text())

    return "\n".join(text)


def extract_text_from_txt(content: bytes, _: str) -> str:
    try:
        return content.decode("utf-8")
    except UnicodeDecodeError:
        return content.decode("latin-1")


def extract_text_from_csv(content: bytes, _: str) -> str:
    df = pd.read_csv(io.BytesIO(content))

    return df.to_string()

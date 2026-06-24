import os
from pathlib import Path

from pypdf import PdfReader
from docx import Document as DocxDocument
from PIL import Image

from app.config import get_settings

settings = get_settings()

if settings.tesseract_cmd:
    import pytesseract
    pytesseract.pytesseract.tesseract_cmd = settings.tesseract_cmd


def extract_text_from_pdf(file_path: str) -> tuple[str, int, bool]:
    reader = PdfReader(file_path)
    pages_text = []
    ocr_needed = False

    for page_num, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        if len(text.strip()) < 50:
            ocr_needed = True
            text = _ocr_pdf_page(file_path, page_num) or text
        pages_text.append(text)

    return "\n\n".join(pages_text), len(reader.pages), ocr_needed


def _ocr_pdf_page(file_path: str, page_num: int) -> str:
    try:
        from pdf2image import convert_from_path
        import pytesseract

        images = convert_from_path(file_path, first_page=page_num, last_page=page_num, dpi=200)
        if images:
            return pytesseract.image_to_string(images[0])
    except Exception:
        pass
    return ""


def extract_text_from_docx(file_path: str) -> tuple[str, int, bool]:
    doc = DocxDocument(file_path)
    paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
    text = "\n\n".join(paragraphs)
    return text, max(1, len(paragraphs) // 20), False


def extract_text_from_image(file_path: str) -> tuple[str, int, bool]:
    try:
        import pytesseract
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image)
        return text, 1, True
    except Exception as e:
        return f"[OCR unavailable: {e}]", 1, True


def extract_document_text(file_path: str, file_type: str) -> tuple[str, int, bool]:
    ext = file_type.lower()
    if ext in ("pdf", ".pdf"):
        return extract_text_from_pdf(file_path)
    if ext in ("docx", ".docx"):
        return extract_text_from_docx(file_path)
    if ext in ("png", "jpg", "jpeg", "tiff", ".png", ".jpg", ".jpeg", ".tiff"):
        return extract_text_from_image(file_path)
    path = Path(file_path)
    if path.suffix.lower() == ".pdf":
        return extract_text_from_pdf(file_path)
    if path.suffix.lower() == ".docx":
        return extract_text_from_docx(file_path)
    if path.suffix.lower() in (".png", ".jpg", ".jpeg", ".tiff"):
        return extract_text_from_image(file_path)
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read(), 1, False

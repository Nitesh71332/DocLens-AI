from pathlib import Path

import pymupdf
from docx import Document
from docx.table import Table
from docx.text.paragraph import Paragraph
from rapidocr_onnxruntime import RapidOCR

ocr_engine = RapidOCR()


def extract_image_ocr(path):
    try:
        result, _ = ocr_engine(str(path))
    except Exception as e:
        raise ValueError(f"OCR failed: {e}")
    if not result:
        return ""
    lines = []
    for item in result:
        if len(item) >= 2 and item[1] and str(item[1]).strip():
            lines.append(str(item[1]).strip())
    return "\n".join(lines)


def extract_pdf(path):
    try:
        doc = pymupdf.open(path)
    except Exception as e:
        raise ValueError(f"Could not open PDF: {e}")

    if doc.is_encrypted and not doc.authenticate(""):
        doc.close()
        raise ValueError("Password-protected PDFs are not supported.")

    pages = []
    try:
        for page_number, page in enumerate(doc, start=1):
            text = page.get_text().strip()
            needs_ocr = len(text) < 20          # no text layer: treat as a scan

            if needs_ocr:
                pix = page.get_pixmap(matrix=pymupdf.Matrix(2, 2))
                image_path = Path(path).with_name(f"{Path(path).stem}_page_{page_number}.png")
                pix.save(image_path)
                try:
                    text = extract_image_ocr(image_path)
                finally:
                    image_path.unlink(missing_ok=True)

            pages.append({"page": page_number, "text": text, "needs_ocr": needs_ocr})
    finally:
        doc.close()
    return pages


def extract_docx(path):
    try:
        doc = Document(path)
    except Exception as e:
        raise ValueError(f"Could not open DOCX: {e}")

    blocks, section = [], None
    for item in doc.iter_inner_content():
        if isinstance(item, Paragraph):
            text = item.text.strip()
            if not text:
                continue
            style = (item.style.name or "").lower()
            if style.startswith("heading") or style == "title":
                section = text
            blocks.append({"type": "paragraph", "section": section, "text": text})
        elif isinstance(item, Table):
            for row in item.rows:
                cells = [cell.text.strip() for cell in row.cells]
                if any(cells):
                    blocks.append({"type": "table_row", "section": section,
                                   "text": " | ".join(cells)})

    text = "\n".join(block["text"] for block in blocks)
    return [{"page": 1, "text": text, "blocks": blocks}]


def extract_txt(path):
    raw = Path(path).read_bytes()
    if raw.startswith((b"\xff\xfe", b"\xfe\xff")):
        return [{"page": 1, "text": raw.decode("utf-16")}]
    for encoding in ("utf-8-sig", "cp1252", "latin-1"):
        try:
            return [{"page": 1, "text": raw.decode(encoding)}]
        except UnicodeDecodeError:
            continue
    raise ValueError("Could not decode text file.")


def extract_document(path):
    extension = Path(path).suffix.lower()
    if extension == ".pdf":
        return extract_pdf(path)
    if extension == ".docx":
        return extract_docx(path)
    if extension == ".txt":
        return extract_txt(path)
    if extension in {".png", ".jpg", ".jpeg"}:
        return [{"page": 1, "text": extract_image_ocr(path), "needs_ocr": True}]
    raise ValueError(f"Unsupported file type: {extension}")
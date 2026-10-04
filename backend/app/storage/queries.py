from app.storage.database import SessionLocal
from app.storage.models import Chunk, Document, Page


def load_chunks(document_pk=None):
    db = SessionLocal()
    try:
        query = (
            db.query(Chunk, Document, Page)
            .join(Document, Chunk.document_id == Document.id)
            .join(Page, Chunk.page_id == Page.id)
        )
        if document_pk is not None:
            query = query.filter(Chunk.document_id == document_pk)
        return [
            {
                "id": chunk.id,
                "text": chunk.text,
                "chunk_index": chunk.chunk_index,
                "section": chunk.section or "",
                "document_id": document.id,
                "page_id": page.id,
                "page_number": page.page_number,
                "filename": document.filename,
                "ocr_used": int(page.needs_ocr),
            }
            for chunk, document, page in query.order_by(Chunk.id).all()
        ]
    finally:
        db.close()
import hashlib
import uuid
from pathlib import Path

from fastapi import APIRouter, BackgroundTasks, File, HTTPException, UploadFile

from app.ingestion.chunker import chunk_page
from app.ingestion.claims import warm_claims
from app.ingestion.extractors import extract_document
from app.retrieval import bm25_store
from app.retrieval.indexer import index_document
from app.retrieval.vector_store import delete_document_chunks
from app.storage.database import SessionLocal
from app.storage.models import Chunk, Document, Page

router = APIRouter(prefix="/api/documents", tags=["Documents"])

UPLOAD_DIR = Path(__file__).resolve().parents[1] / "storage" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt", ".png", ".jpg", ".jpeg"}
MAX_SIZE = 20 * 1024 * 1024


def _purge(document_pk, doc_id):
    """Remove a document everywhere (database, vector index, file)."""
    db = SessionLocal()
    try:
        db.query(Chunk).filter(Chunk.document_id == document_pk).delete(synchronize_session=False)
        db.query(Page).filter(Page.document_id == document_pk).delete(synchronize_session=False)
        db.query(Document).filter(Document.id == document_pk).delete(synchronize_session=False)
        db.commit()
    finally:
        db.close()
    try:
        delete_document_chunks(document_pk)
    except Exception:
        pass
    bm25_store.invalidate()
    for f in UPLOAD_DIR.glob(f"{doc_id}_*"):
        f.unlink(missing_ok=True)


@router.post("/upload")
def upload_document(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    safe_name = Path(file.filename or "unnamed").name
    ext = Path(safe_name).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(400, "Unsupported file type. Use PDF, DOCX, TXT, PNG or JPG.")

    content = file.file.read()
    if not content:
        raise HTTPException(400, "The file is empty.")
    if len(content) > MAX_SIZE:
        raise HTTPException(413, "File too large (max 20 MB).")

    content_hash = hashlib.sha256(content).hexdigest()
    doc_id = uuid.uuid4().hex[:12]
    file_path = None
    pk = None

    db = SessionLocal()
    try:
        dup = db.query(Document).filter(Document.content_hash == content_hash).first()
        if dup:
            raise HTTPException(409, f"This file was already uploaded as '{dup.filename}'.")

        file_path = UPLOAD_DIR / f"{doc_id}_{safe_name}"
        file_path.write_bytes(content)

        try:
            pages = extract_document(file_path)
        except Exception as e:
            raise HTTPException(422, f"Could not read this file: {e}")

        document = Document(doc_id=doc_id, filename=safe_name, file_type=ext,
                            content_hash=content_hash)
        db.add(document)
        db.flush()

        n_chunks = 0
        for pd in pages:
            page = Page(document_id=document.id, page_number=pd["page"],
                        text=pd.get("text", ""), needs_ocr=1 if pd.get("needs_ocr") else 0)
            db.add(page)
            db.flush()
            for ch in chunk_page(pd.get("text", ""), pd["page"], blocks=pd.get("blocks")):
                db.add(Chunk(document_id=document.id, page_id=page.id, chunk_index=n_chunks,
                             section=ch.get("section"), text=ch["text"]))
                n_chunks += 1

        if n_chunks == 0:
            raise HTTPException(422, "No readable text was found (blank file, or OCR could not read it).")

        db.commit()
        pk = document.id
    except HTTPException:
        db.rollback()
        if file_path:
            file_path.unlink(missing_ok=True)
        raise
    except Exception as e:
        db.rollback()
        if file_path:
            file_path.unlink(missing_ok=True)
        raise HTTPException(500, f"Upload failed: {e}")
    finally:
        db.close()

    try:
        indexed = index_document(pk)
    except Exception as e:
        _purge(pk, doc_id)
        raise HTTPException(500, f"Indexing failed, document removed: {e}")

    bm25_store.invalidate()
    background_tasks.add_task(warm_claims, pk)     # extract facts in the background

    return {
        "doc_id": doc_id,
        "filename": safe_name,
        "pages": len(pages),
        "chunks": n_chunks,
        "indexed_chunks": indexed,
        "ocr_pages": sum(1 for p in pages if p.get("needs_ocr")),
        "status": "indexed",
    }


@router.get("")
def list_documents():
    db = SessionLocal()
    try:
        out = []
        for d in db.query(Document).order_by(Document.created_at.desc()).all():
            pages = db.query(Page).filter(Page.document_id == d.id).all()
            out.append({
                "doc_id": d.doc_id,
                "filename": d.filename,
                "file_type": d.file_type,
                "pages": len(pages),
                "ocr_pages": sum(p.needs_ocr for p in pages),
                "chunks": db.query(Chunk).filter(Chunk.document_id == d.id).count(),
                "created_at": d.created_at.isoformat(),
            })
        return {
            "documents": out,
            "totals": {"documents": len(out),
                       "pages": sum(x["pages"] for x in out),
                       "chunks": sum(x["chunks"] for x in out)},
        }
    finally:
        db.close()


@router.delete("/{doc_id}")
def delete_document(doc_id: str):
    db = SessionLocal()
    try:
        d = db.query(Document).filter(Document.doc_id == doc_id).first()
        if not d:
            raise HTTPException(404, "Document not found.")
        pk, filename = d.id, d.filename
    finally:
        db.close()
    _purge(pk, doc_id)
    return {"doc_id": doc_id, "filename": filename, "status": "deleted"}
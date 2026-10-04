from app.retrieval.vector_store import add_chunks, delete_chunks, indexed_ids
from app.storage.queries import load_chunks


def index_document(document_pk):
    chunks = load_chunks(document_pk)
    add_chunks(chunks)
    return len(chunks)


def index_all_chunks():
    chunks = load_chunks()
    add_chunks(chunks)
    return len(chunks)


def ensure_indexed():
    """Make the vector index match the database (adds missing, removes stale)."""
    chunks = load_chunks()
    db_ids = {str(c["id"]) for c in chunks}
    have = indexed_ids()
    missing = [c for c in chunks if str(c["id"]) not in have]
    if missing:
        add_chunks(missing)
    delete_chunks(list(have - db_ids))
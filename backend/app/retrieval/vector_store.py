from pathlib import Path

import chromadb
import numpy as np

from app.retrieval.embeddings import embed_query, embed_texts

CHROMA_DIR = Path(__file__).resolve().parents[1] / "storage" / "chroma"
CHROMA_DIR.mkdir(parents=True, exist_ok=True)

client = chromadb.PersistentClient(path=str(CHROMA_DIR))
collection = client.get_or_create_collection(
    name="doculens_chunks_v2",                 # new name: guarantees cosine distance
    metadata={"hnsw:space": "cosine"},
)


def _meta(c):
    return {
        "document_id": int(c["document_id"]),
        "page_id": int(c["page_id"]),
        "page_number": int(c["page_number"]),
        "filename": c["filename"],
        "section": c.get("section") or "",
        "chunk_index": int(c.get("chunk_index", 0)),
        "ocr_used": int(c.get("ocr_used", 0)),
    }


def add_chunks(chunks):
    if not chunks:
        return
    embeddings = [np.asarray(e).tolist() for e in embed_texts([c["text"] for c in chunks])]
    collection.upsert(
        ids=[str(c["id"]) for c in chunks],
        documents=[c["text"] for c in chunks],
        embeddings=embeddings,
        metadatas=[_meta(c) for c in chunks],
    )


def search_chunks(query, top_k=5):
    """-> list of chunk dicts with a true cosine 'vector_score' (0..1)."""
    total = collection.count()
    if total == 0:
        return []
    res = collection.query(
        query_embeddings=[np.asarray(embed_query(query)).tolist()],
        n_results=min(top_k, total),
    )
    return [
        {"id": int(cid), "text": text, **meta,
         "vector_score": max(0.0, 1.0 - float(dist))}
        for cid, text, meta, dist in zip(
            res["ids"][0], res["documents"][0], res["metadatas"][0], res["distances"][0]
        )
    ]


def similarities_for(ids, query):
    """Cosine similarity between the query and specific stored chunks."""
    if not ids:
        return {}
    got = collection.get(ids=[str(i) for i in ids], include=["embeddings"])
    q = np.asarray(embed_query(query), dtype=float)
    q = q / max(np.linalg.norm(q), 1e-12)
    out = {}
    embeddings = got.get("embeddings")
    if embeddings is None:
        return out
    for cid, emb in zip(got["ids"], embeddings):
        v = np.asarray(emb, dtype=float)
        out[int(cid)] = max(0.0, float(v @ q / max(np.linalg.norm(v), 1e-12)))
    return out


def indexed_ids():
    return set(collection.get(include=[])["ids"])


def delete_chunks(chunk_ids):
    if chunk_ids:
        collection.delete(ids=[str(i) for i in chunk_ids])


def delete_document_chunks(document_pk):
    collection.delete(where={"document_id": int(document_pk)})
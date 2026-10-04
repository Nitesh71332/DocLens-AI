from app.retrieval.bm25_store import bm25_search
from app.retrieval.vector_store import search_chunks, similarities_for

W_VECTOR, W_BM25 = 0.6, 0.4


def search_hybrid(query, top_k=5):
    pool = max(top_k * 4, 20)
    candidates = {c["id"]: c for c in search_chunks(query, pool)}

    bm_hits = bm25_search(query)
    bm_map = {c["id"]: c["bm25_score"] for c in bm_hits}

    # exact-match hits the vector search missed still get a true cosine score
    extra = [c for c in bm_hits[:pool] if c["id"] not in candidates]
    if extra:
        sims = similarities_for([c["id"] for c in extra], query)
        for c in extra:
            candidates[c["id"]] = {**c, "vector_score": sims.get(c["id"], 0.0)}

    for cid, c in candidates.items():
        c["bm25_score"] = bm_map.get(cid, 0.0)
        c["hybrid_score"] = W_VECTOR * c.get("vector_score", 0.0) + W_BM25 * c["bm25_score"]

    ranked = sorted(candidates.values(), key=lambda c: c["hybrid_score"], reverse=True)
    unique, seen = [], set()
    for c in ranked:
        key = (c["filename"], c["page_number"], c["text"].strip())
        if key in seen:
            continue
        seen.add(key)
        unique.append(c)
        if len(unique) >= top_k:
            break
    return unique
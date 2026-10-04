import re

from rank_bm25 import BM25Okapi

from app.storage.queries import load_chunks

STOPWORDS = {
    "a", "an", "the", "is", "are", "was", "were", "of", "to", "in", "on", "for", "and",
    "or", "what", "who", "how", "many", "much", "does", "do", "did", "s", "by", "with",
    "at", "be", "this", "that", "it", "as", "from",
}

_index = {"chunks": None, "model": None}


def tokenize(text):
    text = re.sub(r"(?<=\d),(?=\d)", "", text.lower())     # 8,40,000 -> 840000
    return [t for t in re.findall(r"\w+", text) if t not in STOPWORDS]


def invalidate():
    _index["chunks"] = None
    _index["model"] = None


def _get_index():
    if _index["chunks"] is None:
        chunks = load_chunks()
        corpus = [tokenize(c["text"]) for c in chunks]
        _index["chunks"] = chunks
        _index["model"] = BM25Okapi(corpus) if chunks and any(corpus) else None
    return _index["chunks"], _index["model"]


def bm25_search(query, top_k=None):
    """Only chunks that share a term with the query. Scores are scaled to 0..1."""
    chunks, model = _get_index()
    tokens = tokenize(query)
    if not model or not tokens:
        return []
    raw = model.get_scores(tokens)
    top = float(max(raw))
    if top <= 0:
        return []
    hits = [{**c, "bm25_score": float(s) / top} for c, s in zip(chunks, raw) if s > 0]
    hits.sort(key=lambda c: c["bm25_score"], reverse=True)
    return hits[:top_k] if top_k else hits
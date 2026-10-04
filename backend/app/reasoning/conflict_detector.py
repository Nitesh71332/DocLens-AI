"""Topic-free conflict detection.
Gemini extracts facts (cached) -> code checks quotes and normalises values -> local
embeddings group claims about the same thing -> Gemini confirms candidate groups ->
code resolves amendments and document dates. If Gemini is down, rule-based numeric
claims are used so the system degrades instead of failing."""
import hashlib
import json
import os
import re
from datetime import date
from itertools import combinations

import numpy as np

from app.reasoning.llm import generate_json
from app.retrieval.embeddings import embed_texts
from app.storage.queries import load_chunks

SIM_LLM = float(os.getenv("CLAIM_SIM", "0.75"))        # claims about the same fact (Gemini-read)
SIM_REGEX = float(os.getenv("CLAIM_SIM_REGEX", "0.85"))  # stricter for rule-based claims
Q_ABS_MIN = 0.50                                        # query time: claim must resemble the question
Q_MARGIN = 0.10
VERIFY_BATCH = 8

NUM_WORDS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7,
             "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12, "fifteen": 15,
             "twenty": 20, "thirty": 30, "sixty": 60, "ninety": 90}
DAYS = {"day": 1, "week": 7, "month": 30, "year": 365}
CUR = {"₹": "INR", "rs": "INR", "rs.": "INR", "inr": "INR", "$": "USD", "usd": "USD",
       "€": "EUR", "eur": "EUR", "£": "GBP", "gbp": "GBP"}
MULT = {"lakh": 1e5, "lakhs": 1e5, "crore": 1e7, "crores": 1e7, "million": 1e6, "k": 1e3}

_UNIT = r"(?:days?|weeks?|months?|years?|hours?)"
_WORD_RE = re.compile(r"\b(" + "|".join(NUM_WORDS) + r")\b(?=[\s-]+" + _UNIT + r"\b)", re.I)
_NUM = r"(?<![\w.,])(\d+(?:\.\d+)?)"
MONEY = re.compile(r"(?<![A-Za-z])(₹|rs\.?|inr|\$|usd|€|eur|£|gbp)\s*(\d[\d,]*(?:\.\d+)?)"
                   r"(?:\s*(lakhs?|crores?|million|k)\b)?", re.I)
DURATION = re.compile(_NUM + r"[\s-]*(day|week|month|year|hour)s?\b", re.I)
PERCENT = re.compile(_NUM + r"\s*(?:%|percent)", re.I)


# ------------------------------------------------------------ quantities
def extract_quantities(text):
    """Comparable quantities: 3 months -> 90 days, ₹8,40,000 -> 840000 INR."""
    s = _WORD_RE.sub(lambda m: str(NUM_WORDS[m.group(1).lower()]), text)
    spans, found = [], []

    def free(m):
        return not any(m.start() < e and m.end() > b for b, e in spans)

    def add(m, dim, value):
        spans.append((m.start(), m.end()))
        found.append({"dim": dim, "value": value, "display": m.group(0).strip(), "pos": m.start()})

    for m in MONEY.finditer(s):
        add(m, "money:" + CUR[m.group(1).lower()],
            float(m.group(2).replace(",", "")) * MULT.get((m.group(3) or "").lower(), 1))
    for m in DURATION.finditer(s):
        if not free(m):
            continue
        n, unit = float(m.group(1)), m.group(2).lower()
        add(m, "hours" if unit == "hour" else "duration", n if unit == "hour" else n * DAYS[unit])
    for m in PERCENT.finditer(s):
        if free(m):
            add(m, "percent", float(m.group(1)))

    found.sort(key=lambda q: q["pos"])
    # "revised from 18 days to 24 days": keep the new value and mark it as a revision
    if (len(found) >= 2 and found[-1]["dim"] == found[-2]["dim"]
            and re.search(r"\bfrom\b.+\bto\b", s, re.I)):
        found = found[:-2] + [{**found[-1], "revises": True}]
    return found, s


# ------------------------------------------------------------ dates (fallback only)
_MON = "jan feb mar apr may jun jul aug sep oct nov dec".split()
_MON_RE = r"(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*"


def _parse_date(t):
    try:
        m = re.search(r"\b(\d{4})-(\d{2})-(\d{2})\b", t)
        if m:
            return date(int(m[1]), int(m[2]), int(m[3]))
        m = re.search(r"\b(\d{1,2})(?:st|nd|rd|th)?\s+" + _MON_RE + r"\.?,?\s+(\d{4})\b", t, re.I)
        if m:
            return date(int(m[3]), _MON.index(m[2].lower()) + 1, int(m[1]))
        m = re.search(r"\b" + _MON_RE + r"\.?\s+(\d{1,2})(?:st|nd|rd|th)?,?\s+(\d{4})\b", t, re.I)
        if m:
            return date(int(m[3]), _MON.index(m[1].lower()) + 1, int(m[2]))
    except ValueError:
        pass
    return None


def find_document_date(text):
    m = re.search(r"(?:effective(?:\s+date)?|dated?|as of)\W{0,5}(.{0,40})", text, re.I)
    if m:
        d = _parse_date(m.group(1))
        if d:
            return d
    return _parse_date(text)


# ------------------------------------------------------------ claims
def _norm_value(v):
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]", "", str(v).lower())).strip()


def _regex_claims(chunks):
    """Fallback when no language model is available: numeric facts only."""
    out = []
    for c in chunks:
        section = c.get("section") or ""
        for sent in re.split(r"(?<=[.!?])\s+|\n+", c["text"]):
            sent = sent.strip()
            if len(sent) < 8:
                continue
            qs, norm = extract_quantities(sent)
            masked = re.sub(r"\d[\d,.]*", "#", norm)
            for q in qs:
                out.append({
                    "doc_pk": c["document_id"], "chunk_id": c["id"], "filename": c["filename"],
                    "page": c["page_number"], "section": section, "text": sent,
                    "context": f"{section}: {masked}" if section else masked,
                    "subject": "", "attribute": "", "origin": "regex",
                    "revises": bool(q.get("revises")), "display": q["display"],
                    "kind": "quantity", "dim": q["dim"], "value": q["value"],
                })
    return out


def build_claims(chunks):
    """-> (claims, {doc_pk: date}, all_documents_read_by_the_model)"""
    from app.ingestion.claims import extract_claims_for_document

    by_doc = {}
    for c in chunks:
        by_doc.setdefault(c["document_id"], []).append(c)

    claims, dates, all_llm = [], {}, True
    for pk, doc_chunks in by_doc.items():
        try:
            result = extract_claims_for_document(doc_chunks)
        except Exception:
            all_llm = False
            claims += _regex_claims(doc_chunks)
            continue
        try:
            dates[pk] = date.fromisoformat(result.get("document_date") or "")
        except (ValueError, TypeError):
            pass
        meta = {c["id"]: c for c in doc_chunks}
        for cl in result.get("claims", []):
            chunk = meta.get(cl.get("chunk_id"))
            value = str(cl.get("value", "")).strip()
            if not chunk or not value:
                continue
            subj = str(cl.get("subject", "")).strip()
            attr = str(cl.get("attribute", "")).strip()
            base = {
                "doc_pk": pk, "chunk_id": chunk["id"], "filename": chunk["filename"],
                "page": chunk["page_number"], "section": chunk.get("section") or "",
                "text": cl["quote"], "subject": subj, "attribute": attr, "origin": "llm",
                "context": (f"{attr} of {subj}" if subj else attr) or value,
                "revises": bool(cl.get("revises_earlier_value")), "display": value,
            }
            qs, _ = extract_quantities(value)
            if qs:
                claims.append({**base, "kind": "quantity", "dim": qs[0]["dim"], "value": qs[0]["value"]})
            else:
                claims.append({**base, "kind": "text", "value": _norm_value(value)})
    return claims, dates, all_llm


# ------------------------------------------------------------ grouping
_EMB = {}


def _embed(texts):
    if not texts:
        return np.empty((0, 0))
    if len(_EMB) > 5000:
        _EMB.clear()
    missing = [t for t in dict.fromkeys(texts) if t not in _EMB]
    if missing:
        vecs = np.array([np.asarray(e, dtype=float) for e in embed_texts(missing)])
        vecs = vecs / np.maximum(np.linalg.norm(vecs, axis=1, keepdims=True), 1e-12)
        for t, v in zip(missing, vecs):
            _EMB[t] = v
    return np.array([_EMB[t] for t in texts])


def _same(a, b):
    return abs(a - b) <= 1e-6 * max(1.0, abs(a), abs(b))


def _cluster(pairs):
    parent = {}

    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for i, j in pairs:
        parent[find(i)] = find(j)
    groups = {}
    for x in list(parent):
        groups.setdefault(find(x), set()).add(x)
    return list(groups.values())


def _make_group(members, sim, doc_dates):
    positions = {}
    for m in members:
        key = (m["kind"], m.get("dim"),
               round(m["value"], 6) if m["kind"] == "quantity" else m["value"])
        pos = positions.setdefault(key, {"value": m["display"], "sources": []})
        src = {"filename": m["filename"], "page": m["page"], "section": m["section"],
               "chunk_id": m["chunk_id"], "text": m["text"], "revises": m["revises"]}
        if src not in pos["sources"]:
            pos["sources"].append(src)

    resolution = None
    revs = [m for m in members if m["revises"]]
    if revs:
        r = revs[-1]
        resolution = {"type": "amendment", "current_value": r["display"], "source": r["filename"],
                      "note": f"{r['filename']} states that it revises the earlier value, so the "
                              f"current value appears to be {r['display']}."}
    else:
        per_doc = {m["doc_pk"]: (doc_dates.get(m["doc_pk"]), m) for m in members}
        if len(per_doc) >= 2 and all(d for d, _ in per_doc.values()):
            ordered = sorted(per_doc.values(), key=lambda x: x[0])
            if ordered[-1][0] > ordered[-2][0]:
                d, m = ordered[-1]
                resolution = {"type": "newer_document", "current_value": m["display"],
                              "source": m["filename"],
                              "note": f"{m['filename']} is the newest document ({d.isoformat()}) "
                                      f"and may supersede the others. This is not confirmed."}

    first = members[0]
    topic = ((first["attribute"] + (f" ({first['subject']})" if first["subject"] else "")).strip()
             or first["section"] or first["context"][:70])
    numeric = all(m["kind"] == "quantity" and m.get("dim") == first.get("dim") for m in members)
    return {
        "topic": topic, "kind": "numeric" if numeric else "text", "status": "possible",
        "verified": False, "reason": "", "positions": list(positions.values()),
        "resolution": resolution, "sim": round(sim, 3),
        "relevance": round(max(m.get("qsim", 0.0) for m in members), 3),
        "_members": members, "_has_revision": bool(revs),
    }


# ------------------------------------------------------------ model verification
VERIFY_PROMPT = """Each item lists statements from different documents.
For each item decide:
1. same_fact: do all statements describe the same attribute of the same subject?
   (annual leave and sick leave are different facts; Pune office and Delhi office are different subjects)
2. contradict: if they are the same fact, do the values differ so that they cannot all be
   currently true? An explicit amendment that revises an earlier value counts as true.
   The same value written differently (30 days vs one month) is false.
Return JSON: {"results":[{"id":<int>,"same_fact":true|false,"contradict":true|false,"reason":"short"}]}
Items:
"""
_VCACHE = {}


def _statements(members, doc_dates):
    seen, out = set(), []
    for m in members:
        k = (m["filename"], m["text"])
        if k in seen:
            continue
        seen.add(k)
        d = doc_dates.get(m["doc_pk"])
        out.append({"document": m["filename"], "document_date": d.isoformat() if d else None,
                    "subject": m["subject"], "attribute": m["attribute"],
                    "value": m["display"], "quote": m["text"]})
    return out


def verify_groups(groups, doc_dates):
    """-> (groups, llm_ok). Drops groups the model says are not real conflicts."""
    if not groups:
        return groups, True

    keyed = []
    for g in groups:
        st = _statements(g["_members"], doc_dates)
        keyed.append((g, st, hashlib.sha256(json.dumps(st, sort_keys=True).encode()).hexdigest()))

    llm_ok = True
    todo = [x for x in keyed if x[2] not in _VCACHE]
    for start in range(0, len(todo), VERIFY_BATCH):
        part = todo[start:start + VERIFY_BATCH]
        items = [{"id": n, "statements": st} for n, (_, st, _) in enumerate(part)]
        try:
            res = generate_json(VERIFY_PROMPT + json.dumps(items, ensure_ascii=False))
        except Exception:
            llm_ok = False
            break
        for r in res.get("results", []):
            try:
                k = part[int(r["id"])][2]
            except (KeyError, ValueError, IndexError, TypeError):
                continue
            _VCACHE[k] = {"same": bool(r.get("same_fact")),
                          "contradict": bool(r.get("contradict")),
                          "reason": str(r.get("reason", ""))}

    out = []
    for g, _, k in keyed:
        v = _VCACHE.get(k)
        if v:
            if v["same"] and (v["contradict"] or g["_has_revision"]):
                out.append({**g, "status": "detected", "verified": True, "reason": v["reason"]})
            continue                       # the model says this is not a real conflict
        if g["kind"] == "numeric" and g["sim"] >= SIM_REGEX:
            out.append({**g, "status": "detected",
                        "reason": "Detected by rules; the language model could not confirm it."})
        else:
            out.append({**g, "status": "possible",
                        "reason": "Possible conflict; not verified by the language model."})
    return out, llm_ok


# ------------------------------------------------------------ entry points
def _result(claims, groups, all_llm):
    detected = [g for g in groups if g["status"] == "detected"]
    return {
        "has_conflict": bool(detected),
        "has_possible": any(g["status"] == "possible" for g in groups),
        "topic": detected[0]["topic"] if detected else None,
        "claims_extracted": len(claims),
        "groups": groups,
        "resolution": next((g["resolution"] for g in detected if g["resolution"]), None),
        "llm_verified": all_llm and all(g.get("verified") for g in groups),
    }


def analyse(question=None):
    chunks = load_chunks()
    if not chunks:
        return _result([], [], True)

    claims, doc_dates, all_llm = build_claims(chunks)

    by_doc = {}
    for c in chunks:
        by_doc.setdefault(c["document_id"], []).append(c["text"])
    for pk, texts in by_doc.items():
        if pk not in doc_dates:
            d = find_document_date(" ".join(texts))
            if d:
                doc_dates[pk] = d

    if len(claims) < 2:
        return _result(claims, [], all_llm)

    if question:      # keep only claims that are about what was asked
        sims_q = _embed([c["text"] for c in claims]) @ _embed([question])[0]
        cutoff = max(Q_ABS_MIN, float(sims_q.max()) - Q_MARGIN)
        for c, s in zip(claims, sims_q):
            c["qsim"] = float(s)
        claims = [c for c in claims if c["qsim"] >= cutoff]
        if len(claims) < 2:
            return _result(claims, [], all_llm)

    ctx = _embed([c["context"] for c in claims])
    sims = ctx @ ctx.T

    pair_sim = {}
    for i, j in combinations(range(len(claims)), 2):
        a, b = claims[i], claims[j]
        thr = SIM_LLM if a["origin"] == b["origin"] == "llm" else SIM_REGEX
        if a["doc_pk"] == b["doc_pk"] or sims[i, j] < thr:
            continue
        if a["kind"] == b["kind"] == "quantity" and a["dim"] == b["dim"] and _same(a["value"], b["value"]):
            continue
        if a["kind"] == b["kind"] == "text" and a["value"] == b["value"]:
            continue
        pair_sim[(i, j)] = float(sims[i, j])      # a number vs a phrase: the model decides

    groups = []
    for idx in _cluster(list(pair_sim)):
        s = [v for (i, j), v in pair_sim.items() if i in idx]
        groups.append(_make_group([claims[i] for i in sorted(idx)], sum(s) / len(s), doc_dates))

    groups, llm_ok = verify_groups(groups, doc_dates)
    for g in groups:
        g.pop("_members", None)
        g.pop("_has_revision", None)
    groups.sort(key=lambda g: g["relevance"], reverse=True)
    return _result(claims, groups, all_llm and llm_ok)


def detect_conflicts(question, evidence=None):
    """Query time. Looks at every document's claims, not only the retrieved chunks."""
    return analyse(question)


_SCAN = {"sig": None, "result": None}


def scan_all_conflicts():
    """Scan for the Conflict Center. Cached until the documents change."""
    sig = tuple(sorted(c["id"] for c in load_chunks()))
    if _SCAN["sig"] == sig and _SCAN["result"] is not None:
        return _SCAN["result"]
    result = analyse(None)
    if result["llm_verified"]:                # never cache a degraded (model-down) result
        _SCAN["sig"], _SCAN["result"] = sig, result
    return result
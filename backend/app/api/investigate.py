import os
import re

from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.reasoning.conflict_detector import detect_conflicts
from app.reasoning.llm import ask_gemini
from app.retrieval.hybrid import search_hybrid

router = APIRouter(prefix="/api/investigate", tags=["Investigation"])

# Calibrate with calibrate.py, then set MIN_VECTOR_SIM in .env
MIN_VECTOR_SIM = float(os.getenv("MIN_VECTOR_SIM", "0.55"))

EMPTY_CONFLICT = {"has_conflict": False, "has_possible": False, "topic": None,
                  "claims_extracted": 0, "groups": [], "resolution": None, "llm_verified": False}


class InvestigationRequest(BaseModel):
    question: str = Field(max_length=1000)


def _tok(text):
    """Punctuation- and whitespace-insensitive form for quote checking."""
    return " " + " ".join(re.findall(r"[\w₹$€£%]+", str(text).lower())) + " "


def _clip(x):
    return max(0.0, min(1.0, x))


def strength_label(score):
    if score >= 80:
        return "STRONG"
    if score >= 50:
        return "MODERATE"
    return "WEAK" if score > 0 else "NONE"


# ---------------------------------------------------------------- citation verifier
def verify_citations(result, evidence):
    """A citation counts only if its quote really appears in the cited chunk."""
    by_id = {int(i["id"]): i for i in evidence}
    returned = result.get("citations")
    returned = returned if isinstance(returned, list) else []
    verified, seen = [], set()
    for c in returned:
        if not isinstance(c, dict):
            continue
        try:
            cid = int(c.get("chunk_id"))
        except (TypeError, ValueError):
            continue
        quote = str(c.get("quote", "")).strip()
        item = by_id.get(cid)
        if not item or len(quote) < 8 or (cid, _tok(quote)) in seen:
            continue
        if _tok(quote) in _tok(item["text"]):
            seen.add((cid, _tok(quote)))
            verified.append({"chunk_id": cid, "filename": item["filename"],
                             "page_number": item["page_number"],
                             "section": item.get("section", ""), "quote": quote})
    return verified, len(returned)


# ---------------------------------------------------------------- evidence strength
def answer_strength(verified, returned, evidence):
    """How well verified quotes support the answer (0-100). A heuristic, not a probability."""
    by_id = {i["id"]: i for i in evidence}
    cited = [by_id[c["chunk_id"]] for c in verified if c["chunk_id"] in by_id]
    if not cited:
        return 0
    rel = _clip((sum(i.get("vector_score", 0) for i in cited) / len(cited) - 0.5) / 0.35)
    docs = min(len({c["filename"] for c in verified}), 3)
    src = (docs - 1) / 2                      # 1 document 0.0, 2 -> 0.5, 3+ -> 1.0
    ver = len(verified) / max(returned, 1)
    score = 100 * (0.40 * rel + 0.30 * src + 0.30 * ver)
    if any(i.get("ocr_used") for i in cited):
        score -= 10                           # OCR text can contain misreads
    return int(round(max(0, min(100, score))))


def conflict_strength(groups):
    docs = min(len({s["filename"] for g in groups for p in g["positions"] for s in p["sources"]}), 3)
    llm = all(g.get("verified") for g in groups)
    return int(round(30 + 30 * (docs - 1) / 2 + 40 * (1.0 if llm else 0.4)))


# ---------------------------------------------------------------- conflict helpers
def _group_chunk_ids(g):
    return {s["chunk_id"] for p in g["positions"] for s in p["sources"]}


def _filter_conflict(conflict, ids):
    """Keep only conflicts that involve the passages relevant to this question."""
    groups = [g for g in conflict["groups"] if _group_chunk_ids(g) & ids]
    detected = [g for g in groups if g["status"] == "detected"]
    return {**conflict, "groups": groups, "has_conflict": bool(detected),
            "has_possible": any(g["status"] == "possible" for g in groups),
            "topic": detected[0]["topic"] if detected else None,
            "resolution": next((g["resolution"] for g in detected if g["resolution"]), None)}


def conflict_answer(groups):
    """Built in code from the quoted sources, so the model never picks a side."""
    parts, cites, seen = [], [], set()
    for g in groups[:3]:
        sides = []
        for p in g["positions"]:
            where = "; ".join(f"{s['filename']} (p.{s['page']})" for s in p["sources"])
            sides.append(f"{p['value']} per {where}")
            for s in p["sources"]:
                if (s["filename"], s["text"]) in seen:
                    continue
                seen.add((s["filename"], s["text"]))
                cites.append({"chunk_id": s["chunk_id"], "filename": s["filename"],
                              "page_number": s["page"], "section": s["section"],
                              "quote": s["text"]})
        line = f"The documents give different values for {g['topic']}: " + " vs ".join(sides) + "."
        line += " " + (g["resolution"]["note"] if g["resolution"]
                       else "The documents do not show which value is authoritative.")
        parts.append(line)
    return " ".join(parts), cites


def build_response(answer, verdict, reason, score, citations, evidence, conflict, trace,
                   unverified_answer=None):
    return {
        "answer": answer,
        "verdict": verdict,
        "reason": reason,
        "evidence_score": score,
        "evidence_strength": strength_label(score),
        "citations": citations,
        "unverified_answer": unverified_answer,
        "evidence": [{
            "chunk_id": i["id"], "filename": i["filename"], "page_number": i["page_number"],
            "section": i.get("section", ""), "text": i["text"],
            "ocr_used": bool(i.get("ocr_used")),
            "vector_score": round(i.get("vector_score", 0), 4),
            "hybrid_score": round(i.get("hybrid_score", 0), 4),
        } for i in evidence],
        "conflict": conflict,
        "trace": trace,
    }


@router.post("")
def investigate(request: InvestigationRequest):
    question = request.question.strip()
    trace = []

    if not question:
        return build_response("", "NOT_FOUND", "No question was provided.", 0, [], [],
                              EMPTY_CONFLICT, trace)

    retrieved = search_hybrid(question, top_k=8)
    evidence = [i for i in retrieved if i.get("vector_score", 0) >= MIN_VECTOR_SIM]
    trace.append(f"Retrieved {len(retrieved)} passages; {len(evidence)} passed the relevance gate")

    if not evidence:
        return build_response(
            "I could not find relevant evidence in the uploaded documents. I won't guess.",
            "NOT_FOUND", "No passage was similar enough to the question.", 0, [], [],
            EMPTY_CONFLICT, trace)

    used = evidence[:6]
    result = ask_gemini(question, used)

    if result is not None and not result.get("answerable", False):
        trace.append("Model reported that the excerpts do not contain the answer")
        return build_response(
            str(result.get("answer") or "The documents do not contain this information.")
            + " I won't guess.",
            "NOT_FOUND", str(result.get("reason", "")), 0, [], used, EMPTY_CONFLICT, trace)

    # which passages are relevant to the answer (used to keep unrelated conflicts out)
    used_ids = {i["id"] for i in used}
    cited = set()
    if result:
        for c in result.get("citations") or []:
            try:
                cited.add(int(c.get("chunk_id")))
            except (TypeError, ValueError, AttributeError):
                pass
    relevant_ids = (cited & used_ids) or {i["id"] for i in used[:3]}

    try:
        conflict = _filter_conflict(detect_conflicts(question), relevant_ids)
    except Exception as e:
        conflict = EMPTY_CONFLICT
        trace.append(f"Conflict analysis failed: {type(e).__name__}")

    detected = [g for g in conflict["groups"] if g["status"] == "detected"]
    trace.append(f"Conflict analysis: {len(detected)} confirmed, "
                 f"{len(conflict['groups']) - len(detected)} unverified")

    # ---- the documents disagree
    if detected:
        answer, cites = conflict_answer(detected)
        resolutions = [(g.get("resolution") or {}).get("type") for g in detected]
        if "amendment" in resolutions:
            verdict = "SUPERSEDED"
            reason = ("Sources disagree, but an explicit amendment indicates which value is "
                      "current. Both sources are shown.")
        elif "newer_document" in resolutions:
            verdict = "CONFLICT"
            reason = ("Sources disagree. A newer document exists, but it does not say that it "
                      "replaces the older value.")
        else:
            verdict = "CONFLICT"
            reason = "Sources disagree and the documents do not show which value is authoritative."
        trace.append(f"Verdict {verdict} from {len(cites)} quoted sources")
        return build_response(answer, verdict, reason, conflict_strength(detected),
                              cites, used, conflict, trace)

    # ---- no conflict
    if result is None:
        trace.append("Language model unavailable")
        return build_response(
            "The language model is unavailable, so I cannot produce a verified answer. "
            "The most relevant passages are shown below.",
            "UNCERTAIN", "No verified answer could be produced.", 0, [], used, conflict, trace)

    verified, returned = verify_citations(result, used)
    trace.append(f"Citations verified: {len(verified)} of {returned}")

    if not verified:
        return build_response(
            "I could not verify this answer against the source text, so I am not presenting "
            "it as fact. The closest passages are shown below.",
            "UNCERTAIN", "No quoted passage could be matched to the documents.", 0, [], used,
            conflict, trace, unverified_answer=result.get("answer"))

    score = answer_strength(verified, returned, used)
    verdict = "CONFIRMED" if score >= 50 else "UNCERTAIN"
    reason = str(result.get("reason", ""))
    if conflict["has_possible"]:
        verdict = "UNCERTAIN"
        reason += " A possible conflict with another document could not be verified."
    trace.append(f"Evidence strength {score}/100 -> {verdict}")
    return build_response(str(result.get("answer", "")), verdict, reason, score,
                          verified, used, conflict, trace)
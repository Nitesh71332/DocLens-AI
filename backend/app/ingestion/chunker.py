import re

MAX_WORDS = 120
TITLE_MAX_WORDS = 4


def _words(text):
    return len(text.split())


def _is_heading(line):
    line = line.strip()
    words = line.split()
    if not 0 < len(words) <= 8 or line.endswith((".", ",", ";", "?", "!")):
        return False
    return line.endswith(":") or line.isupper() or line.istitle()


def _is_title_like(text):
    return _words(text) <= TITLE_MAX_WORDS and not text.rstrip().endswith((".", "!", "?"))


def _split_long(text, max_words=MAX_WORDS):
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return []
    if _words(text) <= max_words:
        return [text]
    pieces, cur = [], []
    for sentence in re.split(r"(?<=[.!?])\s+", text):
        if cur and _words(" ".join(cur + [sentence])) > max_words:
            pieces.append(" ".join(cur))
            cur = cur[-1:]                       # one sentence of overlap
        cur.append(sentence)
    if cur:
        pieces.append(" ".join(cur))
    return pieces


def _merge_titles(units):
    """Tiny title-like pieces are attached to the chunk that follows them."""
    out, carry = [], None
    for unit in units:
        if carry:
            unit = {"text": carry["text"] + "\n" + unit["text"],
                    "section": unit["section"] or carry["section"]}
            carry = None
        if _is_title_like(unit["text"]):
            carry = unit
        else:
            out.append(unit)
    if carry:
        if out:
            out[-1] = {"text": out[-1]["text"] + "\n" + carry["text"],
                       "section": out[-1]["section"]}
        else:
            out.append(carry)
    return out


def _chunk_plain(text):
    units, section = [], None
    for para in re.split(r"\n\s*\n", text):
        lines = [l.strip() for l in para.split("\n") if l.strip()]
        if not lines:
            continue
        if _is_heading(lines[0]) and (len(lines) > 1 or lines[0].endswith(":")):
            section = lines[0].rstrip(":").strip()
        for piece in _split_long(" ".join(lines)):
            units.append({"text": piece, "section": section})
    return _merge_titles(units)


def _chunk_blocks(blocks):
    units, cur, count, section = [], [], 0, None

    def flush():
        nonlocal cur, count
        if cur:
            units.append({"text": "\n".join(cur), "section": section})
        cur, count = [], 0

    for block in blocks:
        text = block["text"]
        block_section = block.get("section")
        if block.get("type") == "paragraph" and _is_heading(text) and text.endswith(":"):
            block_section = text.rstrip(":").strip()      # plain "Heading:" lines
        if block_section != section:
            flush()
            section = block_section
        for piece in _split_long(text):
            n = _words(piece)
            if cur and count + n > MAX_WORDS:
                flush()
            cur.append(piece)
            count += n
    flush()
    return _merge_titles(units)


def chunk_page(text, page_number=None, blocks=None):
    """-> [{"text": ..., "section": ...}, ...] for one extracted page."""
    chunks = _chunk_blocks(blocks) if blocks else _chunk_plain(text or "")
    return [c for c in chunks if c["text"].strip()]
#!/usr/bin/env python3
"""Route a --paper source to an ingestor and write <out>/source.md + source.meta.json.

Priority: arXiv URL -> arXiv id -> .pdf (local/URL) -> http(s) HTML.
Exit 0 ok, 1 failure (message on stderr).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
import urllib.request
from pathlib import Path

ARXIV_URL = re.compile(r"arxiv\.org/(abs|pdf)/([^\s?#]+?)(\.pdf)?$", re.I)
ARXIV_ID = re.compile(r"^(arxiv:)?(\d{4}\.\d{4,5}|[a-z\-]+(\.[A-Z]{2})?/\d{7})(v\d+)?$", re.I)


def fetch(url: str, dest: Path | None = None) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "manim-video-skill/0.2"})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
    if dest:
        dest.write_bytes(data)
    return data


def pdf_to_md(path: Path) -> str:
    try:
        from pypdf import PdfReader
    except ImportError:
        from PyPDF2 import PdfReader  # type: ignore
    pages = [(p.extract_text() or "") for p in PdfReader(str(path)).pages]
    return "\n\n".join(t.strip() for t in pages if t.strip())


def html_to_md(html: str) -> str:
    try:
        import trafilatura
        txt = trafilatura.extract(html)
        if txt:
            return txt
    except ImportError:
        pass
    try:
        from readability import Document
        html = Document(html).summary()
    except ImportError:
        pass
    return re.sub(r"\n{3,}", "\n\n", re.sub(r"<[^>]+>", "", re.sub(r"(?is)<(script|style).*?</\1>", "", html)))


def arxiv_id_from(src: str) -> str | None:
    m = ARXIV_URL.search(src)
    if m:
        return m.group(2)
    if ARXIV_ID.match(src):
        return re.sub(r"^arxiv:", "", src, flags=re.I)
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("source")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    src, meta = a.source.strip(), {"source": a.source}

    try:
        aid = arxiv_id_from(src)
        if aid:
            meta.update(kind="arxiv", arxiv_id=aid)
            with tempfile.TemporaryDirectory() as td:
                pdf = Path(td) / "p.pdf"
                fetch(f"https://arxiv.org/pdf/{aid}", pdf)
                body = pdf_to_md(pdf)
            try:
                import re as _re
                abs_html = fetch(f"https://arxiv.org/abs/{aid}").decode("utf-8", "replace")
                t = _re.search(r'<meta name="citation_title" content="([^"]+)"', abs_html)
                if t:
                    meta["title"] = t.group(1)
            except Exception:
                pass
        elif src.lower().endswith(".pdf"):
            meta["kind"] = "pdf"
            if re.match(r"^https?://", src):
                with tempfile.TemporaryDirectory() as td:
                    pdf = Path(td) / "p.pdf"
                    fetch(src, pdf)
                    body = pdf_to_md(pdf)
            else:
                body = pdf_to_md(Path(src))
        elif re.match(r"^https?://", src):
            meta["kind"] = "html"
            body = html_to_md(fetch(src).decode("utf-8", "replace"))
        else:
            raise ValueError(f"unrecognized source: {src!r} (expected arXiv id/url, .pdf path/url, or http(s) url)")
    except Exception as e:  # noqa: BLE001 - report any ingest failure uniformly
        print(f"ingest failed: {type(e).__name__}: {e}", file=sys.stderr)
        return 1

    if len(body.split()) < 50:
        print("ingest failed: extracted fewer than 50 words", file=sys.stderr)
        return 1
    meta["words"] = len(body.split())
    title = meta.get("title", a.source)
    (out / "source.md").write_text(f"---\ntitle: {json.dumps(title)}\nsource: {json.dumps(a.source)}\n---\n\n{body}\n", encoding="utf-8")
    (out / "source.meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(json.dumps({"ok": True, "out": str(out / "source.md"), "words": meta["words"]}))
    return 0


if __name__ == "__main__":
    sys.exit(main())

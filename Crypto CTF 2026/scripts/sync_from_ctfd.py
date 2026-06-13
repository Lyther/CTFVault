#!/usr/bin/env python3
"""Fetch Crypto CTF (cr.yp.toc.tf) challenges and write convention-B folders."""

from __future__ import annotations

import json
import os
import re
import time
import urllib.request
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://cr.yp.toc.tf"
LIST_URL = f"{BASE}/challenges/list"
SLEEP_S = 0.15

# CTFd session cookie must be supplied via environment. Never commit a real value.
SESSION_COOKIE = os.environ.get("CRYPTO_CTF_SESSION", "")

FLAG_BRACE = re.compile(r"CCTF\{[^}]+\}", re.IGNORECASE)
FLAG_PARENS = re.compile(r"CCTF\([^)]+\)", re.IGNORECASE)
HREF_RE = re.compile(r'href=["\']([^"\']+)["\']', re.IGNORECASE)


def slugify(name: str, max_len: int = 56) -> str:
    n = name.strip().lower()
    n = re.sub(r"[^\w\s-]", "", n, flags=re.UNICODE)
    n = re.sub(r"[-\s]+", "-", n).strip("-")
    return (n[:max_len] if n else "challenge").rstrip("-")


def strip_html(html: str | None) -> str | None:
    if not html:
        return None
    t = unescape(re.sub(r"<[^>]+>", "", html))
    return re.sub(r"\s+", " ", t).strip() or None


def fetch_json(url: str) -> dict:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "ctf-vault-sync/1.0",
            "Cookie": f"crypto_ctf_session={SESSION_COOKIE}",
        },
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))


def fetch_text(url: str) -> str:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "ctf-vault-sync/1.0",
            "Cookie": f"crypto_ctf_session={SESSION_COOKIE}",
        },
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8")


def fetch_bytes(url: str) -> bytes:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "ctf-vault-sync/1.0",
            "Cookie": f"crypto_ctf_session={SESSION_COOKIE}",
        },
    )
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()


def description_to_markdown_body(description: str) -> str:
    if not description:
        return "_No description._"
    return description.replace("\r\n", "\n").strip()


def flags_in_text(text: str) -> list[str]:
    out: list[str] = []
    for rx in (FLAG_BRACE, FLAG_PARENS):
        out.extend(m.group(0) for m in rx.finditer(text))
    seen: set[str] = set()
    uniq: list[str] = []
    for f in out:
        if f not in seen:
            seen.add(f)
            uniq.append(f)
    return uniq


def category_dir_name(cat: dict) -> str:
    name = cat.get("name") or "misc"
    n = re.sub(r"[^\w\s-]", "", str(name), flags=re.UNICODE)
    n = re.sub(r"[-\s]+", "-", n).strip("-").lower()
    return n or "misc"


def attachment_urls_from_html(html: str) -> list[str]:
    urls: list[str] = []
    for m in HREF_RE.finditer(html):
        href = m.group(1)
        if href.startswith("/") and not href.startswith("//"):
            urls.append(href)
    return urls


def safe_attachment_name(cid: int, url_path: str) -> str:
    base = Path(url_path).name
    return f"{cid}_{base}" if base else f"{cid}_attachment"


def main() -> None:
    if not SESSION_COOKIE:
        raise SystemExit("error: set CRYPTO_CTF_SESSION env var")

    challenges = fetch_json(LIST_URL)
    challenges.sort(key=lambda c: c["id"])

    manifest: list[dict] = []
    used_files: dict[str, int] = {}

    for d in challenges:
        cid = d["id"]
        cats = d.get("categories") or []
        cat = cats[0] if cats else {"name": "misc"}
        cat_dir = category_dir_name(cat)
        slug = slugify(d.get("name") or "challenge")
        leaf = f"{cid}-{slug}"
        ch_dir = ROOT / cat_dir / leaf
        ch_dir.mkdir(parents=True, exist_ok=True)

        desc_raw = d.get("description") or ""
        desc_md = description_to_markdown_body(desc_raw)
        solves = d.get("solves_count", 0)
        points = d.get("points")
        dynamic = d.get("dynamic_points")

        attachments: list[dict] = []
        for href in attachment_urls_from_html(desc_raw):
            fname = safe_attachment_name(cid, href)
            if fname in used_files:
                used_files[fname] += 1
                stem, suf = Path(fname).stem, Path(fname).suffix
                fname = f"{stem}_{used_files[fname]}{suf}"
            else:
                used_files[fname] = 1
            local_rel = f"files/{fname}"
            dest = ch_dir / local_rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            dl = f"{BASE}{href}"
            try:
                dest.write_bytes(fetch_bytes(dl))
            except Exception as e:
                print(f"download fail {cid} {dl}: {e}")
            attachments.append({"filename": Path(href).name, "local_path": local_rel})

        rel_path = f"{cat_dir}/{leaf}"
        out_json = {
            "id": cid,
            "name": d.get("name"),
            "category": cat.get("name"),
            "value": points,
            "dynamic_points": dynamic,
            "description": desc_raw.replace("\n", "\r\n") if desc_raw else "",
            "attachments": attachments,
            "solves": solves,
            "path": rel_path,
        }
        (ch_dir / "challenge.json").write_text(
            json.dumps(out_json, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

        title = d.get("name") or "Challenge"
        lines = [
            f"# {title}",
            "",
            f"- ID: {cid}",
            f"- Category: {cat.get('name')}",
        ]
        if points is not None:
            lines.append(f"- Value: {points}")
        if dynamic is not None:
            lines.append(f"- Dynamic Points: {dynamic}")
        lines.extend(
            [
                f"- Solves: {solves}",
                "",
                "## Description",
                "",
                desc_md,
                "",
            ]
        )
        if attachments:
            lines.append("## Files")
            lines.append("")
            for a in attachments:
                lines.append(f"- `{a['filename']}` (vendored as `{a['local_path']}`)")
            lines.append("")
        body = "\n".join(lines)
        (ch_dir / "challenge.md").write_text(body, encoding="utf-8")
        (ch_dir / "README.md").write_text(body, encoding="utf-8")

        flags = flags_in_text(desc_raw)
        writeup = ch_dir / "writeup.md"
        sol_flag = ch_dir / "solution" / "flag.txt"
        if not writeup.exists():
            if flags:
                flag_line = flags[0]
                wu = [
                    f"# {title} — Writeup",
                    "",
                    "- Category:",
                    f"- Value: {points}",
                    "",
                    "## Challenge",
                    "",
                    "> " + desc_md.replace("\n", "\n> "),
                    "",
                    "## Flag",
                    "",
                    f"```text\n{flag_line}\n```",
                    "",
                ]
            else:
                wu = [
                    f"# {title} — Writeup",
                    "",
                    "- Category:",
                    f"- Value: {points}",
                    "",
                    "## Challenge",
                    "",
                    "> " + desc_md.replace("\n", "\n> "),
                    "",
                    "## Flag",
                    "",
                    "```text\nTBD\n```",
                    "",
                    "## Solve",
                    "",
                    "(Add after solving.)",
                    "",
                ]
            writeup.write_text("\n".join(wu), encoding="utf-8")

        if not sol_flag.exists():
            sol_flag.parent.mkdir(parents=True, exist_ok=True)
            sol_flag.write_text(
                (flags[0] + "\n") if flags else "TBD\n",
                encoding="utf-8",
            )

        manifest.append(
            {"id": cid, "path": rel_path, "name": title, "category": cat.get("name")}
        )
        time.sleep(SLEEP_S)

    (ROOT / "sync-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    for page in ("rules", "faq"):
        try:
            html = fetch_text(f"{BASE}/{page}")
            (ROOT / f"{page}.html").write_text(html, encoding="utf-8")
            print(f"fetched {page}.html")
        except Exception as e:
            print(f"{page} fetch failed: {e}")

    print(f"wrote {len(manifest)} challenges under {ROOT}")


if __name__ == "__main__":
    main()

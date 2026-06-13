#!/usr/bin/env python3
"""Fetch KubSTU CTF challenges from CTFd API and write convention-B folders."""

from __future__ import annotations

import json
import re
import time
import urllib.request
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://kubstu-ctf.online"
LIST_URL = f"{BASE}/api/v1/challenges"
SLEEP_S = 0.15

FLAG_BRACE = re.compile(r"KubSTU\{[^}]+\}", re.IGNORECASE)
FLAG_PARENS = re.compile(r"KubSTU\([^)]+\)", re.IGNORECASE)


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
    req = urllib.request.Request(url, headers={"User-Agent": "ctf-vault-sync/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))


def description_to_markdown_body(description: str) -> str:
    if not description:
        return "_No description._"
    # API uses \r\n; normalize for markdown
    return description.replace("\r\n", "\n").strip()


def flags_in_text(text: str) -> list[str]:
    out: list[str] = []
    for rx in (FLAG_BRACE, FLAG_PARENS):
        out.extend(m.group(0) for m in rx.finditer(text))
    # de-dup preserve order
    seen: set[str] = set()
    uniq: list[str] = []
    for f in out:
        if f not in seen:
            seen.add(f)
            uniq.append(f)
    return uniq


def safe_attachment_name(cid: int, url_path: str) -> str:
    base = Path(url_path).name
    return f"{cid}_{base}" if base else f"{cid}_attachment"


def main() -> None:
    listing = fetch_json(LIST_URL)
    challenges = listing["data"]
    challenges.sort(key=lambda c: c["id"])

    manifest: list[dict] = []
    used_files: dict[str, int] = {}

    for meta in challenges:
        cid = meta["id"]
        url = f"{BASE}/api/v1/challenges/{cid}"
        blob = fetch_json(url)
        if not blob.get("success"):
            print(f"skip {cid}: {blob}")
            time.sleep(SLEEP_S)
            continue
        d = blob["data"]
        d.pop("view", None)

        cat = d.get("category") or "misc"
        cat_dir = re.sub(r"[/\\]", "-", str(cat))
        if cat_dir.lower() == "start":
            cat_dir = "Start"
        slug = slugify(d.get("name") or "challenge")
        leaf = f"{cid}-{slug}"
        ch_dir = ROOT / cat_dir / leaf
        files_dir = ch_dir / "files"
        ch_dir.mkdir(parents=True, exist_ok=True)

        desc_raw = d.get("description") or ""
        desc_md = description_to_markdown_body(desc_raw)
        author = strip_html(d.get("attribution"))
        solves = d.get("solves", meta.get("solves", 0))
        ch_type = d.get("type", meta.get("type", ""))
        conn = d.get("connection_info")

        attachments: list[dict] = []
        for fp in d.get("files") or []:
            if not isinstance(fp, str):
                continue
            fname = safe_attachment_name(cid, fp)
            if fname in used_files:
                used_files[fname] += 1
                stem, suf = Path(fname).stem, Path(fname).suffix
                fname = f"{stem}_{used_files[fname]}{suf}"
            else:
                used_files[fname] = 1
            local_rel = f"files/{fname}"
            dest = ch_dir / local_rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            dl = f"{BASE}{fp}" if fp.startswith("/") else f"{BASE}/{fp}"
            try:
                req = urllib.request.Request(
                    dl,
                    headers={"User-Agent": "ctf-vault-sync/1.0"},
                )
                with urllib.request.urlopen(req, timeout=120) as r:
                    dest.write_bytes(r.read())
            except Exception as e:
                print(f"download fail {cid} {dl}: {e}")
            attachments.append({"filename": Path(fp).name, "local_path": local_rel})

        rel_path = f"{cat_dir}/{leaf}"
        out_json = {
            "id": cid,
            "name": d.get("name"),
            "category": cat,
            "value": d.get("value"),
            "description": desc_raw.replace("\n", "\r\n") if desc_raw else "",
            "attachments": attachments,
            "author": author,
            "connection_info": conn,
            "type": ch_type,
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
            f"- Category: {cat}",
            f"- Value: {d.get('value')}",
            f"- Solves: {solves}",
            f"- Type: {ch_type}",
        ]
        if author:
            lines.append(f"- Author: {author}")
        if conn:
            lines.append(f"- Connection: `{conn}`")
        lines.extend(["", "## Description", "", desc_md, ""])
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
                    f"# Writeup: {title}",
                    "",
                    "## Flag",
                    "",
                    f"`{flag_line}`",
                    "",
                    "## Solve",
                    "",
                    "Flag appears in the challenge description.",
                    "",
                ]
            else:
                wu = [
                    f"# Writeup: {title}",
                    "",
                    "## Flag",
                    "",
                    "`TBD`",
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

        manifest.append({"id": cid, "path": rel_path, "name": title, "category": cat})
        time.sleep(SLEEP_S)

    (ROOT / "sync-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {len(manifest)} challenges under {ROOT}")


if __name__ == "__main__":
    main()

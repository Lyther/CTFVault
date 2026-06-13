#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///

import hashlib
import pathlib
import re
import sqlite3
import tempfile
import zipfile

HERE = pathlib.Path(__file__).resolve().parent
CHALLENGE = HERE.parent / "files" / "challenge.zip"
CYMRU = HERE.parent / "other" / "cymru.txt"
EXPECTED_SHA1 = "aa50aa4516d0bc7b0aa23139f95d38edd916164a"
HISTORY_PATH = "kurt_backup/AppData/Local/Microsoft/Edge/User Data/Default/History"
TARGET_HOST = "23.179.17.92"


def verify_sha1(path: pathlib.Path) -> None:
    digest = hashlib.sha1(path.read_bytes()).hexdigest()
    if digest != EXPECTED_SHA1:
        raise SystemExit(f"sha1 mismatch: {digest}")


def history_contains_target(history_db: pathlib.Path) -> bool:
    conn = sqlite3.connect(history_db)
    try:
        row = conn.execute(
            "select url from urls where url like ? limit 1",
            (f"%{TARGET_HOST}%",),
        ).fetchone()
    finally:
        conn.close()
    return row is not None


def parse_asn(path: pathlib.Path) -> str:
    match = re.search(
        r"^\s*(\d+)\s*\|\s*23\.179\.17\.92\s*\|", path.read_text(), re.MULTILINE
    )
    if not match:
        raise SystemExit("asn not found in cymru.txt")
    return match.group(1)


def main() -> None:
    verify_sha1(CHALLENGE)

    with zipfile.ZipFile(CHALLENGE) as zf, tempfile.TemporaryDirectory() as tmpdir:
        history_db = pathlib.Path(tmpdir) / "History"
        history_db.write_bytes(zf.read(HISTORY_PATH))
        if not history_contains_target(history_db):
            raise SystemExit(f"{TARGET_HOST} not found in browser history")

    asn = parse_asn(CYMRU)
    print(f"asn={asn}")
    print(f"flag=CIT{{{asn}}}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///

import datetime as dt
import hashlib
import pathlib
import sqlite3
import tempfile
import zipfile

HERE = pathlib.Path(__file__).resolve().parent
CHALLENGE = HERE.parent / "files" / "challenge.zip"
EXPECTED_SHA1 = "aa50aa4516d0bc7b0aa23139f95d38edd916164a"
HISTORY_PATH = "kurt_backup/AppData/Local/Microsoft/Edge/User Data/Default/History"
PSREADLINE_PATH = (
    "kurt_backup/AppData/Roaming/Microsoft/Windows/PowerShell/PSReadLine/"
    "ConsoleHost_history.txt"
)
TARGET_URL = "https://23.179.17.92:5067/"


def verify_sha1(path: pathlib.Path) -> None:
    digest = hashlib.sha1(path.read_bytes()).hexdigest()
    if digest != EXPECTED_SHA1:
        raise SystemExit(f"sha1 mismatch: {digest}")


def chrome_time_to_iso(value: int) -> str:
    unix_seconds = value / 1_000_000 - 11644473600
    timestamp = dt.datetime.fromtimestamp(unix_seconds, tz=dt.UTC)
    return timestamp.replace(microsecond=0).isoformat().replace("+00:00", "Z")


def find_last_visit(history_db: pathlib.Path) -> str:
    conn = sqlite3.connect(history_db)
    try:
        row = conn.execute(
            """
            SELECT v.visit_time
            FROM visits AS v
            JOIN urls AS u ON u.id = v.url
            WHERE u.url = ?
            ORDER BY v.visit_time DESC
            LIMIT 1
            """,
            (TARGET_URL,),
        ).fetchone()
    finally:
        conn.close()

    if row is None:
        raise SystemExit(f"target URL not found: {TARGET_URL}")
    return chrome_time_to_iso(row[0])


def read_console_history(zf: zipfile.ZipFile) -> str:
    return zf.read(PSREADLINE_PATH).decode("utf-8", errors="replace")


def main() -> None:
    verify_sha1(CHALLENGE)

    with zipfile.ZipFile(CHALLENGE) as zf, tempfile.TemporaryDirectory() as tmpdir:
        history_db = pathlib.Path(tmpdir) / "History"
        history_db.write_bytes(zf.read(HISTORY_PATH))
        last_visit = find_last_visit(history_db)
        console_history = read_console_history(zf).strip()

    print(f"last_visit={last_visit}")
    print(f"flag=CIT{{{last_visit}}}")
    print()
    print(console_history)


if __name__ == "__main__":
    main()

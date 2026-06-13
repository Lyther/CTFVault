#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///

from __future__ import annotations

import pathlib
import re
import subprocess
import tempfile
import urllib.parse

HERE = pathlib.Path(__file__).resolve().parent
CHALLENGE = HERE.parent / "files" / "7_Demo.rar"


def extract_archive(target: pathlib.Path) -> pathlib.Path:
    subprocess.run(
        ["bsdtar", "-xf", str(CHALLENGE), "-C", str(target)],
        check=True,
    )
    return target


def read_text(path: pathlib.Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_initial_access(access_log: str) -> tuple[str, str]:
    for line in access_log.splitlines():
        if "sqlmap/" not in line or "INTO%20OUTFILE%20%27" not in line:
            continue

        request_match = re.search(r'"GET ([^"]+) HTTP/1\.1"', line)
        if not request_match:
            continue

        decoded = urllib.parse.unquote(request_match.group(1))
        if "UNION SELECT" not in decoded or "INTO OUTFILE" not in decoded:
            continue

        file_match = re.search(r"INTO OUTFILE '([^']+)'", decoded)
        if not file_match:
            continue

        uploaded = pathlib.PurePosixPath(file_match.group(1)).name
        return "SQLi", uploaded

    raise RuntimeError("could not find SQLi webshell drop in access log")


def parse_lateral_user(auth_log: str) -> str:
    match = re.search(
        r"Accepted publickey for (\w+) from 192\.168\.1\.10",
        auth_log,
    )
    if not match:
        raise RuntimeError("could not find lateral SSH login")
    return match.group(1)


def parse_copied_file(history: str) -> str:
    match = re.search(r"^cp\s+(\S+)\s+\S+$", history, re.MULTILINE)
    if not match:
        raise RuntimeError("could not find copied file in bash history")
    return pathlib.PurePosixPath(match.group(1)).name


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = extract_archive(pathlib.Path(tmp))

        access_log = read_text(root / "service/var/log/apache2/access.log")
        auth_log = read_text(root / "DB/var/log/auth.log")
        db_history = read_text(root / "DB/home/dbadmin/.bash_history")

        vuln, uploaded = parse_initial_access(access_log)
        user = parse_lateral_user(auth_log)
        copied = parse_copied_file(db_history)

        flag = f"KubSTU{{{vuln},{uploaded},{user},{copied}}}"
        print(flag)


if __name__ == "__main__":
    main()

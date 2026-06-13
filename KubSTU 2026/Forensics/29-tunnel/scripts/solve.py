#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///

import pathlib
import re
import subprocess

HERE = pathlib.Path(__file__).resolve().parent
CHALLENGE = HERE.parent / "files" / "29_Krasnodar.pcap"
SUFFIX = ".exfiltrate.kubstu-ctf.ru"
MARKER = re.compile(r"v(\d{2})\.([0-9a-f]{2,})")


def tshark_qnames() -> list[str]:
    cmd = [
        "tshark",
        "-r",
        str(CHALLENGE),
        "-Y",
        "dns && ip.src == 192.168.1.50",
        "-T",
        "fields",
        "-e",
        "dns.qry.name",
    ]
    out = subprocess.check_output(cmd, text=True)
    return [line.strip().lower() for line in out.splitlines() if line.strip()]


def extract_flag() -> str:
    parts: dict[int, str] = {}
    for name in tshark_qnames():
        if not name.endswith(SUFFIX):
            continue
        label = name[: -len(SUFFIX)]
        match = MARKER.fullmatch(label)
        if not match:
            continue
        index = int(match.group(1))
        parts[index] = bytes.fromhex(match.group(2)).decode("utf-8")
    if not parts:
        raise ValueError("no marker fragments found")
    flag = "".join(parts[index] for index in sorted(parts))
    if not re.fullmatch(r"KubSTU\{[^}]+\}", flag):
        raise ValueError(f"unexpected flag format: {flag!r}")
    return flag


def main() -> None:
    print(extract_flag())


if __name__ == "__main__":
    main()

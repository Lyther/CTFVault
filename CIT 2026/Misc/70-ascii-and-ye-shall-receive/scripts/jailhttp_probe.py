#!/usr/bin/env python3
"""Probe jailHTTPd via SSH tunnel."""

import subprocess
import sys

HOST = "23.179.17.92"
PORT = 2222
KEY = "../files/id_ed25519"


def send_request(path: str) -> tuple[int, str]:
    """Send HTTP/1.0 request through SSH, return (status_code, body)."""
    request = f"GET {path} HTTP/1.0\r\n\r\n"
    cmd = ["ssh", "-i", KEY, "-p", str(PORT), f"ctf@{HOST}"]

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
        body = response[body_start + 4 :] if body_start != -1 else ""
        return status, body

    return 0, response


def main():
    paths = sys.argv[1:] if len(sys.argv) > 1 else ["/not_a_flag", "/?", "/flag", "/.."]

    for path in paths:
        status, body = send_request(path)
        print(f"{path} -> {status} ({len(body)} bytes)")
        if status == 200 and "flag" not in path.lower():
            print(f"  INTERESTING: {body[:100]}")


if __name__ == "__main__":
    main()

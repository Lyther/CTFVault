# ASCII and Ye Shall Receive — Session 2 Recon

## New findings

### Port 5000 open — SecureVault (likely separate challenge)

Not in original recon. `GET /` → Flask app titled "SecureVault — Sign In":
- `Server: Werkzeug/3.1.8 Python/3.11.15`
- Login form (username + password) via `POST /login`
- `/forgot-password` form (username only)
- UI: slick dark theme, 🏦 SecureVault branding

No obvious ties to the ASCII chain (no BBS / ZMODEM / jailHTTPd references), so most likely a sibling challenge on the same host.

### Extensive port scan confirms only these:

`22, 80, 2222, 2323, 5000, 6969, 8080` — no NNTP/119, no UUCP/540, no Kermit port, no hidden service.

### BBS menu fully enumerated

Main-menu probes for every letter A-Z, numerics, `?`, `/`, `.`, `*`, `!`, `$`, shell-ish strings: **every non-`M/F/D/W/U/C/N/G` input returns `Unknown command`**. No hidden dot-commands, no Citadel `.` syntax, no sysop override key.

Full menu text:
```
[M] Message Base       [F] File Library
[D] Door Games         [W] Who's Online
[U] User List          [C] Chat with Sysop
[N] News & Bulletins   [G] Goodbye / Logoff
```

- `M` → message list (4731–4734), cannot read individual messages — "Press any key" only
- `D` → all 4 doors "DROP-FILE locked"
- `W`, `U` → flavor tables
- `C` → "ZeroCool is not available. Try paging again later."

Logging in as `SYSOP`, `ADMIN`, `root`, `ZeroCool` etc. does not unlock anything — same menus, same sysop lock on file 4.

### File library fully probed

From `D` → File number prompt:
- `1/2/3/5` → valid, each ZMODEM-sends the advertised joke file
- `4` → always routes to `Override password:` prompt
- `0 / -1 / 6 / 99 / abc / */?/..` → `Bad file number`
- Any path-ish string → `Bad file number`

From the file-library menu prompt (`[D]ownload by number, [B]ack`):
- `D` / `B` only. All of `U/upload/P/K/X/Y/Z/RZ/SZ/kermit/protocol` silently re-print the menu (no override, no alt protocol).

### File 4 sysop-lock override — command injection proven impossible

Tested payloads against the override prompt (`;ls`, `$(id)`, `\`ls\``, `test\n$(cat /etc/passwd)`, `../SECRETS`, `..`, `\x00`, etc.): **every one passes straight through to the same ZMODEM transfer of `CYPHRPNK.TOR`**. The prompt does not exec the string, does not treat it as a path, does not validate it. It's pure theater.

### ZMODEM details (manual handshake)

- BBS initiates as sender: sends `rz\r**\x18B00000000000000\r\x8a\x11` (ZRQINIT).
- After we respond with a valid ZRINIT (e.g., flags `0x23 = CANFDX|CANOVIO|CANFC32`), BBS emits **ZFILE header `02 00 00 00 04 0c 47`** followed by an empty-ish subpacket terminated with `ZDLE k` (ZCRCW).
- `lrz -vv` successfully receives the file and confirms filename exactly matches what the menu advertises.
- No ZCOMMAND / ZSINIT leaks exposed by the BBS's sender.

### jailHTTPd advanced probes (all post-SSH via key)

Paths tested (all return 404 unless noted):
```
/flag, /flag.txt, /flags, /secrets, /SECRETS, /UPLOADS, /uploads,
/private, /protected, /admin, /~ctf, /ctf, /home/ctf, /root, /var, /etc,
/index.html, /README*, /proc/self/root/*, /proc/self/environ,
/bin/ls, /bin/sh, /static/*, /files/*, /hello, /welcome,
/Not_A_Flag (case variants), /flag.html, etc.
```
Interesting non-404s:
- `/.flag`, `/.htaccess`, `/not_a_flag/.`, `/not_a_flag.` → **403 Forbidden: '.' only allowed between alphanumeric characters**
- `/not_a_flag\xa0` (NBSP) → **400 Bad Request**
- `/?` and `/?foo` → **200 root index** (query strings are ignored but parser treats empty query as root)
- `/%2fnot_a_flag`, `//not_a_flag`, `///not_a_flag` → resolve to `/not_a_flag`
- `%2e%2f`, `../`, `%252e%252f`, `%2fnot_a_flag/..%2fflag` etc. → 403 or 404

Methods other than GET → `405 Method Not Allowed: only GET is supported (got 'METHOD')`.

Headers that commonly enable rewriting (`X-Original-URL`, `X-Rewrite-URL`, `Referer`) are ignored.

`GET /\rsmuggled` or `GET /\nsmuggled` — rewritten to `/` before parsing (CR/LF terminate path), same as baseline.

## Still open interpretations of "Manual From 1986"

1. **ZMODEM spec by Chuck Forsberg (Omen Technology, 1986)** — most likely; the chain literally speaks ZMODEM. Exploit angle not yet found, but candidates to test:
   - Spontaneous `ZCOMMAND` from receiver while server's `sz` is running
   - Malformed `ZSINIT` with crafted attention string
   - Overly-long filename in receiver-requested `ZFREECNT` / `ZCHALLENGE` response
   - CAN*5 mid-transfer to force the sender to dump a shell hint
2. **RFC 977 NNTP (Feb 1986)** — BBS has a News section but no port 119, so likely not.
3. **Kermit Protocol Manual, 6th ed. (Columbia Univ., 1986)** — the BBS does not respond to Kermit init bytes (`\x01+ I~% @-#Y1R\r` rejected as "Unknown command").
4. **FidoNet FTS-0001 (1986)** — "Fidonet" is namedropped in the login banner but no FidoNet port (24554/binkd) is open.

Of these, only ZMODEM is actively reachable. The ZMODEM **sender** on the BBS is the attack surface. The specific trick is still not identified.

## Completed advanced jailHTTPd probes

New findings from the full probe sweep:

| probe | response |
| --- | --- |
| `GET /not_a_flag\xa0 HTTP/1.0` (NBSP) | **400 Bad Request: ASCII only** |
| `GET\t/flag\tHTTP/1.0` | 400 Bad Request: malformed request line |
| `GET / HTTP/2.0` | 200 OK (version string ignored) |
| `GET /\r\n\r\n` (HTTP/0.9 style, no version) | 200 OK |
| `GET /not_a_flag\r\n\r\n` (HTTP/0.9 file) | 200 OK, returns file |
| `GET not_a_flag HTTP/1.0` (no leading slash) | 200 OK (auto-prepends /) |
| `GET HTTP/1.0\r\n\r\n` (no path) | 404 (treats `HTTP/1.0` as path) |
| `GET  /flag HTTP/1.0` (double space after GET) | 200 OK root (empty path token) |
| `GET /?` | 200 OK root |
| `X-Original-URL: /flag`, `X-Rewrite-URL: /flag`, `Referer: /flag` | all ignored |

## Title-clue reinterpretation

The 400 response text `"400 Bad Request: ASCII only"` is a **direct reference to the challenge title** ("ASCII and Ye Shall Receive"). That strongly argues the 1986-manual angle lives **inside jailHTTPd's path parser**, not in the BBS ZMODEM handshake — because a ZMODEM hex frame carries high-bit-set CRLF (`0x8D 0x8A`) which this parser would reject outright.

Refinements worth testing next:
- Seven-bit-safe path encodings that still resolve to files outside `/var/www/html/` (pure ASCII traversal that the dot-filter + slash-normalization doesn't catch).
- `GET` with path whose tokens count differently when parsed by the challenge parser vs. Python's `shlex`-style split.
- A **1986-published HTTP/parser-precursor** spec — possibly **TN3270 / Gopher-predecessor ISO 8613-6** or the **hypertext spec in CERN's 1989 proposal** — but 1986 specifically… the candidates are thin. One plausible read: **RFC 977 NNTP** strips to 7-bit ASCII too; jailHTTPd may be speaking "ASCII-only body" à la NNTP while pretending to be HTTP.

Real next step is to read the jailHTTPd behavior as **if it were a 1986 NNTP/USENET-grade 7-bit parser**, not an HTTP one.

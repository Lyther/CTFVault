# Wingstop 2 — progress notes

- Same host as Wingstop 1: 23.179.17.68
- flag1 already solved: `CIT{p1Gs_0n_tH3_W1ng}` (also visible as `backup.xml` contents via anonymous FTP)
- **Wingstop 2 currently has 0 solves.** Service instance is flapping — ports 21/80 come up for ~2 min and drop for 1–3 min. Ports 3300 and 5985 stay open.

## Observed behavior

| Port | State | Notes |
|---|---|---|
| 21 | flapping | Wing FTP anonymous. When up, `backup.xml` readable; `loot.txt` returns `550 banned on server` |
| 80 | flapping | Wing FTP web UI (user). Admin login (`Admin:Password@1`) fails here — only the Wing FTP admin panel accepts those creds, and this panel isn't on 80 |
| 3300 | open, tcpwrapped | Accepts TCP + TLS ClientHello on `TLSv1.3` but drops without serving a cert. Not the admin panel (default 5466). Custom SNI attempts all reset. Plausibly WireGuard or mTLS-gated. |
| 5985 | flapping (502 when not up) | WinRM. NTLM rejects every tried cred (`Admin:Password@1`, `Administrator:Password@1`, `bob:Password@1`, +~20 guesses) |

## Attack paths attempted

- **CVE-2025-47812 Lua injection (Wingstop 1 exploit)** — `%00]]` break-out no longer produces a `UID` cookie (login fully rejected). Either the service was upgraded past the patched version (Wing FTP 7.4.4+) for Wingstop 2, or our null-byte payload is now filtered.
- **Wing FTP admin panel** — standard paths `/admin.html`, `/admin_login.html`, port 5466 all 404 or refused.
- **WinRM spray** — ~50 user/pass combos including the Wing FTP admin creds; all fail NTLM.
- **FTP SITE ZIP path traversal** — `..\..\` and absolute Windows paths all return `530 Zip failed: no permission.`; FTP user is jailed to anonymous root.
- **FTP `STOR` upload** — rejected (service returns `200 Type is set.` on data channel, no upload).
- **Port 3300 TLS probe** — every SNI/ALPN combo drops after ClientHello. No useful response.

## Candidate next angles when service recovers

1. Grab Wing FTP **version banner** from `/login.html` — if it's 7.4.3 or earlier, the CVE should still work; any higher and we need a different bug.
2. Look for `/admin_*` hidden endpoints or an admin panel on a NON-standard port once a fresh full-port scan completes.
3. Wing FTP supports server-side Lua scripts in user home directories (`OnClientConnected.lua`, `events.lua`). If we find any path where we can `STOR` a `.lua` file that the server auto-loads, that's the unauth RCE. Needs a writable FTP account or a writable anonymous subdir that isn't just `/`.
4. Wing FTP **admin JSON API** — `POST /admin_login.html` with `username=Admin&password=Password@1` may still exist as a direct auth endpoint on port 80 even without the HTML admin UI being visible.
5. **Port 3300** — try Ceph, BoltDB mon, Postgres-style startup packets; also check if it's the Wing FTP admin HTTPS once we have a version that supports non-standard ports.
6. **WinRM** — the real Windows account password is almost certainly *not* Wing-FTP's `Admin:Password@1` (that's an FTP-only account). Need another leak.

## Things worth trying

- Poll `/` every 5s with a lightweight probe; the moment a `200` comes back, hammer `/loginok.html` with a list of payload variants (multiple escape sequences for newer Wing FTP session-file formats).
- After grabbing `Server:` header and `login.html` body, search CVEs specific to that exact Wing FTP version.
- Try **masscan** / **rustscan** on the GPU box's IP (our main IP may be temp-banned from 21/80 after our earlier aggressive scanning).

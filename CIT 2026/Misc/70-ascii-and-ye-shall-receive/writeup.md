# ASCII and Ye Shall Receive — Writeup

- Category: Misc
- Value: 998
- Author: hypnos

## Challenge

> Please Hold While Your Packet Is Being Routed Through Different Protocols From Different Decades And One Of Them Requires You To Read A Manual From 1986
>
> `23.179.17.92:2323`

## Current Progress

No flag yet. The current chain is:

```text
BBS on 2323
-> locked file #4
-> CYPHRPNK.TOR
-> webseed on 8080
-> id_ed25519
-> SSH on 2222
-> custom jailHTTPd shell
```

The problem is no longer the BBS or torrent side. The remaining live branch is the custom HTTP jail on `2222`, because every public BBS artifact is a decoy and the torrent swarm only serves the same SSH key.

One organizer-side data point matters: the official notifications feed contains
`ASCII and Ye Shall Receive fixed` at `2026-04-19 14:39 UTC` with content
`no http`. The first public solve landed at `2026-04-19 15:53 UTC`, which
fits a reading of "the HTTP stage was broken before the fix and became
reachable afterwards" more than "HTTP is a fake branch to ignore."

## Recon

### BBS

- `23.179.17.92:2323` is `STATION BBS - est. 1993`.
- Any handle and any password work for login.
- Main menu options are `M F D W U C N G`.
- `News` contains the strongest explicit clue:

```text
03/01/94  New file area: /UPLOADS is now open for submissions!
01/31/94  Sysop note: stop leaving garbage in /SECRETS. You know who you
          are. I had to move the good stuff to a protected dir.
```

- `Message Base` is listing-only so far. `M` shows the four subjects below,
  then drops to `Press any key:` and returns to the main menu. No deeper
  per-message read prompt has surfaced yet, but the subjects are still worth
  remembering:

```text
4732  LordNikon      CrashOverride  about that thing in the stacks
4733  ZeroCool       All            PLEASE stop uploading goatse.jpg
```

- `W` / `U` are real screens but still just flavor. `W` shows `AcidBurn` on
  node 2 playing Trade Wars; `U` lists `ZeroCool`, `AcidBurn`,
  `CerealKiller`, `LordNikon`, `CrashOverride`, and `ThePlague`.

- File library:

```text
1 WAREZ01.ZIP
2 DOOM_WAD.ZIP
3 PKZIP204G.EXE
4 CYPHRPNK.TOR
5 TRADEWARS.ZIP
```

- Files `1`, `2`, `3`, and `5` are fake joke files.
- File `4` asks for a sysop override password, but the override is fake. Different values still download the exact same `CYPHRPNK.TOR`.
- Public file `3` contains the clearest anti-red-herring text:

```text
(not really, just a message: the flag isn't in the public files)
```

### Torrent / Webseed

- `CYPHRPNK.TOR` is a normal single-file torrent.
- Torrent SHA-1: `0b5460950eaba570032c09cd61ab4eeb7f5ee695`
- Info-hash: `0651978ba96851b109d87edaff41133ef2f999f7`
- Comment:

```text
FreeBSD 4.10 kernel sources, mirror from cypherpunks.to
```

- The metadata obtained directly from the swarm matches the local torrent exactly.
- `/announce` and `/scrape` on `:6969` are real, but they only track this same torrent.
- `:8080` is a webseed that serves the same `id_ed25519` private key.

### SSH / jailHTTPd

- The recovered key authenticates on `23.179.17.92:2222` as `ctf`.
- Port `22` rejects the key for the usernames tried so far.
- `2222` is not a shell. It forces a custom HTTP-only jail:

```text
jailHTTPd/0.1 (PROTOTYPE - DO NOT EXPOSE)
Document root: /var/www/html/
Filesystem is read-only. Only GET is supported.
```

- Root listing shows exactly one public file:

```text
Index of /var/www/html/

not_a_flag  (86 bytes)
```

- `/not_a_flag` contains:

```html
<html><body><h1>Hello world!</h1><p>The flag is somewhere else 😉</p></body></html>
```

- One long-lived SSH shell channel can service many sequential or pipelined
  HTTP requests. Reusing the same authenticated SSH transport for a second
  session channel does not work; the server tears the transport down after the
  first shell channel closes.
- `ssh -p 2222 ctf@23.179.17.92 true` and other exec-mode requests do not
  escape the jail. The server still prints the `jailHTTPd` banner and closes.

## HTTP Findings

- Query strings are ignored for routing. `/?path=...` and similar variants just return the root index.
- Raw `?` and raw `#` are real query / fragment delimiters. `GET /not_a_flag?x`
  and `GET /not_a_flag#x` both resolve the public file, while `%3f` / `%23`
  do not.
- Tabs are not treated as separators in the request line. Space parsing is stricter than normal HTTP.
- `GET  /foo HTTP/1.0` returns the root listing because the extra space after `GET` effectively empties the path token.
- `GET /foo  HTTP/1.0` still resolves `/foo`.
- Absolute URIs such as `GET http://localhost/not_a_flag HTTP/1.0` return `404` and do not act as a proxy.
- Direct absolute-looking paths like `/proc/self/root/etc/passwd` and `/etc/passwd` also return `404`.
- Encoded leading slashes work as aliases:

```text
/%2fnot_a_flag
/%2f%2fnot_a_flag
///not_a_flag
```

all resolve to the public `not_a_flag` file.

- The dot filter is real:

```text
403 Forbidden: '.' only allowed between alphanumeric characters
```

- Straight traversal, encoded traversal, and mixed one-step/two-step percent-decoding variants tested so far do not bypass the jail.
- Raw `CR` and `LF` bytes inside the path truncate the request line, but percent-encoded `%0d` / `%0a` do not reproduce that behavior.
- Raw `NUL` inside the path does not terminate the pathname for the server.
- Additional naming families stayed clean `404`: tracker-flavored paths such as
  `/stats`, `/announce`, `/scrape`; uppercase nested forms under
  `/UPLOADS`, `/SECRETS`, and `/PROTECTED`; and phrase-with-space variants
  like `/good%20stuff`, `/thing%20in%20the%20stacks`, and
  `/protected%20dir/good%20stuff`.

## 8080 Findings

- `:8080` is plain `BaseHTTP/0.6 Python/3.12.13`.
- `/` and `/id_ed25519` both return the same 411-byte private key.
- Raw-socket rechecks show no useful traversal here. `../` and `%2e%2e`
  variants all settle to ordinary `404`s; the earlier contradictory
  `%2e%2e/id_ed25519` result was a client-side artifact from a curl-based
  check, not a real breakout.

## Ruled Out

- Hidden torrent via tracker: dead.
- Hidden alternate payload from reachable peers: dead.
- Port `80` virtual host brute over obvious names: dead, always the default Apache page.
- Real shell, `scp`, `sftp`, or `ssh -L` through `2222`: dead.
- Raw `sz` auto-upload attempts from main menu, file library, and file-number prompt: dead.
- Hidden public file numbers in the BBS prompt beyond `1..5`: no signal so far.
- **Main-menu letter `U` is User List, not Upload.** The top-level menu is
  `M F D W U C N G` = Messages / Files / Doors / Who / Users / Chat / News / Goodbye.
  No "Upload" command exists at top level.
- **File Library only advertises `[D]ownload` and `[B]ack`.** Every other
  single-letter input just redraws the menu. No hidden command at this prompt.
- **Door Games are DROP-FILE locked** ("Try again later"). All four doors
  (LORD, TW2002, Usurper, Global War) return the same lock message.
- **Chat (`C`) just pages `ZeroCool` (the sysop) and returns.** No secondary
  interaction.
- **User List (`U`) and News (`N`) are flavor text only.** News re-confirms
  the `/UPLOADS` + `/SECRETS` clues but nothing else.
- **Handle choice does not change BBS behavior.** Every tried handle
  (`SYSOP`, `HYPNOS`, `ROOT`, `ZEROCOOL`, `ACIDBURN`, `LORDNIKON`,
  `THEPLAGUE`, …) produces the same welcome screen. It is pure echo.
- **File-4 "Override password" is cosmetic.** Every tried password — empty,
  `admin`, `root`, `sysop`, `../flag`, `; ls`, `$FLAG`, `hypnos`, `1986`,
  `ZMODEM` — yields the same `CYPHRPNK.TOR` (305 bytes). Confirmed end-to-end
  via real `rz` receive in `scripts/bbs_full_zmodem.py`.
- **File-number prompt does not batch or shell-inject.** The prompt accepts
  whitespace-separated tokens but effectively only the **first digit** matters.
  `"1 2 3"` ships WAREZ01.ZIP only. `"5 4"` ships TRADEWARS.ZIP only.
  Multi-digit inputs like `10`, `11`, and `12` still transfer file `1`, not
  hidden entries. Tested tokens that did NOT change behavior: `04`, `4.0`,
  `4e0`, `4x`, `4;`, `4/flag`, `4 sz /etc/passwd`, `4\t5`, `+4`, `0x04`,
  `4,5`, `4-1`, and shell-metacharacter strings.
- **BBS-hinted jailHTTPd paths all 404** (after fixing the banner-parsing
  bug in earlier probes, see below). Tested: `/SECRETS`, `/UPLOADS`,
  `/protected`, `/good_stuff`, `/sysop`, `/admin`, `/root`, `/home`,
  `/rfc`, `/manual`, `/readme`, `/stacks`, `/goatse.jpg`, `/flag.txt`,
  `/flag.html`, `/flag.asc`, `/flag.ans`, `/secrets.txt`, `/uploads.txt`,
  `/index.html`, `/moved`, `/archive`, `/backup`, plus slash-alias variants
  `//SECRETS`, `/%2fSECRETS`, `///UPLOADS`, and document-root probes
  `/var`, `/var/www`, `/var/www/html`, `/html`. All clean 404.
- **Bare ZMODEM preheaders do not wake the BBS into receiver mode.** Sending
  raw `ZRQINIT` and `ZRQINIT(ZCOMMAND)` headers at the main menu, file library,
  and file-number prompt does not trigger auto-`rz`. The main menu answers
  `Unknown command`, the file library just redraws, and the file-number prompt
  says `Bad file number`.
- **Naive reverse `sz` after a normal download is too late.** After a clean
  `rz` receive of `CYPHRPNK.TOR`, the session has already fallen back to the
  file-library prompt by the time a follow-up `sz` starts talking, so `sz`'s
  leading `rz\r` / pre-header bytes are consumed as menu input instead of
  starting a turn-around upload.
- **Upstream `lrzsz` source backs this up.** Pulling `lrzsz-0.12.20` showed
  that ordinary `ZFILE` sending does not support a reverse upload handoff.
  The only built-in `system("rz")` turn-around lives in `lsz.c:zsendcmd()`
  command mode, not the normal file-send path that file `4` uses.
- **Port `5558` is not the missing protocol hop.** It stays silent under raw
  TCP connects and does not answer HTTP, SSH, Telnet-ish, or basic ZMODEM
  handshake probes.

## Probe bug that was fooling earlier scripts

jailHTTPd sends a **greeting banner as a 200 OK response** *before* reading
the request, and the banner body contains the literal string
`HTTP/1.0 and HTTP/1.0 only.`. Any parser that scans for the first
`HTTP/1.0` in the response stream matches that substring and reports a
fake "200 OK" for every path. Fixed in `scripts/bbs_lead_probe.py` by
anchoring the status-line regex to start-of-line; re-runs now show the
real 404s. Earlier apparent 200s against `/SECRETS`, `/UPLOADS`, etc.
were false positives. **Re-verify any past "200 OK" result from an SSH
HTTP probe using the fixed parser.**

## ZMODEM Reverse Upload (Forsberg §7.5)

Tested the ZMODEM Session Cleanup reverse upload technique:

- After completing normal download (ZFIN received), sent ZRQINIT to initiate
  reverse upload
- **Server ignores ZRQINIT** — returns "Transfer complete" and goes back to
  file library menu
- BBS ZMODEM implementation does not support §7.5 session turn-around
- This avenue is dead
- Upstream `lsz` source agrees with the live result. In normal file-send mode,
  receiver `ZRQINIT` is treated as a bad state / "remote site is sender", not
  as a request to flip into upload mode.

## HTTP Protocol Variations Tested

- **No-version `GET /path` lines are not a useful old-parser path.** One-shot
  requests without `HTTP/1.0` just get the banner / help text and the
  connection closes.
- **HTTP/1.1, HTTP/2.0, HTTP/3.0**: not established as useful alternate
  parsers; the only reliable live branch remains normal `HTTP/1.0`
- **HTTP method case**: `get`, `GeT`, etc. return 405 (case-sensitive GET only)
- **Request smuggling**: Double requests just process sequentially
- **CRLF injection**: CR/LF in path truncates to that point (no bypass)
- **Header injection**: X-Original-URL, X-Rewrite-URL, Host have no effect
- **SSH port forwarding**: direct `direct-tcpip` channels are
  `Administratively prohibited`, so there is no hidden localhost pivot through
  the `ctf@2222` account.

## Encoding Variants Tested

| Encoding | Result | Notes |
|----------|--------|-------|
| `%2e%2e` (single) | 403 | Decoded to `..`, fails validation |
| `%252e%252e` (double) | 404 | Decoded to `%2e%2e` literal, no traversal |
| `%25252e` (triple) | 404 | Same, literal path |
| `/.%2e/` | 403 | Mixed, still fails |
| `/%2e./` | 403 | Mixed, still fails |
| `%2f..%2f` | 403 | Encoded slashes, dots still blocked |

## Alphanumeric Detection Analysis

Confirmed server uses strict ASCII alphanumeric detection:

- 0-9, A-Z, a-z: alphanumeric (dot between these = 404)
- All other ASCII: not alphanumeric (dot adjacent = 403)
- High bytes (≥0x80): 400 Bad Request (ASCII-only enforcement)
- Underscore, hyphen, etc.: not alphanumeric

## Path Enumeration (Comprehensive)

Tested 100+ paths without dots, all 404:

- Common dirs: `/flag`, `/secret`, `/admin`, `/root`, `/home`, `/tmp`
- BBS hints: `/SECRETS`, `/UPLOADS`, `/protected`, `/good_stuff`, `/stacks`
- Challenge hints: `/1986`, `/manual`, `/zmodem`, `/forsberg`, `/ascii`
- Creative: `/the/flag`, `/somewhere/else`, `/proc/self/root/...`

**Document root only contains `not_a_flag`.**

## BBS Buffer Overflow Tests

Tested file #4 override password with:

- Long strings (up to 2048 chars): All accepted, same torrent sent
- Format strings (`%n`, `%s`, `%x`): No effect
- Traversal (`../`): No effect
- Command injection (`;`, `$()`, `` ` ``): No effect

## Remaining Unknowns

1. **The bypass exists but is non-obvious.** The validation checks every `.`
   for alphanumeric neighbors. `..` can never pass. The bypass must be:
   - A parser differential we haven't found
   - A way to access files without using `.` in the path
   - Something in another protocol layer entirely

2. **"1986 manual" hint unexplained.** ZMODEM reverse upload didn't work.
   Other 1986 specs (RFC 977 NNTP, etc.) have no open ports.

3. **Message #4732 "about that thing in the stacks"** — may hint at buffer
   overflow, but tested passwords show no vulnerability

## VPS-based Tests (167.179.91.11)

Tested from external VPS with public IP:

- **ZMODEM ZSKIP**: works correctly. After proper handshake (ZRINIT, ZACK
  for ZSINIT, receive ZFILE), sent ZSKIP to ask server for next file in
  batch. Server responded with **ZFIN** — only one file in batch (no hidden
  second file).
- **ZMODEM malicious ZRPOS**: sent ZRPOS with crafted offsets (0xFFFFFFFF,
  0x80000000, 1000000). Server always responded with ZNAK — no data leak.
- **BitTorrent peer listener**: announced to tracker as seeder, listened
  on port 6881 for 40+ seconds. No incoming peer connections. Swarm is
  dead or fake (one peer IP was our own VPS reflected back).
- **ASCII control characters**: tested all 0x00–0x1F at main menu and
  file library prompts. No hidden triggers — all either "Unknown command"
  or menu redraw.
- **jailHTTPd HTTP verbs**: HEAD, OPTIONS, TRACE, PUT, DELETE, PROPFIND,
  CONNECT all return 405. Request smuggling (CL, TE, double-request) and
  header injection (X-Original-URL, X-Rewrite-URL) have no effect.
- **High-byte / non-ASCII paths**: bytes ≥0x80 return 400 Bad Request.
  Null bytes and backslashes return 403 Forbidden.

## Files

- [challenge.md](/Users/bytedance/Documents/CTF/CIT%202026/Misc/70-ascii-and-ye-shall-receive/challenge.md)
- [challenge.json](/Users/bytedance/Documents/CTF/CIT%202026/Misc/70-ascii-and-ye-shall-receive/challenge.json)
- [README.md](/Users/bytedance/Documents/CTF/CIT%202026/Misc/70-ascii-and-ye-shall-receive/README.md)
- [files/CYPHRPNK.TOR](/Users/bytedance/Documents/CTF/CIT%202026/Misc/70-ascii-and-ye-shall-receive/files/CYPHRPNK.TOR)
- [files/id_ed25519](/Users/bytedance/Documents/CTF/CIT%202026/Misc/70-ascii-and-ye-shall-receive/files/id_ed25519)
- [other/recon-notes.md](/Users/bytedance/Documents/CTF/CIT%202026/Misc/70-ascii-and-ye-shall-receive/other/recon-notes.md)

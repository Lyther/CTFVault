# ASCII and Ye Shall Receive — Recon Notes

## Service Map

- `22/tcp`: OpenSSH, key rejected for tested usernames.
- `80/tcp`: default Apache Ubuntu page.
- `2222/tcp`: SSH with forced `jailHTTPd`.
- `2323/tcp`: `STATION BBS - est. 1993`.
- `6969/tcp`: HTTP BitTorrent tracker.
- `8080/tcp`: simple webseed serving `id_ed25519`.

## Organizer Note

- Official notifications include:

```text
2026-04-19 14:39 UTC  ASCII and Ye Shall Receive fixed  ->  no http
```

- The first public solve followed at `2026-04-19 15:53 UTC`, so the most
  plausible read is that the HTTP stage was missing / broken before the fix and
  became reachable afterwards.

## BBS Details

### News

```text
03/01/94  New file area: /UPLOADS is now open for submissions!
02/25/94  Door game TRADEWARS 2002 upgraded to v3.09.
02/20/94  Second node online! No more busy signals (we hope).
02/14/94  Welcome to new users from 2600 Magazine! Please be cool.
01/31/94  Sysop note: stop leaving garbage in /SECRETS. You know who you
          are. I had to move the good stuff to a protected dir.
```

### Message Subjects

```text
4731  AcidBurn       All            Re: Re: Re: is 2600 still good?
4732  LordNikon      CrashOverride  about that thing in the stacks
4733  ZeroCool       All            PLEASE stop uploading goatse.jpg
4734  ThePlague      All            Hire me.
```

### Who / User List

- `W` shows:

```text
Node 1  GUEST       Main Menu
Node 2  AcidBurn    Playing Trade Wars
```

- `U` shows these registered users:

```text
ZeroCool
AcidBurn
CerealKiller
LordNikon
CrashOverride
ThePlague
```

### Public File Contents

- `WAREZ01.ZIP`:

```text
Yeah right. You actually fell for it?
```

- `DOOM_WAD.ZIP`:

```text
Nice try. This would take 30 minutes at 14.4k and it's just my grocery list.
```

- `PKZIP204G.EXE`:

```text
(not really, just a message: the flag isn't in the public files)
```

- `TRADEWARS.ZIP`:

```text
This is just a text file pretending to be TradeWars. Keep looking.
```

### Locked File #4

- Visible name: `CYPHRPNK.TOR`
- The prompt claims sysop protection, but the override password is fake theater.
- Tested override values include:

```text
test
SECRETS
flag
../../etc/passwd
```

- All tested values returned the same torrent.

## Torrent / Peer Notes

- Torrent file SHA-1: `0b5460950eaba570032c09cd61ab4eeb7f5ee695`
- Info-hash: `0651978ba96851b109d87edaff41133ef2f999f7`
- Torrent metadata:

```text
announce      http://23.179.17.92:6969/announce
comment       FreeBSD 4.10 kernel sources, mirror from cypherpunks.to
created by    Citadel BBS/1.0
creation date 1776607643
name          id_ed25519
length        411
piece length  32768
pieces SHA-1  f7c3c9d4c7e0e192ec5275f5df2ea7144e3345eb
url-list      http://23.179.17.92:8080/
```

- One reachable peer identified itself as `Transmission 4.1.1` with peer id:

```text
-TR4110-6obcxbm16x5g
```

- The peer's `ut_metadata` info dict matches the local torrent exactly. No second torrent or hidden alternate payload was found.

## SSH Key Notes

- `id_ed25519` SHA-1:

```text
f7c3c9d4c7e0e192ec5275f5df2ea7144e3345eb
```

- Embedded key comment:

```text
ctf@23.179.17.92:2222
```

- Key works for `ctf@23.179.17.92:2222`.
- Port `22` rejected the key for the usernames tested so far, including:

```text
ctf
root
ubuntu
guest
ZeroCool
AcidBurn
CerealKiller
LordNikon
CrashOverride
ThePlague
cypherpunk
cypherpunks
bbs
station
sysop
```

## jailHTTPd Notes

### Banner

```text
HTTP/1.0 200 OK
Server: jailHTTPd/0.1 (PROTOTYPE - DO NOT EXPOSE)
Content-Type: text/plain

Welcome to jailHTTPd. This shell speaks HTTP/1.0 and HTTP/1.0 only.
Document root: /var/www/html/
Filesystem is read-only. Only GET is supported.
```

### Public Content

- `GET /` returns the root index.
- `GET /not_a_flag` returns the single decoy HTML page.
- `ssh -p 2222 ctf@23.179.17.92 true` and similar exec-mode requests do not
  escape the jail; the service still prints the banner and closes.

### Parser Behavior

- Literal spaces matter.
- Tabs as separators cause `400 Bad Request`.
- `GET  /not_a_flag HTTP/1.0` resolves to the root index.
- `GET /not_a_flag  HTTP/1.0` still resolves the file.
- `GET /not_a_flag /foo HTTP/1.0` still resolves `/not_a_flag`.
- Query-string routing parameters are ignored.
- Raw `?` and raw `#` are real query / fragment delimiters. Appending either
  to `/not_a_flag` still returns the public file. Percent-encoded `%3f` /
  `%23` do not get this special treatment.
- Absolute URIs are not proxied.
- Plain direct absolute paths outside the jail all tested `404`.
- One long-lived SSH shell channel can service many sequential or pipelined
  GETs. Reusing the same authenticated SSH transport for a second session
  channel does not work; the server tears the transport down after the first
  shell channel closes.

### Path Canonicalization

- Direct slash aliases:

```text
//not_a_flag
///not_a_flag
////not_a_flag
/%2fnot_a_flag
/%2f%2fnot_a_flag
```

all resolve to the public file.

- Dot filter examples:

```text
/a..b    -> 403
/.a      -> 403
/a/.b    -> 403
/a.      -> 403
```

- Benign dotted names like `/a.b` and `/not.a_flag` return `404`, not `403`.

### Traversal Attempts Ruled Out

- Plain `../`
- percent-encoded `..`
- mixed literal/encoded dot-slash variants
- double-encoded `%252e` / `%252f`
- direct `/proc/self/root/...`
- direct `/etc/passwd`
- absolute URI forms such as `http://localhost/...`

No tested `../html/not_a_flag` construction produced the real file through traversal bypass.

Additional naming families ruled out:

- tracker nouns: `/stats`, `/announce`, `/scrape`, `/tracker`
- uppercase nested forms under `/UPLOADS`, `/SECRETS`, `/PROTECTED`
- phrase-with-space paths such as `/good%20stuff`,
  `/thing%20in%20the%20stacks`, `/protected%20dir`, and
  `/protected%20dir/good%20stuff`

### Control Bytes

- Raw `LF` or `CR` inside the request target truncate the path and can still return the file if inserted after `/not_a_flag`.
- Percent-encoded `%0a` and `%0d` do not reproduce that behavior.
- Raw `NUL` in the path does not truncate the server-side path.
- Raw ASCII control-byte sweep on a non-PTY channel found no other useful
  delimiters. `ESC`, `BS`, `DEL`, `Ctrl-X`, and the rest behave like ordinary
  path bytes and lead to `404`, not alternate parsing.

## Upload Branch

- Raw `sz` auto-upload was tested over a binary-clean TCP bridge.
- Results:

```text
main menu         -> Unknown command
file library      -> no upload start, just redraw / idle
file number prompt -> Bad file number
```

- So `/UPLOADS` is not trivially reachable through standard ZMODEM auto-upload from the visible menus.
- The file-number prompt effectively uses the first digit only. `10`, `11`,
  and `12` all transfer file `1`, not hidden entries. So there is no evidence
  for secret public file numbers beyond `1..5`.
- A full `rz` receive of file `4` followed immediately by a naive same-socket
  `sz` does not create a turn-around upload. By the time `sz` starts, the BBS
  is already back at the file-library prompt, and `sz`'s initial `rz\r`
  / pre-header bytes are consumed as menu input.
- Bare raw ZMODEM preheaders also failed as wakeups. Sending plain `ZRQINIT`
  and `ZRQINIT(ZCOMMAND)` hex headers directly at the main menu, file library,
  or file-number prompt produced only normal menu parser behavior:

```text
main menu         -> Unknown command
file library      -> redraw / stay in file library
file number prompt -> Bad file number
```

- That does not fully kill the protocol-level 1986 branch, but it does kill
  the easy versions of it.

## ZMODEM Source Check

- Local `lsz` startup bytes match the BBS file-4 sender behavior.
- Upstream `lrzsz-0.12.20` source confirms the useful limitation:
  ordinary `ZFILE` sending does **not** support a reverse upload handoff.
  The only sender-side `system("rz")` turn-around path lives in
  `lsz.c:zsendcmd()` command mode, not the normal file-send path.
- This makes the "download file 4, then flip direction into /UPLOADS"
  idea effectively dead unless some separate hidden command-mode surface exists.

## 8080 Recheck

- `:8080` is plain `BaseHTTP/0.6 Python/3.12.13`.
- `/` and `/id_ed25519` both return the same private key.
- Raw-socket traversal rechecks show ordinary `404`s only. The earlier
  contradictory `%2e%2e/id_ed25519` result was a client-side artifact from a
  curl-based probe, not a real breakout.

## Other Ports

- `5558/tcp` stayed silent under raw TCP connects and did not answer HTTP,
  SSH, Telnet-ish, or basic ZMODEM handshake probes. No tie to challenge 70
  has surfaced.

## Apache / Vhost Notes

- Port `80` always returned the default Apache page for tested `Host:` values, including:

```text
cypherpunks.to
mirror.cypherpunks.to
freebsd.cypherpunks.to
bbs.cypherpunks.to
station
citadel
uploads
secrets
protected
jailhttpd
zerocool
acidburn
theplague
```

## Current Best Lead

The challenge is bottlenecked on the custom request parser behind `ctf@23.179.17.92:2222`. The BBS, torrent, tracker, webseed, and Apache surfaces have all collapsed into staging or decoy infrastructure. The next useful breakthrough is either:

- a real `jailHTTPd` path canonicalization bug, or
- a non-obvious hidden path name for the moved protected content.

If ZMODEM still matters, the remaining plausible form is a more precise
protocol-aware turn-around / `ZCOMMAND` transaction, not a visible-menu upload.

SSH localhost pivoting is dead as well: authenticated `direct-tcpip` channel
requests through `ctf@23.179.17.92:2222` are `Administratively prohibited`.

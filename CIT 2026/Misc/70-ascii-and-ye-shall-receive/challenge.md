# ASCII and Ye Shall Receive

- ID: 70
- Category: Misc
- Value: 998
- Solves: 3
- Type: dynamic
- Author: hypnos

## Description

Please Hold While Your Packet Is Being Routed Through Different Protocols From Different Decades And One Of Them Requires You To Read A Manual From 1986

## Connection

`23.179.17.92:2323`

## Services

| Port | Service |
|------|---------|
| 2323 | BBS (telnet) with ZMODEM |
| 6969 | BitTorrent tracker |
| 8080 | BitTorrent webseed |
| 2222 | jailHTTPd (HTTP/1.0 over SSH) |

## Artifacts

- `files/id_ed25519` - SSH key for port 2222
- `files/CYPHRPNK.TOR` - Torrent file

## BBS Hints

News: "stop leaving garbage in /SECRETS... moved the good stuff to a protected dir"
Message #4732: "about that thing in the stacks"

## jailHTTPd

**Validation:** `.` only allowed between alphanumeric characters (blocks `..`)
**Doc root:** `/var/www/html/` containing only `not_a_flag`

## Tested Bypasses (All Failed)

- URL encoding: `%2e%2e` decoded before validation
- Double encoding: `%252e%252e` gives 404 (literal path, no traversal)
- CRLF injection: CR truncates path before validation
- Unicode: "ASCII only" rejects non-ASCII
- Control chars: DEL, NULL, TAB - no bypass
- HTTP methods: only GET allowed, case-sensitive
- Headers: X-Original-URL, Host injection - no effect
- Request line tricks: multiple spaces, tab separators - no bypass
- Path parameters: `;` and `@` still validated
- Long paths: validation persists
- Backslash: still blocked

## Key Insight

The validation checks EVERY `.` for alphanumeric neighbors. `..` can never pass since adjacent dots fail.
The bypass must involve a fundamental parser differential or encoding trick not yet discovered.

## BBS File Discovery

File #4 (CYPHRPNK.TOR) is **sysop-locked** with override password required.

- BBS version: 297 bytes
- Webseed version: 305 bytes (already have)
- Password "sysop" triggers ZMODEM transfer but nc can't complete it

The locked BBS torrent may point to a different file (possibly the flag or a different key).

## Next Steps

1. Complete ZMODEM download from BBS (need proper terminal emulator)
2. The locked torrent (297 bytes) may be different from webseed version (305 bytes)
3. Read BBS message #4732 about "the stacks" (may hint at buffer overflow)
4. "1986 manual" = ZMODEM spec - may need specific protocol compliance

## Status

UNSOLVED - Path traversal blocked, ZMODEM transfer incomplete

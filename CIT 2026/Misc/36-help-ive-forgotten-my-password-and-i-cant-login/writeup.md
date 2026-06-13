# Help! I've forgotten my password and I can't login! — Writeup

- **Category:** Misc · **Points:** 986
- **Author:** elemental
- **Flag:** `CIT{Th@nks_4_r3cover1ng_my_p@$$w0rd}`
- **Master password:** `tra358ja`

## Given

- [Database.kdbx](files/Database.kdbx) (2 375 bytes, SHA1 `a7e20fa5c173473caacbe15f786ff61d9cc84074`)
- Challenge text: *"Can you recover the password to my Keepass database, I will forever be in your debt."*

## Header inspection

Parsing the outer KDBX header:

```text
KDBX version : 4.0
cipher       : AES-256-CBC  (UUID 31c1f2e6bf714350be5805216afc5aff)
compression  : gzip
master_seed  : 824ade50150f1fd4c3e312b504c2317799a4df96285d2d20226d92fd5bd4ea5f
KDF UUID     : c9d9f39a628a4460bf740d08c18a4fea   ← AES-KDF (not Argon2)
KDF rounds   : 600 000
KDF salt     : 0922a7c1f83ec16eb33dc38a053ac97e847dc18ce94761706f9d62aaf143e151
IV           : f602c6b4b348118c26dd2bd760d718ad
```

Clean KDBX4 — no `CIT{…}` strings, no leftover `●` (CVE-2023-32784) memory fragments, no trailing bytes past the HMAC end marker. No public KeePass CVE applies to a standalone `.kdbx` offline. This is a plain password-crack challenge.

## The actual blocker — tooling

KDBX4 with AES-KDF is exactly where most popular cracking tools fall over:

| Tool | Supports KDBX4 AES-KDF? |
|---|---|
| `hashcat` mode `13400` | **no** — KDBX 2/3 only |
| `keepass2john` (John 1.9.0-jumbo, Homebrew) | **no** — `File version '40000' is currently not supported!` |
| `pykeepass` / `keepass4brute` (wordlist vs. file) | yes, but CPU-bound: ~1.6 pw/s |
| Custom C cracker (OpenSSL AES-NI, 12 cores) | yes: ~42 pw/s |
| **John `bleeding-jumbo` + `KeePass-opencl`** | **yes** — PR [#5574](https://github.com/openwall/john/pull/5574), merged 2024-11-14 |

`KeePass-opencl` on an NVIDIA L4 benches at 108 379 c/s at the format's reference 24 569 rounds → on our 600 000-round hash the effective rate is **~4 458 c/s**. Full `rockyou.txt` (14 344 391 entries) is therefore ≈ **54 minutes** worst-case — and in our run it hit at **4 m 25 s** (`tra358ja`).

## Solve

```sh
# Build john bleeding-jumbo (one-time)
git clone --depth 1 -b bleeding-jumbo https://github.com/openwall/john.git
cd john/src && ./configure --enable-opencl && make -sj

# Extract KDBX4 hash (this build's keepass2john accepts v4)
./keepass2john Database.kdbx > help.hash

# Crack on GPU
./john --format=KeePass-opencl --wordlist=rockyou.txt help.hash
#  -> tra358ja     (help_db)
#     1g 0:00:04:25 DONE   4704 c/s

# Open the vault and read the flag
python3 -c "
from pykeepass import PyKeePass
kp = PyKeePass('Database.kdbx', password='tra358ja')
for e in kp.entries:
    print(e.title, e.username, e.password)
"
# Bank of America  lol-you-thought  CIT{Th@nks_4_r3cover1ng_my_p@$$w0rd}
```

## What wasted hours before this worked

1. **Homebrew's `john` is 1.9.0-jumbo from 2019** — no KDBX4 support.
2. **`hashcat` mode 13400 isn't it either** — people who read hashcat's format table assume it covers KeePass 4, but mode 13400 only handles the older v3 layout (which exposes an expected-plaintext stream that KDBX4 dropped).
3. **Symptom looks CVE-shaped** — when your tooling rejects a file with "version not supported" it's tempting to hunt a zero-day. Nothing in the public CVE catalog (CVE-2023-32784, CVE-2024-33901, CVE-2023-24055, CVE-2022-0725, etc.) works offline from just a `.kdbx`. It really is just "crack with the right version of john".

## Reproduce

```sh
bash scripts/solve.sh
```

## Key takeaways

- For KDBX4 always reach for **bleeding-jumbo** of John-the-Ripper, specifically `KeePass-opencl` (AES-KDF) or `KeePass-Argon2-opencl`.
- For AES-KDF 600k rounds, expect ~4–5 k c/s on a datacenter GPU (L4); plain rockyou is ~1 h worst-case, which is why this was a ~30-solve challenge despite looking intimidating.
- If `keepass2john` says *"File version '40000' not supported"*, your tool is too old — not your approach.

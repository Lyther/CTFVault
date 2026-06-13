# SAM, I am — Writeup

- Category: Misc
- Value: 764 pts (237 solves)
- Author: elemental

## Challenge

> I dumped the SAM hive and found a document stating the password policy is 5 characters + complexity
>
> `97a3e51e5a006eccac91e0ceabd4965b`

The Windows SAM hive stores account password hashes as **NTLM** (MD4 of UTF-16LE plaintext). The 32-char hex blob is an NTLM hash. Policy: 5 chars + complexity — tiny keyspace.

## Solve

Hashcat mode 1000, mask `?a^5` (all printable ASCII, 95⁵ ≈ 7.7 B candidates). On a modest GPU/CPU it falls in seconds.

```bash
echo 97a3e51e5a006eccac91e0ceabd4965b > sam.hash
hashcat -m 1000 -a 3 sam.hash '?a?a?a?a?a' -o sam.cracked
# 97a3e51e5a006eccac91e0ceabd4965b:C1t!!
```

Rockyou alone doesn't contain `C1t!!` — you must brute the keyspace. Observed speed: ~4.2 GH/s, cracked at ~1.9% progress in ~6 s.

## Flag

```text
CIT{C1t!!}
```

## Files

- [scripts/solve.sh](scripts/solve.sh) — one-shot cracker
- [solution/flag.txt](solution/flag.txt) — recorded submission

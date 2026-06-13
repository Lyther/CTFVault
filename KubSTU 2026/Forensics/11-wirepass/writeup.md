# wirepass — Writeup

- Category: Forensics
- Value: 732
- Author: t.me/thankspluxury

## Challenge

> Arctic intelligence detected anomalous activity in the secret network of the Penguin Command. According to intelligence, operational documents related to the military operation against Capybaraville were being transmitted between two field infrastructure nodes.
>
> Our analysts managed to intercept a network dump, but it turned out the operatives were not so simple: the data was transmitted over an encrypted channel using a custom protocol. Here is `challange.pcap`.

## Recon

The important cleartext leak is on `9999/tcp`:

```text
PASS:IcyFl1pp3r$2026
ACK:OK
```

The actual transfer happens on `31337/tcp`. Concatenating the client payloads gives a 24-byte header and a 3513-byte body. The last part of the body looked structured, so I treated the header core `header[4:20]` as a 16-byte XOR key source and tried byte rotations of that value against the tail.

One rotation cleanly decrypted the ZIP central directory. That exposed three AES-encrypted ZIP entries and their local header offsets:

- `mission_report.txt` at offset `0`
- `roster.txt` at offset `1866`
- `map.txt` at offset `2706`

## Solve

Each ZIP region is XORed with the same 16-byte header core, but with a different rotation:

- local file 1 at `0`: rotation `0`
- local file 2 at `1866`: rotation `10`
- local file 3 at `2706`: rotation `2`
- central directory at `3285`: rotation `5`
- end of central directory at `3491`: rotation `3`

After rebuilding the ZIP archive, open it with the leaked password `IcyFl1pp3r$2026`. The archive contains:

- `mission_report.txt`
- `roster.txt`
- `map.txt`

The flag is in `mission_report.txt`.

## Flag

```text
KubSTU{p1ngu1n_0p_k4p1b4r0v5k_f4ll5}
```

## Files

- [files/11_challenge.pcap](files/11_challenge.pcap)
- [scripts/solve.py](scripts/solve.py)
- [solution/flag.txt](solution/flag.txt)

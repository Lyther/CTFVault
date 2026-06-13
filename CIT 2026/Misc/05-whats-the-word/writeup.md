# What's the word? — Writeup

- Category: Misc
- Value: 927 pts
- Author: bootstrap

## Challenge

> B-b-b-bird, bird, bird! The flag is in the file, but where??
> SHA1: `b2b621068c3632d102c62be9b3cc386c6c175eff`

One file named `file`, no extension.

## Recon

```text
$ file files/file
files/file: CDFV2 Encrypted
$ xxd files/file | head -1
00000000: d0cf 11e0 a1b1 1ae1 ...   <- OLE2 compound document magic
```

OLE2 wrapper + `DataSpaces/` + `EncryptedPackage` + `EncryptionInfo` streams
means a **password-protected modern Office document** (Word/Excel/PowerPoint
OOXML re-wrapped in OLE2 with agile/standard encryption).

## Extract the hash

Use `office2john.py` from John-the-Ripper jumbo (pure Python, only needs
`olefile`):

```text
$office$*2013*100000*256*16*42c71bac48d39fb13c1528f9c39e7b17*
        4aee5a0a38f0e72f05fd413a96f9b03a*
        f377ff864c015f83ad20b8bae2cfaceaa24e196932ecde0813adae4306fc131d
```

`*2013*` tells us this is Office 2013 encryption → **hashcat mode 9600**
(AES-256 + SHA-512, 100 000 iterations).

## Crack

Themed guesses (`bird`, `word`, `theword`, …) and `best66` rules on the theme
all miss — despite the Surfin' Bird hint, the password isn't thematic.

Ship the hash to the L4 GPU box and run rockyou:

```sh
scp office.hash dev-box-gpu:/tmp/
ssh dev-box-gpu 'hashcat -m 9600 /tmp/office.hash /tmp/rockyou.txt -O \
    -o /tmp/office.cracked'
```

On L4 we get ~17 kH/s; cracks in ~15 seconds (first 262k candidates):

```text
$office$*2013*...:q1w2e3r4t5
```

Keyboard walk `q1w2e3r4t5`. Local M3 Pro benched 2.6 kH/s — doable but 7× slower.

## Decrypt & extract

```sh
msoffcrypto-tool -p 'q1w2e3r4t5' files/file solution/decrypted.docx
unzip -j solution/decrypted.docx word/media/image1.png -d solution/
```

The decrypted `.docx` contains only a single embedded PNG
(`word/media/image1.png`). Opening it reveals the flag rendered on top of a
stock landscape photo.

## Flag

```text
CIT{b1rd_1s_th3_w0rd}
```

## Files

- [files/file](files/file) — original encrypted container
- [scripts/solve.sh](scripts/solve.sh) — end-to-end pipeline
- [solution/office.hash](solution/office.hash) — hashcat-format hash
- [solution/decrypted.docx](solution/decrypted.docx) — after password removal
- [solution/image1.png](solution/image1.png) — embedded image with the flag
- [solution/flag.txt](solution/flag.txt) — recovered flag

# Writeup: Catacombs

- Category: Reverse Engineering
- Value: 751 pts (250 solves)
- Author: ronnie
- Status: **SOLVED**

## Challenge

We are given a Linux ELF 64-bit statically linked executable named `catacombs`. The description just says "good luck".

## Solution

Since it's a reverse engineering challenge, the first step is always to run basic static analysis tools like `strings` to see if the flag is stored in plaintext within the binary.

We uploaded the binary to our remote dev box and ran `strings` on it, filtering for the flag format `CIT{`:

```bash
strings catacombs | grep -i "CIT{"
```

This immediately revealed the flag in plaintext! No complex reverse engineering or dynamic analysis was needed.

## Flag

```text
CIT{3R2rA2J0PdFH}
```

# Writeup: Say My Name

- Category: Reverse Engineering
- Value: 822 pts (179 solves)
- Author: ronnie
- Status: **SOLVED**

## Challenge

We are given a Linux ELF 64-bit statically linked executable named `saymyname`. The description just says "Say My Name!".

## Solution

Similar to the previous challenge, we can start with basic static analysis. We uploaded the binary to our remote dev box and ran `strings` on it, filtering for the flag format `CIT{`:

```bash
strings saymyname | grep -i "CIT{"
```

This immediately revealed the flag in plaintext as part of a success message: `yeah that me. heres your flag CIT{Zn583Umnwd4S}`. No further reverse engineering was needed.

## Flag

```text
CIT{Zn583Umnwd4S}
```

# Start Me Up — Writeup

- Category: Forensics
- Value: 1000
- Author: boom

## Challenge

> Are we dealing with TrickBot here or something? What's with the persistence?!
>
> Use the challenge.zip from "The click that may have fixed" to solve this challenge :)

## Recon

The hint is persistence, so the first place to check in the reused backup is the user Startup folder:

```text
AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup/
```

That folder contains an odd file:

```text
e9fje2.txt
```

## Solve

The file contents are base64:

```text
Q0lUe3N0NHJ0X20zX3VwX2kxMV9uM3Yzcl9zdDBwfQ==
```

Decoding it gives the flag directly:

```text
CIT{st4rt_m3_up_i11_n3v3r_st0p}
```

## Flag

```text
CIT{st4rt_m3_up_i11_n3v3r_st0p}
```

## Files

- [challenge.zip](files/challenge.zip)
- [solve.py](scripts/solve.py)
- [e9fje2.txt](other/e9fje2.txt)
- [e9fje2.decoded.txt](other/e9fje2.decoded.txt)

# Autonomous — Writeup

- Category: Forensics
- Value: 987
- Author: boom

## Challenge

> Let's dig a little deeper into where this script might be coming from. What is the ASN associated clickfix site?
>
> **FLAG FORMAT:** `CIT{XXXXXX}`

## Recon

This challenge continues the same ClickFix backup from `The click that may have fixed`.

The fake site already appears in the reused Edge history:

```text
10|https://23.179.17.92:5067/|Download More RAM!|2026-04-18 07:07:26|1
```

So the host we care about is `23.179.17.92`.

## Solve

Resolve that IP to its ASN.
I used Team Cymru and saved the response in `other/cymru.txt`:

```text
AS      | IP               | BGP Prefix          | CC | Registry | Allocated  | AS Name
399562  | 23.179.17.92     | 23.179.17.0/24      | US | arin     | 2022-11-30 | IZT-CLOUD-UNIVERSAL - IZT Cloud, US
```

The ASN is `399562`.

## Flag

```text
CIT{399562}
```

## Files

- [challenge.zip](files/challenge.zip)
- [solve.py](scripts/solve.py)
- [history-hit.txt](other/history-hit.txt)
- [cymru.txt](other/cymru.txt)

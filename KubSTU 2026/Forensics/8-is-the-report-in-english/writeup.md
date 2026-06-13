# Is the report in English? — Writeup

- Category: Forensics
- Value: 304
- Author: @Alkimor1

## Challenge

> На почту пришёл странный файл — финансовый отчёт, да ещё и на английском.
>
> Формат флага: `KubSTU{...}`
>
> A strange file arrived by email — a financial report, and it's in English too.
>
> Flag format: `KubSTU{...}`

## Recon

The PDF renders as a normal two-page financial report, but parser tools immediately complain:

```text
Syntax Error: Dictionary key must be a name object
Syntax Error: Bad 'Length' attribute in stream
Warning: Invalid xref table
```

The visible content also includes an embedded ZIP and password:

```text
ARCHIVE FILENAME: KUBGTU_FINANCIAL_DATA_2025.ZIP
ARCHIVE ACCESS PASSWORD: FinanceKubSTU2025!
```

Extracting that embedded file works, but it only contains a fake flag and a warning message.

## Solve

The real payload sits in the malformed trailer metadata, inside the giant `/HiddenAuditData (...)` string. One of the hidden fields is:

```text
DATA[9376]="S3ViU1RVe1BERl9NM3Q0ZDR0NF9GMHIzbnMxY3NfNGR2NG5jM2RfQ2g0bGwzbmczXzIwMjVfUzNjdXIzX0VtYjNkZDNkX0YxbDNfM25jcnlwdDEwbl9QcjB0MGMwbH0="
```

Base64-decoding that value gives the real flag.

## Flag

```text
KubSTU{PDF_M3t4d4t4_F0r3ns1cs_4dv4nc3d_Ch4ll3ng3_2025_S3cur3_Emb3dd3d_F1l3_3ncrypt10n_Pr0t0c0l}
```

## Files

- [8_KUBSTU_Financial_Report_2025.pdf](files/8_KUBSTU_Financial_Report_2025.pdf)
- [solve.py](scripts/solve.py)

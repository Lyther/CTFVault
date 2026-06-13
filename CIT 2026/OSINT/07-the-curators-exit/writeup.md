# The Curator's Exit — Writeup

- Category: OSINT
- Value: 982 pts
- Author: elemental

## Challenge

> We've received a communication from Interpol, containing a PDF. We are unsure of the contents, but believe it contains information on one of the thieves from the Louvre Heist. Your job is to find out as much as you can about this individual and send the information back to the authorities.
>
> What is the thief's name?
>
> **FLAG FORMAT:** `CIT{First_Last}`
>
> **SHA1:** `c3c8f91ed60e902be482dc26b61a9bc0fa443f26`

## Recon

The attachment `VF0000000011-Enc.pdf` is an encrypted PDF. Cracking it with `pdf2john` + a wordlist gives the password `cherell`.

After decryption, the dossier gives the online persona, not the legal name:

- Primary handle: `VitrineFox`
- Aliases: `vitrine_fox`, `FoxInGlass`, `Curator’s_Exit`, `VF-9`, `SalleDenonGhost`
- Signature phrase: `Glass is a promise.`

That is only the starting point. The PDF explicitly redacts the legal name, so `CIT{Vitrine_Fox}` is a dead end.

## Solve

Using the dossier handles, the public profile chain is:

`VitrineFox` -> X profile -> Linktree -> LinkedIn profile

The useful leak is the LinkedIn contact card. It exposes the email address:

`remy.beauvillier@proton.me`

That gives the thief's real name as `Remy Beauvillier`, which matches the required `First_Last` flag format.

## Flag

```text
CIT{Remy_Beauvillier}
```

## Files

- [scripts/solve.py](scripts/solve.py)
- [solution/flag.txt](solution/flag.txt)

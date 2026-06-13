# Nintendo 3DS — Writeup

- Category: Crypto
- Value: 799
- Author: @ST47IC4

## Challenge

> Слушай, я всё не могу запомнить название алгоритма, но что-то очень похожее на Nintendo 3DS, помоги разобраться что там вообще было написано^^
>
> Формат флага KubSTU{}
>
> ---
>
> Hey, I just can't remember the name of the algorithm, but it's something very similar to Nintendo 3DS. Help me figure out what was written there^^
>
> Flag format: KubSTU{}

## Solve

The title points to `3DES`. The file gives `CBC+PKCS5`, three key chunks, two IV chunks, and the ciphertext.

Decode the key chunks:

```text
1 = base64("TjFudDNuZG8=") = N1nt3ndo
2 = decimal ASCII = S3cur1ty
3 = hex = K3y!2026
```

The 24-byte 3DES key is their concatenation. The IV is `ivx XOR ivm`, which gives:

```text
G4m3C4rd
```

Decrypting with 3DES-CBC and removing PKCS#5 padding gives the flag.

```bash
uv run scripts/solve.py
```

## Flag

```text
KubSTU{3d3s_n1nt3nd0_cbc_m0d3_n07_h4rd_3n0ugh}
```

## Files

- [output_2.txt](./files/45_output_2.txt)
- [solve.py](./scripts/solve.py)

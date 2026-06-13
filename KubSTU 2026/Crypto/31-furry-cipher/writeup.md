# Furry Cipher — Writeup

- Category: Crypto
- Value: 628

## Challenge

> Пролистывал свою почту и увидел письмо от FurryHater_2009) с просьбой расшифровать какое-то странное сообщение, а также он прикрепил два файла.
>
> Формат флага KubSTU()
>
> ---
>
> I was scrolling through my email and saw a message from FurryHater_2009) asking to decrypt some strange message, and he also attached two files.
>
> Flag format: KubSTU()

## Solve

The zip contains the cipher script and a huge mostly-punctuation text file. The script encrypts only alphanumeric characters and preserves `(`, `)`, and `_`.

Filtering `Weird_Furry_text.txt` down to `[A-Za-z0-9()_]` gives the sparse ciphertext:

```text
XiEDJ5(9tV_qY3_v43_t9B3_o9vo_ESM_YR_YA_t_S5t8v_XYL4jt)
```

Using the known prefix `KubSTU(` recovers the three effective position additions for the custom affine cipher. Decrypting the sparse ciphertext gives the flag.

```bash
uv run scripts/solve.py
```

## Flag

```text
KubSTU(h0w_d1d_you_re4d_7ha7_br0_1t_1s_a_furry_c1pher)
```

## Files

- [Furry_Cipher.zip](./files/31_Furry_Cipher.zip)
- [solve.py](./scripts/solve.py)

# Unlucky 13 — Writeup

- Category: Crypto
- Value: 757
- Author: @ST47IC4

## Challenge

> 13 - несчастливое число. Три слоя шифрования, тринадцать причин не пытаться это расшифровать.
> Кое-что утекло, надеюсь хоть это тебе поможет.
>
> Формат флага KubSTU{}
>
> ---
>
> 13 is an unlucky number. Three layers of encryption, thirteen reasons not to try to decrypt this.
> Something leaked — hopefully it will help you.
>
> Flag format: KubSTU{}

## Solve

The leaked encryptor applies three layers:

1. XOR with the `cursed_prng(13, len(flag))` stream.
2. A reversible RC4-like cipher keyed by `sha256(b"Unlucky13").digest()[:16]`.
3. Textbook RSA with `e = 3`.

The RSA plaintext is small enough that `m^3 < n`, so `c` is an exact integer cube. Taking the cube root recovers layer 2, then the RC4-like layer and XOR stream can be reversed directly.

```bash
uv run scripts/solve.py
```

## Flag

```text
KubSTU{unLucky_13_l4y3r5_0f_encrypt10n_n0_luck_h3r3}
```

## Files

- [Unlucky_13.zip](./files/46_Unlucky_13.zip)
- [solve.py](./scripts/solve.py)

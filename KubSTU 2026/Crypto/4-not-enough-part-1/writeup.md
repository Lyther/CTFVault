# Not enough part 1 — Writeup

- Category: Crypto
- Value: 100
- Author: @ST47IC4

## Challenge

> Во время дампа системы часть параметров оказалась повреждена: от `p` сохранились только часть бит, последние 72 бита были потеряны. Затем из восстановленных параметров был получен ключ путём хеширования секрета (ещё уцелело это, по-моему, AES-GCM?).
>
> Формат флага: `KubSTU{...}`
>
> ---
>
> During a system dump, some parameters were corrupted: the last 72 bits of `p` were lost. Then, from the recovered parameters, a key was derived by hashing the secret (I think it was AES-GCM?).
>
> Flag format: `KubSTU{...}`

## Solve

`p_hi` is `p >> 72`, so write:

```text
p = p_hi * 2^72 + x
```

The unknown `x` is small. Build a Coppersmith lattice for `f(x) = p_hi * 2^72 + x` modulo `N`; LLL gives:

```text
x = 1277292877421571572747
```

That recovers `p`, then `q`, then the RSA private exponent `d`. The AES-GCM key is:

```python
sha256(long_to_bytes(d)).digest()[:16]
```

Decrypting the ciphertext with the recovered key gives the flag.

```bash
uv run scripts/solve.py
```

## Flag

```text
KubSTU{1_h0p3_y0u_solv3d_7hi5_wi7h0ut_4ny_pr0bl3m5}
```

## Files

- [output.txt](./files/4_output.txt)
- [solve.py](./scripts/solve.py)

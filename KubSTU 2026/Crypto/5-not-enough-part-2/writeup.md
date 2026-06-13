# Not enough part 2 — Writeup

- Category: Crypto
- Value: 999
- Author: @ST47IC4

## Challenge

> Во время аварийного `g`восстановления системы были сохранены лишь фрагменты двух ***-ключей. От каждого простого числа уцелели только `c` старшие биты, а младшие были `??????`. После восстановления закрытых параметров из них был сформирован мастер-секрет, который затем `m`через KDF был превращён в ключ для чего-то.
>
> Формат флага: `KubSTU{...}`
>
> ---
>
> During an emergency system recovery, only fragments of two ***-keys were saved. Only the top `c` bits of each prime number survived, while the lower bits were `??????`. After recovering the private parameters, a master secret was formed from them, which was then converted through KDF into a key for something.
>
> Flag format: `KubSTU{...}`

## Recon

The text dump leaks the structure directly:

- `lost2` in dump A means `72` lost low bits.
- `lost0` in dump B means `80` lost low bits.
- `1sha256(secret1 || secret2)6` means SHA-256 followed by a `16`-byte key cut.
- The stray letters `g`, `c`, `m` point to AES-GCM.

`dump_b` matches the obvious model:

```text
p2 = (hint2 << 80) + x2
```

with:

```text
x2 = 1069912754115005437856435
```

The blocker was `dump_a`: the normal prefix model did not divide the printed modulus.

## Solve

The key observation is that `dump_a` is not mathematically inconsistent; the printed decimal value of `n1` is corrupted.

At decimal index `234`, the substring:

```text
36
```

must be replaced with:

```text
03
```

So the bad fragment:

```text
...1522135923953913623036666133850180216800...
```

becomes:

```text
...1522135923953913623003666133850180216800...
```

After that, dump A fits the same recovery model:

```text
p1 = (hint1 << 72) + x1
```

with:

```text
x1 = 807033928375566434623
```

Then both RSA keys factor normally, the private exponents are recovered, and the KDF is:

```text
key = sha256(long_to_bytes(d1) + long_to_bytes(d2)).digest()[:16]
```

Using that 16-byte key with the provided AES-GCM nonce, ciphertext, and tag decrypts the final message.

## Flag

```text
KubSTU{1_h0p3_y0u_solv3d_7hi5_p4rt2_th1s_1s_much_h4rd3r}
```

## Files

- [output_1.txt](./files/5_output_1.txt)
- [solve.py](./scripts/solve.py)

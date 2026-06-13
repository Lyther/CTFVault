# Base — Writeup

- Category: Crypto
- Value: 100
- Author: @ST47IC4

## Challenge

> Мы перехватили странное сообщение. Кажется, оно закодировано популярным методом. Помоги понять, что там написано.
>
> Формат флага: `KubSTU(...)`
>
> ---
>
> We intercepted a strange message. It seems to be encoded using a popular method. Help us figure out what it says.
>
> Flag format: `KubSTU(...)`

## Solve

The attachment is a Base64 string:

```text
S3ViU1RVKGI0czNfNjRfMXNfdGhlX2JhNWk1KQ==
```

Decoding it gives the flag.

```bash
uv run scripts/solve.py
```

## Flag

```text
KubSTU(b4s3_64_1s_the_ba5i5)
```

## Files

- [Base.txt](./files/3_Base.txt)
- [solve.py](./scripts/solve.py)

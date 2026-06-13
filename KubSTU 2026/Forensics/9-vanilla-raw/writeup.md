# Vanilla raw — Writeup

- Category: Forensics
- Value: 884
- Author: @Alkimor1

## Challenge

> Нам передали дамп оперативной памяти, но почему-то мы не можем его проанализировать, помоги нам.
>
> Формат флага: `KubSTU{...}`
>
> We received a RAM dump, but for some reason we can't analyze it. Help us out.
>
> Flag format: `KubSTU{...}`

## Recon

`memory.raw` is 2 GB, but almost the entire file is zeroes. A chunk scan shows only one non-zero region:

- first non-zero byte: `0x3df027ed`
- last non-zero byte: `0x3df03088`

So this is not a normal RAM image. The useful data is a tiny blob embedded inside a sparse raw file.

## Solve

Extract that non-zero blob and test byte lanes. The correct data is in the `0 mod 4` lane:

```python
candidate = blob[0::4]
```

Searching that de-interleaved stream immediately reveals the flag.

## Flag

```text
KubSTU{m3m0ry_unl1nk3d_tmpfs_f0r3ns1cs}
```

## Files

- [files/9_memory.rar](files/9_memory.rar)
- [scripts/solve.py](scripts/solve.py)
- [solution/flag.txt](solution/flag.txt)

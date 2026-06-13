# Cat-girl conspiracy — Writeup

- Category: Crypto
- Value: 936
- Author: @ST47IC4

## Challenge

> Слушай, какой-то странный это архив, ещё и название какое-то странное??
> Разберись с этим как только сможешь, пожалуйста
> Формат флага KUBSTU{}
>
> ---
>
> Listen, this is a strange archive, and the name is weird too??
> Deal with this as soon as you can, please.
> Flag format: KUBSTU{}

## Solve

The archive contains many JPGs in character-named folders and one file named `what_could_this_mean.txt`.

`what_could_this_mean.txt` is a continuous hex string. Splitting it into 64-character chunks gives SHA-256 digests. For each digest, hash the JPG files in the archive, find the matching path, and take the top-level folder name as the next flag character.

```bash
uv run scripts/solve.py
```

## Flag

```text
KUBSTU{A7_LE4ST_N0W_Y0U_H4V3_A_BUNCH_0F_P1CTUR3S_OF_C4T_GIRL5}
```

## Files

- [64_what_could_this_mean.zip](./files/32_64_what_could_this_mean.zip)
- [solve.py](./scripts/solve.py)

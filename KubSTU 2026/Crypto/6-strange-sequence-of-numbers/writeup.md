# Strange sequence of numbers — Writeup

- Category: Crypto
- Value: 100
- Author: @ST47IC4

## Challenge

> Получил странный документ с числами внутри, что это может значить?
>
> Формат флага: `KubSTU(...)`
>
> ---
>
> I received a strange document with numbers inside. What could it mean?
>
> Flag format: `KubSTU(...)`

## Solve

The attachment contains decimal ASCII byte values. Converting each number with `chr()` reconstructs the flag.

```bash
uv run scripts/solve.py
```

## Flag

```text
KubSTU(asc11_c0d3s_ar3_an_1nteresting_w4y_to_ge7_into_cryp70graphy)
```

## Files

- [strange_sequence_of_numbers.txt](./files/6_strange_sequence_of_numbers.txt)
- [solve.py](./scripts/solve.py)

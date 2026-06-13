# The Ancient Note — Writeup

- Category: Stego
- Value: 100
- Author: @van_1pi

## Challenge

> Нам дан текстовый файл ancient_note.txt — якобы старинная рукопись из заброшенной библиотеки. Текст на английском языке, философские размышления о поиске скрытой истины.
>
> We are given a text file ancient_note.txt — supposedly an ancient manuscript from an abandoned library. The text is in English, philosophical reflections on the search for hidden truth.

## Recon

The text looks normal at first, but the first block contains lots of invisible Unicode characters between letters.

Dumping the file with escaped characters shows two zero-width code points repeated throughout the heading and opening paragraph:

```text
T\342\200\213h\342\200\214e\342\200\213 ...
```

Those bytes are:

- `U+200B` zero-width space
- `U+200C` zero-width non-joiner

## Solve

Treat the invisible characters as bits:

- `U+200B = 0`
- `U+200C = 1`

Reading all zero-width characters in order and decoding them as 8-bit ASCII yields:

```text
KubSTU{h1dd3n_truth_b3tw33n}
```

## Flag

```text
KubSTU{h1dd3n_truth_b3tw33n}
```

## Files

- [50_ancient_note.txt](files/50_ancient_note.txt)
- [solve.py](scripts/solve.py)

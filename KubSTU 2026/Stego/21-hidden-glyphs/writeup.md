# Hidden Glyphs — Writeup

- Category: Stego
- Value: 100
- Author: @van_1pi

## Challenge

> Категория: Steganography / Forensics. Сложность: HARD.
>
> Наш агент получил зашифрованный документ от информатора. Визуально это обычный PDF, но мы уверены, что в нём скрыто секретное послание.
>
> Говорят, что "ширина взгляда определяет глубину понимания".
>
> Найдите флаг.
>
> Формат: `KubSTU{...}`
>
> Category: Steganography / Forensics. Difficulty: HARD.
>
> Our agent received an encrypted document from an informant. Visually, it's a regular PDF, but we are confident that a secret message is hidden in it.
>
> They say that "the breadth of one's view determines the depth of understanding."
>
> Find the flag.
>
> Format: `KubSTU{...}`

## Recon

The PDF is not encrypted, so the first step is to inspect its internals instead of treating it like an image.

`pdftotext` gives away the core hint:

```text
Hint: The font hides more than you see...
Each glyph has a width. What do they tell?
```

Inspecting the PDF source shows that the visible title and alphabet lines use a custom Type 3 font. The font dictionary points at object `70 0 obj`, which contains the `/Widths` array for character codes `48..122`.

## Solve

Those widths are not normal metrics. Dividing each width by `10` turns the values into ASCII codes:

```text
750  -> 75  -> K
1170 -> 117 -> u
980  -> 98  -> b
830  -> 83  -> S
840  -> 84  -> T
850  -> 85  -> U
1230 -> 123 -> {
...
1250 -> 125 -> }
```

Decoding the width table from left to right yields:

```text
KubSTU{typ3_3_f0nt_w1dth5_4r3_tr1cky}2222222222222222222222222
```

The trailing `2`s come from unused glyph slots that all have width `500`, so the flag is the substring up to the first closing brace.

## Flag

```text
KubSTU{typ3_3_f0nt_w1dth5_4r3_tr1cky}
```

## Files

- [21_stego_challenge.pdf](files/21_stego_challenge.pdf)
- [solve.py](scripts/solve.py)

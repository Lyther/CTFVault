# Meow Message — Writeup

- Category: Stego
- Value: 100
- Author: @van_1pi

## Challenge

> Категория: Стеганография. Сложность: Easy.
>
> Дан текстовый файл `message.txt` с ASCII-артом котика и стишком на русском языке. На первый взгляд — просто милая картинка с текстом.
>
> Подсказка: "Не всё, что кажется пустым, на самом деле пусто".
>
> Формат флага: `KubSTU{...}`
>
> Category: Steganography. Difficulty: Easy.
>
> A text file `message.txt` is given containing an ASCII art cat and a poem in Russian. At first glance — just a cute picture with text.
>
> Hint: "Not everything that seems empty is actually empty."
>
> Flag format: `KubSTU{...}`

## Recon

The visible content is just the cat and poem, but every line also ends with hidden spaces and tabs.

Printing the file with escaped whitespace makes that obvious:

```text
    /\_____/\ \t  \t \t\t
   /  o   o  \ \t\t\t \t \t
  ( ==  ^  == ) \t\t   \t
...
```

Each line has exactly 8 trailing whitespace characters, which strongly suggests one byte per line.

## Solve

Interpret the trailing whitespace after each visible line as bits:

- `space = 0`
- `tab = 1`

That yields these bytes:

```text
01001011
01110101
01100010
01010011
01010100
01010101
01111011
01110111
01101000
00110001
01110100
00110011
01011111
01110011
01110000
00110100
01100011
00110011
01111101
```

ASCII-decoding those bytes gives the flag.

## Flag

```text
KubSTU{wh1t3_sp4c3}
```

## Files

- [23_message.txt](files/23_message.txt)
- [solve.py](scripts/solve.py)

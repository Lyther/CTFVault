# Capybara in Nightmare Land — Writeup

- Category: Stego
- Value: 861
- Author: @van_1pi

## Challenge

> Капибара из КубГТУ заснула на лекции по информационной безопасности и попала в странный кошмарный сон...
>
> В этом сне она оставила секретное послание. Сможешь ли ты найти его?
>
> Подсказка: Не всё то, чем кажется. Загляни глубже.
>
> A capybara from KubGTU fell asleep during an information security lecture and found herself in a strange nightmare...
>
> In this dream, she left a secret message. Can you find it?
>
> Hint: Not everything is as it seems. Look deeper.

## Recon

The PNG has extra data after the `IEND` chunk. `binwalk` identifies that trailer as a ZIP archive with two files:

- `README.txt`
- `encrypted_flag.bin`

The README explains the setup:

```text
The flag is XOR encrypted.
The key is hidden in the original image...
Look closer at the pixels!
Hint: LSB (Least Significant Bit)
Password length: 19 characters
```

## Solve

Reading the least significant bit of each RGB channel in row-major order reveals an ASCII string right at the start of the image data:

```text
N1ghtm4r3_C4py_2026
```

That is the 19-byte XOR key. Decrypting `encrypted_flag.bin` with the repeating key gives:

```text
KubSTU{H0ly_M0ly_CapyHaCk1r}
```

## Flag

```text
KubSTU{H0ly_M0ly_CapyHaCk1r}
```

## Files

- [33_capybara_nightmare.png](files/33_capybara_nightmare.png)
- [solve.py](scripts/solve.py)

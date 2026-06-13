# Mutant — Writeup

- Category: Forensics
- Value: 898
- Author: @Alkimor1

## Challenge

> Поздравляю! Вы поступили в политех на информационную безопасность. Вам выдали образовательный материал. Завтра экзамен, удачи.
>
> Congratulations! You've been admitted to the polytechnic university for information security. You were given educational materials. The exam is tomorrow, good luck.

## Recon

The PDF renders as a normal one-page crypto handout, but text extraction throws:

```text
Syntax Error: Unknown compression method in flate stream
```

That points at a broken or intentionally mislabeled stream. The raw PDF shows:

```text
5 0 obj
<< /Length 1509 /Filter /FlateDecode >>
stream
<~ ... ~>
endstream
```

The payload is clearly Adobe ASCII85, not raw Flate data.

## Solve

Decode object `5` as:

1. strip the `<~ ... ~>` wrapper
2. ASCII85-decode
3. zlib-decompress

The decompressed stream is another PDF text-content stream with many decoys and fake flags mixed in. Since the real flag format is `KubSTU{...}`, a direct regex over the decoded content pulls the correct one immediately.

## Flag

```text
KubSTU{pdf_0bj3ct_m4st3r_v2}
```

## Files

- [files/30_crypt.pdf](files/30_crypt.pdf)
- [scripts/solve.py](scripts/solve.py)
- [solution/flag.txt](solution/flag.txt)

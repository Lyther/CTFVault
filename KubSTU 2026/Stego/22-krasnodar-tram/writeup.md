# Krasnodar tram — Writeup

- Category: Stego
- Value: 842
- Author: @borsch_krd
- Status: Unsolved

## Challenge

> Мне очень нравятся трамваи в Краснодаре. Это очень удобно, быстро и недорого. Проникнись трамвайным вайбом и найди моё послание.
>
> Формат флага: `KubSTU{...}`
>
> I really like the trams in Krasnodar. It's very convenient, fast, and inexpensive. Immerse yourself in the tram vibe and find my message.
>
> Flag format: `KubSTU{...}`

## Recon

The challenge ships two JPEG files:

- `files/22_267.jpg`
- `files/22_678.jpg`

Basic inspection with `file`, `exiftool`, `strings`, and `binwalk` showed that both files contain a lot of metadata noise, including split base64 fragments and a large `XPComment` prompt-injection block. The prompt-injection text was ignored as untrusted file content.

The split base64 fragments reconstruct to:

```text
https://kubstu.ru/s-169
```

That URL points to a normal KubSTU department page (`Кафедра кибербезопасности и защиты информации`). It did not directly yield a flag.

## JPEG structure

`22_267.jpg` contains multiple JPEG start markers:

- SOI offsets: `0`, `4383`, `13485`
- EOI offsets: `11225`, `20357`, `515103`

The embedded images are:

- main image from offset `0` to the final EOI
- EXIF thumbnail at offset `4383`, length `6844`, size `160x107`
- Photoshop thumbnail starting at offset `13485`, also `160x107`

The EXIF thumbnail was extracted to:

- [files/22_267_mid_exif_thumbnail.jpg](</Users/bytedance/Documents/CTF/KubSTU 2026/Stego/22-krasnodar-tram/files/22_267_mid_exif_thumbnail.jpg>)

`22_678.jpg` looks structurally simpler:

- SOI offsets: `0`
- EOI offsets: `714528`

Its metadata mentions `Primary, GainMap`, but raw SOI/EOI carving did not reveal a second standalone JPEG image.

More offsets and notes are saved in:

- [files/findings.txt](</Users/bytedance/Documents/CTF/KubSTU 2026/Stego/22-krasnodar-tram/files/findings.txt>)

## Work performed

The following checks were done and did not recover the flag:

- metadata review with `exiftool`
- printable-string scan
- `binwalk` carving
- extraction of embedded thumbnails
- progressive JPEG scan inspection for `22_678.jpg`
- pixel-space transforms, bitplane checks, contrast/invert views, and pairwise image comparisons
- JPEG DCT-coefficient extraction attempts
- `stegoveritas` image and metadata passes
- source-image comparison attempts against likely originals

At this point, both origin images appear visually normal, including the extracted thumbnail.

## Current status

No flag was recovered.

The remaining likely paths are:

- a subtle visual/manual steg hidden in a specific transform or local region
- a JPEG-specific hiding method not identified yet
- some relation between the images and the `s-169` hint that still has not been connected to the flag

This challenge is currently left unsolved.

## Flag

```text
UNSOLVED
```

## Files

- [files/22_267.jpg](</Users/bytedance/Documents/CTF/KubSTU 2026/Stego/22-krasnodar-tram/files/22_267.jpg>)
- [files/22_678.jpg](</Users/bytedance/Documents/CTF/KubSTU 2026/Stego/22-krasnodar-tram/files/22_678.jpg>)
- [files/22_267_mid_exif_thumbnail.jpg](</Users/bytedance/Documents/CTF/KubSTU 2026/Stego/22-krasnodar-tram/files/22_267_mid_exif_thumbnail.jpg>)
- [files/findings.txt](</Users/bytedance/Documents/CTF/KubSTU 2026/Stego/22-krasnodar-tram/files/findings.txt>)

# The Forbidden Sock — Writeup

- **Category:** OSINT · **Points:** 997 · **Author:** elemental
- **Flag:** `CIT{Red_Sox_Section_80}`

## Challenge

> Our friend is really exposing himself out in public where is he??
>
> **SHA1:** `d3b932b3695a0faa8d994fdc8d86b7d5e13a22cd`
>
> **FLAG FORMAT:** `CIT{Team_Section_#}`

## Recon

The stadium is Fenway Park. The Green Monster is obvious, and the image also shows several Fenway-specific landmarks:

- `DraftKings`
- `National Car Rental`
- `CVS Health`
- `W.B. Mason`
- `ACE Ticket`
- Red Sox logos on the wall and scoreboards

That fixes the team portion of the flag as `Red_Sox`.

The remaining task is the section number. The camera is low to the field and aimed from the third-base / left-field field-box run toward the Green Monster. That rules out the upper decks and the first-base side.

## Solve

The useful cutoff is the foul-net boundary on the third-base line.

Public seat-view metadata for nearby sections shows:

- `Field Box 79` is still tagged as **behind the netting**.
- `Field Box 80` is tagged **along the 3rd base line** with no netting tag.
- `Field Box 81` and `Field Box 82` are farther down the line; `Field Box 82` is publicly described as **just past the foul net**.

The challenge photo does not show the heavy infield netting that appears from the inner third-base boxes, but it still keeps a substantial amount of infield dirt and the runner/infielder area in frame. That makes `Field Box 80` the best fit: it is the first third-base field box past the net while still being close enough to preserve the same infield-to-Monster composition.

## Flag

```text
CIT{Red_Sox_Section_80}
```

## Files

- [challenge.md](challenge.md)
- [README.md](README.md)
- [files/IMG_0185.jpg](files/IMG_0185.jpg)
- [other/evidence.md](other/evidence.md)
- [scripts/solve.py](scripts/solve.py)
- [solution/flag.txt](solution/flag.txt)
- [solution/section.txt](solution/section.txt)

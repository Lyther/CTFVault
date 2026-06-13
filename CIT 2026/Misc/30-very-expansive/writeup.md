# Writeup: Very Expansive

- Category: Misc (trivia / fandom)
- Value: 865 pts
- Author: bootstrap

## Flag

`CIT{Mariner_Valley}`

## TL;DR

The title is a pun on *The Expanse*. *Beratna* and *mi pensa* are Belter Creole; *Dusters* is a slur for Martians. *Wide, wide world of sports* points at a Martian location known for sports in-universe: **Mariner Valley**.

## Recon

Prompt:

> Where in the wide, wide world of sports is this, beratna? Good place for Dusters, mi pensa.
>
> FLAG FORMAT: `CIT{Name_of_Place}` — Example: `CIT{Grand_Canyon}`

| Clue | Reading |
|------|--------|
| **Very Expansive** (title) | Wordplay on ***The Expanse***. |
| **beratna** | Belter Creole for *brother* / *bro*. |
| **mi pensa** | Belter Creole for *I think*. |
| **Dusters** | Pejorative for **Martians** (Mars as a dusty world). |
| **wide, wide world of sports** | Echoes a famous line from *Blazing Saddles*; here it is reused to mean “sports culture” in the story world, not a filming location on Earth. |

## Solve

1. Recognize the Belter words and *Dusters* as *Expanse* vocabulary → the answer is a **named place in that fiction**, not a random geocode puzzle.
2. “Good place for Dusters” → a **Martian** settlement or region.
3. “Wide, wide world of **sports**” → a location in canon tied to **sports** (e.g. low-g football, planet-wide fanbases). That matches **Mariner Valley** on Mars: a major settlement where sports culture is a plot point.

Alternate geography-only reading (real canyon name on Mars): `CIT{Valles_Marineris}` is plausible if the organizer used the astronomical name; the example flag format `CIT{Grand_Canyon}` and in-universe naming favor **Mariner Valley**.

## Verification

```console
$ bash scripts/solve.sh
CIT{Mariner_Valley}
```

## Wrong turns

- Treating the *Blazing Saddles* quote literally and hunting Earth filming locations (e.g. Vasquez Rocks) ignores that the Belter/Martian clues anchor the puzzle in *The Expanse*.
- OpenStreetMap / what3words rabbit-hole scripts from an earlier attempt live under `scripts/scratch/`; they are not part of the intended solve path.

## References

- [Belter Creole 101 | SYFY — The Expanse](https://www.syfy.com/the-expanse/season-1/blogs/belter-creole-101)
- [Martian | The Expanse Wiki | Fandom](https://expanse.fandom.com/wiki/Martian)
- [Mariner Valley | The Expanse Wiki | Fandom](https://expanse.fandom.com/wiki/Mariner_Valley)

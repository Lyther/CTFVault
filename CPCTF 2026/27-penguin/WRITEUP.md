# PENGUIN (OSINT, bn256)

**Flag:** `CPCTF{397}`

**Target:** top-right penguin in the attached photo — report its individual ID.

## Aquarium

The smaller penguin diving below the target is an **Emperor Penguin** (コウテイペンギン). In Japan, only two facilities keep emperors: **Nagoya Port Aquarium** (名古屋港水族館) and **Adventure World**. The tank décor, photo angle through an acrylic underwater viewing window, and the flipper-band style all match Nagoya. The band-reading legend is published on Nagoya's site:

<https://nagoyaaqua.jp/study/column/19753/>

## Reading the band

Band on the target's flipper, from **shoulder → tip** (= せなか → おなか per the legend). Underwater lighting shifts everything a bit cyan; after correcting for it the four beads read as:

1. **Yellow** (shifts to look orangey in-water)
2. **Green**
3. **White** (shifts to look cyan in-water)
4. **Blue**

Base strap colour: **white**.

## Decoding

Nagoya's scheme (from the exhibit panel):

| colour | digit |
|--------|-------|
| 黒 black | 0 |
| 赤 red | 1 |
| 青 blue | 2 |
| 黄 yellow | 3 |
| 緑 green | 4 |
| 白 white | 5 |

Rules:

- Two beads on the **back side** → hundreds, tens.
- Two beads on the **belly side** → summed → ones.
- **Base strap = white** adds **+50**.

Applying:

```text
back:  [yellow=3][green=4]   -> 34_
belly: [white=5][blue=2]     -> _ _ (5+2)=7
            -> 347
white base strap -> +50
            -> 397
```

**Flag:** `CPCTF{397}`.

## Notes

- The public legend only lists six colours (0–5), so in the photo the yellow bead can look orange-ish and the white bead can look cyan-ish because of the water's blue cast — same thing that makes reds disappear in underwater photography. Don't trust naïve HSV hue buckets; eyeball the bead against the clear plastic spacer as a white reference.
- Emperor Penguins at Nagoya are the exception: they wear a white **waist** band, not a flipper band. The target here is the Gentoo-ish bird above, so the normal flipper-band rules apply.

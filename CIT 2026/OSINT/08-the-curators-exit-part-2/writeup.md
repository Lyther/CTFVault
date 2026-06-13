# The Curator's Exit - Part 2 — Writeup (UNSOLVED)

- Category: OSINT
- Value: 979 pts (22 solves, as of 2026-04-20)
- Author: elemental
- Status: **unsolved** — all guesses below rejected, flag not recovered

## Challenge

> Check the archives

## Known chain (inherited from Part 1)

The thief / persona is **VitrineFox → Remy Beauvillier**. Public-facing chain:

| Node | URL |
| --- | --- |
| X / Twitter | <https://x.com/vitrinefox> |
| Linktree | <https://linktr.ee/vitrinefox> |
| LinkedIn | <https://www.linkedin.com/in/vitrine-fox-424b153b3/> |
| PCPartPicker | <https://pcpartpicker.com/user/vitrinefox/> |
| Dropbox (bio link on PCPP) | <https://www.dropbox.com/scl/fi/73nkwkuorewxm8h0xywzy/CuratorsExit-Final.pdf> |
| OSM user | <https://www.openstreetmap.org/user/vitrinefox> |
| OSM node | <https://www.openstreetmap.org/node/13735855418> (Flock Safety ALPR, UNH West Haven) |

Linktree timezone = `America/New_York`; account created `2026-02-27 16:13 UTC` — matches the X account creation time to the minute.

## What the Dropbox PDF contains (decoy)

The PDF `CuratorsExit-Final.pdf` is 1 page, 10 KB, rendered PDF (Aptos font, Quartz PDFContext), and the only text extracted by Dropbox's preview JSON is:

```text
CIT{N0t_ev3ryth1ng_i$_s3cur3}
```

Confirmed as **incorrect** via the platform API. The file has no attachments, no hidden streams, no EXIF beyond colour-profile defaults (`Create/Mod Date: 2026-02-27 18:17:56Z`, same day as all other VitrineFox account creations).

Dropbox HAR (while logged in as an unrelated viewer) exposes no sibling file, no parent folder link, no revision history — `access_type: viewer`, `shared_link_policy: anyone`, `is_cloud_doc: false`, file id `oLJkVjzyg6AAAAAAAAAABg`, rev `0164bd245591fb1000000033380cbb3`.

## What was tried (all rejected by the CTF API)

**From the "Check the archives" wording:**

| Candidate | Reasoning |
| --- | --- |
| `CIT{ch3ck_th3_OSM_t4gs}` | OSM node tag + changeset comment — but this is the *sibling* challenge **Cartographer's Secret (id 21)**, not Part 2 |
| `CIT{N0t_ev3ryth1ng_i$_s3cur3}` | Decoy PDF content |

**From reverse-image-searching the tweet photo** (Yandex matched it to Leonardo da Vinci's birthplace in Anchiano, Vinci, Tuscany):

```text
Anchiano · Vinci · Anchiano_Italy · Vinci_Italy · Vinci_Tuscany · Tuscany · Montalbano
Casa_Natale_di_Leonardo · Casa_Natale_di_Leonardo_da_Vinci · Casa-Natale-di-Leonardo-da-Vinci
casa_natale_di_leonardo_da_vinci · Casa_Natale_Leonardo · Leonardo_da_Vinci · Birthplace_of_Leonardo
Biblioteca_Leonardiana · Museo_Leonardiano
```

**Historical Mona Lisa theft parallel:** `Vincenzo_Peruggia · Peruggia · Mona_Lisa`.

**All rejected.**

## Archives lookups — all empty

| Service | Target | Result |
| --- | --- | --- |
| Wayback `archived_snapshots` | `pcpartpicker.com/user/vitrinefox` | `{}` |
| Wayback CDX | `pcpartpicker.com/user/vitrinefox*` | `[]` |
| Wayback | `dropbox.com/scl/fi/73nkwkuorewxm8h0xywzy` | `{}` |
| Wayback | `linktr.ee/vitrinefox`, `x.com/vitrinefox`, `twitter.com/vitrinefox` | `{}` each |
| Wayback | `linkedin.com/in/vitrine-fox-*` / `remy-beauvillier` | `[]` |
| archive.ph / archive.today | same set | empty / JS challenge (no indexed snapshots) |
| archive.org `@<handle>` profiles | vitrinefox, foxinglass, salledenonghost, vitrine_fox9, curatorsexit, remy-beauvillier | all 0 items |
| archive.org full-text search | vitrinefox, FoxInGlass, salledenonghost, remy beauvillier, VF0000000011 | 0 relevant hits |
| CommonCrawl index (CC-MAIN-2024-51/2025-33/2025-51) | `pcpartpicker.com/user/vitrinefox*` | 504 / no index |
| Google / Bing / DDG | `"vitrinefox" pcpartpicker` | only a false-positive unrelated build `/b/LQKp99` |

## What the PCPP profile actually contains

Pulled with the user's fresh `cf_clearance` cookie (full HTML 84 482 bytes, captured in `~/Downloads/pcpartpicker.com.har`). The profile body is minimal:

```text
Profile
Comments
Topics
Saved Part Lists
Completed Builds        ← count: 0
Created: Feb. 27, 2026, 9:09 a.m.

Profile:
  This is by far my favorite build: https://www.dropbox.com/scl/fi/73nkwkuorewxm8h0xywzy/CuratorsExit-Final.pdf?rlkey=...&st=...&dl=0
```

No completed builds, no topics, no comments, no saved lists. The bio is literally the two lines above. No hidden `display:none` content, no HTML comments, no inline JSON with more data.

Wording is **"by far"** (not "so far"). The strategic read "so far → historical favourites" does *not* survive the raw HTML.

## What the Linktree actually contains

From the embedded `__NEXT_DATA__` JSON:

- 3 outbound links: X, LinkedIn, PCPartPicker.
- `description` = `Nothing valuable is unguarded—only unnoticed` (same as the ROT13 X bio decoded).
- No hidden / archived / deleted links.

## What the OSM account actually contains

3 changesets, all on node `13735855418`. V1 and V3 carry `flag=CIT{ch3ck_th3_OSM_t4gs}`; V2 removed it but its changeset comment leaks the same string. Additional leads in the area (other flag-tagged nodes, user notes with CTF keywords) — **none**. The user has 0 diary entries, 0 GPS traces, 0 map notes.

## What the X account actually contains

1 tweet, 2 following, 0 followers, 1 photo. Tweet text: `"Post score = Vacation Mode Activated"`. The photo is Leonardo da Vinci's birthplace at Anchiano (Yandex reverse-image match confirms — "Home of Leonardo da Vinci, Anchiano, Tuscany"). **The `/following` list (2 accounts) is the biggest untouched piece of evidence** — blocked by X's unauthenticated-scraping policy.

## Remaining leads the author should try manually

1. **X `/following` of @vitrinefox** — 2 accounts, logged-in browser only.
2. **Dropbox web viewer UI** — look for a breadcrumb / "Open parent folder" / "View in folder" button that hydrates after JS runs (the static HTML doesn't carry it).
3. **LinkedIn Activity / Featured / Documents tabs** on `/in/vitrine-fox-424b153b3/`.
4. **Re-open the exact PCPP bio link** in an incognito window — the live page may differ from the HAR capture if the author edits the profile during the CTF.

## Files

- [other/CuratorsExit-Final.pdf](other/CuratorsExit-Final.pdf) — decoy PDF
- [other/osm_node_13735855418_history.xml](other/osm_node_13735855418_history.xml) — OSM node history (V1/V2/V3)
- [other/osm_vitrinefox_changesets.xml](other/osm_vitrinefox_changesets.xml) — all 3 changesets
- [other/tweet_content.json](other/tweet_content.json) — fxtwitter dump
- [other/pcpartpicker.com.har](other/pcpartpicker.com.har) — PCPP browse HAR (cf-cleared)
- [other/www.dropbox.com.har](other/www.dropbox.com.har) — Dropbox viewer HAR
- [other/vitrinefox_linktree.json](other/vitrinefox_linktree.json) — Linktree `__NEXT_DATA__`
- [other/vf_tweet_photo.jpg](other/vf_tweet_photo.jpg) — the villa photo (Anchiano match)
- [scripts/solve.py](scripts/solve.py) — first, wrong OSM-based solver

## Flag (placeholder — WRONG)

```text
CIT{ch3ck_th3_OSM_t4gs}   # this belongs to Cartographer's Secret (#21)
```

Real flag — **unknown**.

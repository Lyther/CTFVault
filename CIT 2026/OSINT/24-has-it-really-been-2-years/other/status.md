# "Has it really been 2 years?" — current status

## Challenge (verbatim)

- **ID:** 24 · **Category:** OSINT · **Value:** 989 pts · **Solves:** 12 / ~552
- **Author:** ronnie
- **Description:** *"Has it really been 2 years...? Find the name of this menu item"*
- **Flag format:** `CIT{name_of_item}` or `CIT{name-of-item}`
- **Attachment:** a Google-Photos-notification screenshot of a take-out food item, 1080×641 `.webp`, no EXIF
- **Hints on scoreboard:** *none listed*

## Current position

- **Not solved yet.**
- The old Voss'/Bojangles/Wings Over/Haven Hot Chicken branches are ruled out by direct submissions.
- The wrapper is now effectively confirmed as **old WOW Cafe American Grill & Wingery** branding used at the University of New Haven.
- The remaining problem is the **exact menu-item label**, not the restaurant family.

## What is now confirmed

- The image is a Google Photos "Memory" notification over a food photo that resurfaced about two years later.
- The main image shows an open clamshell with a bun-based sandwich item topped with thick dill-pickle slices.
- The enhanced center wrapper crop shows `CAFE`, which fits the old `WOW Cafe American Grill & Wingery` logo and rules out the earlier "mystery M/W logo" framing.
- The top-right circular thumbnail suggests the original full photo likely included more of the meal than the cropped challenge image shows.

## Evidence for WOW

- University of New Haven Sodexo page title: `WOW Cafe American Grill & Wingery | University of New Haven`
  - `https://newhaven.sodexomyway.com/en-us/menus/retail-dining/wow-cafe`
- UNH downloadable WOW menu dated `9-10-24`
  - `https://images-prd.sodexomyway.net/web/en-us/media/wow%20menu%20Updated%209-10-24-compressed_tcm17-20604.pdf`
- Current WOW American Eats New Haven storefront page
  - `https://www.wowamericaneats.com/university-of-new-haven-west-haven-ct/`
- The wrapper art in the challenge image matches this old WOW branding far better than Wings Over, Voss', Moe's, McDonald's, Burger King, or Haven Hot Chicken.

## Public menu research completed

- UNH Sodexo WOW menu and PDF both point toward the `Chicken Sandwiches` family.
- Public sandwich names found there:
  - `Classic`
  - `BBQ Ranch`
  - `JBR`
  - `Hot Honey`
  - `Hot BBQ`
  - `Buffalo`
- Current WOW New Haven marketing also shows `#2 Chicken Sandwich` with `Fried or Grilled`.
- UNH Dining WordPress posts exposed older WOW limited-time items:
  - `Hot Honey Chicken Sandwich`
  - `Pimento Cheesy Chicken Sandwich`
- The closest official visual match found so far is WOW's `chicken-classic.png`, but direct `Classic` naming variants already failed.

## What the photo most likely is

- Best current interpretation: a WOW chicken sandwich or chicken-sandwich variant photographed in a UNH context.
- The wrapper clue is now much stronger than the exact-food-shape clue.
- The exact item name may be a storefront label, combo label, or temporary/local naming variant that does not appear cleanly on the public menu PDF.

## Attempt state

- `other/attempt_state.json` currently records:
  - `manual_estimate_prior_attempts`: `200`
  - `automated_attempts`: `30`
  - `total_known_attempts`: `230`
  - `last_candidate`: `CIT{BBQ_Ranch}`
  - `last_status`: `incorrect`
- Full exact automated submission history is in `other/attempt_log.jsonl`.

## Latest automated rejects

```text
CIT{Pimento-Cheesy-Chicken}
CIT{Pimento_Cheesy_Chicken}
CIT{Pimento-Cheesy-Chicken-Sandwich}
CIT{Pimento_Cheesy_Chicken_Sandwich}
CIT{Crispy-Classic-Chicken}
CIT{Crispy_Classic_Chicken}
CIT{Grilled-Classic-Chicken}
CIT{Grilled_Classic_Chicken}
CIT{Blackened-Classic-Chicken}
CIT{Blackened_Classic_Chicken}
CIT{Chicken-Sandwich}
CIT{Chicken_Sandwich}
CIT{Fried-Chicken-Sandwich}
CIT{Fried_Chicken_Sandwich}
CIT{2-Chicken-Sandwich}
CIT{2_Chicken_Sandwich}
CIT{Classic_Chicken_Sandwich}
CIT{Hot_BBQ_Chicken_Sandwich}
CIT{BBQ-Ranch}
CIT{BBQ_Ranch}
```

## Major ruled-out branches

- `Voss' Bar-B-Q / Mexi All-The-Way`
- `Bojangles / Bo's Bird Dog`
- `Wings Over / Big Dill`
- `Haven Hot Chicken / THE Sandwich`
- Generic hot-dog / pickle-dog / bagel / tuna-salad / egg-salad theories
- Public WOW names already tested directly, including `Classic`, `Hot Honey`, `Hot BBQ`, and `BBQ Ranch` variants

## Remaining gap

- Published public menu pages are probably not enough.
- The highest-signal missing artifact is the **exact live order label** or a **historical April 2024 storefront/menu capture**.
- `shop-newhaven.sodexomyway.com` blocked direct curl access with `403`, so browser-only inspection of the live order platform is still the best next lead.
- If another manual clue turns up, it should be written here and cross-checked against `other/attempt_log.jsonl` before more submissions.

## Supporting artefacts in this folder

- [files/has_it_really_been_2_years.webp](../files/has_it_really_been_2_years.webp) — original challenge image
- [other/logo_zooms/](logo_zooms/) — wrapper/logo zooms used to confirm the WOW branding
- [other/attempt_state.json](attempt_state.json) — running attempt counter and last-submission state
- [other/attempt_log.jsonl](attempt_log.jsonl) — exact automated submission history

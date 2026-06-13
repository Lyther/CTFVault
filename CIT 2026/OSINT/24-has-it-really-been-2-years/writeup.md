# Has it really been 2 years? — Writeup (WIP)

- Category: OSINT
- Value: 989 pts
- Author: by **ronnie**

## Challenge

> Has it really been 2 years…? Find the name of this menu item.
>
> Flag format: `CIT{name_of_item}` or `CIT{name-of-item}`

Attached: [files/has_it_really_been_2_years.webp](files/has_it_really_been_2_years.webp) — a Google Photos "Memories" banner pushing a 2-year-old food photo. The image shows a take-out clamshell with a bun-based sandwich item topped with thick-cut dill pickles and wrapped in old WOW Cafe American Grill & Wingery paper.

## Recon

Current status:

- **Not solved yet.**
- The earlier Voss'/Bojangles/Wings Over/Haven Hot Chicken theories are now ruled out by direct submissions.
- The wrapper/logo is now effectively confirmed as **old WOW Cafe American Grill & Wingery** branding used at the University of New Haven.
- Public menu research points toward WOW's `Chicken Sandwiches` family, but the exact item label is still unresolved.

Strongest evidence:

- The enhanced wrapper crop shows `CAFE`, which matches the old WOW logo.
- UNH Sodexo's WOW page and downloadable WOW menu both align with the restaurant family seen in the image.
- Public WOW labels found so far include `Classic`, `BBQ Ranch`, `JBR`, `Hot Honey`, `Hot BBQ`, and `Buffalo`.
- Older UNH Dining posts also surfaced `Hot Honey Chicken Sandwich` and `Pimento Cheesy Chicken Sandwich`.
- Direct submissions for these public labels and their obvious variants have all failed.

## Current best lead

The remaining gap is likely an exact storefront label or historical April 2024 naming variant not visible on the public PDF menu. The most useful next artifact would be a browser-visible order page or archived order/menu capture for the UNH WOW location.

## Flag

```text
UNSOLVED
```

## Files

- [files/has_it_really_been_2_years.webp](files/has_it_really_been_2_years.webp) — the Google Photos memory image
- [other/status.md](other/status.md) — current research status and ruled-out paths
- [other/attempt_state.json](other/attempt_state.json) — running submission counter
- [other/attempt_log.jsonl](other/attempt_log.jsonl) — exact automated submissions

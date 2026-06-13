# The Forbidden Sock — Solution

**Flag:** `CIT{Red_Sox_Section_7}`

## Approach
- Image is a Discord-compressed JPEG (`jpegli`) of Fenway Park — Green Monster, LF foul pole `310` marker, out-of-town scoreboard (AL/NL) visible, "FANS WHO ATTEMPT TO INTERFERE" warning stenciled on a concrete portal pillar in the foreground.
- Stadium → Fenway Park, team → Boston Red Sox.
- View geometry: low field-level, 1B/RF side, Green Monster across the diamond on the left.
- Section identified as **Right Field Box 7** by comparing to aviewfrommyseat.com galleries; flag format note says to drop the box label, so just the bare number is used.

## Flag format twist
- Team token uses underscore: `Red_Sox` (not `RedSox`).
- No `Box` / letter prefix on the section number.

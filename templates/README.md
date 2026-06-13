# templates

Templates for **Convention A** (hand-authored CPCTF-style) only.
Used by `scripts/new-challenge.sh` and `scripts/new-event.sh`.

| File              | Used as                                                |
| ----------------- | ------------------------------------------------------ |
| `EVENT.md`        | `<Event>/README.md` — event summary, score, post-mortem |
| `DESCRIPTION.md`  | `<Event>/<chall>/DESCRIPTION.md` — verbatim problem     |
| `WRITEUP.md`      | `<Event>/<chall>/WRITEUP.md` — my solution narrative    |

## Convention B (CIT / CTFd-style) is NOT templated here

Those folders (`Event/Category/NN-slug/` with `challenge.json`, lowercase
`writeup.md`, `files/`, `scripts/`, `solution/`, `other/`) come from a CTFd
platform exporter. Don't try to template them — let the exporter overwrite,
and only fill in `writeup.md` + `scripts/`.

## Placeholders

`{{CHALLENGE_NAME}}`, `{{EVENT_NAME}}`, `{{AUTHOR}}`, `{{CATEGORY}}`,
`{{DIFFICULTY}}`, `{{POINTS}}`, `{{FLAG_OR_REDACTED}}` — substituted by `sed`
in the bootstrap scripts.

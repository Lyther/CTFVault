# CTF Vault

Personal log of CTF challenges and writeups.

## Layout

```text
.
├── <Event Year>/              # one folder per CTF event (top-level)
│   ├── ...                    # see "Two challenge conventions" below
│   └── README.md              # event summary, score, ranking
├── notes/                     # personal cheatsheets & playbooks
├── tools/                     # reusable scripts (decoders, helpers)
├── templates/                 # challenge/event/writeup templates (Convention A)
├── scripts/                   # bootstrap helpers (new-event, new-challenge, stats)
└── docs/                      # repo conventions & roadmap
```

## Two challenge conventions (both supported)

| Convention | Layout                                        | Files                                                          | Source         |
| ---------- | --------------------------------------------- | -------------------------------------------------------------- | -------------- |
| **A** (CPCTF style) | `Event/NN-slug/`                     | `DESCRIPTION.md` + `WRITEUP.md` + solver + artifacts           | hand-authored  |
| **B** (CIT/CTFd style) | `Event/Category/NN-slug/`         | `challenge.{md,json}` + `README.md` + `writeup.md` + `files/` `scripts/` `solution/` `other/` | platform export |

`make stats` recognises both. Bootstrap scripts only generate **A**.

## Quick start

```bash
make event NAME="DEF CON Quals 2026" STYLE=numbered     # or STYLE=categorized
make chall EVENT="DEF CON Quals 2026" NAME="cool-pwn"             # A, auto NN
make chall EVENT="DEF CON Quals 2026" NAME="cool-pwn" ID=42       # A, force NN=42
make chall EVENT="DEF CON Quals 2026" NAME="cool-pwn" CATEGORY="Pwn"        # A categorized
make chall EVENT="DEF CON Quals 2026" NAME="cool-pwn" CATEGORY="Pwn" ID=42  # A categorized + NN
make stats     # events / challenges / writeups / pending
make lint      # markdownlint + shellcheck
make clean     # nuke .DS_Store, __pycache__
```

## Conventions

- Each leaf folder = one challenge. Holds at least one of `DESCRIPTION.md`, `challenge.md`, `challenge.json`.
- Vendor original artifacts as-is (don't rename). Solver lives next to them.
- Big binaries / pcaps / disk images → Git LFS (see `.gitattributes`).
- Flags in writeups are fine **after** the event ends. Before, mark `[REDACTED]` (A) or `TBD` (B).
- Notes go in `notes/`, never inside an event folder.
- Convention B exported files are upstream — don't edit them, only add `writeup.md` and put solvers in `scripts/`.

## Events

<!-- run `make stats` for live counts -->

- [CPCTF 2026](./CPCTF%202026/) — Convention A (`NN-slug/`), 54 challenges
- [CIT 2026](./CIT%202026/) — Convention B (`Category/NN-slug/`), 44 challenges
- [KubSTU 2026](./KubSTU%202026/) — Convention B, **53** challenge folders + `scripts/sync_from_ctfd.py`

## License

Code: MIT. Writeups: CC BY 4.0. Vendored challenge artifacts: property of their organizers. See [LICENSE](./LICENSE).

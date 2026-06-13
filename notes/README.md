# notes

Personal CTF reference material. Not tied to any single challenge.

## Layout

```text
notes/
├── cheatsheets/   # one-page references (commands, formulas, gadgets)
├── playbooks/     # step-by-step procedures (recon, exploitation flows)
└── payloads/      # reusable inputs (XSS, SSTI, ROP chains, shellcode)
```

## Naming

- `kebab-case.md` (e.g. `xss-filter-bypass.md`, `rop-chain-glibc-2.39.md`).
- Group by category in subfolders if it gets crowded
  (e.g. `cheatsheets/web/`, `cheatsheets/pwn/`).

## What goes here vs. in a challenge folder

| Goes here                               | Goes in challenge folder       |
| --------------------------------------- | ------------------------------ |
| "How HTTP request smuggling works"      | "How I smuggled into ACME 2026's proxy" |
| Reusable Burp config                    | One-off solver script          |
| Cheatsheet for pwntools `ROP()`         | The exploit using that ROP     |

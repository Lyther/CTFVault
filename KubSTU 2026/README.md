# KubSTU CTF 2026

- Platform: [CTFd — Challenges](https://kubstu-ctf.online/challenges)
- Site: <https://kubstu-ctf.online/>

## Challenge index

- **[CHALLENGES.md](./CHALLENGES.md)** — table of all **53** tasks + relative paths (from synced `challenge.json`)
- **[challenges-api.json](./challenges-api.json)** — [`GET /api/v1/challenges`](https://kubstu-ctf.online/api/v1/challenges) (lightweight listing)
- **[sync-manifest.json](./sync-manifest.json)** — id → path map from last sync
- **Sync script:** `python3 scripts/sync_from_ctfd.py` — pulls each [`/api/v1/challenges/<id>`](https://kubstu-ctf.online/api/v1/challenges/57), writes `challenge.{json,md}`, `README.md`, downloads attachments into `files/`, adds stub `writeup.md` / `solution/flag.txt` only when missing (won’t clobber your writeups)

## Layout

All **53** challenges live under `Category/<id>-slug/` (convention B). Category names match the platform (`Start`, `Crypto`, `Web`, …).

## Score / ranking

(TBD after the event.)

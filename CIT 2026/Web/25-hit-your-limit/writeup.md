# Writeup: Hit Your Limit

## TL;DR

The flag checker is exposed on two routes:

- `/api/flag`
- `/api/flag/`

The non-slashed route is rate limited.
The slashed route uses the same prefix oracle but is not in the same limiter bucket, so it can be brute-forced directly.

## Recon

The landing page sends guesses to:

```javascript
fetch(`/api/flag?guess=${encodeURIComponent(val)}`);
```

The API behaves like a prefix oracle:

- `200 {"result":"correct"}` for a correct prefix
- `500 {"error":"Internal Server Error", ...}` for a wrong prefix
- `429 {"error":"Rate limit exceeded", ...}` on the limited route

The key discovery is that `/api/flag/` behaves differently:

- `/api/flag` quickly returns `429`
- `/api/flag/` returns `200` for correct prefixes and `500` for wrong ones without sharing the same rate-limit bucket

## Vulnerability

This is a route normalization / rate-limit bypass.

The app appears to protect `/api/flag`, but the slash-suffixed variant `/api/flag/` reaches equivalent flag-check logic without the same limiter protection.
That turns the prefix oracle into an unrestricted brute-force endpoint.

## Exploit

Start from the known prefix `CIT{` and brute-force one character at a time against `/api/flag/`.
For each candidate character:

- `200` means the prefix is still correct
- `500` means the candidate is wrong

Using that oracle yields:

```text
CIT{R@T3_L1m1t1nG_15_Bypass@ble}
```

## Reproduction

There was no source archive attached, so I fetched representative live artifacts into `other/fetched/`:

- `home.html`
- `api-flag-rate-limited.json`
- `api-flag-slash-correct.json`

I also added a minimal reconstructed Flask app in `other/reconstructed/` that mirrors the observed bug:

- `/api/flag` is rate limited
- `/api/flag/` exposes the same prefix oracle without that limiter

Fetch the live artifacts again:

```bash
./scripts/fetch-live-artifacts.sh
```

Run the reconstructed app locally:

```bash
./scripts/run-local.sh 5007
```

Solve either local or remote:

```bash
uv run ./scripts/solve.py http://127.0.0.1:5007
uv run ./scripts/solve.py http://23.179.17.92:5559
```

## Flag

`CIT{R@T3_L1m1t1nG_15_Bypass@ble}`

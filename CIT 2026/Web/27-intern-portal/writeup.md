# Writeup: Intern Portal

## TL;DR

The app has an insecure direct object reference on `/report?id=<id>`.
After registering a normal user, any report can be viewed just by changing the numeric `id` parameter.
The seeded flag report is `id=347`.

## Recon

The app has a simple flow:

- `/register` creates a user
- `/login` authenticates
- `/` shows your dashboard and your own reports
- `POST /report` creates a report
- `GET /report?id=<id>` views a report

After creating a new account and two reports, the dashboard only listed my own report IDs, but nothing stopped me from changing the `id` parameter manually.

## Vulnerability

This is broken access control / IDOR.

The app appears to filter the dashboard view to only the current user’s reports, but the report-view endpoint accepts any numeric ID and returns the corresponding report without checking ownership.

## Exploit

1. Register a fresh account.
2. Log in.
3. Request other report IDs directly.

The first low IDs contain fake seeded reports, confirming that arbitrary report reads work for any authenticated user.
Requesting report `347` returns the flag:

```bash
curl -b "session=<cookie>" 'http://23.179.17.92:5001/report?id=347'
```

## Reproduction

There was no source archive attached, so I fetched representative live pages into `other/fetched/`:

- `login.html`
- `register.html`
- `dashboard.html`
- `report-347.html`

I also added a minimal reconstructed Flask app in `other/reconstructed/` that mirrors the observed behavior and intentionally omits the ownership check on `/report`.

Fetch the live pages again:

```bash
./scripts/fetch-live-artifacts.sh
```

Run the reconstructed app locally:

```bash
./scripts/run-local.sh 5006
```

Solve either local or remote:

```bash
uv run ./scripts/solve.py http://127.0.0.1:5006
uv run ./scripts/solve.py http://23.179.17.92:5001
```

## Flag

`CIT{Acc355_C0ntr0l_M@tt3rs!}`

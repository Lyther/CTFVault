# Writeup: Sign Up and Enjoy

## TL;DR

This app uses Flask signed session cookies.
The session secret is weak: `Password1!`.

Once the secret is known, any real user session can be re-signed with:

- the same `uid`
- the same `username`
- `role=admin`

That forged cookie unlocks `/admin` and reveals the flag.

## Recon

The public app is very small:

- `/`
- `/login`
- `/register`
- `/workspace`
- `/tools/link-preview`
- `/admin`

`/admin` redirects standard users back to `/workspace`.
The session cookie is a stock Flask signed cookie and decodes to fields like:

```json
{
  "role": "standard",
  "uid": "u_2498cfde",
  "username": "administrator"
}
```

The preview feature is effectively a dead end.
No useful preview results ever come back, and it does not expose the flag path.

## Weak Defaults

Username enumeration is possible through registration because existing usernames return:

```text
That username is already in use.
```

Spraying a small set of synthetic default passwords found several seeded standard users:

- `operations / Aa1!aaaa`
- `administrator / Abcd1234!`
- `guest / Abcd1234!`
- `demo / Abcd1234!`
- `user / Abcd1234!`
- `system / Abcd1234!`
- `root / Abcd1234!`

Those weak placeholder passwords strongly suggested the Flask `SECRET_KEY` might also be another weak default string.

## Vulnerability

Testing that same placeholder family against a known session cookie showed that the Flask session secret is:

```text
Password1!
```

That means the session cookie can be re-signed offline.

One extra check matters here:

- a completely fake `uid` gets redirected to `/login`

So the forged cookie must reuse a real user record.
Any valid account works as long as the cookie keeps its original `uid` and `username`.

## Exploit

1. Register a fresh account.
2. Log in and grab the `session` cookie.
3. Decode the signed cookie with `Password1!`.
4. Change only `role` from `standard` to `admin`.
5. Re-sign the cookie.
6. Request `/admin` with the forged session.

That returns:

```text
CIT{W3ak_S3cr3t5_C@n_B3_Un5ign3d}
```

## Reproduction

There was no organizer attachment for this challenge, so I added:

- `scripts/solve.py`
- `scripts/fetch-live-artifacts.sh`
- `scripts/run-local.sh`
- `other/reconstructed/app.py`

The fetched artifacts in `other/fetched/` include representative live pages:

- home
- login
- register
- workspace
- link preview
- admin
- `style.css`

Run the live fetcher:

```bash
./scripts/fetch-live-artifacts.sh
```

Run the local reconstruction:

```bash
./scripts/run-local.sh 5009
```

Solve local or remote:

```bash
uv run ./scripts/solve.py http://127.0.0.1:5009
uv run ./scripts/solve.py http://23.179.17.92:5557
```

## Flag

`CIT{W3ak_S3cr3t5_C@n_B3_Un5ign3d}`

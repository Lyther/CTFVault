#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///

from __future__ import annotations

import argparse
import json
import os
import pathlib
import random
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
STATE_PATH = ROOT / "other" / "attempt_state.json"
LOG_PATH = ROOT / "other" / "attempt_log.jsonl"
API_URL = "https://ctf.cyber-cit.club/api/v1/challenges/attempt"
CHALLENGE_ID = 24

DEFAULT_HEADERS = {
    "accept": "application/json",
    "accept-language": "en",
    "content-type": "application/json",
    "dnt": "1",
    "origin": "https://ctf.cyber-cit.club",
    "priority": "u=1, i",
    "referer": "https://ctf.cyber-cit.club/challenges",
    "sec-ch-ua": '"Google Chrome";v="147", "Not.A/Brand";v="8", "Chromium";v="147"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "sec-gpc": "1",
    "user-agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/147.0.0.0 Safari/537.36"
    ),
}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_state() -> dict:
    if STATE_PATH.exists():
        return json.loads(STATE_PATH.read_text())
    return {
        "challenge_id": CHALLENGE_ID,
        "challenge_slug": "has-it-really-been-2-years",
        "manual_estimate_prior_attempts": 200,
        "automated_attempts": 0,
        "total_known_attempts": 200,
        "last_attempt_at": None,
        "last_candidate": None,
        "last_status": None,
        "delay_range_seconds": [8.0, 12.0],
        "notes": [
            "Baseline estimate carried over from other/status.md.",
            "This file tracks automated attempts from scripts/attempt.py.",
        ],
    }


def save_state(state: dict) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n")


def append_log(entry: dict) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, sort_keys=True) + "\n")


def build_request(
    candidate: str, session_cookie: str, csrf_token: str
) -> urllib.request.Request:
    payload = json.dumps(
        {
            "challenge_id": CHALLENGE_ID,
            "submission": candidate,
        },
    ).encode()
    headers = dict(DEFAULT_HEADERS)
    headers["cookie"] = f"session={session_cookie}"
    headers["csrf-token"] = csrf_token
    return urllib.request.Request(API_URL, data=payload, headers=headers, method="POST")


def submit_candidate(
    candidate: str, session_cookie: str, csrf_token: str
) -> tuple[int, dict]:
    request = build_request(candidate, session_cookie, csrf_token)
    with urllib.request.urlopen(request, timeout=30) as response:
        status_code = response.status
        body = response.read().decode()
    return status_code, json.loads(body)


def load_candidates(args: argparse.Namespace) -> list[str]:
    candidates: list[str] = []
    for candidate in args.candidate:
        if candidate not in candidates:
            candidates.append(candidate)
    if args.candidate_file:
        for line in args.candidate_file.read_text().splitlines():
            value = line.strip()
            if not value or value.startswith("#"):
                continue
            if value not in candidates:
                candidates.append(value)
    return candidates


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--candidate",
        action="append",
        default=[],
        help="Exact flag submission to send, e.g. CIT{Crispy-Chicken}",
    )
    parser.add_argument(
        "--candidate-file",
        type=pathlib.Path,
        help="Text file with one exact submission per line.",
    )
    parser.add_argument(
        "--min-delay",
        type=float,
        default=8.0,
        help="Minimum seconds to sleep between attempts.",
    )
    parser.add_argument(
        "--max-delay",
        type=float,
        default=12.0,
        help="Maximum seconds to sleep between attempts.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show the exact candidates without submitting.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.max_delay < args.min_delay:
        raise SystemExit("--max-delay must be >= --min-delay")

    candidates = load_candidates(args)
    if not candidates:
        raise SystemExit("No candidates provided.")

    if args.dry_run:
        for candidate in candidates:
            print(candidate)
        return

    session_cookie = os.environ.get("CIT24_SESSION")
    csrf_token = os.environ.get("CIT24_CSRF_TOKEN")
    if not session_cookie or not csrf_token:
        raise SystemExit("Set CIT24_SESSION and CIT24_CSRF_TOKEN in the environment.")

    state = load_state()
    state["delay_range_seconds"] = [args.min_delay, args.max_delay]
    save_state(state)

    for index, candidate in enumerate(candidates, start=1):
        attempt_started = now_iso()
        print(f"[{index}/{len(candidates)}] submitting {candidate}", flush=True)
        try:
            http_status, response = submit_candidate(
                candidate, session_cookie, csrf_token
            )
            message = response.get("data", {}).get("message")
            status_text = response.get("data", {}).get("status")
        except urllib.error.HTTPError as exc:
            http_status = exc.code
            body = exc.read().decode()
            try:
                response = json.loads(body)
            except json.JSONDecodeError:
                response = {"raw_body": body}
            message = response.get("message") or response.get("data", {}).get("message")
            status_text = "http_error"
        except Exception as exc:
            http_status = 0
            response = {"exception": repr(exc)}
            message = repr(exc)
            status_text = "exception"

        entry = {
            "attempt_started_at": attempt_started,
            "candidate": candidate,
            "http_status": http_status,
            "response": response,
            "status": status_text,
            "message": message,
        }
        append_log(entry)

        state["automated_attempts"] = int(state.get("automated_attempts", 0)) + 1
        state["total_known_attempts"] = int(
            state.get("manual_estimate_prior_attempts", 0)
        ) + int(state.get("automated_attempts", 0))
        state["last_attempt_at"] = attempt_started
        state["last_candidate"] = candidate
        state["last_status"] = status_text
        save_state(state)

        print(
            json.dumps(
                {
                    "candidate": candidate,
                    "http_status": http_status,
                    "status": status_text,
                    "message": message,
                },
                ensure_ascii=True,
            ),
            flush=True,
        )

        if status_text == "correct":
            return

        if index != len(candidates):
            delay = random.uniform(args.min_delay, args.max_delay)
            print(f"sleeping {delay:.2f}s", flush=True)
            time.sleep(delay)

    sys.exit(1)


if __name__ == "__main__":
    main()

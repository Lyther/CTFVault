import os
import time
from collections import deque

from flask import Flask, jsonify, render_template_string, request

app = Flask(__name__)

FLAG = os.getenv("FLAG_VALUE", "CIT{test_flag}")
WINDOW = 300
LIMIT = 5
REQUESTS = deque()

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <title>CTF :: Rate Limit Bypass</title>
</head>
<body>
  <input id="flagInput" maxlength="32" />
  <script>
    const input = document.getElementById('flagInput');
    input.addEventListener('input', async () => {
      await fetch(`/api/flag?guess=${encodeURIComponent(input.value)}`);
    });
  </script>
</body>
</html>"""


def check_prefix(guess: str):
    if FLAG.startswith(guess):
        return jsonify({"result": "correct"}), 200
    return jsonify(
        {"error": "Internal Server Error", "message": "An unexpected error occurred."},
    ), 500


def limited_check(guess: str):
    now = time.time()
    while REQUESTS and now - REQUESTS[0] > WINDOW:
        REQUESTS.popleft()
    if len(REQUESTS) >= LIMIT:
        retry = int(WINDOW - (now - REQUESTS[0]))
        return (
            jsonify(
                {
                    "error": "Rate limit exceeded",
                    "limit": LIMIT,
                    "message": f"Too many requests. Retry in {retry}s.",
                    "requests": len(REQUESTS),
                },
            ),
            429,
        )
    REQUESTS.append(now)
    return check_prefix(guess)


@app.route("/")
def index():
    return render_template_string(PAGE)


@app.route("/api/flag")
def flag_no_slash():
    guess = request.args.get("guess")
    if guess is None:
        return jsonify({"error": "Missing 'guess' parameter"}), 400
    return limited_check(guess)


@app.route("/api/flag/")
def flag_with_slash():
    guess = request.args.get("guess")
    if guess is None:
        return jsonify({"error": "Missing 'guess' parameter"}), 400
    return check_prefix(guess)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.getenv("PORT", "5007")))

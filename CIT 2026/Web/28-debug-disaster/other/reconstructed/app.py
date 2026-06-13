import os

from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return "<h2>Welcome to Startup Portal</h2>"


@app.route("/admin")
def admin():
    raise Exception("Debug leak triggered: Dirbuster maybe in your future!")


@app.route("/flg_bar")
def env():
    return open(".env").read(), 200, {"Content-Type": "text/plain"}


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.getenv("PORT", "5002")), debug=True)

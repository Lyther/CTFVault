import os
import sqlite3

from flask import Flask, redirect, render_template_string, request, session, url_for

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev-secret"
app.config["DB_PATH"] = os.getenv("DB_PATH", "/tmp/intern-portal.db")


LOGIN_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title>Login</title></head>
<body>
  <h2>Login</h2>
  <form method="POST">
    <input name="username" required>
    <input name="password" type="password" required>
    <button type="submit">Login</button>
  </form>
  <a href="/register">Register</a>
</body>
</html>"""

REGISTER_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title>Register</title></head>
<body>
  <h2>Register</h2>
  <form method="POST">
    <input name="username" required>
    <input name="password" type="password" required>
    <button type="submit">Register</button>
  </form>
  <a href="/login">Login</a>
</body>
</html>"""

DASHBOARD_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title>Dashboard</title></head>
<body>
  <h2>Dashboard</h2>
  <a href="/logout">Logout</a>
  <h3>Your Reports</h3>
  <div class="report-list">
  {% for report in reports %}
    <a href="/report?id={{ report['id'] }}">📄 Report {{ report['id'] }}</a>
  {% endfor %}
  </div>
  <h3>Create a New Report</h3>
  <form method="POST" action="/report">
    <input name="title" required>
    <input name="content" required>
    <button type="submit">Create Report</button>
  </form>
</body>
</html>"""

REPORT_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title>Report</title></head>
<body>
  <div class="container">
    <div class="header">
      <h2>📄 Report</h2>
      <a href="/">← Back to Dashboard</a>
    </div>
    <div class="report-content">
      {{ report['title'] }}: {{ report['content'] }}
    </div>
    <div class="meta">Report ID: {{ report['id'] }}</div>
  </div>
</body>
</html>"""


def db() -> sqlite3.Connection:
    conn = sqlite3.connect(app.config["DB_PATH"])
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    conn = db()
    conn.execute(
        "create table if not exists users (id integer primary key autoincrement, username text unique, password text)",
    )
    conn.execute(
        "create table if not exists reports (id integer primary key, user_id integer, title text, content text)",
    )
    conn.execute(
        "insert or ignore into users (id, username, password) values (1, 'admin', 'admin')",
    )
    for i in range(1, 61):
        conn.execute(
            "insert or ignore into reports (id, user_id, title, content) values (?, 1, ?, ?)",
            (
                i,
                f"Report {i}",
                f"Fake report #{i}"
                if i != 6
                else "Fake report #6 — This is too low, maybe 300 above us",
            ),
        )
    conn.execute(
        "insert or ignore into reports (id, user_id, title, content) values (347, 1, 'Flag Report', ?)",
        (os.getenv("FLAG_VALUE", "CIT{test_flag}"),),
    )
    conn.commit()
    conn.close()


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        conn = db()
        user = conn.execute(
            "select id from users where username = ? and password = ?",
            (request.form["username"], request.form["password"]),
        ).fetchone()
        conn.close()
        if user:
            session["user_id"] = user["id"]
            return redirect(url_for("dashboard"))
    return render_template_string(LOGIN_TEMPLATE)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        conn = db()
        conn.execute(
            "insert into users (username, password) values (?, ?)",
            (request.form["username"], request.form["password"]),
        )
        conn.commit()
        conn.close()
        return redirect(url_for("login"))
    return render_template_string(REGISTER_TEMPLATE)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))
    conn = db()
    reports = conn.execute(
        "select id from reports where user_id = ? order by id",
        (session["user_id"],),
    ).fetchall()
    conn.close()
    return render_template_string(DASHBOARD_TEMPLATE, reports=reports)


@app.route("/report", methods=["GET", "POST"])
def report():
    if "user_id" not in session:
        return redirect(url_for("login"))
    conn = db()
    if request.method == "POST":
        cur = conn.execute(
            "insert into reports (user_id, title, content) values (?, ?, ?)",
            (session["user_id"], request.form["title"], request.form["content"]),
        )
        conn.commit()
        conn.close()
        return redirect(url_for("dashboard"))

    report_id = request.args.get("id", type=int)
    report = conn.execute(
        "select id, title, content from reports where id = ?",
        (report_id,),
    ).fetchone()
    conn.close()
    if not report:
        return ("Not Found", 404)
    return render_template_string(REPORT_TEMPLATE, report=report)


if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=int(os.getenv("PORT", "5006")))

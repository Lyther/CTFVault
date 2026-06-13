import os
import secrets

from flask import Flask, redirect, render_template_string, request, session, url_for

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "Password1!")

FLAG = os.getenv("FLAG_VALUE", "CIT{test_flag}")

USERS = {
    "admin": {
        "uid": "u_00000001",
        "full_name": "Admin",
        "password": "AdminArea!2026",
        "role": "admin",
    },
    "operations": {
        "uid": "u_1ce31533",
        "full_name": "Tester Name",
        "password": "Aa1!aaaa",
        "role": "standard",
    },
    "administrator": {
        "uid": "u_2498cfde",
        "full_name": "X",
        "password": "Abcd1234!",
        "role": "standard",
    },
    "guest": {
        "uid": "u_88beeb8c",
        "full_name": "X",
        "password": "Abcd1234!",
        "role": "standard",
    },
    "demo": {
        "uid": "u_d68531d9",
        "full_name": "X",
        "password": "Abcd1234!",
        "role": "standard",
    },
    "user": {
        "uid": "u_f352652e",
        "full_name": "X",
        "password": "Abcd1234!",
        "role": "standard",
    },
    "system": {
        "uid": "u_80f978c0",
        "full_name": "X",
        "password": "Abcd1234!",
        "role": "standard",
    },
    "root": {
        "uid": "u_bf43ba7d",
        "full_name": "X",
        "password": "Abcd1234!",
        "role": "standard",
    },
}

WORKSPACE_HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Workspace · Campaign City</title>
</head>
<body>
  <main>
    <h1>Creator Workspace</h1>
    <p>Keep campaign assets, publishing tools, and private releases in one place.</p>
    <section>
      <span>Signed in</span>
      <strong>{{ user.full_name }}</strong>
      <em>@{{ user.username }}</em>
    </section>
    <p><a href="/tools/link-preview">Open Link Preview</a></p>
    <ul>
      <li>Investor room export</li>
      <li>Document seal refresh</li>
      <li>Guest link moderation</li>
      <li>Preview queue balancing</li>
    </ul>
  </main>
</body>
</html>
"""

PREVIEW_HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Link Preview · Campaign City</title>
</head>
<body>
  <main>
    <h1>Link Preview</h1>
    <p>Preview remote links before sharing them to your workspace.</p>
    <form method="post">
      <input type="url" name="target_url" value="{{ target_url }}" required>
      <button type="submit">Fetch preview</button>
    </form>
    {% if submitted %}
    <strong>Currently Processing... this may take a moment.</strong>
    <p>Request staged for metadata extraction and validation.</p>
    {% else %}
    <strong>Awaiting a preview request.</strong>
    <p>Submit a URL to place a preview request into the queue.</p>
    {% endif %}
  </main>
</body>
</html>
"""

INDEX_HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Campaign City</title>
</head>
<body>
  <main>
    <h1>Secure access for modern document operations.</h1>
    <p>Manage protected workspaces, review activity, and coordinate internal access from a single production console.</p>
    <p><a href="/login">Sign in</a></p>
    <p><a href="/register">Create account</a></p>
  </main>
</body>
</html>
"""

LOGIN_HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Sign In · Campaign City</title>
</head>
<body>
  <main>
    {% if error %}<p>{{ error }}</p>{% endif %}
    <form method="post">
      <input type="text" name="username" required>
      <input type="password" name="password" required>
      <button type="submit">Continue</button>
    </form>
  </main>
</body>
</html>
"""

REGISTER_HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Create Account · Campaign City</title>
</head>
<body>
  <main>
    {% if message %}<p>{{ message }}</p>{% endif %}
    <form method="post">
      <input type="text" name="full_name" required>
      <input type="text" name="username" required>
      <input type="email" name="email" required>
      <input type="password" name="password" required>
      <button type="submit">Create account</button>
    </form>
  </main>
</body>
</html>
"""

ADMIN_HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Admin Console · Campaign City</title>
</head>
<body>
  <main>
    <h1>Administrative access confirmed.</h1>
    <p>This area is reserved for privileged workspace sessions.</p>
    <div>
      <span>Vault token</span>
      <strong>{{ flag }}</strong>
    </div>
  </main>
</body>
</html>
"""


def get_current_user():
    username = session.get("username")
    uid = session.get("uid")
    if not username or not uid:
        return None

    user = USERS.get(username)
    if not user or user["uid"] != uid:
        return None

    return {"username": username, **user}


@app.route("/")
def index():
    return INDEX_HTML


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "")
        if username in USERS:
            return render_template_string(
                REGISTER_HTML,
                message="That username is already in use.",
            )

        USERS[username] = {
            "uid": f"u_{secrets.token_hex(4)}",
            "full_name": request.form.get("full_name", ""),
            "password": request.form.get("password", ""),
            "role": "standard",
        }
        return render_template_string(
            LOGIN_HTML,
            error="Account created. Sign in to continue.",
        )

    return render_template_string(REGISTER_HTML, message="")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        user = USERS.get(username)
        if user and user["password"] == password:
            session.clear()
            session["role"] = user["role"]
            session["uid"] = user["uid"]
            session["username"] = username
            return redirect(url_for("workspace"))
        return render_template_string(LOGIN_HTML, error="Invalid username or password.")

    return render_template_string(LOGIN_HTML, error="")


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/workspace")
def workspace():
    user = get_current_user()
    if not user:
        return redirect(url_for("login"))
    return render_template_string(WORKSPACE_HTML, user=user)


@app.route("/tools/link-preview", methods=["GET", "POST"])
def link_preview():
    user = get_current_user()
    if not user:
        return redirect(url_for("login"))

    if request.method == "POST":
        return render_template_string(
            PREVIEW_HTML,
            submitted=True,
            target_url=request.form.get("target_url", ""),
        )

    return render_template_string(PREVIEW_HTML, submitted=False, target_url="")


@app.route("/admin")
def admin():
    user = get_current_user()
    if not user:
        return redirect(url_for("login"))
    if session.get("role") != "admin":
        return redirect(url_for("workspace"))
    return render_template_string(ADMIN_HTML, flag=FLAG)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5009")))

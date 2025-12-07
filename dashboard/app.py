import os
import json
import requests
from flask import Flask, redirect, url_for, session, request, render_template
from flask_session import Session

# ---------------------- Flask Setup ----------------------
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", os.urandom(24))
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# ---------------- Discord OAuth2 -----------------
CLIENT_ID = os.environ.get("CLIENT_ID", "1447189067535224913")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET", "PwonKPQvj6hUMUcP-Py7Up2GvA3F6iEi")
REDIRECT_URI = os.environ.get("REDIRECT_URI", "https://guardianx-wmye.onrender.com/callback")
API_BASE_URL = "https://discord.com/api"

# ---------------- Helper Functions -----------------
def get_bot_servers():
    """Read servers bot is in"""
    try:
        with open("data/bot_servers.json", "r") as f:
            return json.load(f)
    except:
        return []

def save_bot_servers(bot_servers):
    with open("data/bot_servers.json", "w") as f:
        json.dump(bot_servers, f, indent=4)

# ---------------- Routes -----------------
@app.route("/login")
def login():
    scope = "identify guilds"
    return redirect(
        f"{API_BASE_URL}/oauth2/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope={scope}"
    )

@app.route("/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return redirect(url_for("login"))

    # Exchange code for access token
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "scope": "identify guilds"
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    r = requests.post(f"{API_BASE_URL}/oauth2/token", data=data, headers=headers)
    r.raise_for_status()
    token_data = r.json()
    session["access_token"] = token_data["access_token"]

    # Get user info
    user_data = requests.get(
        f"{API_BASE_URL}/users/@me",
        headers={"Authorization": f"Bearer {session['access_token']}"}
    ).json()
    session["user"] = user_data

    # Get user guilds
    guilds = requests.get(
        f"{API_BASE_URL}/users/@me/guilds",
        headers={"Authorization": f"Bearer {session['access_token']}"}
    ).json()

    # Load bot servers
    bot_servers = get_bot_servers()

    # Filter only servers where user + bot are present
    user_guilds_with_bot = [g for g in guilds if g["id"] in bot_servers or int(g["id"]) in bot_servers]
    session["guilds"] = user_guilds_with_bot

    return redirect(url_for("home"))

@app.route("/")
def home():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("home.html", user=session["user"], guilds=session["guilds"])

@app.route("/dashboard/<guild_id>")
def server_dashboard(guild_id):
    if "user" not in session:
        return redirect(url_for("login"))

    bot_servers = get_bot_servers()
    if guild_id not in bot_servers and int(guild_id) not in bot_servers:
        return "You cannot manage this server", 403

    # Load server config
    try:
        with open("data/dashboard_config.json", "r") as f:
            configs = json.load(f)
    except:
        configs = {}

    server_config = configs.get(guild_id, {})

    return render_template(
        "server_dashboard.html",
        guild_id=guild_id,
        config=server_config,
        user=session["user"]
    )

# ---------------- Feature Update -----------------
@app.route("/update/<guild_id>/<feature>", methods=["POST"])
def update_feature(guild_id, feature):
    if "user" not in session:
        return redirect(url_for("login"))

    bot_servers = get_bot_servers()
    if guild_id not in bot_servers and int(guild_id) not in bot_servers:
        return "You cannot manage this server", 403

    try:
        with open("data/dashboard_config.json", "r") as f:
            configs = json.load(f)
    except:
        configs = {}

    if guild_id not in configs:
        configs[guild_id] = {}

    if feature == "automod":
        configs[guild_id]["automod"] = {
            "enabled": "enabled" in request.form,
            "bad_words": request.form.get("bad_words","")
        }
    elif feature == "antinuke":
        configs[guild_id]["antinuke"] = {
            "enabled": "enabled" in request.form
        }
    elif feature == "tickets":
        configs[guild_id]["tickets"] = {
            "enabled": "enabled" in request.form
        }
    elif feature == "logs":
        configs[guild_id]["logs"] = {
            "enabled": "enabled" in request.form
        }
    elif feature == "status":
        messages = request.form.get("messages","")
        configs[guild_id]["status"] = {
            "messages": messages.split(",")
        }
    elif feature == "embed":
        configs[guild_id]["embed"] = {
            "title": request.form.get("title",""),
            "description": request.form.get("description","")
        }

    with open("data/dashboard_config.json", "w") as f:
        json.dump(configs, f, indent=4)

    return redirect(url_for("server_dashboard", guild_id=guild_id))

# ---------------- Run App -----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

# SimSite: A Flask Web App Scaffold with Tooltip, Modal, Snapshot, Chart, Auto-Refresh, Session, Save/Load, and DB Support

from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import random
import json
import os
from datetime import datetime
import sqlite3

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev_key")

DB_FILE = "snapshots.db"

STORY_LOG = []

PASTEBIN_STEPS = [
    "You are starting a simple version of pastebin.com with just a single server in development.",
    "You now support user submissions and need persistent storage.",
    "Traffic increases: caching is needed for frequent reads.",
    "You add load balancers to split traffic between multiple web servers.",
    "You introduce a CDN to serve static content.",
    "You start storing data in a replicated database setup.",
    "Outages require alerting and log aggregation.",
    "A CI/CD pipeline is added to streamline deployments.",
    "Marketing increases traffic dramatically; autoscaling is introduced.",
]


def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id TEXT,
                timestamp TEXT,
                budget INTEGER,
                score INTEGER,
                uptime INTEGER,
                features TEXT
            )
        """
        )


init_db()

DEFAULT_STATE = {
    "BUDGET": 1000,
    "SCORE": 0,
    "UPTIME": 0,
    "hired_devs": 0,
    "features_launched": 0,
    "marketing_budget": 0,
    "enabled_features": {
        "cache": False,
        "autoscale": False,
        "cdn": False,
        "logging": False,
        "ci_cd": False,
        "alerting": False,
    },
    "step_index": 0,
}


def get_player_id():
    if "player_id" not in session:
        session["player_id"] = f"player_{random.randint(1000, 9999)}"
    return session["player_id"]


def get_game_state():
    import copy

    if "game_state" not in session:
        session["game_state"] = copy.deepcopy(DEFAULT_STATE)
    else:
        for key, default_val in DEFAULT_STATE.items():
            if key not in session["game_state"]:
                session["game_state"][key] = copy.deepcopy(default_val)
    return session["game_state"]


def generate_mermaid(features):
    parts = ["graph TD"]
    parts.append("Client --> LoadBalancer")
    if features.get("cdn"):
        parts.append("Client --> CDN --> LoadBalancer")
    if features.get("autoscale"):
        parts.append("LoadBalancer --> Web1")
        parts.append("LoadBalancer --> Web2")
    else:
        parts.append("LoadBalancer --> Web")
    if features.get("cache"):
        parts.append("Web --> Cache --> DB")
    else:
        parts.append("Web --> DB")
    if features.get("logging"):
        parts.append("Web --> Logging")
    if features.get("alerting"):
        parts.append("Logging --> Alerting")
    if features.get("ci_cd"):
        parts.append("Dev --> CI_CD --> Web")

    return "\n".join(parts)


@app.route("/reset")
def reset():
    session.pop("game_state", None)
    session.pop("player_id", None)
    session["flash_message"] = "Game has been reset."
    return redirect(url_for("index"))


@app.route("/")
def index():
    state = get_game_state()
    story = PASTEBIN_STEPS[state["step_index"]]
    flash_message = session.pop("flash_message", None)
    return render_template(
        "index.html",
        state=state,
        story=story,
        flash_message=flash_message,
        state_diagram=generate_mermaid(state["enabled_features"]),
    )

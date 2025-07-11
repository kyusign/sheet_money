from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

import requests
from flask import Flask, request
from threading import Thread

CONFIG = Path(__file__).resolve().parent.parent / "config" / "app_secrets.json"
TOKEN_FILE = Path.home() / ".sns_dash" / "instagram.json"
REDIRECT_URI = "http://localhost:8888/ig-callback"

def _load_config() -> dict:
    return json.loads(CONFIG.read_text())

def get_ig_token() -> str:
    cfg = _load_config()
    app = Flask("ig_auth")
    token_data: dict = {}

    @app.route("/ig-callback")
    def ig_callback():
        code = request.args.get("code")
        token_resp = requests.get(
            "https://graph.facebook.com/v18.0/oauth/access_token",
            params={
                "client_id": cfg["IG_APP_ID"],
                "client_secret": cfg["IG_APP_SECRET"],
                "redirect_uri": REDIRECT_URI,
                "code": code,
            },
            timeout=10,
        )
        token_data.update(token_resp.json())
        return "Authentication complete. You may close this window."

    thread = Thread(target=lambda: app.run(port=8888))
    thread.daemon = True
    thread.start()

    auth_url = (
        f"https://www.facebook.com/v18.0/dialog/oauth?client_id={cfg['IG_APP_ID']}"
        f"&redirect_uri={REDIRECT_URI}&scope=user_profile,user_media"
    )
    import webbrowser

    webbrowser.open(auth_url)
    thread.join()

    long_lived = refresh_ig_token(token_data.get("access_token"))
    TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
    TOKEN_FILE.write_text(json.dumps({"token": long_lived}))
    return long_lived

def refresh_ig_token(long_lived_token: str) -> str:
    cfg = _load_config()
    resp = requests.get(
        "https://graph.facebook.com/v18.0/oauth/access_token",
        params={
            "grant_type": "ig_exchange_token",
            "client_secret": cfg["IG_APP_SECRET"],
            "access_token": long_lived_token,
        },
        timeout=10,
    )
    data = resp.json()
    return data.get("access_token")

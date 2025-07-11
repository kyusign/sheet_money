from __future__ import annotations

import json
from pathlib import Path
from typing import Dict

import requests

CONFIG = Path(__file__).resolve().parent.parent / "config" / "app_secrets.json"
TOKEN_FILE = Path.home() / ".sns_dash" / "tiktok.json"
REDIRECT_URI = "http://localhost:8888/callback"

def _load_config() -> dict:
    return json.loads(CONFIG.read_text())

def get_tt_token() -> Dict:
    cfg = _load_config()
    auth_url = (
        "https://www.tiktok.com/v2/auth/authorize/?client_key="
        f"{cfg['TT_KEY']}&response_type=code&scope=user.info.basic,video.list"
        f"&redirect_uri={REDIRECT_URI}&state=state"
    )
    import webbrowser

    webbrowser.open(auth_url)
    from flask import Flask, request
    from threading import Thread

    app = Flask("tt_auth")
    token_data: Dict = {}

    @app.route("/callback")
    def callback():
        code = request.args.get("code")
        resp = requests.post(
            "https://open.tiktokapis.com/v2/oauth/token/",
            data={
                "client_key": cfg["TT_KEY"],
                "client_secret": cfg["TT_SECRET"],
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": REDIRECT_URI,
            },
            timeout=10,
        )
        token_data.update(resp.json())
        return "TikTok authentication complete."

    thread = Thread(target=lambda: app.run(port=8888))
    thread.daemon = True
    thread.start()
    thread.join()

    TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
    TOKEN_FILE.write_text(json.dumps(token_data))
    return token_data

def refresh_tt_token(refresh_token: str) -> Dict:
    cfg = _load_config()
    resp = requests.post(
        "https://open.tiktokapis.com/v2/oauth/token/refresh/",
        data={
            "client_key": cfg["TT_KEY"],
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        },
        timeout=10,
    )
    return resp.json()

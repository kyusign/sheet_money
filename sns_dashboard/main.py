from __future__ import annotations

import json
from pathlib import Path

import typer

from auth.google import get_google_creds, get_sheets_service, get_youtube_service

from auth.instagram import get_ig_token
from auth.tiktok import get_tt_token
from services.youtube import fetch_youtube_views
from services.instagram import fetch_instagram_views
from services.tiktok import fetch_tiktok_views
from services.sheets import append_rows

app = typer.Typer()
CONFIG_FILE = Path.home() / ".sns_dash" / "config.json"



def init():
    """OAuth 인증 + 시트 ID 저장"""
    sheet_id = typer.prompt("Google Spreadsheet ID")
    creds = get_google_creds(["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/youtube.readonly"])
    ig_token = get_ig_token()
    tt_token = get_tt_token()
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps({"sheet_id": sheet_id}))
    typer.echo("Initialization complete")


@app.command()
def update(channel_url: str):
    """세 플랫폼 조회수 수집 → 시트 append"""
    cfg = json.loads(CONFIG_FILE.read_text())
    creds = get_google_creds(["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/youtube.readonly"])
    sheets_svc = get_sheets_service(creds)
    yt_svc = get_youtube_service(creds)

    yt_data = fetch_youtube_views(channel_url, yt_svc)
    ig_token = json.loads((Path.home() / ".sns_dash" / "instagram.json").read_text()).get("token")
    ig_data = fetch_instagram_views(ig_token)
    tt_token = json.loads((Path.home() / ".sns_dash" / "tiktok.json").read_text()).get("access_token")
    tt_data = fetch_tiktok_views(tt_token)

    rows = []
    for vid, title, views in yt_data:
        rows.append(["youtube", vid, title, views])
    for vid, title, views in ig_data:
        rows.append(["instagram", vid, title, views])
    for vid, title, views in tt_data:
        rows.append(["tiktok", vid, title, views])

    append_rows(sheets_svc, cfg["sheet_id"], rows)
    typer.echo("Data updated")


@app.command()
def schedule():
    """윈도 작업 스케줄러 등록 (placeholder)"""
    typer.echo("Scheduling not implemented in this environment")


if __name__ == "__main__":
    app()

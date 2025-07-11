from __future__ import annotations

import json
from pathlib import Path

import typer

# ────────────────────────── 내부 서비스 & 인증 모듈 ──────────────────────────
from .auth.google_auth import (
    get_google_creds,
    get_sheets_service,
    get_youtube_service,
)
from .auth.instagram import get_ig_token
from .auth.tiktok import get_tt_token
from .services.youtube import fetch_youtube_views
from .services.instagram import fetch_instagram_views
from .services.tiktok import fetch_tiktok_views
from .services.sheets import append_rows

# ─────────────────────────────── Typer CLI ────────────────────────────────
cli = typer.Typer(help="SNS dashboard CLI")

@cli.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """Display help if no sub-command is given."""
    if ctx.invoked_subcommand is None:
        typer.echo(cli.get_help(ctx))
        raise typer.Exit()

CONFIG_FILE = Path.home() / ".sns_dash" / "config.json"

# -------------------------- 1) setup (=init) ------------------------------
@cli.command(name="setup")
def init() -> None:
    """OAuth 인증 + 스프레드시트 ID 저장"""
    sheet_id = typer.prompt("Google Spreadsheet ID")
    # Google OAuth → creds 객체만 만들어 두고, 각 플랫폼 토큰도 받아둠
    _ = get_google_creds(
        [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/youtube.readonly",
        ]
    )
    _ = get_ig_token()
    _ = get_tt_token()

    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps({"sheet_id": sheet_id}, ensure_ascii=False, indent=2))
    typer.echo("Initialization complete!")

# -------------------------- 2) update -------------------------------------
@cli.command()
def update(channel_url: str) -> None:
    """세 플랫폼 조회수 수집 → 시트 append"""
    cfg = json.loads(CONFIG_FILE.read_text())
    creds = get_google_creds(
        [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/youtube.readonly",
        ]
    )
    sheets_svc = get_sheets_service(creds)
    yt_svc = get_youtube_service(creds)

    yt_data = fetch_youtube_views(channel_url, yt_svc)
    ig_token = json.loads((Path.home() / ".sns_dash" / "instagram.json").read_text())["token"]
    ig_data = fetch_instagram_views(ig_token)
    tt_token = json.loads((Path.home() / ".sns_dash" / "tiktok.json").read_text())["access_token"]
    tt_data = fetch_tiktok_views(tt_token)

    rows: list[list[str | int]] = (
        [["youtube", vid, title, views] for vid, title, views in yt_data]
        + [["instagram", vid, title, views] for vid, title, views in ig_data]
        + [["tiktok", vid, title, views] for vid, title, views in tt_data]
    )

    append_rows(sheets_svc, cfg["sheet_id"], rows)
    typer.echo("Data updated!")

# -------------------------- 3) schedule (placeholder) ----------------------
@cli.command()
def schedule() -> None:
    """윈도 작업 스케줄러 등록 (placeholder)"""
    typer.echo("Scheduling not implemented in this environment")

# --------------------------------------------------------------------------
if __name__ == "__main__":
    cli()

from __future__ import annotations

import json
from pathlib import Path
from typing import List

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

TOKEN_PATH = Path.home() / ".sns_dash" / "google.json"
CLIENT_SECRETS = Path(__file__).resolve().parent.parent / "config" / "client_secrets.json"

def get_google_creds(scopes: List[str]) -> Credentials:
    TOKEN_PATH.parent.mkdir(parents=True, exist_ok=True)
    creds = None
    if TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), scopes)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRETS), scopes)
            creds = flow.run_local_server(port=0)
        with TOKEN_PATH.open("w") as f:
            f.write(creds.to_json())
    return creds

def get_sheets_service(creds: Credentials):
    return build("sheets", "v4", credentials=creds)

def get_youtube_service(creds: Credentials):
    return build("youtube", "v3", credentials=creds)

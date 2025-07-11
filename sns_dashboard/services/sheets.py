from __future__ import annotations

from typing import List
from googleapiclient.discovery import Resource


def append_rows(service: Resource, spreadsheet_id: str, rows: List[List]):
    body = {"values": rows}
    service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range="Raw_Data",
        valueInputOption="RAW",
        insertDataOption="INSERT_ROWS",
        body=body,
    ).execute()

def init_dashboard(service: Resource, spreadsheet_id: str):
    # Placeholder for checking and creating charts
    service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()

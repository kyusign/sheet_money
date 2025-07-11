from __future__ import annotations

from typing import List, Tuple

import requests

API_URL = "https://open.tiktokapis.com/v1/video/list"


def fetch_tiktok_views(token: str) -> List[Tuple[str, str, int]]:
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(API_URL, headers=headers, timeout=10)
    results: List[Tuple[str, str, int]] = []
    for item in resp.json().get("data", []):
        results.append((item.get("id"), item.get("title", ""), int(item.get("stats", {}).get("play_count", 0))))
    return results

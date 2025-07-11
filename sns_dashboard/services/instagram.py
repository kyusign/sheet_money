from __future__ import annotations

from typing import List, Tuple

import requests

GRAPH_URL = "https://graph.facebook.com/v18.0/me/media"


def fetch_instagram_views(token: str) -> List[Tuple[str, str, int]]:
    results: List[Tuple[str, str, int]] = []
    params = {"access_token": token, "fields": "id,caption,media_type,media_product_type,video_insights"}
    resp = requests.get(GRAPH_URL, params=params, timeout=10)
    for item in resp.json().get("data", []):
        if item.get("media_type") == "VIDEO" or item.get("media_product_type") == "REELS":
            insights = item.get("video_insights", {})
            views = int(insights.get("play_count", 0))
            results.append((item["id"], item.get("caption", ""), views))
    return results

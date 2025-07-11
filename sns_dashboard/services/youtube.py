from __future__ import annotations

from typing import List, Tuple

from googleapiclient.discovery import Resource


def extract_uploads_playlist(channel_url: str, service: Resource) -> str:
    channel_id = channel_url.split("/")[-1]
    resp = service.channels().list(part="contentDetails", id=channel_id).execute()
    items = resp.get("items", [])
    if not items:
        raise ValueError("Channel not found")
    return items[0]["contentDetails"]["relatedPlaylists"]["uploads"]

def list_video_ids(uploads_id: str, service: Resource, max_items: int = 300) -> List[str]:
    ids: List[str] = []
    next_page = None
    while next_page is not None or not ids:
        resp = (
            service.playlistItems()
            .list(part="contentDetails", playlistId=uploads_id, maxResults=50, pageToken=next_page)
            .execute()
        )
        ids.extend(i["contentDetails"]["videoId"] for i in resp.get("items", []))
        next_page = resp.get("nextPageToken")
        if len(ids) >= max_items or not next_page:
            break
    return ids[:max_items]

def get_views(video_ids: List[str], service: Resource) -> List[Tuple[str, str, int]]:
    results: List[Tuple[str, str, int]] = []
    for i in range(0, len(video_ids), 50):
        resp = service.videos().list(part="snippet,statistics", id=",".join(video_ids[i:i+50])).execute()
        for item in resp.get("items", []):
            vid = item["id"]
            title = item["snippet"]["title"]
            views = int(item["statistics"].get("viewCount", 0))
            results.append((vid, title, views))
    return results

def fetch_youtube_views(channel_url: str, service: Resource) -> List[Tuple[str, str, int]]:
    uploads = extract_uploads_playlist(channel_url, service)
    ids = list_video_ids(uploads, service)
    return get_views(ids, service)

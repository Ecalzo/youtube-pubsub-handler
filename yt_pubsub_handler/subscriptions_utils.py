import requests
from flask import current_app


def validate_subreddit(subreddit: str) -> bool:
    # not implemented yet
    return True


def validate_yt_channel(channel_id: str) -> bool:
    url = f"https://www.youtube.com/channel/{channel_id}"
    if not channel_id.lower().startswith("uc"):
        return False
    try:
        resp = requests.get(url)
        resp.raise_for_status() 
    except requests.exceptions.HTTPError:
        current_app.logger.exception(f"invalid url: {url}")
        return False
    return True

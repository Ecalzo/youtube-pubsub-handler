import requests
import os
from flask import Flask, current_app, request, has_request_context
from datetime import datetime, timedelta
from . import models


def renew_leases(app: Flask, url_root: str = None):
    # check for leases that expire in 24 hours
    # with yt_pubsub_handler.app_context():
    with app.app_context():
        threshold = datetime.utcnow() + timedelta(seconds=60 * 60 * 24)
        current_app.logger.info(f"querying for leases that expire before {threshold}")
        exp_leases = models.Lease.query.filter(models.Lease.lease_expire_ts < threshold)
        if exp_leases.first():
            for lease in exp_leases:
                current_app.logger.info(f"renewing lease for https://youtube.com/channel/{lease.channel_id}")
                request_new_lease(lease.channel_id, url_root=url_root)
        else:
            current_app.logger.info(f"no leases to renew, bye!")


def request_new_lease(channel_id: str, url_root: str = None):
    # helper function to renew a lease with pubsubhub
    headers = {
        "authority": "pubsubhubbub.appspot.com",
        "cache-control": "max-age=0",
        "sec-ch-ua":  '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
        "sec-ch-ua-mobile": "?0",
        "upgrade-insecure-requests": "1",
        "origin": "https://pubsubhubbub.appspot.com",
        "content-type": "application/x-www-form-urlencoded",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "navigate",
        "sec-fetch-user": "?1",
        "sec-fetch-dest": "document",
        "referer": "https://pubsubhubbub.appspot.com/subscribe",
        "accept-language": "en-US,en;q=0.9",
    }

    if url_root is not None:
        root = url_root
    elif has_request_context():
        root = request.url_root
    else:
        raise Exception(f"No request context found, root provided: {url_root}")

    data = {
        "hub.callback": f"{root}pubsubhub/hook",
        "hub.topic": f"https://www.youtube.com/xml/feeds/videos.xml?channel_id={channel_id}",
        "hub.verify": "async",
        "hub.mode": "subscribe",
        "hub.verify_token": "",
        "hub.secret": "",
        "hub.lease_seconds": str(60 * 60 * 24 * 10)  # max 10 days
    }

    response = requests.post(
        "https://pubsubhubbub.appspot.com/subscribe",
        headers=headers,
        data=data
    )


def ensure_lease_sucess(channel_id: str):
    headers = {
        'authority': 'pubsubhubbub.appspot.com',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'sec-ch-ua-mobile': '?0',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://pubsubhubbub.appspot.com/subscribe',
        'accept-language': 'en-US,en;q=0.9',
    }

    params = (
        ('hub.callback', f'{request.url_root}pubsubhub/hook'),
        ('hub.topic', f'https://www.youtube.com/xml/feeds/videos.xml?channel_id={channel_id}'),
        ('hub.secret', ''),
    )

    response = requests.get('https://pubsubhubbub.appspot.com/subscription-details', headers=headers, params=params)
    if 'unverified' in response.text:
        return False
    else:
        return True

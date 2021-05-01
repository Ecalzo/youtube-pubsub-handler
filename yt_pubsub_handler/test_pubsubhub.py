import pytest
from . import models

CHANNEL_ID = "UC3O3P7AsOC17INXR5L2APHQ"
REQUEST_QUERY = "?hub.topic=https://www.youtube.com/xml/feeds/videos.xml%3Fchannel_id%3DUC3O3P7AsOC17INXR5L2APHQ&hub.challenge=9156451986150874295&hub.mode={hub_mode}&hub.lease_seconds=864000"

def test_pubsubhub_get(client, app):
    test_query = f"pubsubhub/hook{REQUEST_QUERY}"
    assert client.get(test_query.format(hub_mode="subscribe")).data == b"9156451986150874295"
    with app.app_context():
        assert models.Lease.query.filter_by(channel_id=CHANNEL_ID).first() is not None
    
    assert client.get(test_query.format(hub_mode="unsubscribe")).status_code == 200
    with app.app_context():
        assert models.Lease.query.filter_by(channel_id=CHANNEL_ID).first() is None


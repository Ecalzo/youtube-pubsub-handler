import pytest
from . import models

CHANNEL_ID = "UC3O3P7AsOC17INXR5L2APHQ"
REQUEST_QUERY = "?hub.topic=https://www.youtube.com/xml/feeds/videos.xml%3Fchannel_id%3DUC3O3P7AsOC17INXR5L2APHQ&hub.challenge=9156451986150874295&hub.mode={hub_mode}&hub.lease_seconds=864000"


def test_pubsubhub_get(client, app):
    test_query = f"pubsubhub/hook{REQUEST_QUERY}"
    # testing that the hub challenge is successfully returned
    # this validates our lease with pubsubhub
    assert client.get(test_query.format(hub_mode="subscribe")).data == b"9156451986150874295"
    # testing new lease is added to db
    with app.app_context():
        lease = models.Lease.query.filter_by(channel_id=CHANNEL_ID).first()
        assert lease is not None
        # grab the timestamps so we can compare to an update GET request
        original_ts_map = {
            "lease_start_ts": lease.lease_start_ts,
            "lease_expire_ts": lease.lease_expire_ts,
            "updated_at": lease.updated_at
        }
    # send the same subscription request to update the record
    client.get(test_query.format(hub_mode="subscribe")).data == b"9156451986150874295"
    with app.app_context():
        new_lease = models.Lease.query.filter_by(channel_id=CHANNEL_ID).first()
        new_ts_map = {
            "lease_start_ts": new_lease.lease_start_ts,
            "lease_expire_ts": new_lease.lease_expire_ts,
            "updated_at": new_lease.updated_at
        }
    # compare the timestamps to make sure the ts were updated in the db
    for column in original_ts_map:
        assert original_ts_map[column] < new_ts_map[column]

    # testing lease is removed from db
    assert client.get(test_query.format(hub_mode="unsubscribe")).status_code == 200
    with app.app_context():
        assert models.Lease.query.filter_by(channel_id=CHANNEL_ID).first() is None


def test_pubusbhub_post(client, app):
    populate_subscriptions(client)
    with open("test.xml", "r") as xml_file:
        xml = xml_file.read()

    # make a post with the test xml
    assert client.post("pubsubhub/hook", data=xml).data == b"200"

    # assert that you can't make the same post twice
    assert client.post("pubsubhub/hook", data=xml).data == b"already posted, but thanks"


def populate_subscriptions(client):
    for subreddit in ["pics", "doge", "science", "woodworking"]:
        client.post(
            "subscriptions/new",
            data={"channel_id": "UCSHZKyawb77ixDdsGog4iWA", "subreddit": subreddit}
        )

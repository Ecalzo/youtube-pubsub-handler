import pytest
from . import models

db = models.db
CHANNEL_ID = "UCYO_jab_esuFRV4b17AJtAw"
SUBREDDIT = "pics"


def test_subscriptions(client, app):
    assert client.get("subscriptions/new").status_code == 200
    response = client.post(
        "subscriptions/new", data={"channel_id": CHANNEL_ID, "subreddit": SUBREDDIT}
    )
    with app.app_context():
        assert models.Subscription.query.filter_by(
            channel_id=CHANNEL_ID, subreddit=SUBREDDIT).first() is not None


@pytest.mark.parametrize(("channel_id", "subreddit", "message"), (
    ("", "", b"channel_id is required"),
    (CHANNEL_ID, "", b"subreddit is required"),
    (CHANNEL_ID, SUBREDDIT,
     b"UCYO_jab_esuFRV4b17AJtAw is already subscribed for subreddit pics")
))
def test_subscriptions_validate_input(client, channel_id, subreddit, message):
    response = client.post(
        "subscriptions/new",
        data={"channel_id": channel_id, "subreddit": subreddit}
    )
    assert message in response.data


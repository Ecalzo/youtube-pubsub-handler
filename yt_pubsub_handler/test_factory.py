from yt_pubsub_handler import create_app


def test_config():
    assert not create_app().testing
    assert create_app({"TESTING": True}).testing


def test_hello(client):
    response = client.get("/")
    assert b"Connect any YouTube Channel to a subreddit" in response.data

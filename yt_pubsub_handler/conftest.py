from yt_pubsub_handler import create_app
from yt_pubsub_handler.db_utils import init_db_command
from . import models
import pytest


@pytest.fixture
def app():
    app = create_app({
        "TESTING": True
    })

    with app.app_context():
        models.db.create_all()

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()

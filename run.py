import os
from yt_pubsub_handler import create_app
from yt_pubsub_handler.lease_utils import renew_leases

app = create_app()


def run_renew_leases():
    url_root = os.getenv("URL_ROOT")
    renew_leases(app, url_root=url_root)


if __name__ == "__main__":
    app.run()

from yt_pubsub_handler import create_app
from yt_pubsub_handler.lease_utils import renew_leases

app = create_app()


def run_renew_leases():
    renew_leases(app)


if __name__ == "__main__":
    app.run(debug=True)

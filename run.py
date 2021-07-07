import os
from yt_pubsub_handler import create_app
from yt_pubsub_handler.lease_utils import renew_leases
from yt_pubsub_handler.db_utils import alembic_downgrade, alembic_migrate, alembic_upgrade

app = create_app()


def run_renew_leases():
    url_root = os.getenv("URL_ROOT")
    renew_leases(app, url_root=url_root)


def run_alembic_migrate():
    alembic_migrate(app)


def run_alembic_upgrade():
    alembic_upgrade(app)


def run_alembic_downgrade():
    alembic_downgrade(app)


if __name__ == "__main__":
    app.run()

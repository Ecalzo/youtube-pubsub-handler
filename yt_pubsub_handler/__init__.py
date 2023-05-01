import os

from flask import Flask, render_template
from . import models


db = models.db


def create_app(test_config=None):
    certs_dir = os.path.abspath(os.path.join(
        os.path.dirname(__file__), 'certs'))
    ssl_cert_path = os.path.join(certs_dir, 'ca-certificates.crt')
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY", 'dev'),
        SQLALCHEMY_DATABASE_URI=os.getenv(
            "DATABASE_URL", "sqlite:///yt_pubsub_handler.db") + ssl_cert_path,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SCHEDULER_API_ENABLED=True
    )
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/renew_leases")
    def renew_lease():
        from . import lease_utils
        lease_utils.renew_leases(app)
        return "lease renew triggered"

    db.app = app
    db.init_app(app)
    # sets up flask init-db cmd
    from . import db_utils
    db_utils.init_app(app)

    from . import pubsubhub
    app.register_blueprint(pubsubhub.bp)
    from . import subscriptions
    app.register_blueprint(subscriptions.bp)
    from flask_migrate import Migrate
    migrate = Migrate(app, db)
    return app

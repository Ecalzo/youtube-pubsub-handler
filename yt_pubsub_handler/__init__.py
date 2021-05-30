import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from . import models


db = models.db


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY", 'dev'),
        SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_URL", "sqlite:///yt_pubsub_handler.db"),
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
    def hello():
        return "Hello, World!"


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
    return app

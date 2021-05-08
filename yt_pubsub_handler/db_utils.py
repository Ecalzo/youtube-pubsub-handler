from flask_sqlalchemy import SQLAlchemy
from flask.cli import with_appcontext
import click
from datetime import datetime
from . import models


@click.command("init-db")
@with_appcontext
def init_db_command():
    print("creating database")
    models.db.create_all()
    print("database created")


def init_app(app):
    app.cli.add_command(init_db_command)

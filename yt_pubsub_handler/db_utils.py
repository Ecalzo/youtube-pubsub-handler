from flask import Flask
from flask.cli import with_appcontext
from flask_migrate import migrate, upgrade, downgrade
import click
from datetime import datetime
from . import models


@click.command("init-db")
@with_appcontext
def init_db_command():
    init_db()


def init_db():
    print("creating database")
    models.db.create_all()
    print("database created")


def init_app(app):
    app.cli.add_command(init_db_command)


def alembic_migrate(app: Flask):
    """Creates an automatic revision script"""
    with app.app_context():
        migrate()


def alembic_upgrade(app: Flask):
    """Upgrades the database to the latest revision"""
    with app.app_context():
        upgrade()


def alembic_downgrade(app: Flask):
    """Downgrades the database to the latest revision"""
    with app.app_context():
        downgrade()

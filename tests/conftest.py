import pytest
from app import db
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

@pytest.fixture()
def app_db():
    return db


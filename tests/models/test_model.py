from flask import Flask
import unittest

from app import db


def test_create_all(app_db):
    app_db.create_all() 
    print("successfully created the database")


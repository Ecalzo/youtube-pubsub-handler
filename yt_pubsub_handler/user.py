from flask_login import UserMixin
from yt_pubsub_handler import db
from . import models


class User(UserMixin):
    def __init__(self, id_, email):
        self.id = id_
        self.email = email

    @staticmethod
    def get(user_id):
        user = models.User.query.filter_by(id=user_id).first()
        if not user:
            return None
        user = User(
            id_=user.id,
            email=user.email
        )
        return user

    @staticmethod
    def create(id_, email):
        new_user = models.User(
            id=str(id_),
            email=email
        )
        db.session.add(new_user)
        db.session.commit()

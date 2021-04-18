from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Post(db.Model):
    video_id = db.Column(db.String(), unique=True, nullable=False, primary_key=True)
    channel_id = db.Column(db.String(), unique=False, nullable=False)
    title = db.Column(db.String(), unique=True, nullable=False)
    published = db.Column(db.DateTime(timezone=True))
    updated = db.Column(db.DateTime(timezone=True))
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow())
    updated_at = db.Column(db.DateTime(timezone=True), defaulyt=datetime.utcnow())

    def __repr__(self):
        return f"<Post {self.video_id}>" 


class Lease(db.Model):
    channel_id = db.Column(db.String(), unique=True, nullable=False, primary_key=True)
    lease_start_ts = db.Column(db.DateTime(timezone=True))
    lease_expire_ts = db.Column(db.DateTime(timezone=True))
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow())
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow())

    def __repr__(self):
        return f"<Lease {self.channel_id}"

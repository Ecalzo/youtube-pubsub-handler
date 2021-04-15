from app import db

class Posts(db.Model):
    video_id = db.Column(db.String(), unique=True, nullable=False)
    channel_id = db.Column(db.String(), unique=False, nullable=False)
    title = db.Column(db.String(), unique=True, nullable=False)
    published = db.Column(db.TIMESTAMP(timezone=True))
    updated = db.Column(db.TIMESTAMP(timezone=True))
    created_at = db.Column(db.TIMESTAMP(timezone=True))
    updated_at = db.Column(db.TIMESTAMP(timezone=True))
    
    def __repr__(self):
        return f"<Post {self.video_id}>" 

class Leases(db.Model):
    channel_id = db.Column(db.String(), unique=True, nullable=False)
    lease_start_ts = db.Column(db.TIMESTAMP(timezone=True))
    lease_expire_ts = db.Column(db.TIMESTAMP(timezone=True))
    created_at = db.Column(db.TIMESTAMP(timezone=True))
    updated_at = db.Column(db.TIMESTAMP(timezone=True))
    
    def __repr__(self):
        return f"<Lease {self.channel_id}"


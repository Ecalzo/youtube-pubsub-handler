from yt_pubsub_handler import db
from flask import Blueprint, request, current_app
from . import models
from datetime import datetime, timedelta

bp = Blueprint("pubsubhub", __name__, url_prefix="/pubsubhub")

@bp.route("/hook", methods=("GET", "POST"))
def hook():
    request.get_data()
    data = request.data.decode("utf-8")
    if request.method == "GET":
        args = request.args
        # get the data from the lease request
        channel_id = extract_channel_id(args["hub.topic"])
        if models.Lease.query.filter_by(channel_id=channel_id):
            # update the lease, or can we upsert???
            # also handle unsubscribing here...
            pass
        else:  # this is a new lease
            if args["hub.mode"] == "subscribe":
                new_lease = models.Lease(
                    channel_id=channel_id,
                    lease_start_ts=datetime.utcnow(),
                    lease_expire_ts=datetime.utcnow() + timedelta(seconds=int(args["hub.lease_seconds"]))
                )
                db.session.add(new_lease)
                db.session.commit()
        return args["hub.challenge"]

    if request.method == "POST":
        xml = PSH_XML(data)
        if models.Post.query.filter_by(video_id=xml.video_id):
           current_app.logger.info(f"video {xml.video_id} has already been posted")
        else:
            current_app.logger.info(f"creating new post for video: {xml.title}, channel: {xml.channel_id}"
            new_post = models.Post(
                    video_id=xml.video_id,
                    channe_id=xml.channel_id,
                    title=xml.title,
                    published=xml.published,
                    updated=xml.updated
                    )
            db.session.add(new_post)
            db.session.commit()
            # make post here
            return "200" 



from yt_pubsub_handler import db
from flask import Blueprint, request, current_app
from . import models
bp = Blueprint("pubsubhub", __name__, url_prefix="/pubsubhub")

@bp.route("/hook", methods=("GET", "POST"))
def hook():
    request.get_data()
    data = request.data.decode("utf-8")
    if request.method == "GET":
        # get the data from the lease request
        if models.Lease.query.filter(channel_id=request.args["channel_id"]
        return "200"
    if request.method == "POST":
        error = None
        if models.Post.query.filter_by(video_id=xml["video_id"]):
           current_app.logger.info(f"video {xml.video_is} has already been posted")
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



        


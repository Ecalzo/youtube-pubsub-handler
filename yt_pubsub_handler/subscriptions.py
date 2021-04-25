from urllib3.exceptions import HTTPError
from yt_pubsub_handler import db
from flask import Blueprint, request, current_app, flash
from . import models

bp = Blueprint("subscriptions", __name__, url_prefix="/subscriptions")

@bp.route("/new", methods=("GET", "POST"))
def new():
    if request.method == "POST":
        channel_id = request.form["channel_id"]
        subreddit = request.form["subreddit"]
        error = None
        if not channel_id:
            error = "channel_id is required"
        elif not subreddit:
            error = "subreddit is required"
        elif models.Subscriptions.query.filter_by(channel_id=channel_id, subreddit=subreddit):
            error = f"{channel_id} is already subscribed for subreddit {subreddit}"
        elif validate_yt_channel(channel_id) is not True:
            error = f"{channel_id} is an invalid youtube channel ID"
        elif validate_subreddit(subreddit) is not True:
            error = f"{subreddit} does not seem to exist"

        if error is None:
            new_sub = models.Subscription(channel_id=channel_id, subreddit=subreddit)
            db.session.add(new_sub)
            db.session.commit()
            return f"successfully subscribed {channel_id} for subreddit {subreddit}"
        
        flash(error)
        
        return render_template("subscriptions/new.html")


def validate_subreddit(subreddit: str) -> bool:
    # not implemented yet
    return True


def validate_yt_channel(channel_id: str) -> bool:
    url = "https://www.youtube.com/channel/{channeld_id}"
    if not channel_id.lower().startswith("uc"):
        return False
    try:
        resp = requests.get(url)
        resp.raise_for_status() 
    except HTTPError:
        current_app.logger.exception(f"invalid url: {url}")
        return False
    return True
        


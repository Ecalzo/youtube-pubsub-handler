import requests
from urllib3.exceptions import HTTPError
from yt_pubsub_handler import db
from flask import Blueprint, request, current_app, flash, render_template
from . import models
from . import subscriptions_utils
from . import lease_utils

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
        elif models.Subscription.query.filter_by(channel_id=channel_id, subreddit=subreddit).first():
            error = f"{channel_id} is already subscribed for subreddit {subreddit}"
        elif subscriptions_utils.validate_yt_channel(channel_id) is not True:
            error = f"{channel_id.upper()} is an invalid youtube channel ID"
        elif subscriptions_utils.validate_subreddit(subreddit) is not True:
            error = f"{subreddit} does not seem to exist"

        if error is None:
            lease_utils.request_new_lease(channel_id=channel_id)
            new_sub = models.Subscription(channel_id=channel_id, subreddit=subreddit)
            db.session.add(new_sub)
            db.session.commit()
            return f"successfully subscribed {channel_id} for subreddit {subreddit}"

        flash(error)

    return render_template("subscriptions/new.html")

from yt_pubsub_handler import db
import urllib.parse as urlparse
from urllib.parse import parse_qs
from flask import Blueprint, request, current_app
from . import models
from . import xml_utils
from . import reddit_utils
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
        lease_row = models.Lease.query.filter_by(channel_id=channel_id).first()
        if lease_row and args["hub.mode"] == "subscribe":
            # update record w/ new lease
            lease_row.lease_start_ts = datetime.utcnow()
            lease_row.lease_expire_ts = datetime.utcnow() + timedelta(seconds=int(args["hub.lease_seconds"]))
            lease_row.updated_at = datetime.utcnow()
            db.session.commit()
        elif lease_row and args["hub.mode"] == "unsubscribe":
            # unsubscribe
            current_app.logger.info(f"unsubscribing {channel_id}")
            db.session.delete(lease_row)
            db.session.commit()
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
        xml = xml_utils.PSH_XML(data)
        if models.Post.query.filter_by(video_id=xml.video_id).first():
            # already posted
            current_app.logger.info(f"video {xml.video_id} has already been posted")
            return "already posted, but thanks"
        else:  # new post
            # get list of subreddits to post to
            subs_results = models.Subscription.query.filter_by(channel_id=xml.channel_id)
            subreddits = get_subs_for_channel(query_results=subs_results)

            current_app.logger.info(f"creating new post for video: {xml.title}, channel: {xml.channel_id}")

            current_app.logger.info(f"{len(subreddits)} for channel: {xml.channel_id}")
            if subreddits:
                for subreddit in subreddits:
                    # make post here
                    current_app.logger.info(f"posting to sub {subreddit}")
                    if not current_app.config["TESTING"]:
                        reddit_utils.reddit_make_post(subreddit, xml.title, xml.url)
                new_post = models.Post(
                    video_id=xml.video_id,
                    channel_id=xml.channel_id,
                    title=xml.title,
                    published=xml.published,
                    updated=xml.updated
                )
                db.session.add(new_post)
                db.session.commit()
            return "200"


def get_subs_for_channel(query_results):
    # FIXME: the data type for query_results needs to be inspected
    # sqlalchemy docs do not have a straightforward answer for the datatype
    subreddits = set()
    for result in query_results:
        subreddits.add(result.subreddit)
    return subreddits


def extract_channel_id(url: str) -> str:
    "looks like https://www.youtube.com/xml/feeds/videos.xml?channel_id=UCma-7DYdsG6CrEj-h1OPOaA"
    parsed = urlparse.urlparse(url)
    return parse_qs(parsed.query)["channel_id"][0]

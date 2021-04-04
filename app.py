import os
from flask import Flask, request
from utils.xml_parser import parse_yt_xml
from utils.reddit import reddit_make_post

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello, World!"

@app.route("/receive", methods=["GET", "POST"])
def receive():
    request.get_data()
    data = request.data.decode("utf-8")
    if request.method == "POST":
        title, url, channel_id = parse_yt_xml(data)
        subreddits = query_for_sub_based_on_channel_id(channel_id)  # not implemented
        app.logger.info(f"found post: {title}, {url}, channel_id: {channel_id}. Starting reddit subroutine")
        for subreddit in subreddits:
            app.logger.info(f"making post to subreddit: {subreddit}")
            reddit_make_post(subreddit=os.getenv("SUBREDDIT"), title=title, url=url, app=app)
        return "200"
    elif request.method == "GET":
        challenge = request.args["hub.challenge"]
        return challenge

if __name__ == "__main__":
    # if runnning locally, use the .env file
    from dotenv import load_dotenv
    load_dotenv()
    app.run()


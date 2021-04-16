import os
import logging
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from utils.xml_parser import parse_yt_xml
from utils.reddit import reddit_make_post

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///test.db")
db = SQLAlchemy(app)

@app.route("/")
def index():
    return "Hello, World!"

@app.route("/receive", methods=["GET", "POST"])
def receive():
    request.get_data()
    data = request.data.decode("utf-8")
    if request.method == "POST":
        app.logger.info(data)
        title, url, is_new = parse_yt_xml(data)
        if is_new:
            app.logger.info(f"found new video: {title}, {url}, starting reddit subroutine")
            reddit_make_post(subreddit=os.getenv("SUBREDDIT"), title=title, url=url, app=app)
        else:
            app.logger.info(f"found video: {title}, {url}, but it is not a new post")
        return "200"
    elif request.method == "GET":
        challenge = request.args["hub.challenge"]
        return challenge

if __name__ != "__main__":
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

if __name__ == "__main__":
    # if runnning locally, use the .env file
    from dotenv import load_dotenv
    load_dotenv()
    app.run()


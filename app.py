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
        title, url = parse_yt_xml(data)
        app.logger.info(f"found post: {title}, {url}, starting reddit subroutine")
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


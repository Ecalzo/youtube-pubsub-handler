from flask import Flask, request
from xml_parser import parse_yt_xml

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello, World!"

@app.route("/receive", methods=["GET", "POST"])
def receive():
    request.get_data()
    data = request.data.decode("utf-8")
    if request.method == "POST":
        title, link = parse_yt_xml(data)
        print(title, link)
        return "200"
    elif request.method == "GET":
        challenge = request.args["hub.challenge"]
        return challenge

if __name__ == "__main__":
    app.run()

from flask import Flask, request
from xml_parser import parse_yt_xml

app = Flask(__name__)

@app.route("/receive", methods=["GET", "POST"])
def receive():
    request.get_data()
    data = request.data.decode("utf-8")
    if request.method == "POST":
        title, link = parse_yt_xml(data)
        print(title, link)
        return "200"
    elif request.method == "GET":
        print(data)
        return "Hello, world!"

if __name__ == "__main__":
    app.run(debug=True)

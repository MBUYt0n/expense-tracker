from flask import Flask, request, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return render_template("input.html")

@app.route("/input", methods=["POST"])
def input():
    data = request.get_json()
    print(data)
    return "x"

if __name__ == "__main__":
    app.run(port=3000)

from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
from nbconvert import HTMLExporter
from nbconvert.preprocessors import ExecutePreprocessor
import nbformat
import csv
import subprocess
import os

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/input")
def input_screen():
    return render_template("input.html")


@app.route("/api/input", methods=["POST"])
def input_api():
    data = request.get_json()
    print(data)
    with open("expenses.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                data["date"],
                data["amount"],
                data["item"],
                data["category"],
                data["split"],
                data["notme"],
            ]
        )
    return jsonify(data)


@app.route("/api/done", methods=["POST"])
def ipynb():
    notebook_filename = "stats.ipynb"
    with open(notebook_filename, "r", encoding="utf-8") as f:
        notebook = nbformat.read(f, as_version=4)

    executor = ExecutePreprocessor(timeout=600, kernel_name="python3")
    executor.preprocess(notebook, {"metadata": {"path": "./"}})

    with open(notebook_filename, "w", encoding="utf-8") as f:
        nbformat.write(notebook, f)

    html_exporter = HTMLExporter()
    body, _ = html_exporter.from_notebook_node(notebook)

    with open("templates/index.html", "w", encoding="utf-8") as f:
        f.write(body)

    try:
        github_pat = os.getenv("GITHUB_PAT")
        if github_pat is None:
            raise ValueError("GITHUB_PAT is not set")
        url = f"https://{github_pat}@github.com/mbuyt0n/expense-tracker.git"
        subprocess.run(["git", "remote", "set-url", "origin", url])
        subprocess.run(["git", "add", "."])
        subprocess.run(["git", "commit", "-m", "Update index.html"])
        subprocess.run(["git", "push", "origin", "main"])
    except Exception as e:
        return jsonify(str(e)), 500
    return jsonify("done")


@app.route("/index")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(port=3000)

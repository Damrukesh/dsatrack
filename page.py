from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
from datetime import datetime

app = Flask(__name__)

DATA_FILE = "data.json"

def load_data():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"last_day": 1, "entries": {}}

def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

@app.route("/", methods=["GET", "POST"])
def index():
    data = load_data()
    current_day = data["last_day"]

    if request.method == "POST":
        topic = request.form.get("topic")
        data["entries"][current_day] = {"topic": topic}  # Store both
        data["last_day"] += 1  # Move to the next day
        save_data(data)
        return redirect(url_for("index"))

    return render_template("index.html", day=current_day, data=data["entries"])

@app.route("/calendar")
def calendar():
    data = load_data()
    return render_template("calender.html", entries=data["entries"])

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
import os
import random

app = Flask(__name__)

MEMORIES_FOLDER = os.path.expanduser(
    "~/storage/downloads/NOT ME"
)

current_mood = "No mood selected ❤️"


def get_photos():

    if not os.path.exists(MEMORIES_FOLDER):
        return []

    return [
        f for f in os.listdir(MEMORIES_FOLDER)
        if f.lower().endswith(
            (".jpg", ".jpeg", ".png", ".webp")
        )
    ]


@app.route("/")
def home():

    photos = get_photos()

    memories = random.sample(
        photos,
        min(4, len(photos))
    )

    return render_template(
        "index.html",
        memories=memories,
        mood=current_mood
    )


@app.route("/memory/<path:filename>")
def memory(filename):

    return send_from_directory(
        MEMORIES_FOLDER,
        filename
    )


@app.route("/mood", methods=["POST"])
def mood():

    global current_mood

    current_mood = request.form.get(
        "mood",
        "No mood selected ❤️"
    )

    return redirect(url_for("home"))


@app.route("/current-mood")
def current_mood_api():

    return jsonify({
        "mood": current_mood
    })


@app.route("/gallery")
def gallery():

    return render_template(
        "gallery.html",
        photos=get_photos()
    )


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )

from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
import os
import random
import psycopg2

app = Flask(__name__)

MEMORIES_FOLDER = os.path.expanduser("~/storage/downloads/NOT ME")


def get_db():
    return psycopg2.connect(os.environ["DATABASE_URL"])


def setup_database():

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS mood (
            id INTEGER PRIMARY KEY,
            value TEXT NOT NULL
        )
    """)

    cur.execute("""
        INSERT INTO mood (id, value)
        VALUES (1, 'No mood selected ❤️')
        ON CONFLICT (id) DO NOTHING
    """)

    conn.commit()
    cur.close()
    conn.close()


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

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT value FROM mood WHERE id = 1"
    )

    result = cur.fetchone()

    current_mood = (
        result[0]
        if result
        else "No mood selected ❤️"
    )

    cur.close()
    conn.close()

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

    selected_mood = request.form.get(
        "mood",
        "No mood selected ❤️"
    )

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE mood
        SET value = %s
        WHERE id = 1
        """,
        (selected_mood,)
    )

    conn.commit()

    cur.close()
    conn.close()

    return redirect(url_for("home"))


@app.route("/current-mood")
def current_mood():

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT value FROM mood WHERE id = 1"
    )

    result = cur.fetchone()

    cur.close()
    conn.close()

    return jsonify({
        "mood": result[0] if result else "No mood selected ❤️"
    })


@app.route("/gallery")
def gallery():

    return render_template(
        "gallery.html",
        photos=get_photos()
    )


setup_database()


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000
    )

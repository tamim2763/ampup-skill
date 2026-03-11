"""
AmpUp Skill — Open Source Course Platform
CS50x Final Project

A web app that curates free YouTube courses for career tracks
in Blockchain, Backend Engineering, DevOps, and Machine Learning.
"""

import json
import sqlite3
import os

from flask import Flask, flash, redirect, render_template, request, session, jsonify, g
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required

# ─── Configuration ────────────────────────────────────────────────────────────

app = Flask(__name__)
app.secret_key = "ampup-skill-cs50x-secret-key-change-in-production"

# Configure server-side session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tracks.db")


# ─── Database Helper ──────────────────────────────────────────────────────────

def get_db():
    """Get a database connection, creating one if needed."""
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exception):
    """Close the database connection at the end of each request."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


# ─── Template Context ─────────────────────────────────────────────────────────

@app.after_request
def after_request(response):
    """Ensure responses aren't cached."""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# ─── Routes ───────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    """Homepage — show all career tracks."""
    db = get_db()
    tracks = db.execute("SELECT * FROM tracks ORDER BY id").fetchall()
    return render_template("index.html", tracks=tracks)


@app.route("/track/<slug>")
def track(slug):
    """Individual track page with phases and lectures."""
    db = get_db()

    # Get the track
    track = db.execute("SELECT * FROM tracks WHERE slug = ?", (slug,)).fetchone()
    if not track:
        flash("Track not found.", "error")
        return redirect("/")

    # Get phases with lectures
    phases = db.execute(
        "SELECT * FROM phases WHERE track_id = ? ORDER BY phase_number", (track["id"],)
    ).fetchall()

    phases_data = []
    for phase in phases:
        lectures = db.execute(
            "SELECT * FROM lectures WHERE phase_id = ? ORDER BY lecture_number",
            (phase["id"],),
        ).fetchall()

        # Parse resource links and add completion status
        lectures_data = []
        for lec in lectures:
            lec_dict = dict(lec)
            if lec_dict["resource_links"]:
                try:
                    lec_dict["resource_links"] = json.loads(lec_dict["resource_links"])
                except json.JSONDecodeError:
                    lec_dict["resource_links"] = []

            # Check if user has completed this lecture
            lec_dict["completed"] = False
            if session.get("user_id"):
                progress = db.execute(
                    "SELECT id FROM progress WHERE user_id = ? AND lecture_id = ?",
                    (session["user_id"], lec["id"]),
                ).fetchone()
                lec_dict["completed"] = progress is not None

            lectures_data.append(lec_dict)

        phases_data.append({
            "phase": dict(phase),
            "lectures": lectures_data,
        })

    # Calculate progress if logged in
    total_lectures = sum(len(p["lectures"]) for p in phases_data)
    completed_lectures = sum(
        1 for p in phases_data for l in p["lectures"] if l["completed"]
    )
    progress_pct = (
        round(completed_lectures / total_lectures * 100) if total_lectures > 0 else 0
    )

    return render_template(
        "track.html",
        track=track,
        phases=phases_data,
        total_lectures=total_lectures,
        completed_lectures=completed_lectures,
        progress_pct=progress_pct,
    )


@app.route("/track/<slug>/lecture/<int:lecture_id>")
def lecture(slug, lecture_id):
    """Individual lecture page with YouTube embed."""
    db = get_db()

    track = db.execute("SELECT * FROM tracks WHERE slug = ?", (slug,)).fetchone()
    if not track:
        flash("Track not found.", "error")
        return redirect("/")

    lec = db.execute("SELECT * FROM lectures WHERE id = ?", (lecture_id,)).fetchone()
    if not lec:
        flash("Lecture not found.", "error")
        return redirect(f"/track/{slug}")

    lec_dict = dict(lec)
    if lec_dict["resource_links"]:
        try:
            lec_dict["resource_links"] = json.loads(lec_dict["resource_links"])
        except json.JSONDecodeError:
            lec_dict["resource_links"] = []

    # Check completion status
    lec_dict["completed"] = False
    if session.get("user_id"):
        progress = db.execute(
            "SELECT id FROM progress WHERE user_id = ? AND lecture_id = ?",
            (session["user_id"], lecture_id),
        ).fetchone()
        lec_dict["completed"] = progress is not None

    # Get the phase info
    phase = db.execute("SELECT * FROM phases WHERE id = ?", (lec["phase_id"],)).fetchone()

    # Get prev / next lectures (across all phases in this track)
    all_lectures = db.execute(
        """
        SELECT l.*, p.phase_number, p.title as phase_title
        FROM lectures l
        JOIN phases p ON l.phase_id = p.id
        WHERE p.track_id = ?
        ORDER BY p.phase_number, l.lecture_number
        """,
        (track["id"],),
    ).fetchall()

    prev_lec = None
    next_lec = None
    for i, l in enumerate(all_lectures):
        if l["id"] == lecture_id:
            if i > 0:
                prev_lec = all_lectures[i - 1]
            if i < len(all_lectures) - 1:
                next_lec = all_lectures[i + 1]
            break

    return render_template(
        "lecture.html",
        track=track,
        lecture=lec_dict,
        phase=phase,
        prev_lec=prev_lec,
        next_lec=next_lec,
    )


@app.route("/roadmap/<slug>")
def roadmap(slug):
    """Roadmap viewer page with roadmap.sh iframe."""
    db = get_db()
    track = db.execute("SELECT * FROM tracks WHERE slug = ?", (slug,)).fetchone()
    if not track:
        flash("Track not found.", "error")
        return redirect("/")
    return render_template("roadmap.html", track=track)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register a new user."""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        confirmation = request.form.get("confirmation", "")

        # Validate
        if not username:
            flash("Username is required.", "error")
            return render_template("register.html")
        if not password:
            flash("Password is required.", "error")
            return render_template("register.html")
        if password != confirmation:
            flash("Passwords do not match.", "error")
            return render_template("register.html")
        if len(password) < 6:
            flash("Password must be at least 6 characters.", "error")
            return render_template("register.html")

        db = get_db()

        # Check if username exists
        existing = db.execute(
            "SELECT id FROM users WHERE username = ?", (username,)
        ).fetchone()
        if existing:
            flash("Username already taken.", "error")
            return render_template("register.html")

        # Insert new user
        db.execute(
            "INSERT INTO users (username, hash) VALUES (?, ?)",
            (username, generate_password_hash(password)),
        )
        db.commit()

        flash("Registered successfully! Please log in.", "success")
        return redirect("/login")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""
    session.clear()

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or not password:
            flash("Username and password are required.", "error")
            return render_template("login.html")

        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()

        if not user or not check_password_hash(user["hash"], password):
            flash("Invalid username or password.", "error")
            return render_template("login.html")

        session["user_id"] = user["id"]
        session["username"] = user["username"]

        flash(f"Welcome back, {user['username']}!", "success")
        return redirect("/")

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    """Log user out."""
    session.clear()
    flash("You have been logged out.", "success")
    return redirect("/")


@app.route("/dashboard")
@login_required
def dashboard():
    """User dashboard with progress overview."""
    db = get_db()
    user_id = session["user_id"]

    tracks = db.execute("SELECT * FROM tracks ORDER BY id").fetchall()

    track_progress = []
    for track in tracks:
        # Total lectures in this track
        total = db.execute(
            """
            SELECT COUNT(*) as cnt FROM lectures l
            JOIN phases p ON l.phase_id = p.id
            WHERE p.track_id = ?
            """,
            (track["id"],),
        ).fetchone()["cnt"]

        # Completed lectures
        completed = db.execute(
            """
            SELECT COUNT(*) as cnt FROM progress pr
            JOIN lectures l ON pr.lecture_id = l.id
            JOIN phases p ON l.phase_id = p.id
            WHERE pr.user_id = ? AND p.track_id = ?
            """,
            (user_id, track["id"]),
        ).fetchone()["cnt"]

        pct = round(completed / total * 100) if total > 0 else 0

        # Get the next uncompleted lecture
        next_lecture = db.execute(
            """
            SELECT l.*, p.phase_number, p.title as phase_title
            FROM lectures l
            JOIN phases p ON l.phase_id = p.id
            WHERE p.track_id = ?
            AND l.id NOT IN (SELECT lecture_id FROM progress WHERE user_id = ?)
            ORDER BY p.phase_number, l.lecture_number
            LIMIT 1
            """,
            (track["id"], user_id),
        ).fetchone()

        track_progress.append({
            "track": dict(track),
            "total": total,
            "completed": completed,
            "pct": pct,
            "next_lecture": dict(next_lecture) if next_lecture else None,
        })

    # Recent completions
    recent = db.execute(
        """
        SELECT l.title as lecture_title, l.id as lecture_id, t.slug, t.name as track_name,
               p.title as phase_title, pr.completed_at
        FROM progress pr
        JOIN lectures l ON pr.lecture_id = l.id
        JOIN phases p ON l.phase_id = p.id
        JOIN tracks t ON p.track_id = t.id
        WHERE pr.user_id = ?
        ORDER BY pr.completed_at DESC
        LIMIT 10
        """,
        (user_id,),
    ).fetchall()

    return render_template(
        "dashboard.html",
        track_progress=track_progress,
        recent=recent,
    )


@app.route("/toggle-complete", methods=["POST"])
@login_required
def toggle_complete():
    """AJAX endpoint to mark a lecture as complete/incomplete."""
    lecture_id = request.json.get("lecture_id")
    if not lecture_id:
        return jsonify({"error": "Missing lecture_id"}), 400

    db = get_db()
    user_id = session["user_id"]

    # Check if already completed
    existing = db.execute(
        "SELECT id FROM progress WHERE user_id = ? AND lecture_id = ?",
        (user_id, lecture_id),
    ).fetchone()

    if existing:
        db.execute(
            "DELETE FROM progress WHERE user_id = ? AND lecture_id = ?",
            (user_id, lecture_id),
        )
        db.commit()
        return jsonify({"completed": False, "message": "Lecture marked as incomplete."})
    else:
        db.execute(
            "INSERT INTO progress (user_id, lecture_id) VALUES (?, ?)",
            (user_id, lecture_id),
        )
        db.commit()
        return jsonify({"completed": True, "message": "Lecture marked as complete!"})


# ─── Run ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app.run(debug=True)
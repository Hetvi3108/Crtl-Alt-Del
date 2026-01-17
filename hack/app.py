from flask import Flask, render_template, request, redirect, session
import sqlite3
from datetime import datetime, timedelta
from calendar import month_abbr

app = Flask(__name__)
app.secret_key = "skill_intelligence_secret"


# ---------------- DATABASE ----------------
def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cur = conn.cursor()

    # USERS
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    # PROFILE
    cur.execute("""
    CREATE TABLE IF NOT EXISTS profile (
        user_id INTEGER PRIMARY KEY,
        qualification TEXT,
        graduation TEXT,
        skills TEXT,
        interests TEXT,
        career_field TEXT,
        goal TEXT,
        daily_time INTEGER
    )
    """)

    # SCHEDULE
    cur.execute("""
    CREATE TABLE IF NOT EXISTS schedule (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        skill TEXT,
        course_title TEXT,
        course_link TEXT,
        planned_minutes INTEGER
    )
    """)

    # SESSIONS
    cur.execute("""
    CREATE TABLE IF NOT EXISTS sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        skill TEXT,
        start_time TEXT,
        end_time TEXT,
        minutes INTEGER
    )
    """)

    # ACTIVITY
    cur.execute("""
    CREATE TABLE IF NOT EXISTS activity (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        date TEXT,
        minutes INTEGER
    )
    """)

    conn.commit()
    conn.close()


# ---------------- HOME ----------------
@app.route("/")
def home():
    return redirect("/login")


# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        conn = get_db()
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (request.form["username"], request.form["password"])
            )
            conn.commit()
        except sqlite3.IntegrityError:
            return "Username already exists"
        conn.close()
        return redirect("/login")

    return render_template("register.html")


# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "SELECT id FROM users WHERE username=? AND password=?",
            (request.form["username"], request.form["password"])
        )
        user = cur.fetchone()
        conn.close()

        if user:
            session["user_id"] = user["id"]

            # Log today's activity
            today = datetime.now().strftime("%Y-%m-%d")
            conn = get_db()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO activity (user_id, date, minutes) VALUES (?, ?, ?)",
                (user["id"], today, 30)
            )
            conn.commit()
            conn.close()

            return redirect("/dashboard")

        return "Invalid credentials"

    return render_template("login.html")


# ---------------- PROFILE ----------------
@app.route("/profile", methods=["GET", "POST"])
def profile():
    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
        INSERT OR REPLACE INTO profile
        (user_id, qualification, graduation, skills, interests, career_field, goal, daily_time)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            session["user_id"],
            request.form["qualification"],
            request.form["graduation"],
            request.form["skills"],
            request.form["interests"],
            request.form["career"],
            request.form["goal"],
            request.form["time"]
        ))
        conn.commit()
        conn.close()
        return redirect("/dashboard")

    return render_template("profile.html")


# ---------------- DASHBOARD ----------------
from datetime import datetime, timedelta

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]
    conn = get_db()
    cur = conn.cursor()

    # ---------------- USER PROFILE ----------------
    cur.execute("""
        SELECT daily_time
        FROM profile
        WHERE user_id = ?
    """, (user_id,))
    profile = cur.fetchone()

    if not profile:
        conn.close()
        return redirect("/profile")

    daily_time = profile["daily_time"]

    # ---------------- WEEK STREAK ----------------
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    today_day = datetime.now().strftime("%a")
    week = [{"name": d, "active": d == today_day} for d in days]

    # ---------------- ACTIVITY DATA ----------------
    cur.execute("""
        SELECT date, SUM(minutes) AS total_minutes
        FROM activity
        WHERE user_id = ?
        GROUP BY date
    """, (user_id,))
    rows = cur.fetchall()

    activity_data = {
        row["date"]: row["total_minutes"] for row in rows
    }

    # ---------------- HEATMAP + MONTH LABELS ----------------
    today = datetime.today().date()
    start_date = today - timedelta(days=364)

    heatmap = []
    month_labels = []

    # Align first column to Monday
    start_weekday = start_date.weekday()
    for _ in range(start_weekday):
        heatmap.append(0)

    current_day = start_date
    last_month = None
    column_index = 0

    while current_day <= today:
        # Add month label at first week of new month
        if current_day.day <= 7 and current_day.month != last_month:
            month_labels.append({
                "name": current_day.strftime("%b"),
                "col": column_index
            })
            last_month = current_day.month

        minutes = activity_data.get(current_day.isoformat(), 0)

        if minutes == 0:
            heatmap.append(0)
        elif minutes < 30:
            heatmap.append(1)
        elif minutes < 60:
            heatmap.append(2)
        elif minutes < 120:
            heatmap.append(3)
        else:
            heatmap.append(4)

        if current_day.weekday() == 6:  # Sunday → new column
            column_index += 1

        current_day += timedelta(days=1)

    conn.close()

    return render_template(
        "dashboard.html",
        week=week,
        heatmap=heatmap,
        month_labels=month_labels,
        daily_time=daily_time
    )

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# ---------------- RUN ----------------
if __name__ == "__main__":
    init_db()
    app.run(debug=True)

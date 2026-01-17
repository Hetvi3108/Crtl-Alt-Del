from flask import Flask, render_template, request, redirect, session
import sqlite3
from datetime import datetime, timedelta
from calendar import month_abbr

app = Flask(__name__)
app.secret_key = "smart_academic_calendar_secret"

# =========================================================
# CAREER → ROADMAP (ORDERED SKILLS)
# =========================================================
CAREER_ROADMAP = {
    "Software Developer": [
        {"skill": "programming fundamentals", "priority": 1},
        {"skill": "python", "priority": 2},
        {"skill": "data structures", "priority": 3},
        {"skill": "git", "priority": 4},
        {"skill": "databases", "priority": 5},
        {"skill": "apis", "priority": 6},
        {"skill": "backend framework", "priority": 7}
    ],
    "Data Scientist": [
        {"skill": "python", "priority": 1},
        {"skill": "statistics", "priority": 2},
        {"skill": "sql", "priority": 3},
        {"skill": "machine learning", "priority": 4},
        {"skill": "data visualization", "priority": 5}
    ],
    "AI Engineer": [
        {"skill": "python", "priority": 1},
        {"skill": "linear algebra", "priority": 2},
        {"skill": "machine learning", "priority": 3},
        {"skill": "deep learning", "priority": 4},
        {"skill": "model deployment", "priority": 5}
    ]
}

# =========================================================
# MULTI-PLATFORM LEARNING RESOURCES
# =========================================================
LEARNING_RESOURCES = {
    "python": {
        "Coursera": "https://www.coursera.org/specializations/python",
        "Udemy": "https://www.udemy.com/topic/python/",
        "YouTube": "https://www.youtube.com/results?search_query=python+full+course+playlist"
    },
    "data structures": {
        "Coursera": "https://www.coursera.org/specializations/data-structures-algorithms",
        "Udemy": "https://www.udemy.com/topic/data-structures/",
        "YouTube": "https://www.youtube.com/results?search_query=data+structures+playlist"
    },
    "git": {
        "Coursera": "https://www.coursera.org/learn/introduction-git-github",
        "Udemy": "https://www.udemy.com/topic/git/",
        "YouTube": "https://www.youtube.com/results?search_query=git+github+playlist"
    },
    "databases": {
        "Coursera": "https://www.coursera.org/specializations/database-systems",
        "Udemy": "https://www.udemy.com/topic/sql/",
        "YouTube": "https://www.youtube.com/results?search_query=database+management+playlist"
    },
    "apis": {
        "Coursera": "https://www.coursera.org/learn/apis",
        "Udemy": "https://www.udemy.com/topic/rest-api/",
        "YouTube": "https://www.youtube.com/results?search_query=rest+api+development+playlist"
    },
    "backend framework": {
        "Coursera": "https://www.coursera.org/specializations/django",
        "Udemy": "https://www.udemy.com/topic/flask/",
        "YouTube": "https://www.youtube.com/results?search_query=backend+development+playlist"
    }
}

# =========================================================
# DATABASE
# =========================================================
def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

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

# =========================================================
# ROUTES
# =========================================================
@app.route("/")
def home():
    return redirect("/login")


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

        if not user:
            return "Invalid credentials"

        session["user_id"] = user["id"]

        cur.execute(
            "SELECT daily_time FROM profile WHERE user_id=?",
            (user["id"],)
        )
        profile = cur.fetchone()

        daily_time = profile["daily_time"] if profile else 1
        minutes = daily_time * 30

        today = datetime.now().strftime("%Y-%m-%d")

        cur.execute(
            "SELECT id FROM activity WHERE user_id=? AND date=?",
            (user["id"], today)
        )

        if not cur.fetchone():
            cur.execute(
                "INSERT INTO activity (user_id, date, minutes) VALUES (?, ?, ?)",
                (user["id"], today, minutes)
            )
            conn.commit()

        conn.close()
        return redirect("/dashboard")

    return render_template("login.html")


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
            int(request.form["time"])
        ))

        conn.commit()
        conn.close()
        return redirect("/dashboard")

    return render_template("profile.html")


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT skills, goal, daily_time
        FROM profile WHERE user_id=?
    """, (user_id,))
    profile = cur.fetchone()

    if not profile:
        return redirect("/profile")

    user_skills = {
        s.strip().lower()
        for s in profile["skills"].split(",")
        if s.strip()
    }

    goal = profile["goal"]
    daily_time = profile["daily_time"]

    roadmap = CAREER_ROADMAP.get(goal, [])

    missing_skills = [
        step["skill"]
        for step in roadmap
        if step["skill"] not in user_skills
    ]

    recommendations = []
    for skill in missing_skills[:3]:
        for platform, link in LEARNING_RESOURCES.get(skill, {}).items():
            recommendations.append({
                "skill": skill,
                "platform": platform,
                "link": link
            })

    roadmap_graph = [
        {
            "skill": step["skill"],
            "completed": step["skill"] in user_skills
        }
        for step in roadmap
    ]

    today_name = datetime.now().strftime("%a")
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    week = [{"name": d, "active": d == today_name} for d in days]

    today = datetime.today().date()
    start_date = today - timedelta(days=364)

    cur.execute("""
        SELECT date, SUM(minutes) AS total_minutes
        FROM activity
        WHERE user_id=?
        GROUP BY date
    """, (user_id,))
    rows = cur.fetchall()
    activity = {row["date"]: row["total_minutes"] for row in rows}

    heatmap = []
    month_labels = []

    for i in range(365):
        day = start_date + timedelta(days=i)
        minutes = activity.get(day.isoformat(), 0)

        if minutes == 0:
            level = 0
        elif minutes <= 30:
            level = 1
        elif minutes <= 60:
            level = 2
        elif minutes <= 120:
            level = 3
        else:
            level = 4

        heatmap.append(level)

        if day.day == 1:
            month_labels.append({
                "name": month_abbr[day.month],
                "col": i + 1
            })

    conn.close()

    return render_template(
        "dashboard.html",
        daily_time=daily_time,
        heatmap=heatmap,
        month_labels=month_labels,
        week=week,
        missing_skills=missing_skills,
        recommendations=recommendations,
        roadmap_graph=roadmap_graph,
        goal=goal
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


if __name__ == "__main__":
    init_db()
    app.run(debug=True)

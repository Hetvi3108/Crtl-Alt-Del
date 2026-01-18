from flask import Flask, render_template, request, redirect, session, jsonify
import sqlite3
from datetime import datetime, timedelta
from calendar import month_abbr
import requests
import json

app = Flask(__name__)
app.secret_key = "smart_academic_calendar_hackathon_2026"

# =========================================================
# COMPREHENSIVE CAREER ROADMAPS (Healthcare, Agriculture, Urban Planning)
# =========================================================
CAREER_ROADMAP = {
    # Healthcare Sector
    "Healthcare Data Analyst": [
        {"skill": "medical terminology", "priority": 1},
        {"skill": "python", "priority": 2},
        {"skill": "sql", "priority": 3},
        {"skill": "healthcare analytics", "priority": 4},
        {"skill": "data visualization", "priority": 5},
        {"skill": "hipaa compliance", "priority": 6}
    ],
    "Medical AI Specialist": [
        {"skill": "python", "priority": 1},
        {"skill": "machine learning", "priority": 2},
        {"skill": "medical imaging", "priority": 3},
        {"skill": "deep learning", "priority": 4},
        {"skill": "healthcare systems", "priority": 5}
    ],
    "Clinical Research Coordinator": [
        {"skill": "research methodology", "priority": 1},
        {"skill": "medical ethics", "priority": 2},
        {"skill": "data management", "priority": 3},
        {"skill": "regulatory compliance", "priority": 4},
        {"skill": "clinical trials", "priority": 5}
    ],
    "Health Informatics Specialist": [
        {"skill": "ehr systems", "priority": 1},
        {"skill": "healthcare databases", "priority": 2},
        {"skill": "health data standards", "priority": 3},
        {"skill": "interoperability", "priority": 4},
        {"skill": "healthcare analytics", "priority": 5}
    ],
    
    # Agriculture Sector
    "Precision Agriculture Specialist": [
        {"skill": "gis mapping", "priority": 1},
        {"skill": "iot sensors", "priority": 2},
        {"skill": "data analysis", "priority": 3},
        {"skill": "crop management", "priority": 4},
        {"skill": "remote sensing", "priority": 5}
    ],
    "Agricultural Data Scientist": [
        {"skill": "python", "priority": 1},
        {"skill": "statistics", "priority": 2},
        {"skill": "soil science", "priority": 3},
        {"skill": "machine learning", "priority": 4},
        {"skill": "crop modeling", "priority": 5}
    ],
    "Smart Farming Engineer": [
        {"skill": "iot systems", "priority": 1},
        {"skill": "automation", "priority": 2},
        {"skill": "sensor networks", "priority": 3},
        {"skill": "agricultural robotics", "priority": 4},
        {"skill": "data analytics", "priority": 5}
    ],
    "AgriTech Developer": [
        {"skill": "mobile development", "priority": 1},
        {"skill": "apis", "priority": 2},
        {"skill": "cloud computing", "priority": 3},
        {"skill": "agriculture domain", "priority": 4},
        {"skill": "satellite imagery", "priority": 5}
    ],
    
    # Urban Sector
    "Smart City Planner": [
        {"skill": "urban planning", "priority": 1},
        {"skill": "gis systems", "priority": 2},
        {"skill": "data analytics", "priority": 3},
        {"skill": "sustainability", "priority": 4},
        {"skill": "iot infrastructure", "priority": 5}
    ],
    "Urban Data Analyst": [
        {"skill": "python", "priority": 1},
        {"skill": "spatial analysis", "priority": 2},
        {"skill": "visualization", "priority": 3},
        {"skill": "urban modeling", "priority": 4},
        {"skill": "transportation systems", "priority": 5}
    ],
    "Infrastructure IoT Engineer": [
        {"skill": "iot platforms", "priority": 1},
        {"skill": "networking", "priority": 2},
        {"skill": "embedded systems", "priority": 3},
        {"skill": "smart infrastructure", "priority": 4},
        {"skill": "cybersecurity", "priority": 5}
    ],
    "Sustainable Development Specialist": [
        {"skill": "environmental science", "priority": 1},
        {"skill": "data analysis", "priority": 2},
        {"skill": "policy frameworks", "priority": 3},
        {"skill": "green technology", "priority": 4},
        {"skill": "impact assessment", "priority": 5}
    ],
    
    # General Tech
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
    ],
    "Full Stack Developer": [
        {"skill": "html css", "priority": 1},
        {"skill": "javascript", "priority": 2},
        {"skill": "react", "priority": 3},
        {"skill": "nodejs", "priority": 4},
        {"skill": "databases", "priority": 5}
    ],
    "DevOps Engineer": [
        {"skill": "linux", "priority": 1},
        {"skill": "docker", "priority": 2},
        {"skill": "kubernetes", "priority": 3},
        {"skill": "ci cd", "priority": 4},
        {"skill": "cloud platforms", "priority": 5}
    ]
}

# =========================================================
# FREE LEARNING RESOURCES WITH API INTEGRATION
# =========================================================
LEARNING_RESOURCES = {
    "python": {
        "YouTube": "python programming tutorial",
        "freeCodeCamp": "python",
        "GitHub": "python projects"
    },
    "machine learning": {
        "YouTube": "machine learning course",
        "freeCodeCamp": "machine learning",
        "GitHub": "machine learning projects"
    },
    "data structures": {
        "YouTube": "data structures algorithms",
        "freeCodeCamp": "algorithms",
        "GitHub": "data structures"
    },
    "git": {
        "YouTube": "git github tutorial",
        "freeCodeCamp": "git",
        "GitHub": "git resources"
    },
    "sql": {
        "YouTube": "sql database tutorial",
        "freeCodeCamp": "sql",
        "GitHub": "sql projects"
    },
    "healthcare analytics": {
        "YouTube": "healthcare data analytics",
        "freeCodeCamp": "data analytics",
        "GitHub": "healthcare analytics"
    },
    "gis mapping": {
        "YouTube": "gis mapping tutorial",
        "freeCodeCamp": "data visualization",
        "GitHub": "gis projects"
    },
    "iot systems": {
        "YouTube": "iot projects tutorial",
        "freeCodeCamp": "iot",
        "GitHub": "iot projects"
    }
}

# YouTube API Integration
YOUTUBE_API_KEY = "AIzaSyDummy_Replace_With_Real_Key"  # Replace with your YouTube API key

def get_youtube_courses(skill):
    """Fetch real courses from YouTube Data API"""
    search_query = LEARNING_RESOURCES.get(skill.lower(), {}).get("YouTube", skill)
    
    try:
        url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            "part": "snippet",
            "q": search_query + " full course",
            "type": "video",
            "videoDuration": "long",
            "maxResults": 3,
            "key": YOUTUBE_API_KEY
        }
        response = requests.get(url, params=params, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            courses = []
            for item in data.get("items", []):
                courses.append({
                    "title": item["snippet"]["title"],
                    "platform": "YouTube",
                    "link": f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                    "thumbnail": item["snippet"]["thumbnails"]["medium"]["url"]
                })
            return courses
    except:
        pass
    
    # Fallback to search URLs
    return [{
        "title": f"{skill.title()} Complete Tutorial",
        "platform": "YouTube",
        "link": f"https://www.youtube.com/results?search_query={search_query}+full+course",
        "thumbnail": None
    }]

def get_github_projects(skill):
    """Fetch project ideas from GitHub"""
    try:
        url = "https://api.github.com/search/repositories"
        params = {
            "q": f"{skill} projects",
            "sort": "stars",
            "order": "desc",
            "per_page": 3
        }
        response = requests.get(url, params=params, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            projects = []
            for item in data.get("items", []):
                projects.append({
                    "name": item["name"],
                    "description": item["description"] or "No description",
                    "url": item["html_url"],
                    "stars": item["stargazers_count"]
                })
            return projects
    except:
        pass
    
    return []

# =========================================================
# DATABASE SETUP
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
        graduation_year TEXT,
        current_skills TEXT,
        interests TEXT,
        career_field TEXT,
        long_term_goal TEXT,
        short_term_goal TEXT,
        daily_time INTEGER,
        sector TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS activity (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        date TEXT,
        minutes INTEGER,
        skill TEXT,
        goal_met INTEGER DEFAULT 0
    )
    """)
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS achievements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        title TEXT,
        description TEXT,
        date TEXT
    )
    """)
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        course_name TEXT,
        platform TEXT,
        status TEXT,
        completion_percentage INTEGER
    )
    """)

    conn.commit()
    conn.close()

# =========================================================
# HELPER FUNCTIONS
# =========================================================
def get_heatmap_data(user_id, daily_goal):
    """Generate proper GitHub-style heatmap data for current year"""
    conn = get_db()
    cur = conn.cursor()
    
    # Get today's date
    today = datetime.today().date()
    
    # For heatmap, show from January 1st of current year to today
    year_start = datetime(today.year, 1, 1).date()
    
    # Find the Sunday before or on January 1st
    days_to_previous_sunday = (year_start.weekday() + 1) % 7
    grid_start = year_start - timedelta(days=days_to_previous_sunday)
    
    # End date is today
    end_date = today
    
    # Fetch all activity data for the period
    cur.execute("""
        SELECT date, SUM(minutes) AS total_minutes
        FROM activity
        WHERE user_id=? AND date >= ? AND date <= ?
        GROUP BY date
    """, (user_id, grid_start.isoformat(), end_date.isoformat()))
    
    rows = cur.fetchall()
    activity_map = {row["date"]: row["total_minutes"] for row in rows}
    
    # Build heatmap: weeks as columns, days as rows (Sunday-Saturday)
    heatmap_weeks = []
    month_labels = []
    current_month = None
    
    # Calculate total days from grid_start to today
    total_days = (end_date - grid_start).days + 1
    
    week_data = []
    week_num = 0
    
    for day_num in range(total_days):
        day_date = grid_start + timedelta(days=day_num)
        
        # Skip if date is after today
        if day_date > today:
            week_data.append({"level": -1, "date": "", "minutes": 0, "goal_met": 0})
        else:
            minutes = activity_map.get(day_date.isoformat(), 0)
            
            # Calculate level based on daily goal
            if minutes == 0:
                level = 0
            elif minutes < daily_goal * 0.25:
                level = 1
            elif minutes < daily_goal * 0.5:
                level = 2
            elif minutes < daily_goal:
                level = 3
            else:
                level = 4
            
            goal_met = 1 if minutes >= daily_goal else 0
            
            week_data.append({
                "level": level,
                "date": day_date.isoformat(),
                "minutes": minutes,
                "goal_met": goal_met
            })
        
        # Track month labels (show at start of each month on first day of week)
        if len(week_data) == 1:  # First day of week (Sunday)
            if day_date <= today and current_month != day_date.month:
                month_labels.append({
                    "name": month_abbr[day_date.month],
                    "week": week_num
                })
                current_month = day_date.month
        
        # Every 7 days, complete the week
        if len(week_data) == 7:
            heatmap_weeks.append(week_data)
            week_data = []
            week_num += 1
    
    # Add remaining days (pad incomplete week)
    if week_data:
        while len(week_data) < 7:
            week_data.append({"level": -1, "date": "", "minutes": 0, "goal_met": 0})
        heatmap_weeks.append(week_data)
    
    conn.close()
    
    return {
        "weeks": heatmap_weeks,
        "month_labels": month_labels
    }

def check_and_award_achievements(user_id):
    """Check for new achievements and award them"""
    conn = get_db()
    cur = conn.cursor()
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Check for streak achievements
    cur.execute("""
        SELECT date, goal_met FROM activity 
        WHERE user_id=? AND goal_met=1 
        ORDER BY date DESC
    """, (user_id,))
    
    activities = cur.fetchall()
    
    # Calculate current streak
    streak = 0
    prev_date = None
    for activity in activities:
        activity_date = datetime.strptime(activity["date"], "%Y-%m-%d").date()
        if prev_date is None:
            prev_date = activity_date
            streak = 1
        elif (prev_date - activity_date).days == 1:
            streak += 1
            prev_date = activity_date
        else:
            break
    
    # Award streak achievements
    achievements_to_add = []
    
    if streak >= 7:
        cur.execute("""
            SELECT id FROM achievements 
            WHERE user_id=? AND title=?
        """, (user_id, "7 Day Streak"))
        if not cur.fetchone():
            achievements_to_add.append(("7 Day Streak", "Completed daily goal for 7 days straight! 🔥"))
    
    if streak >= 30:
        cur.execute("""
            SELECT id FROM achievements 
            WHERE user_id=? AND title=?
        """, (user_id, "30 Day Streak"))
        if not cur.fetchone():
            achievements_to_add.append(("30 Day Streak", "A month of consistent learning! Incredible! 🏆"))
    
    if streak >= 100:
        cur.execute("""
            SELECT id FROM achievements 
            WHERE user_id=? AND title=?
        """, (user_id, "100 Day Streak"))
        if not cur.fetchone():
            achievements_to_add.append(("100 Day Streak", "100 days of dedication! You're unstoppable! 💯"))
    
    # Total learning time achievements
    cur.execute("""
        SELECT SUM(minutes) as total FROM activity WHERE user_id=?
    """, (user_id,))
    total_minutes = cur.fetchone()["total"] or 0
    total_hours = total_minutes / 60
    
    if total_hours >= 100:
        cur.execute("""
            SELECT id FROM achievements 
            WHERE user_id=? AND title=?
        """, (user_id, "100 Hours Learned"))
        if not cur.fetchone():
            achievements_to_add.append(("100 Hours Learned", "100+ hours of learning completed! 📚"))
    
    # Insert new achievements
    for title, description in achievements_to_add:
        cur.execute("""
            INSERT INTO achievements (user_id, title, description, date)
            VALUES (?, ?, ?, ?)
        """, (user_id, title, description, today))
    
    conn.commit()
    conn.close()
    
    return len(achievements_to_add) > 0

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
            conn.close()
            return redirect("/login")
        except sqlite3.IntegrityError:
            conn.close()
            return render_template("register.html", error="Username already exists. Please choose another.")

    return render_template("register.html", error=None)

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
            conn.close()
            return render_template("login.html", error="Invalid username or password. Please try again.")

        session["user_id"] = user["id"]
        session["username"] = request.form["username"]

        conn.close()
        return redirect("/dashboard")

    return render_template("login.html", error=None)

@app.route("/profile", methods=["GET", "POST"])
def profile():
    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":
        conn = get_db()
        cur = conn.cursor()

        cur.execute("""
        INSERT OR REPLACE INTO profile
        (user_id, qualification, graduation_year, current_skills, interests, 
         career_field, long_term_goal, short_term_goal, daily_time, sector)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            session["user_id"],
            request.form["qualification"],
            request.form["graduation_year"],
            request.form["current_skills"],
            request.form["interests"],
            request.form["career_field"],
            request.form["long_term_goal"],
            request.form["short_term_goal"],
            int(request.form["daily_time"]),
            request.form["sector"]
        ))

        conn.commit()
        conn.close()
        return redirect("/dashboard")

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM profile WHERE user_id=?", (session["user_id"],))
    user_profile = cur.fetchone()
    conn.close()

    return render_template("profile.html", profile=user_profile, careers=CAREER_ROADMAP.keys())

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]
    conn = get_db()
    cur = conn.cursor()

    # Get user profile
    cur.execute("SELECT * FROM profile WHERE user_id=?", (user_id,))
    profile = cur.fetchone()

    if not profile:
        conn.close()
        return redirect("/profile")

    # Parse user skills
    user_skills = {
        s.strip().lower()
        for s in (profile["current_skills"] or "").split(",")
        if s.strip()
    }

    goal = profile["long_term_goal"]
    daily_time = profile["daily_time"]
    sector = profile["sector"]

    # Get career roadmap
    roadmap = CAREER_ROADMAP.get(goal, [])

    # Calculate missing skills
    missing_skills = [
        step["skill"]
        for step in roadmap
        if step["skill"] not in user_skills
    ]

    # Generate AI-powered recommendations
    recommendations = []
    for skill in missing_skills[:5]:  # Top 5 missing skills
        youtube_courses = get_youtube_courses(skill)
        github_projects = get_github_projects(skill)
        
        recommendations.append({
            "skill": skill,
            "courses": youtube_courses,
            "projects": github_projects[:2]
        })

    # Roadmap visualization
    roadmap_graph = [
        {
            "skill": step["skill"],
            "completed": step["skill"] in user_skills,
            "priority": step["priority"]
        }
        for step in roadmap
    ]

    # Calculate completion percentage
    total_skills = len(roadmap)
    completed_skills = sum(1 for step in roadmap if step["skill"] in user_skills)
    completion_percentage = int((completed_skills / total_skills * 100)) if total_skills > 0 else 0

    # Get proper heatmap data
    heatmap_data = get_heatmap_data(user_id, daily_time)

    # Calculate streak - FIXED VERSION
    today = datetime.now().date()
    cur.execute("""
        SELECT date, goal_met FROM activity 
        WHERE user_id=? AND goal_met=1 
        ORDER BY date DESC
    """, (user_id,))
    
    activities = cur.fetchall()
    current_streak = 0
    
    if activities:
        # Convert to date objects
        activity_dates = [datetime.strptime(a["date"], "%Y-%m-%d").date() for a in activities]
        
        # Check if there's activity today or yesterday to start streak
        if activity_dates[0] >= today - timedelta(days=1):
            current_streak = 1
            prev_date = activity_dates[0]
            
            # Count consecutive days
            for activity_date in activity_dates[1:]:
                if (prev_date - activity_date).days == 1:
                    current_streak += 1
                    prev_date = activity_date
                else:
                    break

    # Get today's progress
    today_str = today.isoformat()
    cur.execute("""
        SELECT SUM(minutes) as total FROM activity 
        WHERE user_id=? AND date=?
    """, (user_id, today_str))
    today_minutes = cur.fetchone()["total"] or 0
    today_percentage = min(int((today_minutes / daily_time) * 100), 100)

    # Get recent achievements
    cur.execute("""
        SELECT * FROM achievements 
        WHERE user_id=? 
        ORDER BY date DESC 
        LIMIT 5
    """, (user_id,))
    achievements = cur.fetchall()

    conn.close()

    return render_template(
        "dashboard.html",
        username=session.get("username"),
        daily_time=daily_time,
        heatmap_weeks=heatmap_data["weeks"],
        month_labels=heatmap_data["month_labels"],
        missing_skills=missing_skills,
        recommendations=recommendations,
        roadmap_graph=roadmap_graph,
        goal=goal,
        sector=sector,
        completion_percentage=completion_percentage,
        achievements=achievements,
        current_streak=current_streak,
        today_minutes=today_minutes,
        today_percentage=today_percentage
    )

@app.route("/log_activity", methods=["POST"])
def log_activity():
    if "user_id" not in session:
        return jsonify({"error": "Not logged in"}), 401
    
    data = request.json
    conn = get_db()
    cur = conn.cursor()
    
    # Get user's daily goal
    cur.execute("SELECT daily_time FROM profile WHERE user_id=?", (session["user_id"],))
    profile = cur.fetchone()
    daily_goal = profile["daily_time"] if profile else 60
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Check if activity exists for today
    cur.execute("""
        SELECT id, minutes FROM activity 
        WHERE user_id=? AND date=?
    """, (session["user_id"], today))
    
    existing = cur.fetchone()
    
    if existing:
        # Update existing activity
        new_minutes = existing["minutes"] + data.get("minutes", 30)
        goal_met = 1 if new_minutes >= daily_goal else 0
        
        cur.execute("""
            UPDATE activity 
            SET minutes=?, goal_met=? 
            WHERE id=?
        """, (new_minutes, goal_met, existing["id"]))
    else:
        # Insert new activity
        minutes = data.get("minutes", 30)
        goal_met = 1 if minutes >= daily_goal else 0
        
        cur.execute("""
            INSERT INTO activity (user_id, date, minutes, skill, goal_met)
            VALUES (?, ?, ?, ?, ?)
        """, (
            session["user_id"],
            today,
            minutes,
            data.get("skill", ""),
            goal_met
        ))
    
    conn.commit()
    conn.close()
    
    # Check for new achievements
    new_achievement = check_and_award_achievements(session["user_id"])
    
    return jsonify({
        "success": True, 
        "message": "Activity logged!",
        "new_achievement": new_achievement
    })

@app.route("/track_course_click", methods=["POST"])
def track_course_click():
    """Track when user clicks on a course link and mark skill as learning"""
    if "user_id" not in session:
        return jsonify({"error": "Not logged in"}), 401
    
    data = request.json
    skill = data.get("skill", "").lower()
    
    conn = get_db()
    cur = conn.cursor()
    
    # Get user's daily goal
    cur.execute("SELECT daily_time FROM profile WHERE user_id=?", (session["user_id"],))
    profile = cur.fetchone()
    daily_goal = profile["daily_time"] if profile else 60
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Add 30 minutes for clicking a course (assumed learning time)
    cur.execute("""
        SELECT id, minutes FROM activity 
        WHERE user_id=? AND date=?
    """, (session["user_id"], today))
    
    existing = cur.fetchone()
    
    if existing:
        new_minutes = existing["minutes"] + 30
        goal_met = 1 if new_minutes >= daily_goal else 0
        
        cur.execute("""
            UPDATE activity 
            SET minutes=?, skill=?, goal_met=?
            WHERE id=?
        """, (new_minutes, skill, goal_met, existing["id"]))
    else:
        goal_met = 1 if 30 >= daily_goal else 0
        
        cur.execute("""
            INSERT INTO activity (user_id, date, minutes, skill, goal_met)
            VALUES (?, ?, ?, ?, ?)
        """, (
            session["user_id"],
            today,
            30,
            skill,
            goal_met
        ))
    
    # AUTO-ADD SKILL: Check if this skill is tracked and add to profile if threshold met
    cur.execute("""
        SELECT COUNT(*) as count, SUM(minutes) as total_minutes
        FROM activity 
        WHERE user_id=? AND skill=?
    """, (session["user_id"], skill))
    
    skill_stats = cur.fetchone()
    course_clicks = skill_stats["count"] if skill_stats else 0
    total_skill_minutes = skill_stats["total_minutes"] if skill_stats else 0
    
    # Get current skills from profile
    cur.execute("SELECT current_skills FROM profile WHERE user_id=?", (session["user_id"],))
    profile_data = cur.fetchone()
    current_skills = profile_data["current_skills"] if profile_data and profile_data["current_skills"] else ""
    
    # Parse current skills
    skills_list = [s.strip().lower() for s in current_skills.split(",") if s.strip()]
    
    # AUTO-ADD SKILL: If user has studied this skill for 2+ hours (120+ min), auto-add it!
    skill_unlocked = False
    if skill and skill not in skills_list and total_skill_minutes >= 120:
        skills_list.append(skill)
        new_skills_str = ", ".join(skills_list)
        
        cur.execute("""
            UPDATE profile 
            SET current_skills=? 
            WHERE user_id=?
        """, (new_skills_str, session["user_id"]))
        
        skill_unlocked = True
        
        # Add achievement for learning new skill
        cur.execute("""
            INSERT INTO achievements (user_id, title, description, date)
            VALUES (?, ?, ?, ?)
        """, (
            session["user_id"],
            f"Mastered {skill.title()}!",
            f"Completed 2+ hours of {skill} learning",
            today
        ))
    
    conn.commit()
    conn.close()
    
    # Check for other new achievements
    new_achievement = check_and_award_achievements(session["user_id"])
    
    return jsonify({
        "success": True, 
        "message": "Course tracked!",
        "new_achievement": new_achievement or skill_unlocked,
        "skill_unlocked": skill_unlocked,
        "skill_name": skill if skill_unlocked else None,
        "minutes_learned": total_skill_minutes
    })

@app.route("/demo_mode")
def demo_mode():
    """Demo mode for hackathon presentation - shows the app with realistic data"""
    if "user_id" not in session:
        return redirect("/login")
    
    conn = get_db()
    cur = conn.cursor()
    
    today = datetime.now().date()
    
    # Add realistic learning activity for past 30 days
    for i in range(30):
        activity_date = (today - timedelta(days=i)).isoformat()
        
        # Vary minutes realistically (60-120 min on study days, 0 on some days)
        if i % 7 not in [5, 6]:  # Skip some weekends
            minutes = 60 + (i % 4) * 15  # 60, 75, 90, 105 minutes
            goal_met = 1
            
            # Rotate through skills
            skills = ['python', 'statistics', 'machine learning', 'data analysis']
            skill = skills[i % len(skills)]
            
            cur.execute("""
                INSERT OR REPLACE INTO activity (user_id, date, minutes, skill, goal_met)
                VALUES (?, ?, ?, ?, ?)
            """, (session["user_id"], activity_date, minutes, skill, goal_met))
    
    # Add demo achievements
    achievements_data = [
        ("First Steps", "Started your learning journey!", (today - timedelta(days=29)).isoformat()),
        ("7 Day Streak", "Completed 7 days of learning!", (today - timedelta(days=22)).isoformat()),
        ("Python Master", "Mastered Python programming!", (today - timedelta(days=15)).isoformat()),
        ("Data Wizard", "Completed 50 hours of learning!", (today - timedelta(days=10)).isoformat()),
        ("Consistency King", "21 day learning streak!", (today - timedelta(days=5)).isoformat()),
    ]
    
    # Clear old achievements first
    cur.execute("DELETE FROM achievements WHERE user_id=?", (session["user_id"],))
    
    for title, desc, date in achievements_data:
        cur.execute("""
            INSERT INTO achievements (user_id, title, description, date)
            VALUES (?, ?, ?, ?)
        """, (session["user_id"], title, desc, date))
    
    # Auto-add skills to profile for demo (simulate completed learning)
    cur.execute("SELECT current_skills FROM profile WHERE user_id=?", (session["user_id"],))
    profile_data = cur.fetchone()
    
    demo_skills = "python, statistics, machine learning"
    
    cur.execute("""
        UPDATE profile 
        SET current_skills=? 
        WHERE user_id=?
    """, (demo_skills, session["user_id"]))
    
    conn.commit()
    conn.close()
    
    return redirect("/dashboard")

@app.route("/clear_data")
def clear_data():
    if "user_id" not in session:
        return redirect("/login")
    
    conn = get_db()
    cur = conn.cursor()
    
    # Clear activity & achievements
    cur.execute("DELETE FROM activity WHERE user_id=?", (session["user_id"],))
    cur.execute("DELETE FROM achievements WHERE user_id=?", (session["user_id"],))
    
    # Reset profile career-related fields
    cur.execute("""
        UPDATE profile
        SET current_skills='',
            long_term_goal=NULL,
            short_term_goal=NULL,
            sector=NULL
        WHERE user_id=?
    """, (session["user_id"],))
    
    conn.commit()
    conn.close()
    
    return redirect("/profile")


@app.route("/check_data")
def check_data():
    if "user_id" not in session:
        return "Not logged in"
    
    conn = get_db()
    cur = conn.cursor()
    
    # Check activity
    cur.execute("SELECT * FROM activity WHERE user_id=?", (session["user_id"],))
    activities = cur.fetchall()
    
    # Check achievements
    cur.execute("SELECT * FROM achievements WHERE user_id=?", (session["user_id"],))
    achievements = cur.fetchall()
    
    conn.close()
    
    return f"""
    <h2>Your Data:</h2>
    <h3>Activities: {len(activities)}</h3>
    <pre>{[dict(a) for a in activities]}</pre>
    
    <h3>Achievements: {len(achievements)}</h3>
    <pre>{[dict(a) for a in achievements]}</pre>
    
    <br><a href="/dashboard">Back to Dashboard</a>
    """

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5000)

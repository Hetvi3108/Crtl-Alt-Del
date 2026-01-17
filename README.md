# Skill Intelligence 🚀

*A Personalized Skill Tracking & Progress Visualization Platform*

---

## 📌 Project Overview

**Skill Intelligence** is a web-based platform designed to help users **track their skills, education, and progress visually** over time.
It enables students and professionals to register, create a profile, and view a **GitHub-style activity heatmap dashboard** that represents their learning consistency.

The project focuses on:

* Clean UI/UX
* Data privacy
* Scalability
* Simplicity for hackathon deployment

---

## ✨ Features

* 🔐 User Authentication (Register & Login)
* 👤 Profile Completion

  * Highest qualification
  * Expected graduation
  * Skill domains
* 📊 Dashboard with Yearly Progress Heatmap
* 🗓 Month-wise activity visualization
* 🌙 Modern dark-theme UI
* ⚡ Lightweight Flask backend
* 🎯 Hackathon-ready structure

---

## 🛠 Tech Stack

### Frontend

* HTML5
* CSS3 (Custom, no framework)
* Jinja2 Templates

### Backend

* Python
* Flask

### Database

* SQLite (local, lightweight)

---

## 📂 Project Structure

```
skill-intelligence/
│
├── app.py
├── database.db
├── requirements.txt
├── README.md
│
├── static/
│   └── style.css
│
└── templates/
    ├── login.html
    ├── register.html
    ├── profile.html
    └── dashboard.html
```

---

## ⚙️ Setup & Run Locally

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/skill-intelligence.git
cd skill-intelligence
```

### 2️⃣ Create Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
```

Activate it:

**Windows**

```bash
venv\Scripts\activate
```

**Mac / Linux**

```bash
source venv/bin/activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Run the Application

```bash
python app.py
```

---

### 5️⃣ Open in Browser

```
http://127.0.0.1:5000/login
```

---

## 🔐 Environment Variables (Example)

This project does **not require sensitive environment variables**.

If needed for deployment:

```bash
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your_secret_key_here
```

⚠️ **Do NOT commit real secrets to GitHub**

---

## 🧪 Test Login Credentials

You can create a test account using the **Register page**.

Example:

```
Username: testuser
Password: test123
```

(No default credentials are hardcoded)

---

## 🧯 Basic Error Handling

* Required form fields enforced using HTML validation
* Login failure shows error message
* Invalid routes return 404
* Duplicate usernames prevented at backend level
* Safe redirects using Flask sessions

---

## 🔒 Security & Privacy

* Passwords are **never hardcoded**
* No API keys or secrets committed
* SQLite database is local-only
* Session-based authentication
* No third-party tracking scripts

---

## ✅ Confirmation

✔ No secrets are stored in the repository
✔ Safe for public GitHub submission
✔ Suitable for hackathons & demos

---

## 📌 Future Enhancements

* AI-based skill roadmap generation
* Heatmap data persistence
* Charts & analytics
* OAuth login
* Cloud deployment

---

## 👩‍💻 Built For Hackathons

Designed with **clean architecture, extensibility, and judge-friendly UI** in mind.


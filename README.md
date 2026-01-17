# 📅 Smart Academic Calendar 🚀

*A Personalized Skill Tracking & Academic Progress Visualization Platform*

---

## 📌 Project Overview

**Smart Academic Calendar** is a web-based platform designed to help students and professionals **track academic activities, skills, and learning consistency visually over time**.

The platform allows users to register, complete their academic profile, and view a **GitHub-style activity heatmap dashboard** that reflects their daily learning or academic engagement.

The project emphasizes:

* Clean and intuitive UI/UX
* Academic progress visualization
* Data privacy and security
* Scalability and simplicity
* Hackathon-friendly deployment

---

## ✨ Features

* 🔐 User Authentication (Register & Login)
* 👤 Academic Profile Completion

  * Highest qualification
  * Expected graduation year
  * Skill or subject domains
* 📊 Dashboard with Yearly Academic Activity Heatmap
* 🗓 Month-wise learning consistency visualization
* 🌙 Modern dark-themed UI
* ⚡ Lightweight Flask backend
* 🎯 Optimized for hackathons and demos

---

## 🛠 Tech Stack

### Frontend

* HTML5
* CSS3 (Custom, no frameworks)
  

### Backend

* Python
* Flask

### Database

* SQLite (Local & lightweight)

---

## 📂 Project Structure

```
smart-academic-calendar/
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
git clone https://github.com/your-username/smart-academic-calendar.git
cd smart-academic-calendar
```

---

### 2️⃣ Create Virtual Environment (Optional)

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

## 🔐 Environment Variables (Optional)

This project does **not require sensitive environment variables**.

For development or deployment:

```bash
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your_secret_key_here
```

⚠️ **Never commit real secrets to public repositories**

---

## 🧪 Test Account

Create a test user via the **Register page**.

Example:

```
Username: testuser
Password: test123
```

(No default credentials are hardcoded)

---

## 🧯 Basic Error Handling

* Mandatory form fields enforced via HTML validation
* Invalid login shows error messages
* Duplicate usernames prevented at backend level
* Safe session-based redirects
* Invalid routes return 404

---

## 🔒 Security & Privacy

* Passwords are securely handled (not hardcoded)
* No API keys or secrets stored in code
* Local SQLite database
* Session-based authentication
* No third-party trackers or analytics

---

## ✅ Confirmation

✔ No sensitive data committed
✔ Safe for public GitHub repositories


---

## 📌 Future Enhancements

* AI-powered academic roadmap generation
* Persistent heatmap activity data
* Analytics & performance insights
* OAuth / Google login
* Cloud deployment (AWS / Render / Railway)




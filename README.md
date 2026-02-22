# 🏭 AI Course Factory

> **Built for the "Automate Me If You Can" Hackathon — powered by Accomplish AI**

AI Course Factory is a SaaS web application that **automatically generates complete, structured courses** on any topic using AI. Enter a topic, choose a level, and get a full course with modules, lessons, and quizzes — in seconds.

---

## 🎯 The Problem (Before)

Creating a structured course manually takes hours:
- Writing a curriculum outline
- Breaking it into modules and lessons
- Writing lesson content
- Creating quizzes for each module
- Formatting everything consistently

This is exactly the kind of **boring, repetitive knowledge work** that eats up educators' and creators' time every day.

---

## ✨ The Solution (After — with Accomplish AI)

Using **Accomplish AI**, the entire Django SaaS project was built step by step — from database models to API integration — without writing a single line of code manually.

Accomplish:
- Created Django apps (`accounts`, `dashboard`, `agents`)
- Configured PostgreSQL (Supabase) database
- Built authentication (signup, login, logout)
- Set up templates and base layout
- Integrated Groq AI API for course generation
- Saved all generated content to the database

**What used to take days now takes minutes — for both building the app AND generating courses.**

---

## 🚀 Features

- 🔐 User authentication (signup, login, logout)
- 🤖 AI-powered course generation using Groq (LLaMA 3.3)
- 📚 Structured output: Modules → Lessons → Quizzes
- 🗄️ PostgreSQL database (Supabase) to store all courses
- 👤 Personal dashboard per user
- 📱 Clean, responsive UI

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django 6.0 |
| Database | PostgreSQL (Supabase) |
| AI | Groq API (LLaMA 3.3 70B) |
| Frontend | Django Templates + Tailwind CSS |
| Built with | Accomplish AI |

---

## ⚙️ Setup & Installation

### 1. Clone the repo
```bash
git clone https://github.com/jass2422/AI-Course-Factory.git
cd AI-Course-Factory
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Create `.env` file
```
GROQ_API_KEY=your-groq-api-key-here
DATABASE_URL=postgres://USER:PASSWORD@HOST:5432/DBNAME
```

### 5. Run migrations
```bash
python manage.py migrate
```

### 6. Start the server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` 🎉

---

## 🎬 How It Works

1. **Sign up** for an account
2. Go to **Dashboard**
3. Enter a **topic** (e.g. "Machine Learning")
4. Choose a **level** (Beginner / Intermediate / Advanced)
5. Click **Generate My Course**
6. AI generates a complete course with modules, lessons, and quizzes
7. Course is saved to your dashboard for future access

---

## 🤖 Built with Accomplish AI

This entire project was built using [Accomplish](https://accomplish.ai) — an open source AI coworker that runs locally on your desktop.

**Accomplish handled:**
- Project scaffolding
- Database configuration
- View and URL creation
- Template generation
- API integration
- Git setup

Every action was shown and approved before running. Nothing left the machine without permission.

---

## 📁 Project Structure

```
ai_course_factory/
├── accounts/          # Auth: signup, login, logout
├── dashboard/         # Course generation & display
│   ├── models.py      # Course, Module, Lesson, Quiz
│   └── views.py       # Generate & display courses
├── agents/            # AI agent logic
├── templates/         # HTML templates
│   ├── base.html
│   ├── landing.html
│   ├── dashboard/
│   └── partials/
└── ai_course_factory/ # Django settings & URLs
```

---

## 🏆 Hackathon Track

**Highlight Track** — Showcasing how Accomplish AI was used to automate the building of a real SaaS product from scratch, step by step, without manual coding.

---

## 📄 License

MIT License — feel free to use and build on this!

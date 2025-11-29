# 🧠 Smart Task Analyzer — Junikyun Edition  
### A lightweight task-prioritization system powered by Django REST + Vanilla JS

This project analyzes tasks using intelligent scoring strategies to help users decide *what to work on next*.  
It was built as part of the **Singularium Internship Assignment 2025**.

---

## 🎯 Features at a Glance

✔ REST API built with Django REST Framework  
✔ Frontend built using HTML + CSS + JavaScript  
✔ Multiple analysis strategies  
✔ Color-coded priority results  
✔ Circular dependency detection  
✔ Weekend-aware urgency logic  
✔ Top-3 Suggestion API  
✔ JSON bulk input support  

---

## Project Structure

```
task-analyzer/
│
├── backend/
│   ├── manage.py
│   ├── task_analyzer/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   └── tasks/
│       ├── serializers.py
│       ├── scoring.py
│       ├── views.py
│       ├── urls.py
│       └── tests.py
│
└── frontend/
    ├── index.html
    ├── styles.css
    └── script.js
```

Simple. Clean. No unnecessary clutter.

---

## 🧠 How the Algorithm Works

Each task receives a score based on:

### Urgency  
Calculated from due date  
Past-due tasks get a very high urgency score  
Weekends reduce urgency slightly (bonus feature)

### Importance  
Converted from scale **1–10 → 0–100**

### Effort  
Lower effort = higher score  
Uses a log-based transformation

###  Dependency Impact  
Tasks that block other tasks receive extra weight

---

##  Strategy Modes

You can analyze tasks in multiple ways:

| Strategy        | What it does                            |
|-----------------|-----------------------------------------|
|  Smart Balance  | Balanced across urgency, impact, effort |
|  Fastest Wins   | Focus on low-effort tasks               |
|  High Impact    | Importance matters most                 |
|  Deadline Driven| Urgency dominates                       |

The backend changes weights dynamically depending on the selected strategy.

---

## 🔌 API Endpoints

###  **Analyze All Tasks**
`POST /api/tasks/analyze/`

###  **Get Top-3 Recommendations**
`POST /api/tasks/suggest/`

Both endpoints accept:
```json
{
  "strategy": "smart",
  "tasks": [ ... ]
}
```

---

## 🖥️ Running the Project

### 1 Create Virtual Environment
```
python -m venv venv
venv\Scripts\activate
```

### 2 Install Requirements
```
cd backend
pip install -r requirements.txt
```

### 3 Run Backend
```
python manage.py runserver
```

API URL:
```
http://127.0.0.1:8000/api/tasks/
```

### 4 Run Frontend
Open:
```
frontend/index.html
```

No build tools needed — fully static frontend.

---

## Frontend Screens & Features

- Clean card-based UI  
- Add single task  
- Add tasks via JSON  
- Delete tasks  
- Strategy selection  
- Real-time results  
- Color-coded priority levels:
  - 🔴 High  
  - 🟠 Medium  
  - 🟢 Low  

---

##  Tests

Run backend tests:

```
python manage.py test
```

Covers:
- Urgency score  
- Effort calculation  
- Strategy differences  
- Analysis output  

---

## 👩‍💻 Developer  
**Devika K**  
Smart Task Analyzer — Junikyun Edition  
Built for the Singularium Internship Assignment 2025 

---

If you like this project, ⭐ star it on GitHub!

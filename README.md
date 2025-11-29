🧠 Smart Task Analyzer — Junikyun Edition

A lightweight, full-stack task prioritization system that helps users decide what to work on next.
Built using Django REST Framework for the backend and Vanilla JavaScript + HTML/CSS for the frontend.

This project was created as part of the Singularium Internship Assignment (2025).


🚀Features

Analyze tasks based on urgency, importance, effort, and dependencies.

Supports multiple prioritization strategies:
smart → balanced approach
fastest → favors low-effort tasks
impact → favors high-importance tasks
deadline → favors urgent tasks
Detects circular dependencies among tasks.
Returns top 3 suggestions for "what should I do now?".


User-friendly frontend with task form, JSON input, and visual priority indicators.

🛠️ Setup Instructions
1. Clone the repository:
git clone https://github.com/Devika-Gowda/task-analyzer.git
cd task-analyzer

2. Create a virtual environment and activate it:
python -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows

3. Install dependencies:
pip install -r requirements.txt

4. Run the server:
python manage.py runserver

Backend API will be available at http://127.0.0.1:8000/api/tasks/analyze/.

5. Open the frontend:
Open index.html in your browser. Input tasks manually or paste JSON, select a strategy, and analyze.

Algorithm Explanation:

The priority scoring algorithm assigns each task a numeric score between 0–100 using four factors:
1.	Urgency
o	Converts the due date into a score, where near-deadline or past-due tasks get higher scores.
o	Includes weekend adjustment, reducing urgency by 10% on Saturdays/Sundays.

2.	Importance
o	Based on user input (1–10). Normalized to a 0–100 scale.

3.	Effort
o	Low-effort tasks receive higher scores to promote quick wins.
o	Computed using an inverse logarithmic function to avoid extreme differences.

4.	Dependency Impact
o	Tasks that many other tasks depend on are given higher scores.
o	Computed as a percentage of maximum dependency counts.

Weighted Scoring & Strategies:
Default (smart): balanced weight between urgency, importance, effort, and dependency.
Other strategies adjust weights to emphasize one factor over others:

fastest → more weight to effort
impact → more weight to importance
deadline → more weight to urgency

Circular Dependency Detection:
Uses Kahn’s topological sorting algorithm to detect cycles.
If cycles exist, a warning is displayed on the frontend.
After computing individual scores, tasks are sorted descending and returned with a detailed explanation of each factor.


💡 Design Decisions
•	No database storage: simplifies the assignment and focuses on scoring logic.
•	Task IDs: fallback to title if id missing; ensures unique identification in frontend & backend.
•	Frontend: lightweight, minimal dependencies, works without server-side rendering.
•	Scoring weights: chosen for balance but adjustable per strategy for flexibility.
•	JSON input option: supports bulk task input and testing.

Trade-offs:
•	Did not implement persistent storage due to assignment scope.
•	No user authentication or multi-user support.
•	Circular dependency visualization limited to warning message.


Section / Task	                                                                                      Time Spent
Backend Development (models, scoring algorithm)	                                                        2 hours
API Endpoints (analyze & suggest)	                                                                    1 hour
Frontend Development (form, JSON input, strategy toggle)	                                            1.5 hours
Algorithm Testing & Unit Tests	                                                                        1 hour
Bonus Features (Smart Balance, Weekend-aware urgency, circular dependency detection)	                1.5 hours
Documentation & README	                                                                                1 hour
Total	                                                                                                8 hours


Bonus Challenges Implemented:
•	JSON bulk input for multiple tasks
•	Smart Balance mode for workload distribution
•	Weekend-aware urgency calculation
•	Circular dependency detection


Future Improvements:
•	Visual dependency graph for tasks
•	Eisenhower Matrix view (Urgent vs Important)
•	Learning system to adjust algorithm based on user feedback
•	Full mobile-first responsive redesign
•	Integration with external calendar APIs for real-time deadlines


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

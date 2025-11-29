"""
scoring.py
-----------
This module contains the heart of the assignment:
a clean, explainable scoring algorithm that prioritizes tasks
based on urgency, importance, effort, and dependency impact.

Includes:
- Weekend-aware urgency adjustment
- Circular dependency detection
- Strategy-based weight variation
"""

from datetime import date, datetime
from collections import defaultdict, deque
import math

# --------------------------------------------------------
# Helper: Safe date conversion
# --------------------------------------------------------
def safe_date(d):
    try:
        return datetime.fromisoformat(d).date()
    except:
        return None


# --------------------------------------------------------
# Circular Dependency Detection (Kahn's Algorithm)
# --------------------------------------------------------
def detect_cycle(tasks):
    """
    Detect circular dependencies using topological sorting logic.
    Returns True if a cycle exists.
    """
    graph = defaultdict(list)
    ids = {str(t["id"]) for t in tasks}

    for t in tasks:
        tid = str(t["id"])
        for dep in t.get("dependencies", []):
            if dep in ids:
                graph[dep].append(tid)

    in_deg = {x: 0 for x in ids}
    for u in graph:
        for v in graph[u]:
            in_deg[v] += 1

    queue = deque([x for x in ids if in_deg[x] == 0])
    visited = 0

    while queue:
        u = queue.popleft()
        visited += 1
        for v in graph[u]:
            in_deg[v] -= 1
            if in_deg[v] == 0:
                queue.append(v)

    return visited != len(ids)  # True if cycle exists


# --------------------------------------------------------
# Urgency Score (includes weekend adjustments)
# --------------------------------------------------------
def urgency_score(due):
    """
    Converts due date proximity into 0–100 urgency scale.
    - Near deadlines → high score.
    - Past due → very high.
    - Weekends reduce urgency slightly for realism.
    """
    if not due:
        return 30  # neutral

    due = safe_date(due)
    today = date.today()
    diff = (due - today).days

    # Past-due tasks
    if diff < 0:
        return min(100, 85 + abs(diff))

    # Base urgency
    if diff <= 30:
        score = 100 - diff * 2
    else:
        score = max(5, 50 - math.log(diff + 1) * 4)

    # Weekend adjustment (bonus feature)
    if today.weekday() >= 5:  # Saturday/Sunday
        score *= 0.9  # Reduce urgency by 10%

    return round(score)


# --------------------------------------------------------
# Effort Score (lower hours = higher score)
# --------------------------------------------------------
def effort_score(hours):
    if not hours or hours <= 0:
        return 100
    return max(10, 100 / (1 + math.log1p(hours)))


# --------------------------------------------------------
# Dependency Impact Score
# --------------------------------------------------------
def dependency_scores(tasks):
    counts = defaultdict(int)

    for t in tasks:
        for dep in t.get("dependencies", []):
            counts[dep] += 1

    if not counts:
        return {t["id"]: 0 for t in tasks}

    max_dep = max(counts.values())

    return {
        t["id"]: int((counts.get(t["id"], 0) / max_dep) * 100)
        for t in tasks
    }


# --------------------------------------------------------
# Main Analyzer Function
# --------------------------------------------------------
def analyze(tasks, strategy="smart"):
    """
    Applies weighting logic based on selected strategy.

    Supported strategies:
    - fastest   (effort-focused)
    - impact    (importance-focused)
    - deadline  (urgency-focused)
    - smart     (balanced)
    """

    # Detect circular dependencies
    cycle_exists = detect_cycle(tasks)

    # Compute dependency influence
    dep_scores = dependency_scores(tasks)

    # Base weights (balanced)
    weights = {
        "urgency": 0.35,
        "importance": 0.35,
        "effort": 0.15,
        "dependency": 0.15,
    }

    # Adjust weights per strategy
    if strategy == "fastest":
        weights["effort"] += 0.3
    elif strategy == "impact":
        weights["importance"] += 0.4
    elif strategy == "deadline":
        weights["urgency"] += 0.4

    results = []

    for t in tasks:
        uid = t["id"]

        urg = urgency_score(t.get("due_date"))
        imp = (t.get("importance", 5) - 1) / 9 * 100
        eff = effort_score(t.get("estimated_hours"))
        dep = dep_scores.get(uid, 0)

        # Weighted score computation
        score = (
            urg * weights["urgency"] +
            imp * weights["importance"] +
            eff * weights["effort"] +
            dep * weights["dependency"]
        )

        results.append({
            "task": t,
            "score": round(score, 2),
            "explanation": f"Urg={urg}, Imp={imp:.1f}, Eff={eff:.1f}, Dep={dep}"
        })

    # Sort highest priority first
    results.sort(key=lambda x: x["score"], reverse=True)

    return {
        "has_cycle": cycle_exists,
        "results": results
    }

// script.js

let tasks = [];

// Render tasks in Current Tasks list
function renderTasks() {
    const list = document.getElementById("taskList");
    list.innerHTML = "";

    tasks.forEach((t, i) => {
        let li = document.createElement("li");
        li.className = "task-card";
        li.innerHTML = `
            <strong>${t.title}</strong>
            <span class="tag">ID: ${t.id}</span><br>
            <small>Due: ${t.due_date || "—"} | Effort: ${t.estimated_hours}h | Importance: ${t.importance}</small>
            <br>
            <button onclick="removeTask(${i})" class="btn-secondary" style="margin-top:8px;">Remove</button>
        `;
        list.appendChild(li);
    });
}

// Remove a task
function removeTask(i) {
    tasks.splice(i, 1);
    renderTasks();
}

// Add task from form
document.getElementById("addTask").onclick = () => {
    const t = {
        id: Date.now().toString(),
        title: document.getElementById("title").value.trim(),
        due_date: document.getElementById("due_date").value,
        estimated_hours: parseFloat(document.getElementById("estimated_hours").value),
        importance: parseInt(document.getElementById("importance").value),
        dependencies: document.getElementById("dependencies").value
            .split(",")
            .map(s => s.trim())
            .filter(Boolean)
    };

    if (!t.title) {
        alert("Title is required.");
        return;
    }

    tasks.push(t);
    renderTasks();

    // Clear form fields
    document.getElementById("title").value = "";
    document.getElementById("due_date").value = "";
    document.getElementById("estimated_hours").value = 1;
    document.getElementById("importance").value = 5;
    document.getElementById("dependencies").value = "";
};

// Clear all tasks and results
document.getElementById("clearAll").onclick = () => {
    tasks = [];
    renderTasks();
    document.getElementById("results").innerHTML = "";
    document.getElementById("jsonInput").value = "";
};

// Analyze tasks
document.getElementById("analyze").onclick = async () => {
    let taskPayload = [...tasks];

    // If user pasted JSON
    try {
        const jsonInput = document.getElementById("jsonInput").value.trim();
        if (jsonInput) {
            taskPayload = JSON.parse(jsonInput);
            tasks = [...taskPayload]; // update global tasks
            renderTasks(); // show in Current Tasks
        }
    } catch (err) {
        alert("Invalid JSON input.");
        return;
    }

    if (taskPayload.length === 0) {
        alert("No tasks to analyze.");
        return;
    }

    const strategy = document.getElementById("strategy").value;

    try {
        const res = await fetch("http://127.0.0.1:8000/api/tasks/analyze/", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({tasks: taskPayload, strategy})
        });

        if (!res.ok) throw new Error("Server error");

        const data = await res.json();
        showResults(data);
    } catch(err) {
        alert("Analysis failed: " + err.message);
    }
};

// Show analysis results
function showResults(data) {
    const container = document.getElementById("results");
    container.innerHTML = "";

    // Show selected strategy
    container.innerHTML = `<p><strong>Strategy Used:</strong> ${document.getElementById("strategy").value}</p>`;

    // Warning for cycle
    if (data.has_cycle) {
        container.innerHTML += `<p style="color:red;"><strong>Warning:</strong> Circular dependency detected!</p>`;
    }

    // List results
    data.results.forEach(item => {
        const score = Number(item.score);
        let cls = "priority-low";

        if (score >= 75) cls = "priority-high";
        else if (score >= 50) cls = "priority-medium";

        const card = document.createElement("div");
        card.className = cls;
        card.style.padding = "12px";
        card.style.marginTop = "10px";
        card.style.borderRadius = "8px";

        card.innerHTML = `
            <strong>${item.task.title}</strong>
            <span class="tag">Score: ${score}</span>
            <br>
            <small>${item.explanation}</small>
            <br>
            <small>Due: ${item.task.due_date || "—"} | Effort: ${item.task.estimated_hours}h | Importance: ${item.task.importance}</small>
        `;

        container.appendChild(card);
    });
}



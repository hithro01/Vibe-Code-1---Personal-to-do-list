"""
Beginner Project 1: Simple To‑Do List Web App
------------------------------------------------

This Flask application implements a minimalist to‑do list that runs
locally in your browser. It stores tasks in a JSON file on disk so
they persist across server restarts. Users can add new tasks, mark
tasks as complete, and delete tasks from the list. A lightweight
Bootstrap stylesheet provides basic styling without the need to write
custom CSS.

Running the app
===============

1. Install the dependencies from `requirements.txt` (Flask and
   click, which Flask uses under the hood)::

    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

2. Start the development server::

    flask --app app run --reload

3. Navigate to http://localhost:5000/ in your browser. You can now
   add, complete and delete tasks.

This code is intentionally straightforward so that beginners can
understand how the routes and template rendering work. If you want
to extend this into a more robust application (for example by using
SQLite or SQLAlchemy, adding user authentication, or deploying to a
hosted service) the modular structure makes it easy to grow.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import List, Dict, Any

from flask import Flask, render_template, request, redirect, url_for


BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "tasks.json"

app = Flask(__name__)


def load_tasks() -> List[Dict[str, Any]]:
    """Load tasks from the JSON data file.

    If the file does not exist, return an empty list.
    """
    if not DATA_FILE.exists():
        return []
    try:
        with DATA_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        # In case the file is corrupted or empty
        return []


def save_tasks(tasks: List[Dict[str, Any]]) -> None:
    """Write the list of tasks back to the JSON data file."""
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2)


@app.route("/")
def index() -> str:
    """Render the main page showing all tasks."""
    tasks = load_tasks()
    return render_template("index.html", tasks=tasks)


@app.route("/add", methods=["POST"])
def add_task() -> str:
    """Add a new task to the list."""
    title = request.form.get("title", "").strip()
    if title:
        tasks = load_tasks()
        tasks.append({
            "title": title,
            "completed": False
        })
        save_tasks(tasks)
    return redirect(url_for("index"))


@app.route("/complete/<int:task_id>", methods=["POST"])
def complete_task(task_id: int) -> str:
    """Mark the selected task as completed."""
    tasks = load_tasks()
    if 0 <= task_id < len(tasks):
        tasks[task_id]["completed"] = True
        save_tasks(tasks)
    return redirect(url_for("index"))


@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id: int) -> str:
    """Delete the selected task from the list."""
    tasks = load_tasks()
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
        save_tasks(tasks)
    return redirect(url_for("index"))


if __name__ == "__main__":
    # Ensures the tasks file exists so that the folder can be mounted in
    # Docker or other deployment scenarios
    if not DATA_FILE.exists():
        save_tasks([])
    app.run(debug=True)
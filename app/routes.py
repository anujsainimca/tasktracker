"""
app/routes.py  —  TaskTracker API
Simple task management REST API.
"""
from flask import jsonify, request
from app import app

TASKS = []

@app.route("/health")
def health():
    return jsonify({"status": "ok", "tasks": len(TASKS)})

@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(TASKS)

@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "title is required"}), 400
    task = {"id": len(TASKS) + 1, "title": data["title"], "done": False}
    TASKS.append(task)
    return jsonify(task), 201

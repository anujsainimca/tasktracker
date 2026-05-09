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

@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "request body required"}), 400
    for task in TASKS:
        if task["id"] == task_id:
            if "title" in data:
                task["title"] = data["title"]
            if "done" in data:
                task["done"] = bool(data["done"])
            return jsonify(task), 200
    return jsonify({"error": "task not found"}), 404

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    for i, task in enumerate(TASKS):
        if task["id"] == task_id:
            TASKS.pop(i)
            return "", 204
    return jsonify({"error": "task not found"}), 404

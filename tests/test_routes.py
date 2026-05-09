"""tests/test_routes.py"""
import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c

def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200

def test_create_task(client):
    r = client.post("/tasks", json={"title": "Buy milk"})
    assert r.status_code == 201
    assert r.get_json()["title"] == "Buy milk"

def test_update_task_done(client):
    r = client.post("/tasks", json={"title": "Fix bug"})
    task_id = r.get_json()["id"]
    r = client.put(f"/tasks/{task_id}", json={"done": True})
    assert r.status_code == 200
    assert r.get_json()["done"] is True

def test_update_task_title(client):
    r = client.post("/tasks", json={"title": "Old title"})
    task_id = r.get_json()["id"]
    r = client.put(f"/tasks/{task_id}", json={"title": "New title"})
    assert r.status_code == 200
    assert r.get_json()["title"] == "New title"

def test_update_task_not_found(client):
    r = client.put("/tasks/9999", json={"done": True})
    assert r.status_code == 404

def test_update_task_no_body(client):
    r = client.post("/tasks", json={"title": "Some task"})
    task_id = r.get_json()["id"]
    r = client.put(f"/tasks/{task_id}", data="", content_type="application/json")
    assert r.status_code == 400

def test_delete_task(client):
    r = client.post("/tasks", json={"title": "To delete"})
    task_id = r.get_json()["id"]
    r = client.delete(f"/tasks/{task_id}")
    assert r.status_code == 204

def test_delete_task_not_found(client):
    r = client.delete("/tasks/9999")
    assert r.status_code == 404

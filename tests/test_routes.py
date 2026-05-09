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

def test_delete_task(client):
    r = client.post("/tasks", json={"title": "To delete"})
    task_id = r.get_json()["id"]
    r = client.delete(f"/tasks/{task_id}")
    assert r.status_code == 204

def test_delete_task_not_found(client):
    r = client.delete("/tasks/9999")
    assert r.status_code == 404

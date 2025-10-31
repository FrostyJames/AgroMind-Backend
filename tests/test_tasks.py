import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.routes import tasks


app = FastAPI()
app.include_router(tasks.router)

client = TestClient(app)


def test_add_task():
    payload = {"crop": "Maize", "date": "2025-10-28", "activity": "Watering"}
    response = client.post("/tasks", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Task added"
    assert data["task"]["crop"] == "Maize"


def test_get_tasks():
    # Add one task first
    client.post("/tasks", json={"crop": "Beans", "date": "2025-10-28", "activity": "Weeding"})

    response = client.get("/tasks")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "crop" in data[0]

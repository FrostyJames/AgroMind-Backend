from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter()

# Temporary in-memory store
tasks_db = []

class Task(BaseModel):
    crop: str
    date: str
    activity: str

@router.post("/tasks")
def add_task(task: Task):
    tasks_db.append(task)
    return {"message": "Task added", "task": task}

@router.get("/tasks")
def get_tasks() -> List[Task]:
    return tasks_db
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()
router = APIRouter()

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend domain for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Temporary in-memory store
tasks_db = []

class Task(BaseModel):
    crop: str
    date: str
    activity: str

@router.post("/tasks")
def add_task(task: Task):
    print(f"📥 Received task: {task}")
    tasks_db.append(task)
    return {"message": "Task added", "task": task}

@router.get("/tasks", response_model=List[Task])
def get_tasks():
    print(f"📤 Returning {len(tasks_db)} tasks")
    return tasks_db


app.include_router(router)
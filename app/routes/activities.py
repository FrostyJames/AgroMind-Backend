from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter()

# Temporary in-memory store
activities_db = []

class Activity(BaseModel):
    date: str
    task: str
    crop: str
    yield_: str  # avoid Python keyword conflict
    notes: str
    status: str

@router.post("/activities")
def add_activity(activity: Activity):
    activities_db.append(activity)
    return {"message": "Activity added", "activity": activity}

@router.get("/activities")
def get_activities() -> List[Activity]:
    return activities_db
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db import Base, engine
from app.routes import auth_routes, crop_routes, farm_routes, tasks, alert_route
from app.routes.recommendation_routes import router as recommendation_routes
from app.routes.ai import router as ai_routes
from app.routes.activities import router as activities_routes  # ✅ NEW import

# ✅ Create database tables
Base.metadata.create_all(bind=engine)

# ✅ Initialize FastAPI app
app = FastAPI(title="AgroMind Backend API", version="1.0.0")

# ✅ Allow frontend origins (local + deployed)
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://agro-mind-frontend.vercel.app",
    "https://agromind-backend-2v1j.onrender.com"
]

# ✅ Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Register all routers
app.include_router(auth_routes)
app.include_router(farm_routes)
app.include_router(crop_routes)
app.include_router(recommendation_routes)
app.include_router(tasks.router)
app.include_router(alert_route.router)
app.include_router(ai_routes)
app.include_router(activities_routes)  

# ✅ Root endpoint
@app.get("/", tags=["Root"])
def root():
    return {"message": "AgroMind Backend Running"}
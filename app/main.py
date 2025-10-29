from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db import Base, engine
from app.routes import auth_routes, crop_routes, farm_routes, tasks
from app.routes.recommendation_routes import router as recommendation_routes
from app.routes import alert_route  # ✅ Climate alerts route

# ✅ Create database tables
Base.metadata.create_all(bind=engine)

# ✅ Initialize FastAPI app
app = FastAPI(
    title="AgroMind Backend API 🌾",
    description="""
    AgroMind is an intelligent agriculture platform powered by AI.  
    It helps farmers monitor crop health, receive AI-driven recommendations, manage farms, and plan agricultural tasks.

    **Main Features:**
    - 🌦 Real-time climate alerts  
    - 🌱 AI-based crop health analysis  
    - 🚜 Farm management (CRUD)  
    - 🧠 Crop recommendations  
    - ✅ Task scheduling  
    """,
    version="1.0.0",
)

# ✅ Allow frontend origins (including Vite dev server on port 5174)
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5174",
    "https://your-production-domain.com"
]

# ✅ Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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

# ✅ Root endpoint
@app.get("/", tags=["Root"])
def root():
    return {"message": "AgroMind Backend Running"}
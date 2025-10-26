from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db import Base, engine
from app.routes import auth_routes, crop_routes, farm_routes, tasks  # 👈 include tasks
from app.routes.recommendation_routes import router as recommendation_routes
from app.routes import alert_route  # ✅ NEW: import climate alerts route

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AgroMind Backend API", version="1.0.0")

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://your-production-domain.com"
]

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

@app.get("/", tags=["Root"])
def root():
    return {"message": "AgroMind Backend Running"}
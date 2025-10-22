from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db import Base, engine
from app.routes import auth_routes, crop_routes, farm_routes

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(title="AgroMind Backend API", version="1.0.0")

origins = [
    "http://localhost:5173",   
    "http://127.0.0.1:5173",
    "https://your-production-domain.com"  

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router)
app.include_router(farm_routes.router)
app.include_router(crop_routes.router)

@app.get("/", tags=["Root"])
def root():
    return {"message": "AgroMind Backend Running"}

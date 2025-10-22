from pydantic_settings import BaseSettings
from fastapi.security import OAuth2PasswordBearer

class Settings(BaseSettings):
    # JWT Secret Key
    SECRET_KEY: str = "supersecretkey"  # Replace with a strong key in production

    # Database connection string (e.g., SQLite, PostgreSQL)
    DATABASE_URL: str = "sqlite:///./agromind.db"

    # OpenAI API Key (optional, used for crop AI service)
    OPENAI_API_KEY: str = ""

    # OAuth2 token scheme for FastAPI
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

    class Config:
        env_file = ".env"

settings = Settings()

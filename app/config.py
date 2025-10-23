from pydantic_settings import BaseSettings
from fastapi.security import OAuth2PasswordBearer

class Settings(BaseSettings):
    SECRET_KEY: str = "supersecretkey"  

    DATABASE_URL: str = "sqlite:///./agromind.db"

    OPENAI_API_KEY: str = ""

    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

    class Config:
        env_file = ".env"

settings = Settings()

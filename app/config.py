from pydantic_settings import BaseSettings
from fastapi.security import OAuth2PasswordBearer

class Settings(BaseSettings):
    SECRET_KEY: str
    DATABASE_URL: str
    OPENAI_API_KEY: str

    oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="/auth/login")

    class Config:
        env_file = ".env"

settings = Settings()

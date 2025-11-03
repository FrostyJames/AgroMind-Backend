from pydantic_settings import BaseSettings
from fastapi.security import OAuth2PasswordBearer

class Settings(BaseSettings):
    SECRET_KEY:  str = "dev_secret"
    DATABASE_URL: str = "sqlite:///./test.db"
    OPENAI_API_KEY: str

    oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="/auth/login")

    class Config:
        env_file = ".env"

settings = Settings()

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str
    DATABASE_URL: str
    OPENROUTER_API_KEY: str  # required since it's in .env

    class Config:
        env_file = ".env"

settings = Settings()
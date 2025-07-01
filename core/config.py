from pydantic_settings import BaseSettings
from typing import Optional, List

class Settings(BaseSettings):
    # Application
    app_name: str = "UniversalAI"
    app_version: str = "1.0.0"
    
    # Database
    database_url: str = "sqlite+aiosqlite:///./aicore.db"
    
    # AI Model
    model_provider: str = "mock"  # mock, openai, anthropic
    model_name: str = "gpt-4"
    model_temperature: float = 0.7
    
    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    class Config:
        env_file = ".env"

settings = Settings()

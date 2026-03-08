from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    database_url: str
    openai_api_endpoint: str
    openai_api_key: str
    cors_origins: str = "http://localhost:4200"

    class Config:
        env_file = ".env"
        case_sensitive = False

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.cors_origins.split(",")]


settings = Settings()

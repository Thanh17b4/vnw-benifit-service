from dotenv import load_dotenv, dotenv_values
from pydantic import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    PG_HOST: str
    PG_PORT: str
    PG_DATABASE: str
    PG_USER: str
    PG_PASSWORD: str

    class Config:
        config = dotenv_values(".env")


settings = Settings()


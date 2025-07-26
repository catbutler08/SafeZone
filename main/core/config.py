from functools import lru_cache
import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

URL = os.getenv("MONGO_URI")
KEY = os.getenv("SECRET_KEY")
class Settings:
    APP_NAME: str = "SafeZone"
    SECRET_KEY: str = KEY
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE: timedelta = timedelta(minutes=45)

    # DB
    MONGO_URI: str = URL
    DB_NAME: str = "SafeZone"

@lru_cache
def get_settings() -> Settings:
    return Settings()

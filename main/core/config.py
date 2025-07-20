from functools import lru_cache
import os
from datetime import timedelta

class Settings:
    APP_NAME: str = "SafeZone"
    SECRET_KEY: str = "657df88713959387d83a9da5fbda9e872d5739d24065d59adbe463decdb58324"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE: timedelta = timedelta(minutes=45)

    # DB
    MONGO_URI: str = "mongodb+srv://Wsuck:6qvd5ThUkCaZMdRQ@cluster0.kupvcum.mongodb.net/"
    DB_NAME: str = "SafeZone"

@lru_cache
def get_settings() -> Settings:
    return Settings()

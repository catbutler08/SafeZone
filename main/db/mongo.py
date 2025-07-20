from pymongo import MongoClient, ASCENDING
from ..core.config import get_settings

settings = get_settings()

client = MongoClient(settings.MONGO_URI)
db = client[settings.DB_NAME]

users = db["user"]
gpses = db["gps"]

gpses.create_index([("createdAt", ASCENDING)], expireAfterSeconds=7776000)

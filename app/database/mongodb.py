from pymongo import MongoClient
from app.config.settings import MONGO_URI, DB_NAME

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

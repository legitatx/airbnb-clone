from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from os import getenv
from utils.models import Database

username: str = getenv("DB_USER")
password: str = getenv("DB_USER_PASSWORD")
cluster: str = getenv("DB_CLUSTER")
dbName: str = getenv("DB_NAME")

connectionString = f"mongodb+srv://{username}:{password}@{cluster}.mongodb.net/{dbName}?retryWrites=true&w=majority"

def connect_database():
  client = AsyncIOMotorClient(connectionString)
  db = AsyncIOMotorDatabase(client.main)
  collections = Database(db.bookings, db.listings, db.users)
  return collections


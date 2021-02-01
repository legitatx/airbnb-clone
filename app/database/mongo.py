from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from os import getenv
from app.lib.models import Database

username: str = getenv("DB_USER")
password: str = getenv("DB_USER_PASSWORD")
cluster: str = getenv("DB_CLUSTER")
dbName: str = getenv("DB_NAME")

connection_string = f"mongodb+srv://{username}:{password}@{cluster}.mongodb.net/{dbName}?retryWrites=true&w=majority"


def connect_database():
    client = AsyncIOMotorClient(connection_string)
    db = AsyncIOMotorDatabase(client.main)
    collections = Database(db.bookings, db.listings, db.users)
    return collections

from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorCollection
from typing import Optional
from bson.objectid import ObjectId
from enum import Enum

class Database(BaseModel):
  bookings: AsyncIOMotorCollection
  listings: AsyncIOMotorCollection
  users: AsyncIOMotorCollection

class Viewer(BaseModel):
  _id: Optional[str]
  token: Optional[str]
  avatar: Optional[str]
  walletId: Optional[str]
  didRequest: bool


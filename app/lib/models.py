from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorCollection
from typing import List, Dict, Optional
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


class ListingType(str, Enum):
    Apartment = "APARTMENT"
    House = "HOUSE"


class BookingsIndex(BaseModel):
    index: List[Dict[str, dict]]


class BookingsIndexYear(BaseModel):
    year: Dict[str, dict]


class BookingsIndexMonth(BaseModel):
    month: Dict[str, bool]


class Booking(BaseModel):
    _id: ObjectId
    listing: ObjectId
    tenant: str
    checkIn: str
    checkOut: str


class Listing(BaseModel):
    _id: ObjectId
    title: ObjectId
    description: str
    image: str
    host: str
    type: ListingType
    address: str
    country: str
    admin: str
    city: str
    bookings: List[ObjectId]
    bookingsIndex: BookingsIndex
    price: int
    numOfGuests: int
    authorized: Optional[bool]


class User(BaseModel):
    _id: str
    token: str
    name: str
    avatar: str
    contact: str
    walletId: str
    income: int
    bookings: List[ObjectId]
    listings: List[ObjectId]
    authorized: Optional[bool]

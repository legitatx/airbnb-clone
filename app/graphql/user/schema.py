from graphene import Interface, String, Int, ID, Boolean, Field
from app.graphql.booking.schema import Bookings, Listings


class User(Interface):
    id = ID(required=True)
    name = String(required=True)
    avatar = String(required=True)
    contact = String(required=True)
    hasWallet = Boolean(required=True)
    income = Int
    bookings = Field(
        Bookings,
        limit=Int(required=True),
        page=Int(required=True),
    )
    listings = Field(
        Listings,
        required=True,
        limit=Int(required=True),
        page=Int(required=True),
    )

from graphene import Interface, ID, String
from app.graphql.booking.schema import Listing, User


class Booking(Interface):
    id = ID(required=True)
    listing = Listing(required=True)
    tenant = User(required=True)
    checkIn = String(required=True)
    checkOut = String(required=True)

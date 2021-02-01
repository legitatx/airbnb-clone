from graphene import Field, Interface, Enum, ID, String, List, Int
from app.graphql.booking.schema import Bookings


class ListingType(Enum):
    APARTMENT = "APARTMENT"
    HOUSE = "HOUSE"


class ListingFilter(Enum):
    PRICE_LOW_TO_HIGH = "PRICE_LOW_TO_HIGH"
    PRICE_HIGH_TO_LOW = "PRICE_HIGH_TO_LOW"


class Listing(Interface):
    id = ID(required=True)
    title = String(required=True)
    description = String(required=True)
    image = String(required=True)
    host = String(required=True)
    type = ListingType(required=True)
    address = String(required=True)
    country = String(required=True)
    admin = String(required=True)
    city = String(required=True)
    bookings = Field(
        Bookings,
        limit=Int(required=True),
        page=Int(required=True),
    )
    bookingsIndex = String(required=True)
    price = Int(required=True)
    numOfGuests = Int(required=True)


class Listings(Interface):
    region = String()
    total = Int(required=True)
    result = List(Listing, required=True)

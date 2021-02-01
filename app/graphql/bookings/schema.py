from graphene import Interface, Int, List
from app.graphql.booking.schema import Booking


class Bookings(Interface):
    total = Int(required=True)
    result = List(Booking, required=True)

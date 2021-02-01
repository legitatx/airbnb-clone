from graphene import Interface, String, Int, List
from app.graphql.booking.schema import Listing


class Listings(Interface):
    region = String()
    total = Int(required=True)
    result = List(Listing, required=True)

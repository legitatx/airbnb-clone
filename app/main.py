from fastapi import FastAPI
from dotenv import load_dotenv
import graphene
from starlette.graphql import GraphQLApp
from graphql.execution.executors.asyncio import AsyncioExecutor
from app.database import load_database
from app.graphql.booking.schema import Booking, Bookings
from app.graphql.booking.resolvers import CreateBooking
from app.graphql.listing.schema import (
    Listing,
    ListingFilter,
    ListingType,
    Listings,
)
from app.graphql.user.schema import User
from app.graphql.user.resolvers import Query
from app.graphql.viewer.schema import Viewer

load_dotenv()
db = load_database()

app = FastAPI()
app.add_route(
    "/",
    GraphQLApp(
        #todo add root level query/mutation
        schema=graphene.Schema(
            query=Query,
            types=[
                Booking,
                Bookings,
                Listing,
                ListingFilter,
                ListingType,
                Listings,
                User,
                Viewer,
            ],
            mutation=CreateBooking,
        ),
        executor_class=AsyncioExecutor,
    ),
)

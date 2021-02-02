from fastapi import FastAPI
from dotenv import load_dotenv
import graphene
from starlette.graphql import GraphQLApp
from graphql.execution.executors.asyncio import AsyncioExecutor
from app.database.mongo import load_database
from app.graphql.booking.schema import Booking, Bookings
from app.graphql.booking.resolvers import CreateBooking
from app.graphql.listing.schema import (
    Listing,
    ListingFilter,
    ListingType,
    Listings,
)
from app.graphql.user.schema import User
from app.graphql.user.resolvers import Query as UserQuery
from app.graphql.viewer.schema import Viewer

load_dotenv()
db = load_database()


class Query(UserQuery, graphene.ObjectType):
    pass


class Mutation(CreateBooking, graphene.Mutation):
    pass


app = FastAPI()
app.add_route(
    "/",
    GraphQLApp(
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
            mutation=Mutation,
        ),
        executor_class=AsyncioExecutor,
    ),
)

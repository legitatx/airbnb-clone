import arrow
import graphene
from app.lib.models import BookingsIndex
from app.graphql.booking.schema import Booking
from copy import deepcopy
from fastapi import HTTPException
from app.main import db
from app.lib.utils import authorize
from app.lib.models import User, Listing
from bson.objectid import ObjectId
from app.lib.api.stripe import charge


def resolve_bookings_index(
    bookings_index: BookingsIndex, check_in_date: str, check_out_date: str
):
    date_cursor = arrow.get(check_in_date)
    check_out = arrow.get(check_out_date)
    new_bookings_index = deepcopy(bookings_index)

    for r in arrow.Arrow.range(
        "day", date_cursor.datetime, check_out.datetime
    ):
        year = r.year
        month = r.month
        date = r.day

        if new_bookings_index[year] is None:
            new_bookings_index[year] = {}
        if new_bookings_index[year][month] is None:
            new_bookings_index[year][month] = {}
        if new_bookings_index[year][month][date] is None:
            new_bookings_index[year][month][date] = True
        else:
            raise HTTPException(
                status_code=400,
                detail="Selected dates can't overlap dates that have already been booked",
            )
    return new_bookings_index


class CreateBooking(graphene.Mutation):
    class Arguments:
        id = graphene.String()
        source = graphene.String()
        checkIn = graphene.String()
        checkOut = graphene.String()

    inserted_booking = graphene.Field(lambda: Booking)

    async def mutate(_, info, id, source, checkIn, checkOut):
        viewer = await authorize(db, info.context["request"])
        if viewer is None:
            raise HTTPException(
                status_code=500, detail="Viewer can't be found"
            )

        listing = await db.listings.find_one(
            {
                "_id": ObjectId(id),
            }
        )
        if listing is None:
            raise HTTPException(
                status_code=500, detail="Listing can't be found"
            )

        listing = Listing(**listing)
        viewer = User(**viewer)

        if listing.host == viewer._id:
            raise HTTPException(
                status_code=400, detail="Host can't book their own listing"
            )

        check_in_date = arrow.get(checkIn)
        check_out_date = arrow.get(checkOut)

        bookings_index = resolve_bookings_index(
            listing.bookingsIndex, checkIn, checkOut
        )

        total_price = (
            listing.price
            * (check_in_date.timestamp - check_out_date.timestamp)
            / 86400000
            + 1
        )

        host = await db.users.find_one(
            {
                "_id": listing.host,
            }
        )
        if host is None or host.walletId is None:
            raise HTTPException(
                status_code=400,
                detail="The host either can't be found or is not connected with Stripe",
            )

        host = User(**host)

        await charge(total_price, source, host.walletId)

        insert_res = await db.bookings.insert_one(
            {
                "_id": ObjectId(),
                "listing": listing._id,
                "tenant": viewer._id,
                "checkIn": checkIn,
                "checkOut": checkOut,
            }
        )

        inserted_booking = insert_res.inserted_id
        booking = await db.bookings.find_one(
            {
                "_id": inserted_booking,
            }
        )
        if booking is None:
            raise HTTPException(
                status_code=500, detail="Booking can't be found"
            )

        await db.users.update_one(
            {
                "_id": host._id,
            },
            {
                "$inc": {"income": total_price},
            },
        )

        await db.users.update_one(
            {
                "_id": viewer._id,
            },
            {
                "$push": {"bookings": inserted_booking},
            },
        )

        await db.listings.update_one(
            {
                "_id": listing._id,
            },
            {
                "$set": {bookings_index},
                "$push": {"bookings": inserted_booking},
            },
        )

        return CreateBooking(inserted_booking=Booking(**booking))


class Booking(graphene.ObjectType):
    class Meta:
        interfaces = (Booking,)

    async def resolve_listing(parent: Booking, info):
        return await db.listings.find_one(
            {
                "_id": parent.listing,
            }
        )

    async def resolve_tenant(parent: Booking, info):
        return await db.users.find_one(
            {
                "_id": parent.tenant,
            }
        )

import graphene
from app.graphql.user.schema import User
from fastapi import HTTPException
from app.main import db
from app.lib.utils import authorize
from app.lib.models import User as UserModel


class Query(graphene.ObjectType):
    user = graphene.Field(graphene.User, id=graphene.String(required=True))

    async def resolve_user(parent: User, info, id):
        user = await db.users.find_one({"_id": parent._id})
        if user is None:
            raise HTTPException(
                status_code=400, detail="Viewer could not be found"
            )

        viewer = await authorize(db, info.context["request"])
        if viewer:
            viewer = UserModel(**viewer)

        if viewer._id == parent._id:
            parent.authorized = True

        return parent


class User(graphene.ObjectType):
    class Meta:
        interfaces = (User,)

    class Arguments:
        limit = graphene.Int()
        page = graphene.Int()

    async def resolve_bookings(parent: User, info, limit, page):
        if not parent.authorized:
            return None

        data = {"total": 0, "result": []}
        cursor = db.bookings.find({"_id": {"$in": parent.bookings}})

        cursor = cursor.skip((page - 1 if page > 0 else 0) * limit)
        cursor = cursor.limit(limit)

        data["total"] = await cursor.count()
        data["result"] = await cursor.to_list()

        return data

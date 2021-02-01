from fastapi import Request
from lib.models import Database, User


async def authorize(db: Database, req: Request):
    token = req.headers["X-CSRF-TOKEN"]
    viewer = await db.users.find_one(
        {"_id": req.cookies.get("viewer"), "token": token}
    )
    return User(**viewer)

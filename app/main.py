from fastapi import FastAPI
from dotenv import load_dotenv
import graphene
from starlette.graphql import GraphQLApp
from graphql.execution.executors.asyncio import AsyncioExecutor
from app.database import load_database

load_dotenv()
db = load_database()

app = FastAPI()
app.add_route(
    "/",
    GraphQLApp(
        schema=graphene.Schema(query=Query), executor_class=AsyncioExecutor
    ),
)

from fastapi import FastAPI
from dotenv import load_dotenv
import graphene
from starlette.graphql import GraphQLApp

load_dotenv()

app = FastAPI()
app.add_route("/", GraphQLApp(schema=graphene.Schema(query=Query)))

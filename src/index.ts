require("dotenv").config();

import express, { Application } from "express";
import { ApolloServer } from "apollo-server-express";
import { connectDatabase } from "./db";
import { typeDefs, resolvers } from "./graphql";

const port = process.env.PORT;

const start = async (app: Application) => {
  const db = await connectDatabase();
  const server = new ApolloServer({
    typeDefs,
    resolvers,
    context: () => ({ db }),
  });

  server.applyMiddleware({ app, path: "/api" });
  app.listen(port);

  console.log(`[app]: http://localhost:${port}`);
};

start(express());

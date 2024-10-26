# mongo_resource.py
from dagster import resource, InitResourceContext
from pymongo import MongoClient
import os

@resource
def mongo_resource(init_context: InitResourceContext):
    uri = os.getenv("MONGO_URL")
    database = os.getenv("MONGO_DATABASE")

    client = MongoClient(uri)
    db = client[database]
    return db

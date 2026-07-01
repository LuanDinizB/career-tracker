import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)

db = client.get_default_database()

companies_collection = db["companies"]
jobs_collection = db["jobs"]
applications_collection = db["applications"]

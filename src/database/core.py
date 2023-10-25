from pymongo import MongoClient

from settings import env

URL = f"{env.DB_PROVIDER}+{env.DB_DRIVER}://{env.DB_USERNAME}:{env.DB_PASSWORD}@{env.DB_HOST}/?retryWrites=true&w=majority"

client = MongoClient(URL)

db = client.get_database(env.DB_NAME)
collection = db.get_collection(env.DB_COLLECTION)
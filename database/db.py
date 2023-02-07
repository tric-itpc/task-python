from pymongo import MongoClient
import config

client = MongoClient(config.db_url)

db = client[config.db_name]

from pymongo import MongoClient
client = MongoClient()

db = client.test_database

collection = db.tweets

print(db.collection_names())

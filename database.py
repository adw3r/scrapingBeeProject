import pymongo

mongo_client = pymongo.MongoClient('mongodb://root:example@10.107.8.10:27017')
print(mongo_client.server_info())

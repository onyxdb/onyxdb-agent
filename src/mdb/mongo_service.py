from pymongo import MongoClient

class MongoService:
    def __init__(self, mongo_client: MongoClient):
        self._mongo_client = mongo_client

    async def create_database(self, name: str):
        db = self._mongo_client[name]
        collection = db["onyxdb_system"]
        collection.insert_one({})

    async def delete_database(self, name: str):
        self._mongo_client.drop_database(name)

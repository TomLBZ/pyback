from pymongo.mongo_client import MongoClient

class Mdb:
    def __init__(self, url, db_name):
        self.client = MongoClient(url)
        self.db = self.client[db_name]

    def insert(self, collection, data):
        return self.db[collection].insert_one(data)

    def find(self, collection, query, remove_id=False):
        res_cursor = self.db[collection].find(query)
        res = [r for r in res_cursor]
        if remove_id:
            for r in res:
                r.pop("_id")
        return res

    def find_one(self, collection, query, remove_id=False):
        res = self.db[collection].find_one(query)
        if res is not None and remove_id:
            res.pop("_id")
        return res
    
    def find_all(self, collection, remove_id=False):
        res_cursor = self.db[collection].find()
        res = [r for r in res_cursor]
        if remove_id:
            for r in res:
                r.pop("_id")
        return res

    def update(self, collection, query, data):
        return self.db[collection].update_one(query, data)
    
    def update_all(self, collection, data, remove_old=False, upsert=True):
        try:
            if remove_old:
                self.db[collection].delete_many({"id": {"$nin": [d["id"] for d in data]}})
            for d in data:
                self.db[collection].update_one(d, {"$set": d}, upsert=upsert)
            return True
        except:
            return False

    def delete(self, collection, query):
        return self.db[collection].delete_one(query)
# coding=utf8
from pymongo.mongo_client import MongoClient

class MongoDbConnect:
    client = MongoClient("127.0.0.1",27017)
    db = client.apesay
    
    @staticmethod
    def save(collection,data):
        c = MongoDbConnect.db[collection]
        query={'key':data['key']}
        if c.find(query).count()!=0:
            print 'saved'
        else:
            c.insert(data)
    
    @staticmethod
    def saveError(collection,data):
        c = MongoDbConnect.db[collection]
        c.insert(data)
    
    @staticmethod
    def update(collection,data):
        c = MongoDbConnect.db[collection]
        query={'key':data['key']}
        c.remove(query)
        c.insert(data)

    @staticmethod
    def list(collection,data):
        query = {}
        for key in data:
            print key
            print data[key]
            query.setdefault(key,data[key])
        print query
        c = MongoDbConnect.db[collection]
        return c.find(query)

    @staticmethod
    def count(collection,data):
        query = {}
        for key in data:
            query.setdefault(key,data[key])
        c = MongoDbConnect.db[collection]
        return c.find(query).count()
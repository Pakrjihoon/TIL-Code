import pymongo

client = pymongo.MongoClient("mongodb://ip:portNumber")
database = client['databaseName']
collection = database['collectionName']

insertData = {
    "text" : "text",
    "data" : "data"
}

collection.insert_one(insertData)
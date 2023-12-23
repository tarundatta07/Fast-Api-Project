from pymongo import MongoClient

client = MongoClient("mongodb+srv://admin:admin123@cluster0.yrmc5gf.mongodb.net/?retryWrites=true&w=majority")
db = client.employee_db
collection_name = db['employee_collection']
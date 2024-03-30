import json
import pymongo
import certifi
from pymongo.mongo_client import MongoClient
from pymongo.errors import ConnectionFailure

# Підключення до MongoDB
uri = "mongodb+srv://user:user1@cluster0.gadv49o.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

try:
    client = MongoClient(uri, tlsCAFile=certifi.where())
    print("Підключення до MongoDB вдале")
except ConnectionFailure as e:
    print("Не вдалося підключитися до MongoDB:", e)

# Вибір бази даних
db = client['Ex3']


# Вставка даних з файлу authors.json у колекцію authors
with open('authors.json') as file:
    authors_data = json.load(file)
    try:
        db.authors.insert_many(authors_data)
        print("Дані з файлу authors.json успішно додані до колекції authors")
    except pymongo.errors.BulkWriteError as e:
        print(f"Помилка під час вставки даних: {e}")

# Вставка даних з файлу quotes.json у колекцію quotes
with open('quotes.json') as file:
    quotes_data = json.load(file)
    try:
        db.quotes.insert_many(quotes_data)
        print("Дані з файлу quotes.json успішно додано до колекції quotes.")
    except pymongo.errors.BulkWriteError as e:
        print(f"Помилка під час вставки даних: {e}")

print("Дані успішно додано до бази даних MongoDB Atlas.")

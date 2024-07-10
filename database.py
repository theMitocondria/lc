from mongoengine import connect
import os
from dotenv import load_dotenv

load_dotenv()

def connect_database():
    try:
        connect(host=os.getenv('MONGO_URI'))
        print("Database connected successfully")
    except Exception as e:
        print("Failed to connect to the database")
        print(e)

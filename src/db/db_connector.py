import os
import asyncio
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv('.env', override=True)

MONGODB_URI = os.getenv('MONGODB_URI')
mongo_client = AsyncIOMotorClient(MONGODB_URI)
db = mongo_client['sneaky-vaccine']
users = db['users']

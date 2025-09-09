import os
from dotenv import load_dotenv, find_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
from utils.logging import log

load_dotenv(find_dotenv())

async def connect_db():
    uri = os.getenv("MONGO_URI")

    client = AsyncIOMotorClient(
        uri,
        server_api=ServerApi('1'),
    )
    
    try:
        await client.admin.command("ping")
        return client
    except Exception as e:
        log("Connection failed:", repr(e), "critical")


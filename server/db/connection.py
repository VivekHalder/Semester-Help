import os
from dotenv import load_dotenv, find_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
from contextlib import asynccontextmanager
from utils.logging import log
from passlib.context import CryptContext
import sys

load_dotenv(find_dotenv())

client = None

pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")

async def connect_db():
    uri = os.getenv("MONGO_URI")
    _client = AsyncIOMotorClient(uri, server_api=ServerApi("1"))
    await _client.admin.command("ping")
    return _client

@asynccontextmanager
async def lifespan(app):
    global client
    try:
        client = await connect_db()
        log("Database connected", "info")
    except Exception as e:
        log(f"Error connecting to DB: {e}", "critical")
        sys.exit(1)

    yield

    client.close()
    log("Database disconnected", "info")

def get_users_collection():
    db = client["db"]
    return db["users"]
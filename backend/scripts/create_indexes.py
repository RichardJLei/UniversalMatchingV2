from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
from config.config import Config

async def create_indexes():
    config = Config()
    client = AsyncIOMotorClient(config.MONGODB_CONNECTION_STRING)
    db = client[config.MONGODB_DATABASE]
    
    # Create unique index on email
    await db.users.create_index('email', unique=True)
    
    print("Indexes created successfully")

if __name__ == "__main__":
    asyncio.run(create_indexes()) 
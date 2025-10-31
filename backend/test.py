# test_db.py
import asyncio
from app.db import db, products_collection

async def test_connection():
    await products_collection.insert_one({"test": "ok"})
    result = await products_collection.find_one({"test": "ok"})
    print(result)

asyncio.run(test_connection())

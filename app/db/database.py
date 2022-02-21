import databases
from sqlalchemy.ext.asyncio import create_async_engine

from app.db.models import metadata

DATABASE_URL = (
    "postgresql+asyncpg://admin:123qweasd@localhost/weather_data_storage")

database = databases.Database(DATABASE_URL)

engine = create_async_engine(DATABASE_URL, echo=True)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)

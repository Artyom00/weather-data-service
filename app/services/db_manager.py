from sqlalchemy import select

from app.db.database import database
from app.db.models import weather


class DbManager:
    @staticmethod
    async def retrieve_result_by(params: str):
        query = select(weather.c.weather_data).where(
            weather.c.query.ilike(params))
        return await database.fetch_one(query=query)

    @staticmethod
    async def save(query_params: str, forecast: dict):
        query = weather.insert().values(query=query_params,
                                        weather_data=forecast)
        await database.execute(query=query)

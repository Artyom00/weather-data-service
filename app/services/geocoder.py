from fastapi import HTTPException, status
import httpx

from app import settings


class Geocoder:
    remote_url = 'http://api.openweathermap.org/geo/1.0/direct'

    def __init__(self, country_code: str, city: str,
                 api_key: str = settings.API_KEY):
        self.country_code = country_code
        self.city = city
        self.__api_key = api_key

    async def make_geocoding(self) -> tuple:
        async with httpx.AsyncClient() as request:
            resp = await request.get(self.remote_url, params={
                "q": ",".join((self.city, self.country_code)),
                "appid": self.__api_key
            })

            if not resp.json():
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail=f"city {self.city} is invalid")

            return resp.json()[0]['lat'], resp.json()[0]['lon']

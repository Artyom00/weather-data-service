import datetime
import os

from dateutil import tz
from fastapi import HTTPException, status
import httpx


class RequestExecutor:
    history_weather_url = (
        'https://api.openweathermap.org/data/2.5/onecall/timemachine')
    actual_weather_url = 'https://api.openweathermap.org/data/2.5/onecall'

    def __init__(self, lat, lon, dt, api_key: str = os.getenv('API_KEY')):
        self.lat = lat
        self.lon = lon
        self.dt = dt
        self.__api_key = api_key

    async def get_forecast(self):
        if self.dt.date() < datetime.date.today():
            url = self.history_weather_url

        else:
            url = self.actual_weather_url

        async with httpx.AsyncClient() as request:
            resp = await request.get(url, params={
                "lat": self.lat,
                "lon": self.lon,
                "dt": int(self.dt.timestamp()),
                "units": "metric",
                "lang": "ru",
                "appid": self.__api_key})

            if resp.status_code != httpx.codes.OK:
                raise HTTPException(status_code=resp.status_code,
                                    detail=resp.json())

            if url.endswith('/timemachine'):
                return resp.json()['current']

            forecast_is_found = False

            for forecast in resp.json()['daily']:
                curr_tz = tz.gettz(resp.json()["timezone"])

                if datetime.datetime.fromtimestamp(
                        forecast["dt"], tz=curr_tz).replace(
                    tzinfo=None) == self.dt:
                    return forecast

            if not forecast_is_found:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail={
                                        "cod": "400",
                                        "message": "forecast out of range"
                                    })

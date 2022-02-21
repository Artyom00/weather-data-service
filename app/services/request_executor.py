import datetime

from dateutil import tz
from fastapi import HTTPException, status
import httpx

from app import settings


class RequestExecutor:
    history_weather_url = (
        'https://api.openweathermap.org/data/2.5/onecall/timemachine')
    actual_weather_url = 'https://api.openweathermap.org/data/2.5/onecall'
    common_params = {
        "units": "metric",
        "lang": "ru",
        "appid": settings.API_KEY
    }

    def __init__(self, **kwargs):
        self.dt = kwargs.get('dt')
        self.params = {
            key: value for key, value in kwargs.items() if
            key != 'dt'}  # -> {'lat': float, 'lon': float}

    async def get_forecast(self):
        if self.dt.date() < datetime.date.today():
            url = self.history_weather_url
            self.params.update(
                {'dt': int(datetime.datetime.timestamp(self.dt)),
                 **self.common_params})

        else:
            url = self.actual_weather_url
            self.params.update({**self.common_params})

        async with httpx.AsyncClient() as request:
            resp = await request.get(url, params=self.params)
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
                                        "message": "you can only query the"
                                                   " weather forecast at "
                                                   "12 a.m for the next week"
                                    })

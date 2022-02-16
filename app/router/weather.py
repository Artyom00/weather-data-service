from fastapi import APIRouter, Request, Depends

from app.dependencies import QueryParams
from app.services.db_manager import DbManager
from app.services.geocoder import Geocoder
from app.services.request_executor import RequestExecutor

router = APIRouter(prefix="/weather", tags=["weather"])


@router.get("")
async def get_weather_forecast(request: Request,
                               params: QueryParams = Depends()):
    country_code = params.check_country_code()
    query_params = str(request.query_params)
    forecast = await DbManager.retrieve_result_by(query_params)

    if not forecast:
        lat, lon = await Geocoder(country_code=country_code,
                                  city=params.city).make_geocoding()

        forecast = await RequestExecutor(
            lat=lat, lon=lon, dt=params.date).get_forecast()

        await DbManager.save(query_params, forecast)

    return forecast

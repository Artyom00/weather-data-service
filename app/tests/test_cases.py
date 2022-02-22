from fastapi import status
from httpx import AsyncClient
import pytest

from app.main import app


@pytest.mark.anyio
@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url='http://localhost:8000') as client:
        yield client


@pytest.mark.anyio
async def test_country_code_length(client):
    response = await client.get('/weather', params={
        'country_code': 'RUS',
        'city': 'Moscow',
        'date': '2022-02-21 12:00:00'
    })

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json()['detail'][0][
               'msg'] == "ensure this value has at most 2 characters"


@pytest.mark.anyio
async def test_country_code_correctness(client):
    params = {
        'country_code': 'ZZ',
        'city': 'Moscow',
        'date': '2022-02-21 12:00:00'
    }

    response = await client.get('/weather', params=params)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['detail'] == (
        f"country_code '{params['country_code']}' does not match"
        f" the ISO 3166-1 alpha-2 standard")


@pytest.mark.anyio
async def test_city_correctness(client):
    params = {
        'country_code': 'RU',
        'city': 'Asgard',
        'date': '2022-02-21 12:00:00'
    }

    response = await client.get('/weather', params=params)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['detail'] == f'city {params["city"]} is invalid'

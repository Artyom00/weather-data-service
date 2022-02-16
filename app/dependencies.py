from datetime import datetime

from fastapi import HTTPException, status
import pycountry


class QueryParams:
    def __init__(self, country_code: str, city: str, date: datetime):
        self.country_code = country_code
        self.city = city
        self.date = date

    def check_country_code(self):
        try:
            pycountry.countries.lookup(self.country_code)
        except LookupError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"country_code '{self.country_code}'"
                                       f" does not match"
                                       f" the ISO 3166 standard")

        return self.country_code

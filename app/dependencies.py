from datetime import datetime
from typing import Optional

from fastapi import HTTPException, status, Query
import pycountry


class QueryParams:
    def __init__(self, country_code: Optional[str] = Query(None, max_length=2),
                 city: Optional[str] = Query(None),
                 date: Optional[datetime] = Query(None)):
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
                                       f" the ISO 3166-1 alpha-2 standard")

        return self.country_code

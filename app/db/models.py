from sqlalchemy import MetaData, Table, Column, Integer, String
from sqlalchemy.dialects.postgresql import JSON

metadata = MetaData()

weather = Table("weather", metadata,
                Column("id", Integer, primary_key=True),
                Column("query", String, index=True),
                Column("weather_data", JSON),
                )

from fastapi import FastAPI

from app.db.database import init_db, database
from app.router.weather import router

app = FastAPI()

app.include_router(router)


@app.on_event("startup")
async def on_startup():
    await init_db()
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

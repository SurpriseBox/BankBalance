
from fastapi import FastAPI

from apps import get_apps_router
from config import Config
from db.database import Database

Database.create_connection(Config.DB_URL)

app = FastAPI()
app.include_router(get_apps_router())

import typing as t

from fastapi import FastAPI

from apps import router as final_router
from config import Config
from db.database import Database


def config(conf: t.Type[Config]):
    Database.create_connection(conf.DB)


config(Config)

app = FastAPI()
app.include_router(final_router)

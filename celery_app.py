
from celery import Celery

from config import Config
from db.database import Database

Database.create_connection(Config.DB_URL)
app = Celery('operations', config_source=Config.CeleryConfig)

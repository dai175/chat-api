from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

from app.core.constants import DB_DRIVER_NAME
from app.core.env import DB_HOST, DB_NAME, DB_PASSWORD, DB_USER
from app.db.db import Base
from app.models import *  # noqa F401

load_dotenv()

DATABASE_URL = URL.create(
    drivername=DB_DRIVER_NAME,
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    database=DB_NAME,
)

engine = create_engine(DATABASE_URL)

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

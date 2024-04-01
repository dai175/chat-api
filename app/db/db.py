import os

from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.constants import DB_DRIVER_NAME

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = URL.create(
    drivername=DB_DRIVER_NAME,
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    database=DB_NAME,
)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

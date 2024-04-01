import os

from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

SMTP_HOST = os.getenv("SMTP_HOST", "")
SMTP_PORT = int(os.getenv("SMTP_PORT", "1025"))

_v = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
ACCESS_TOKEN_EXPIRE_MINUTES = int(_v if _v else 30)

SECRET_KEY = os.getenv("SECRET_KEY", "secret")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
TOKEN_TYPE = os.getenv("TOKEN_TYPE", "bearer")
CRYPT_SCHEME = os.getenv("CRYPT_SCHEME", "bcrypt")

FROM_EMAIL = os.getenv("FROM_EMAIL", "")

PUSHER_INSTANCE_ID = os.getenv("PUSHER_INSTANCE_ID", "")
PUSHER_SECRET_KEY = os.getenv("PUSHER_SECRET_KEY", "")

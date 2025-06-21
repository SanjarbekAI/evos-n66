import os

from dotenv import load_dotenv

load_dotenv(
    dotenv_path=".env"
)

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

TOKEN = os.getenv("TOKEN")
DEVELOPER = 1358470521
ADMINS = []

DB_CONFIG = {
    "database": DB_NAME,
    "user": DB_USER,
    "port": DB_PORT,
    "host": DB_HOST,
    "password": DB_PASS
}

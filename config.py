import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")

DB_URL = os.getenv("DB_URL")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")


TYPE_CHOICES = [ 'Замена масла',
                 'Замена колодок',
                 'Замена фильтра',
                 'Замена фар'
                ]

# sqlite
TORTOISE_ORM = {
    "connections": {
        "default": DB_URL,
    },
    "apps": {
        "models": {
            "models": ["app.database.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}

# https://github.com/Sayrrexe/SF-Car-Bot


<<<<<<< HEAD
TOKEN='8086979841:AAHJbYtgpUzBfMaz4_GnL0WcoVE1Oc2h3BA'
DB_URL='sqlite://db.sqlite3'

# t.me/sf_car_bot
=======
import os
from dotenv import load_dotenv


load_dotenv()

TOKEN = os.getenv("TOKEN")
DB_URL = os.getenv("DB_URL")

TYPE_CHOICES = [
    ("OL", "OIL"),  # масло
    ("FL", "filter"),  # фильтр
    ("SP", "Support"),  # тормозные колодки
    ("FS", "Full Service"),  # полное ТО
]

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

# t.me/sf_car_bot
>>>>>>> 69d77fafa307a24adad86e6d1fee3c264992c247

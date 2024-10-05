from tortoise.models import Model
from tortoise import fields

from config import DB_URL


class Team(Model):
    id = fields.IntField(primary_key=True)
    name = fields.TextField()

    def __str__(self):
        return self.name

    
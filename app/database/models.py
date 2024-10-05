from tortoise.models import Model
from tortoise import fields

from config import DB_URL


class User(Model):
    id = fields.IntField(primary_key=True)
    username = fields.CharField(max_length=15)
    tg_id = fields.BigIntgield()
    created_at = fields.DateField(auto_now_add=True)

    def __str__(self):
        return self.username


    
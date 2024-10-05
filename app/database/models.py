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

class Car(Model):
    id = fields.IntField(primary_key=True)
    user = fields.ForeignKeyField('app.database.models.User', related_name='cars')
    brand = fields.CharField(max_length=255)
    model = fields.CharField(max_length=255)
    year = fields.IntField()
    engine = fields.CharField(max_length=255)
    mileage = fields.BigIntField()
    
class Purchases(Model):
    id = fields.IntField(primary_key=True)
    user = fields.ForeignKeyField('app.database.models.User', related_name='purchases')
    image = fields.TextField()
    text = fields.TextField()
    price = fields.DecimalField(max_digits=16, decimal_places=2)
    
class Notes(Model):
    id = fields.IntField(primary_key=True)
    user = fields.ForeignKeyField('app.database.models.User', related_name='notes')
    created_date = fields.DatetimeField(auto_now = True)
    price = fields.DecimalField(max_digits=10, decimal_places=2)
    title = fields.CharField(max_length=255)
    
class Reminders(Model):
    id = fields.IntField(primary_key=True)
    user = fields.ForeignKeyField('app.database.models.User', related_name='reminders')
    created_at = fields.DatetimeField(auto_now_add=True)
    total_date = fields.DatetimeField()
    text = fields.TextField()
from tortoise.models import Model
from tortoise import fields, on_delete

from config import DB_URL

TYPE_CHOICES = [
        ('OL', 'OIL'), # масло
        ('FL', 'filter'), # фильтр
        ('SP', 'Support'), # тормозные колодки
        ('FS', 'Full Service'), # полное ТО
    ]

class User(Model):
    id = fields.IntField(primary_key=True)
    username = fields.CharField(max_length=15)
    tg_id = fields.BigIntField()
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return self.username

class Car(Model):
    id = fields.IntField(primary_key=True)
    user = fields.ForeignKeyField('models.User', related_name='cars', on_delete=on_delete.CASCADE)
    brand = fields.CharField(max_length=255)
    model = fields.CharField(max_length=255)
    year = fields.IntField()
    engine = fields.CharField(max_length=255)
    mileage = fields.BigIntField()
    
class Purchases(Model):
    id = fields.IntField(primary_key=True)
    user = fields.ForeignKeyField('models.User', related_name='purchases', on_delete=on_delete.CASCADE)
    image = fields.TextField()
    text = fields.TextField()
    price = fields.DecimalField(max_digits=16, decimal_places=2)
    
class Notes(Model):
    id = fields.IntField(primary_key=True)
    user = fields.ForeignKeyField('models.User', related_name='notes', on_delete=on_delete.CASCADE)
    created_date = fields.DatetimeField(auto_now = True)
    price = fields.DecimalField(max_digits=10, decimal_places=2)
    title = fields.CharField(max_length=255)
    
class Reminders(Model):
    id = fields.IntField(primary_key=True)
    user = fields.ForeignKeyField('models.User', related_name='reminders', on_delete=on_delete.CASCADE)
    created_at = fields.DatetimeField(auto_now_add=True)
    total_date = fields.DatetimeField()
    text = fields.TextField()
    
class Service(Model):
    id = fields.IntField(pk=True)
    car = fields.ForeignKeyField('models.Car', related_name='services', on_delete=on_delete.CASCADE)
    type = fields.CharField(max_length=2, choices=TYPE_CHOICES)
    date = fields.DatetimeField(auto_now = True)

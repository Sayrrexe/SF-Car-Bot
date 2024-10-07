from tortoise.exceptions import DoesNotExist
from datetime import datetime, timedelta
from tortoise.functions import Sum

from app.database.models import User, Car, Notes


async def create_user(tg_id: int, username: str = None, ):
    user = await User.get_or_create(tg_id = tg_id, username = username)
    return

async def create_car(data):
    try:
        user = await User.get(tg_id=data['id'])
        # Создаем объект Car
        car = await Car.create(
            user=user,  # Передаем объект User
            brand=data['brand'],
            model=data['model'],
            year=data['year'],
            engine=data['engine'],
            mileage=data['mileage']
        )
    except DoesNotExist:
        return
    except Exception as e:
        return
    
async def get_all_user_cars(tg_id: int):
    # Получаем пользователя по tg_id
    user = await User.get(tg_id=tg_id)

    if not user:
        return {"cars": [], "total_expenses": 0}

    # Получаем все автомобили пользователя
    cars = await Car.filter(user=user).values("brand", "model", "year", "engine", "mileage")
    return cars
    
async def get_all_user_nots_per_year(tg_id: int):
    # Получаем текущую дату и дату год назад
    one_year_ago = datetime.now() - timedelta(days=365)
    
    user = await User.get(tg_id=tg_id)
    
    recent_notes = await Notes.filter(user=user, created_date__gte=one_year_ago).all()
    total_expenses = sum(note.price for note in recent_notes if note.price is not None)
    return total_expenses 

async def delete_car_by_model(tg_id: int, message):
    message = message.split(' ')
    if len(message) < 2:
        return False
    brand, model = message[0], message[1]
    user = await User.get(tg_id = tg_id)
    car = await Car.get(user=user, brand=brand, model=model).first()
    if car:
        await car.delete()
        return True
    return False

async def get_car_by_model(tg_id: int, message):
    message = str(message).split(' ')
    if len(message) < 2:
        return False
    brand, model = message[0], message[1]
    try:
        user = await User.get(tg_id = tg_id)
        car = await Car.filter(user=user, brand = brand, model = model).values("brand", "model", "year", "engine", "mileage")
        if car:
            return car
        return False
    except: 
        return False

async def create_notes(data):
    try:
        user = await User.get(tg_id=data['id'])
        # Создаем объект Car
        notes = await Notes.create(
            user=user, # передача внешнего ключа объекта модели User
            created_date=data['created_date'],
            price=data['price'],
            title=data['title'],
        )
    except DoesNotExist:
        return
    except Exception as e:
        return

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
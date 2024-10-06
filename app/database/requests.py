from app.database.models import User, Car
from tortoise.exceptions import DoesNotExist


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
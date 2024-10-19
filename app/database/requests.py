import logging

from tortoise.exceptions import DoesNotExist
from datetime import datetime, timedelta

from app.database.models import User, Car, Notes, Reminders, Purchases, Service

logger = logging.getLogger(__name__)


# ----- ПОЛЬЗОВАТЕЛЬ -----------
async def create_user(tg_id: int, username: str = None):  # создание пользователя
    user = await User.get_or_create(tg_id=tg_id, username=username)
    return


# ----- АВТО -----------
async def create_car(data):  # создание авто
    try:
        user = await User.get(tg_id=data["id"])

        await Car.create(
            user=user,
            brand=data["brand"],
            model=data["model"],
            year=data["year"],
            engine=data["engine"],
            mileage=data["mileage"],
            image=data.get("image", None),
        )
    except DoesNotExist:
        logger.error("User does not exist.")
        return
    except Exception as e:
        logger.error(f"Error creating car: {e}")
        return


async def get_all_user_cars(tg_id: int):  # получить все авто нужного пользователя
    # Получаем пользователя по tg_id
    user = await User.get(tg_id=tg_id)

    if not user:
        return {"cars": []}
    # Получаем все автомобили пользователя
    cars = await Car.filter(user=user).values(
        "brand", "model", "year", "engine", "mileage"
    )
    return cars



async def get_car_by_model(tg_id: int, message):  # получить авто пользователя по названию
    message = str(message).split(" ")
    if len(message) < 2:
        return False
    brand, model = message[0], message[1]

    user = await User.get(tg_id=tg_id)
    car = await Car.filter(user=user, brand=brand, model=model).values(
        "brand", "model", "year", "engine", "mileage", "image","id"
    )
    if car:
        return car
    return False


async def delete_car_by_model(tg_id: int, message):  # удалить авто по названию и пользователю
    message = message.split(" ")
    if len(message) < 2:
        return False
    brand, model = message[0], message[1]
    user = await User.get(tg_id=tg_id)
    car = await Car.get(user=user, brand=brand, model=model).first()
    if car:
        await car.delete()
        return True
    return False


# ------- ЗАМЕТКИ ---------
async def create_notes(data):  # создание заметки
    try:
        user = await User.get(tg_id=data["id"])
        await Notes.create(
            user=user,
            price=data["price"],
            title=data["title"],
        )
    except DoesNotExist:
        return
    except Exception as e:
        return


async def get_all_user_nots_per_year(tg_id: int):  # получить заметки о тратах пользователя за год
    # Получаем текущую дату и дату год назад
    one_year_ago = datetime.now() - timedelta(days=365)

    user = await User.get(tg_id=tg_id)
    if not user:
        return {"total_expenses": []}

    recent_notes = await Notes.filter(user=user, created_date__gte=one_year_ago).all()
    total_expenses = sum(note.price for note in recent_notes if note.price is not None)
    return total_expenses


async def get_user_notes(tg_id):  # получить все заметки пользователя
    user = await User.get_or_none(tg_id=tg_id)

    if not user:
        return "Пользователь не найден\nПропишите /start что бы исправить это."

    # Получаем все заметки пользователя, сортируя от самой новой к самой старой

    recent_notes = await Notes.filter(user=user).order_by("-created_date").all()

    if not recent_notes:
        return "У вас нет заметок."

    # Форматируем вывод заметок
    notes_list = [
        f"{note.created_date.strftime('%Y-%m-%d')} : {note.title} - {int(note.price)} ₽."
        for note in recent_notes
    ]
    return "\n".join(notes_list)

async def delete_note_by_title(tg_id: int, title):  # удалить авто по названию и пользователю
    user = await User.get(tg_id=tg_id)
    if user:
        note = await Notes.get(user=user, title=title).first()
        if note:
            await note.delete()
            return True
    return False


# ------- НАПОМИНАНИЯ ---------
async def create_reminder(data):  # создание напоминания
    try:
        user = await User.get(tg_id=data["id"])
        reminders = await Reminders.create(
            user=user,
            created_at=data["created_at"],
            total_date=data["total_date"],
            text=data["text"],
        )
    except DoesNotExist:
        return
    except Exception as e:
        return

    
async def get_user_reminders(tg_id):
    user = await User.get(tg_id=tg_id)
    reminders = await Reminders.filter(user = user).all()  
    return reminders

async def delete_user_reminders_by_text(user_id, data):
    user = await User.get(tg_id=user_id)
    args = data.split('&')
    if user:
        reminder = await Reminders.get(user=user, text = args[0],).first()
        if reminder:
            await reminder.delete()
            return True
    return False



# ------- Покупки ---------
async def create_purchase(data):  # создание покупки
    try:
        user = await User.get(tg_id=data["id"])
        await Purchases.create(
            user=user,
            image=data.get("image", None),
            text=data["text"],
            price=data["price"],
        )
    except DoesNotExist:
        logger.error("User does not exist.")
        return
    except Exception as e:
        logger.error(f"Error creating car: {e}")
        return

async def get_user_purchases(user_id):# Запрашиваем все покупки пользователя
    user = await User.get(tg_id=user_id)
    if not user:
        return []
    purchases = await Purchases.filter(user = user).all()  
    return purchases

async def delete_user_purchases(user_id, text):
    user = await User.get(tg_id=user_id)
    if user:
        purchase = await Purchases.get(user=user,text=text).first()
        if purchase:
            await purchase.delete()
            return True
    return False


# ------- СЕРВИС ---------
async def create_service(data):  # создание заметки
    try:
        service =await Service.create(
                    car_id=data["car_id"],
                    date=data["date"],
                    type=data["type"],
        )
    except DoesNotExist:
        return
    except Exception as e:
        return


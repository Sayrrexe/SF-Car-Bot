from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from app.database.requests import get_all_user_cars


# клавиатуры для сообщений
start_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Добавить Авто", callback_data="car_add_callback")]
    ]
)

return_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Отмена", callback_data="return_callback")]
    ]
)

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Создать заметку о расходах")],
        [KeyboardButton(text="Добавить продукт в избранное")],
        [KeyboardButton(text="Создать Напоминание")],
        [KeyboardButton(text="Профиль")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите пункт меню.",)

async def profile_kb(tg_id):
    cars = await get_all_user_cars(tg_id)
    keyboard = ReplyKeyboardBuilder()
    for car in cars:
        brand = car["brand"]
        model = car["model"]
        keyboard.add(KeyboardButton(text=f"{brand} {model}"))
    keyboard.add(KeyboardButton(text="Список покупок"))
    keyboard.add(KeyboardButton(text="Меню"))
    return keyboard.adjust(1).as_markup(resize_keyboard=True)

settings_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Удалить Авто")],
        [KeyboardButton(text="Добавить Авто")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите пункт меню.",)

async def all_cars_kb(tg_id):
    cars = await get_all_user_cars(tg_id)
    keyboard = ReplyKeyboardBuilder()
    for car in cars:
        brand = car["brand"]
        model = car["model"]
        keyboard.add(KeyboardButton(text=f"{brand} {model}"))
    keyboard.add(KeyboardButton(text="Отмена"))
    return keyboard.adjust(1).as_markup(resize_keyboard=True)

skip_kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="пропустить")],
        [KeyboardButton(text="Меню")]
],      resize_keyboard=True,
        input_field_placeholder="Напишите или выберите 'пропустить'",)

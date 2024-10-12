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

main_kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="Создать заметку о расходах")],
        [KeyboardButton(text="Избранное")],
        [KeyboardButton(text="Создать Напоминание")],
        [KeyboardButton(text="Профиль")]
    ],
                              resize_keyboard=True, 
                              input_field_placeholder="Выберите пункт меню.",)

favorites_kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="Мои товары")],
        [KeyboardButton(text="Добавить товар в избранное")],
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

settings_kb = ReplyKeyboardMarkup(keyboard=[
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

# Функция для создания клавиатуры пагинации 
async def get_pagination_keyboard(current_index, total_count):
    keyboard = InlineKeyboardBuilder()

    # Кнопка "Назад"
    if current_index > 0:
        keyboard.add(InlineKeyboardButton(text="◀️ Назад", callback_data=f"prev_{current_index}"))
    else:
        keyboard.add(InlineKeyboardButton(text=" ", callback_data="ignore"))  # Пустая кнопка

    # Текущая страница в формате "X/Y"
    keyboard.add(InlineKeyboardButton(text=f"{current_index + 1}/{total_count}", callback_data="page_info"))

    # Кнопка "Вперед"
    if current_index < total_count - 1:
        keyboard.add(InlineKeyboardButton(text="Вперед ▶️", callback_data=f"next_{current_index}"))
    else:
        keyboard.add(InlineKeyboardButton(text=" ", callback_data="ignore"))  # Пустая кнопка

    # Организуем кнопки в ряд
    keyboard.adjust(3)
    return keyboard.as_markup()



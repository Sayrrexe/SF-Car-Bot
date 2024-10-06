from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

# клавиатуры для сообщений
start_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Добавить Авто', callback_data='car_add_callback')]
])

return_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Отмена', callback_data='return_callback')]
])
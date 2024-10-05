from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

from app.database.requests import create_user
# для основной пользовательской части

user = Router()



@user.message(CommandStart())
async def cmd_start(message: Message):
    await create_user(message.from_user.id, message.from_user.username) # добавление пользователя в бд
    await message.answer('Добро пожаловать в бот!')

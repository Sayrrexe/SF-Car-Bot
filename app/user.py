from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

# from middlewares import BaseMiddleware

user = Router()

# user.message.middleware(BaseMiddleware())

@user.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Добро пожаловать в бот!')

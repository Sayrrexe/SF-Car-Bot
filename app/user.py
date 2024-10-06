from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from app.database.requests import create_user, create_car
import app.keyboards as kb
import app.states as st
# для основной пользовательской части

user = Router()



@user.message(CommandStart())
async def cmd_start(message: Message):
    await create_user(message.from_user.id, message.from_user.username) # добавление пользователя в бд
    await message.answer('Добро пожаловать в бот!\nУзнате список всех команд с помощью /help\nНажмите на кнопку что бы добавить характеристики вашего авто', reply_markup=kb.start_kb)
    
@user.callback_query(F.data == 'car_add_callback')
async def cq_car_add(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer('Для добавления вашего авто пожалуйста введите его марку вашего авто', reply_markup=kb.return_kb)
    await state.set_state(st.CreateAutoFSM.brand)
    
@user.callback_query(F.data == 'return_callback')
async def return_callback(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer('Вы в главном меню!')

@user.message(st.CreateAutoFSM.brand)
async def create_auto_brand(message: Message, state: FSMContext):
    await state.update_data(brand = message.text, id = message.from_user.id)
    await message.answer('Введите модель вашего авто', reply_markup=kb.return_kb)
    await state.set_state(st.CreateAutoFSM.model)

@user.message(st.CreateAutoFSM.model)
async def create_auto_model(message: Message, state: FSMContext):
    await state.update_data(model = message.text)
    await message.answer('ВВедите год выпуска авто', reply_markup=kb.return_kb)
    await state.set_state(st.CreateAutoFSM.year)
    
@user.message(st.CreateAutoFSM.year)
async def create_auto_model(message: Message, state: FSMContext):
    text = message.text
    try:
        text = int(text)
        await state.update_data(year = text)
        await message.answer('Введите объём вашего мотора', reply_markup=kb.return_kb)
        await state.set_state(st.CreateAutoFSM.engine)
    except:
        await message.answer('Год должен быть в формате числа, попроуйте ещё раз', reply_markup=kb.return_kb)
        return

@user.message(st.CreateAutoFSM.engine)
async def create_auto_engine(message: Message, state: FSMContext):
    await state.update_data(engine = message.text)
    await message.answer('Почти у цели!\nВведите пробег вашего авто', reply_markup=kb.return_kb)
    await state.set_state(st.CreateAutoFSM.mileage)
    
@user.message(st.CreateAutoFSM.mileage)
async def create_auto_mileage(message: Message, state: FSMContext):
    await state.update_data(mileage = message.text)
    await create_car(data = await state.get_data())
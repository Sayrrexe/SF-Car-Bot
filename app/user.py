import logging
from datetime import datetime, timedelta

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from aiogram_calendar import SimpleCalendar, SimpleCalendarCallback, get_user_locale

from app.database.requests import (
    create_user,
    create_car,
    get_all_user_cars,
    get_all_user_nots_per_year,
    delete_car_by_model,
    get_car_by_model,
    create_notes,
    create_reminder,
)
import app.keyboards as kb
import app.states as st

# TODO перенести добавление расписания в настройки, переписать правильные профиль пользователя
# TODO убрать возможность задать пробег не числом
# TODO фикс вывода трат
# TODO 

logger = logging.getLogger(__name__)

user = Router()


# ----- ОБРАБОТКА /start -----------
@user.message(CommandStart())
async def cmd_start(message: Message):
    await create_user(message.from_user.id, message.from_user.username)
    await message.answer(
        "Добро пожаловать в бот!\nУзнате список всех команд с помощью /help\nНажмите на кнопку что бы добавить характеристики вашего авто",
        reply_markup=kb.start_kb,
    )


# ----- RETURN_CALLBACK -----------
@user.callback_query(F.data == "return_callback")
async def return_callback(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer('Вы в главном меню', reply_markup = kb.main_kb)


# ----- ДОБАВЛЕНИЕ АВТО В БАЗУ -----------
@user.message(F.text == "Добавить Авто")
async def message_car_add(message: Message, state: FSMContext):
    await message.answer(
        "Для добавления вашего авто пожалуйста введите марку вашего авто",
        reply_markup=kb.return_kb,
    )
    await state.set_state(st.CreateAutoFSM.brand)


@user.callback_query(F.data == "car_add_callback")
async def cq_car_add(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(
        "Пожалуйста введите марку вашего авто",
        reply_markup=kb.return_kb,
    )
    await state.set_state(st.CreateAutoFSM.brand)


@user.message(st.CreateAutoFSM.brand)
async def create_auto_brand(message: Message, state: FSMContext):
    await state.update_data(brand=message.text, id=message.from_user.id)
    await message.answer("Введите модель вашего авто", reply_markup=kb.return_kb)
    await state.set_state(st.CreateAutoFSM.model)


@user.message(st.CreateAutoFSM.model)
async def create_auto_model(message: Message, state: FSMContext):
    await state.update_data(model=message.text)
    await message.answer("ВВедите год выпуска авто", reply_markup=kb.return_kb)
    await state.set_state(st.CreateAutoFSM.year)


@user.message(st.CreateAutoFSM.year)
async def create_auto_model(message: Message, state: FSMContext):
    text = message.text
    try:
        text = int(text)
        if text < 1885 or text > datetime.now().year:
            raise ValueError
        await state.update_data(year=text)
        await message.answer("Введите объём двигателя", reply_markup=kb.return_kb)
        await state.set_state(st.CreateAutoFSM.engine)
    except:
        await message.answer(
            "Год должен быть в формате числа, попробуйте ещё раз",
            reply_markup=kb.return_kb,
        )
        return


@user.message(st.CreateAutoFSM.engine)
async def create_auto_engine(message: Message, state: FSMContext):
    text = message.text
    try:
        text = float(text)
        if text < 0 or text > 10:
            raise ValueError
        await state.update_data(engine=message.text)
        await message.answer(
            "Почти у цели!\nВведите пробег вашего авто в киллометрах(укажите только число)",
            reply_markup=kb.return_kb,
        )
        await state.set_state(st.CreateAutoFSM.mileage)
    except:
        await message.answer(
            "Объем двигателя не подходит, попробуйте ещё раз",
            reply_markup=kb.return_kb,
        )
        return


@user.message(st.CreateAutoFSM.mileage)
async def create_auto_mileage(message: Message, state: FSMContext):
    await state.update_data(mileage=message.text)
    await message.answer(
        "Хотите загрузить изображение вашего авто? Пришлите файл или пропустите этот шаг, нажав /skip.",
        reply_markup=kb.return_kb,
    )
    await state.set_state(st.CreateAutoFSM.image)


@user.message(F.text == "/skip")
async def skip_image(message: Message, state: FSMContext):
    await create_car(data=await state.get_data())
    await state.clear()
    await message.answer(
        "Автомобиль добавлен без изображения!", reply_markup=kb.main_kb
    )


@user.message(st.CreateAutoFSM.image)
async def create_auto_image(message: Message, state: FSMContext):
    file_name = f"media/cars/{message.from_user.id}_{message.photo[-1].file_id}.jpg"

    await message.bot.download(file=message.photo[-1].file_id, destination=file_name)

    await state.update_data(image=file_name)

    await create_car(data=await state.get_data())
    await state.clear()
    await message.answer("Автомобиль и изображение добавлены!", reply_markup=kb.main_kb)


# ----- МЕНЮ -----------
@user.message(Command('menu'))
async def menu_cmd(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Вы в главном меню!\nВыберите действие используя встроенную клавиатуру', reply_markup= kb.main_kb)
    
@user.message(F.text == 'Меню')
async def menu_text_cmd(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Вы в главном меню!\nВыберите действие используя встроенную клавиатуру', reply_markup= kb.main_kb)
    
# ----- ПРОФИЛЬ -----------
@user.message(F.text == "Профиль")
async def profile_cmd(message: Message, state: FSMContext):
    cars = await get_all_user_cars(message.from_user.id)
    expenses = await get_all_user_nots_per_year(message.from_user.id)

    cars_text = "Автомобили:\n"
    if cars:
        for car in cars:
            brand = car["brand"]
            model = car["model"]
            year = car["year"]
            image = car.get("image", None)

            car_info = f"- {brand} {model} | год выпуска: {year}\n"
            cars_text += car_info

            if image:
                try:
                    logger.info(f"{image}")
                    await message.answer_photo(
                        photo=FSInputFile(image, filename="Car"), caption=cars_text
                    )
                except FileNotFoundError:
                    await message.answer(f"Картинка не найдена для {brand} {model}")
    else:
        cars_text = "У пользователя нет автомобилей.\n"

    await message.answer(
        f"Профиль пользователя: {message.from_user.username}\n\n{cars_text}\nТраты на автомобиль за год: {expenses}",
        reply_markup=await kb.profile_kb(message.from_user.id),
    )
    await state.set_state(st.ProfileUserFSM.car)


@user.message(st.ProfileUserFSM.car)
async def settings_car_fsm(message: Message, state: FSMContext):
    text = message.text
    if text == "Отмена":
        await state.clear()
        await message.answer("Выберите пункт меню", reply_markup=await kb.main_kb)
        return

    cars = await get_car_by_model(message.from_user.id, text)

    if cars:
        for car in cars:
            car_info = (
                f"Автомобиль {car['brand']} {car['model']}:\n\n"
                f"Производитель - {car['brand']}\n"
                f"Модель - {car['model']}\n"
                f"Год выпуска - {car['year']}\n"
                f"Объём двигателя - {car['engine']}\n"
                f"Пробег - {car['mileage']}км"
            )

            image = car.get("image", None)

            if image:
                try:
                    logger.info(f"{image}")
                    await message.answer_photo(
                        photo=FSInputFile(image, filename="Car"), caption=car_info
                    )
                except FileNotFoundError:
                    await message.answer(
                        f"Изображение не найдено для {car['brand']} {car['model']}", reply_markup=kb.main_kb
                    )
            else:
                await message.answer(car_info, reply_markup=kb.main_kb)
    else:
        await message.answer("У пользователя нет такого авто.", reply_markup=kb.main_kb)
    await state.clear()

# ----- НАСТРОЙКИ -----------
@user.message(Command('settings'))
async def settings_cmd(message: Message):
    await message.answer("Выберите действие", reply_markup=kb.settings_kb)

@user.message(F.text == "Удалить Авто")
async def delete_car_cmd(message: Message, state: FSMContext):
    await message.answer(
        "Выберите авто на встроенной клавиатуре\nВнимание восстановить авто после удаления НЕЛЬЗЯ!!!",
        reply_markup=await kb.all_cars_kb(message.from_user.id),
    )
    await state.set_state(st.CarDeleteFSM.car)

@user.message(st.CarDeleteFSM.car)
async def delete_car_fsm(message: Message, state: FSMContext):
    success = await delete_car_by_model(message.from_user.id, message.text)
    if success:
        await message.answer("Авто успешно удалено.")
    else:
        await message.answer("Авто не найдено или уже удалено.")
    await state.clear()  # Завершить состояние
    await message.answer("Вы в главном меню", reply_markup=kb.main_kb)

# ----- ДОБАВЛЕНИЕ ЗАМЕТКИ -----------
@user.message(F.text == "Создать заметку о расходах")
async def notes_tittle_add(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(st.CreateNotesFSM.title)
    await message.answer("Введите названия купленного товара для авто:",
        reply_markup=kb.return_kb)

@user.message(st.CreateNotesFSM.title)
async def notes_add_coast(message: Message, state: FSMContext):
    await state.update_data(id = message.from_user.id, title = message.text)
    await state.set_state(st.CreateNotesFSM.price)
    await message.answer("Введите стоимость этого товара:",
        reply_markup=kb.return_kb)

@user.message(st.CreateNotesFSM.price)
async def notes_add_final(message: Message, state: FSMContext):
    try:
        await state.update_data(price=int(message.text))
    except ValueError:
        await message.answer("Введен неверный формат цены. Повторите ввод: ",
        reply_markup=kb.return_kb)
        return
    data = await state.get_data()
    await create_notes(data=data)
    await message.answer(f"Заметка о покупке товара {data.get('title')} создана.",
        reply_markup=kb.return_kb)
    await state.clear()


# ------ ДОБАВЛЕНИЕ НАПОМИНАНИЯ -------------
@user.message(F.text.lower() == "создать напоминание")
async def start_add_reminder(message: Message):
    await message.answer(
        "Выберите дату напоминания в пределах от 1 до 365 дней:",
        reply_markup=await SimpleCalendar(
            locale='ru_RU.utf8'
        ).start_calendar(),
    )

@user.callback_query(SimpleCalendarCallback.filter())
async def choose_total_date_reminder(
    callback_query: CallbackQuery,
    callback_data: SimpleCalendarCallback,
    state: FSMContext,
):
    await state.clear()
    calendar = SimpleCalendar(
        locale='ru_RU.utf8', show_alerts=True
    )

    early_date = datetime.now() + timedelta(days=1)  # ранняя дата напоминания (завтра)
    late_date = datetime.now() + timedelta(days=365)  # поздняя дата (через год)

    calendar.set_dates_range(early_date, late_date)
    selected, date = await calendar.process_selection(callback_query, callback_data)

    if selected:
        await state.set_state(st.CreateRemindersFSM.text)
        await state.update_data(
            total_date=date, id=callback_query.from_user.id, created_at=datetime.now()
        )
        await callback_query.message.answer(f'Выбрана дата {date.strftime("%d/%m/%Y")}')
        await callback_query.message.answer("Введите текст: ")


@user.message(st.CreateRemindersFSM.text)
async def add_text_and_final_reminder(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    data = await state.get_data()
    await create_reminder(data)
    await message.answer("Напоминание добавлено успешно!")
    await state.clear()

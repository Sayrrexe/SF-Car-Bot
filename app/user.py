import logging

from datetime import datetime, timedelta

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from app.calendar import NewCalendar

from aiogram_calendar import SimpleCalendarCallback, SimpleCalendar

from app.database.requests import (
    create_user,
    create_car,
    get_all_user_cars,
    get_all_user_nots_per_year,
    delete_car_by_model,
    get_car_by_model,
    create_notes,
    create_reminder,
    get_user_notes,
    create_purchase,
    get_user_purchases,
)
import app.keyboards as kb
import app.states as st

# TODO реализовать вывод всех покупок в профиле

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
    await callback.message.answer('Вы в главном меню', reply_markup=kb.main_kb)
    
@user.callback_query(F.data == "ignore")
async def ignore_callback(callback_query: CallbackQuery):
    await callback_query.answer()


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
        if text < 0 or text > 20:
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
    text = message.text
    try:
        text = int(text)
        await state.update_data(mileage=message.text)
        await message.answer(
            "Хотите загрузить изображение вашего авто? Пришлите файл или пропустите этот шаг, нажав /skip.",
            reply_markup=kb.return_kb,
        )
        await state.set_state(st.CreateAutoFSM.image)
    except:
        await message.answer('Введите пробег в формате числа без лишних символов!', reply_markup=kb.return_kb)


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
    await message.answer('Вы в главном меню!\nВыберите действие используя встроенную клавиатуру',
                         reply_markup=kb.main_kb)


@user.message(F.text == 'Меню')
async def menu_text_cmd(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Вы в главном меню!\nВыберите действие используя встроенную клавиатуру',
                         reply_markup=kb.main_kb)


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
        await message.answer("Выберите пункт меню", reply_markup=kb.main_kb)
        return
    if text == 'Список покупок':
        message_note = await get_user_notes(tg_id=message.from_user.id)
        await message.answer(f'Список ваших покупок:\n{message_note}', reply_markup=kb.main_kb)
        await state.clear()
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
    await state.update_data(id=message.from_user.id, title=message.text)
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
                         reply_markup=kb.main_kb)
    await state.clear()


# ------ ДОБАВЛЕНИЕ НАПОМИНАНИЯ -------------
@user.message(F.text.lower() == "создать напоминание")
async def start_add_reminder(message: Message):
    await message.answer(
        "Выберите дату напоминания в пределах от 1 до 365 дней:",
        reply_markup=await NewCalendar().start_calendar(),

    )

@user.callback_query(SimpleCalendarCallback.filter())
async def choose_total_date_reminder(
        callback_query: CallbackQuery,
        callback_data: SimpleCalendarCallback,
        state: FSMContext,
):
    await state.clear()

    calendar = NewCalendar()
    calendar.show_alerts = True

    early_date = datetime.now() + timedelta(days=1)  # ранняя дата напоминания (завтра)
    late_date = datetime.now() + timedelta(days=365)  # поздняя дата (через год)

    calendar.set_dates_range(early_date, late_date)
    selected, date = await calendar.process_selection(callback_query, callback_data)

    if selected:
        await state.set_state(st.CreateRemindersFSM.text)
        await state.update_data(
            total_date=date, id=callback_query.from_user.id, created_at=datetime.now()
        )
        await callback_query.answer (f'Выбрана дата {date.strftime("%d.%m.%Y")}')
        await callback_query.message.answer("Введите текст: ")

@user.message(st.CreateRemindersFSM.text)
async def add_text_and_final_reminder(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    data = await state.get_data()
    await create_reminder(data)
    await message.answer(f'Напоминание о событии {data.get('text')} добавлено успешно!')
    await state.clear()


# ------ ДОБАВЛЕНИЕ ИНТЕРСНЫХ ПОКУПОК -------------
@user.message(F.text == "Избранное")
async def purchases_cmd(message: Message, state: FSMContext):
    await message.answer(
        'Добавление интересной покупки в ваш личный список, это поможет вам в будущем вспмнить, какой товар вы покупали', reply_markup=kb.favorites_kb)
    
    
@user.message(F.text == "Добавить товар в избранное")
async def purchases_cmd(message: Message, state: FSMContext):
    await state.set_state(st.CreatePurchasesFSM.text)
    await message.answer("Введите всё нужную информацию о товаре ( цена будет отдельно ):",
                         reply_markup=kb.skip_kb)


@user.message(st.CreatePurchasesFSM.text)
async def purchases_add_text(message: Message, state: FSMContext):
    if message.text == 'пропустить':
        await message.answer("Вы пропустили этот шаг!", reply_markup=kb.main_kb)
        await state.update_data(id=message.from_user.id, text=None)
    else:
        await state.update_data(id=message.from_user.id, text=message.text)
    await state.set_state(st.CreatePurchasesFSM.price)
    await message.answer("Введите стоимость этого товара:",
                         reply_markup=kb.skip_kb)


@user.message(st.CreatePurchasesFSM.price)
async def purchases_add_price(message: Message, state: FSMContext):
    if message.text == 'пропустить':
        await message.answer("Вы пропустили этот шаг!", reply_markup=kb.main_kb)
        await state.update_data(price=None)
    else:
        try:
            await state.update_data(price=int(message.text))
        except ValueError:
            await message.answer(
                "Введен неверный формат цены. Повторите ввод( цена указывается в формате полного числа ): ",
                reply_markup=kb.skip_kb)
            return
    await state.set_state(st.CreatePurchasesFSM.image)
    await message.answer("Пришлите фото этого товара:",
                         reply_markup=kb.skip_kb)


@user.message(st.CreatePurchasesFSM.image)
async def purchases_add_image(message: Message, state: FSMContext):
    if message.text == 'пропустить':
        await message.answer("Вы пропустили этот шаг!", reply_markup=kb.main_kb)
        await create_purchase(data=await state.get_data())
    else:
        file_name = f"media/purchases/{message.from_user.id}_{message.photo[-1].file_id}.jpg"
        await message.bot.download(file=message.photo[-1].file_id, destination=file_name)
        await state.update_data(image=file_name)
        await create_purchase(data=await state.get_data())
    await state.clear()
    await message.answer("Покупка добавлена", reply_markup=kb.main_kb)

# ------ Вывод избранных покупок -------------
@user.message(F.text == "Мои товары") # после команды обрабатывает пользователя и генерирует пагинацию
async def purchases_cmd(message: Message, state: FSMContext):
    purchases = await get_user_purchases(message.from_user.id)
    if not purchases:
        await message.answer("У вас нет сохранённых покупок.")
        return
    
    # Сохраняем индекс текущей покупки в состояние
    await state.update_data(current_purchase=0)

    # Выводим первую покупку
    await show_purchase(message, purchases[0], 0, len(purchases))
    
async def show_purchase(message: Message, purchase, current_index, total_count): # универсальная функция для вывода
    text = (
        f"Покупка: {purchase.text}\n"
        f"Цена: {purchase.price} ₽\n\n"
    )
    
    if purchase.image:
        try:
            await message.answer_photo(photo=FSInputFile(purchase.image, filename="Car"), caption=text, reply_markup=await kb.get_pagination_keyboard(current_index, total_count))
        except Exception as e:
            await message.answer(f"Столкнулись с ошибкой: {e}\n возможно картинка вашего товара была удалена, хотите удалить товар?")
    else:
        await message.answer(
            text, 
            reply_markup=await kb.get_pagination_keyboard(current_index, total_count)
        )
    
@user.callback_query(F.data.startswith("prev_") | F.data.startswith("next_"))
async def pagination_handler(callback_query: CallbackQuery, state: FSMContext):
    data = callback_query.data.split("_")
    direction = data[0]
    current_index = int(data[1])
    await callback_query.message.delete()
    # Получаем покупки пользователя из базы данных
    user = callback_query.from_user
    purchases = await get_user_purchases(user.id)
    
    if direction == "prev":
        new_index = current_index - 1
    else:
        new_index = current_index + 1
    
    # Обновляем индекс в состоянии
    await state.update_data(current_purchase=new_index)
    
    # Отображаем новую покупку
    await show_purchase(callback_query.message, purchases[new_index], new_index, len(purchases))
    
    # Убираем уведомление о нажатии кнопки
    await callback_query.answer()
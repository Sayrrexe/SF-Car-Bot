from aiogram.fsm.state import State, StatesGroup


class CreateAutoFSM(StatesGroup):
    user = State()
    brand = State()
    model = State()
    year = State()
    engine = State()
    mileage = State()
    image = State()

class CreateServiceFSM(StatesGroup):
    car_id=State()
    type=State()
    date=State()

class CarDeleteFSM(StatesGroup):
    car = State()
    user = State()


class CreateNotesFSM(StatesGroup):
    user = State()
    price = State()
    title = State()

class CreateRemindersFSM(StatesGroup):
    user = State()
    created_at = State()
    total_date = State()
    # total_date_time = State()
    text = State()

class CreatePurchasesFSM(StatesGroup):
    id = State()
    text = State()
    price = State()
    image = State()

from aiogram.fsm.state import State, StatesGroup

# Для состояний


class CreateAutoFSM(StatesGroup):
    user = State()
    brand = State()
    model = State()
    year = State()
    engine = State()
    mileage = State()
    image = State()


class CarDeleteFSM(StatesGroup):
    car = State()
    user = State()


class ProfileUserFSM(StatesGroup):
    car = State()


class CreateNotesFSM(StatesGroup):
    user = State()
    created_date = State()
    price = State()
    title = State()


class CreateRemindersFSM(StatesGroup):
    user = State()
    created_at = State()
    total_date = State()
    text = State()


class CreatePurchasesFSM(StatesGroup):
    user = State()
    image = State()
    text = State()
    price = State()

from aiogram.fsm.state import State, StatesGroup

# Для состояний


class CreateAutoFSM(StatesGroup):
    user = State()
    brand = State()
    model = State()
    year = State()
    engine = State()
    mileage = State()

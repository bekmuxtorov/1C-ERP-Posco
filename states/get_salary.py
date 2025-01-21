from aiogram.dispatcher.filters.state import State, StatesGroup

class GetSalary(StatesGroup):
    year   = State()
    month  = State()
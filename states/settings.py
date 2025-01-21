from aiogram.dispatcher.filters.state import State, StatesGroup

class Settings(StatesGroup):
    username = State()
    password = State()
    phone_number = State()
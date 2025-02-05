from aiogram.dispatcher.filters.state import State, StatesGroup


class Registration(StatesGroup):
    username = State()
    password = State()
    phone_number = State()
    language_code = State()

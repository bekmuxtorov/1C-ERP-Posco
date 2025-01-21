from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import datetime


def make_inline_buttons(words: dict, row_width: int = 1) -> InlineKeyboardMarkup:
    buttons_group = InlineKeyboardMarkup(row_width=row_width)
    for text, callback_data in words.items():
        if text is not None and callback_data is not None:
            buttons_group.insert(InlineKeyboardButton(
                text=text, callback_data=callback_data))
    return buttons_group


register_button = InlineKeyboardMarkup().add(
    InlineKeyboardButton("Ro'yhatdan o'tish", callback_data="register")
)

get_salary_button = InlineKeyboardMarkup().add(
    InlineKeyboardButton("Oylik hisobotni olish", callback_data="get_salary")
)


def get_years() -> InlineKeyboardMarkup:
    years = dict()
    first_year = 2024
    last_year = datetime.datetime.now().year
    while first_year < last_year + 1:
        years[first_year] = f"year_{first_year}"
        first_year += 1
    return make_inline_buttons(years, row_width=2)


def get_months() -> InlineKeyboardMarkup:
    months = dict()
    months["Jan"] = "month_01"
    months["Feb"] = "month_02"
    months["Mar"] = "month_03"
    months["Apr"] = "month_04"
    months["May"] = "month_05"
    months["Jun"] = "month_06"
    months["Jul"] = "month_07"
    months["Aug"] = "month_08"
    months["Sep"] = "month_09"
    months["Oct"] = "month_10"
    months["Nov"] = "month_11"
    months["Dec"] = "month_12"
    return make_inline_buttons(months, row_width=4)

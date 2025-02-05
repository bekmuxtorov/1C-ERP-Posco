from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def make_buttons(words: list, row_width: int = 1) -> ReplyKeyboardMarkup:
    buttons_group = ReplyKeyboardMarkup(
        row_width=row_width, resize_keyboard=True)
    for word in words:
        if word is not None:
            buttons_group.insert(KeyboardButton(text=word))
    return buttons_group


phone_button = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
    KeyboardButton("☎️ Telefon raqamni ulashish", request_contact=True)
)

phone_button_ru = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
    KeyboardButton("☎️ Поделиться номером телефона", request_contact=True)
)

words = ["💡Oylik hisobotni olish", "🛠️Sozlamalar", "🔙Bekor qilish"]
menu_button = make_buttons(words=words, row_width=2)

words_ru = ["💡Получите ежемесячный отчет", "🛠️Настройки", "🔙Отмена"]
menu_button_ru = make_buttons(words=words_ru, row_width=2)

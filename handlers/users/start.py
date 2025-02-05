import re

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import ReplyKeyboardRemove
from keyboards.default.default_buttons import phone_button, phone_button_ru
from keyboards.inline import get_salary_button, select_language_code
from keyboards.default import menu_button, menu_button_ru
from states.registration import Registration

from loader import dp, db


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    user = await db.select_user(chat_id=message.from_user.id)
    if user:
        await message.answer("Asosiy menu", reply_markup=menu_button)
    else:
        # user_programm = await check_status(message.from_user.id)
        # if user_programm:
        #     await message.answer("1C dasturdagi loginingizni quyida kiriting:")
        #     await Registration.username.set()
        # else:
        await message.answer("📃 Tilni tanlang:\n\nВыберите язык:", reply_markup=select_language_code)
        await Registration.language_code.set()


@dp.message_handler(state=Registration.language_code)
async def process_adding_departmant(message: types.Message, state: FSMContext):
    await message.answer("📃 Tilni tanlang:/n/nВыберите язык:", reply_markup=select_language_code)
    await Registration.language_code.set()


@dp.callback_query_handler(lambda c: "uz" in c.data, state=Registration.language_code)
async def adding_departmant(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(language_code="uz")
    await call.message.answer("Botdan foydalanish uchun telefon raqamingizni quyidagi tugma yordamida jo'nating yoki namuna ko'rinishida yuboring.\n\nNamuna: +998901644101", reply_markup=phone_button)
    await Registration.phone_number.set()


@dp.callback_query_handler(lambda c: "ru" in c.data, state=Registration.language_code)
async def adding_departmant(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(language_code="ru")
    await call.message.answer("Чтобы воспользоваться ботом, отправьте свой номер телефона с помощью кнопки ниже или отправьте его в качестве образца.\n\nNamuna: +998901644101", reply_markup=phone_button_ru)
    await Registration.phone_number.set()


@dp.message_handler(content_types=types.ContentType.TEXT, state=Registration.username)
async def process_adding_departmant(message: types.Message, state: FSMContext):
    username = message.text.strip()
    # await message.delete()
    await state.update_data(username=username)
    await message.answer("1C dasturdagi parolingizni quyida kiriting:")
    await Registration.password.set()


@dp.message_handler(state=Registration.username)
async def process_adding_departmant(message: types.Message, state: FSMContext):
    await message.delete()
    await message.answer("1C dasturdagi loginingizni quyida kiriting:")
    await Registration.username.set()


@dp.message_handler(content_types=types.ContentType.TEXT, state=Registration.password)
async def process_adding_departmant(message: types.Message, state: FSMContext):
    await message.delete()
    password = message.text.strip()
    await state.update_data(password=password)
    await message.answer("Telefon raqamingizni quyidagi tugma yordamida yoki namuna ko'rinishida yuboring.\n\nОбразец: +998901644101", reply_markup=phone_button)
    await Registration.phone_number.set()


@dp.message_handler(content_types=types.ContentType.CONTACT, state=Registration.phone_number)
async def process_adding_departmant(message: types.Message, state: FSMContext):
    contact = message.contact.phone_number
    await message.delete()
    await create_user(message, contact, state)


@dp.message_handler(content_types=types.ContentType.TEXT, state=Registration.phone_number)
async def process_adding_departmant(message: types.Message, state: FSMContext):
    contact = message.text.strip()
    pattern = r"^\+998\d{9}$"
    if re.match(pattern, contact):
        service_message = await message.answer(text=".", reply_markup=ReplyKeyboardRemove())
        await service_message.delete()
        await message.delete()
        await create_user(message, contact, state)
        await state.finish()
    else:
        data = await state.get_data()
        language_code = data.get("language_code")
        await Registration.phone_number.set()

        if language_code == "uz":
            await message.answer("‼️Iltimos telefon raqamingizni to'liq kiriting yoki quyidagi tugma yordamida telefon raqamingizni ulashing.", reply_markup=phone_button)
            await message.delete()
            return

        await message.answer("‼️Введите свой полный номер телефона или поделитесь им, нажав на кнопку ниже.", reply_markup=phone_button_ru)
        await message.delete()


async def create_user(message: types.Message, contact: str, state: FSMContext):
    data = await state.get_data()
    username = data.get("username")
    password = data.get("password")
    language_code = data.get("language_code")
    if username or password:
        status = db.add_user(
            username=username,
            password=password,
            language_code=language_code,
            phone_number=contact,
            chat_id=message.from_user.id
        )
    else:
        status = db.add_employee(
            phone_number=contact,
            language_code=language_code,
            chat_id=message.from_user.id
        )
    if status:
        if language_code == "uz":
            await message.answer("✅ Muaffaqiyatli ro'yhatdan o'tdingiz!", reply_markup=menu_button)
        else:
            await message.answer("✅ Вы успешно зарегистрировались!", reply_markup=menu_button_ru)

    else:
        if language_code == "uz":
            await message.answer("❌ Nimadir xato\n\nQayta /start ni yuborib urinib ko'ring!")
        else:
            await message.answer("❌ Что-то пошло не так\n\nПопробуйте отправить /start снова!")
    await state.finish()

import re

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import ReplyKeyboardRemove
from keyboards.default.default_buttons import phone_button
from keyboards.inline import get_salary_button
from keyboards.default import menu_button
from states.registration import Registration

from loader import dp, db

from utils.using_api import check_status


@dp.message_handler(CommandStart())
# @dp.message_handler(text="Ro'yhatdan o'tish")
async def bot_start(message: types.Message):
    name = message.from_user.full_name
    user = await db.select_user(chat_id=message.from_user.id)
    if user:
        await message.answer("Asosiy menu", reply_markup=menu_button)
    else:
        user_programm = await check_status(message.from_user.id)
        if user_programm:
            await message.answer("1C dasturdagi loginingizni quyida kiriting:")
            await Registration.username.set()
        else:
            await message.answer("Botdan foydalanish uchun telefon raqamingizni quyidagi tugma yordamida jo'nating yoki namuna ko'rinishida yuboring.\n\nNamuna: +998901644101", reply_markup=phone_button)
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
    await message.answer("Telefon raqamingizni quyidagi tugma yordamida yoki namuna ko'rinishida yuboring.\n\nNamuna: +998901644101", reply_markup=phone_button)
    await Registration.phone_number.set()


@dp.message_handler(content_types=types.ContentType.CONTACT, state=Registration.phone_number)
async def process_adding_departmant(message: types.Message, state: FSMContext):
    contact = message.contact.phone_number
    chat_id = message.from_user.id
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
        await message.answer("‼️Iltimos telefon raqamingizni to'liq kiriting yoki quyidagi tugma yordamida telefon raqamingizni ulashing.", reply_markup=phone_button)
        await Registration.phone_number.set()
        await message.delete()
        return


async def create_user(message, contact: str, state: FSMContext):
    data = await state.get_data()
    username = data.get("username")
    password = data.get("password")
    if username or password:
        status = db.add_user(
            username=username,
            password=password,
            phone_number=contact,
            chat_id=message.from_user.id
        )
    else:
        status = db.add_employee(phone_number=contact,
                                 chat_id=message.from_user.id)
    if status:
        await message.answer("✅ Muaffaqiyatli ro'yhatdan o'tdingiz!", reply_markup=menu_button)
        await state.finish()
        service_message = await message.answer(text=".", reply_markup=menu_button)
        await service_message.delete()
    else:
        await message.answer("❌ Nimadir xato\n\nQayta /start ni yuborib urinib ko'ring!")

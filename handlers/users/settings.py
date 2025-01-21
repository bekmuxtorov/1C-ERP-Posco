from aiogram.types import ReplyKeyboardRemove
from aiogram import types
from aiogram.types import InputFile

from loader import dp, db, bot
from keyboards.inline import get_years, get_months, get_salary_button
from states.get_salary import GetSalary
from aiogram.dispatcher import FSMContext

from utils.using_api import check_status, get_salary_report, get_file, convert_to_png, delete_file


@dp.message_handler(text="🔙Bekor qilish", state="*")
async def adding_departmant(message: types.Message, state: FSMContext):
    print("🔙Bekor qilish")
    await state.finish()
    await message.delete()
    await message.answer("Jarayon bekor qilindi!", reply_markup=get_salary_button)


@dp.message_handler(text="🛠️Sozlamalar")
async def adding_departmant(message: types.Message, state: FSMContext):
    chat_id = message.from_user.id
    await message.delete()
    select_user = await db.select_user(chat_id=message.from_user.id)
    if not select_user:
        service_message = await message.answer(text=".", reply_markup=ReplyKeyboardRemove())
        await service_message.delete()
        await message.answer("Siz ro'yhatdan o'tmagansiz, avval ro'yhatdan o'ting!\n\n👉/start")
        return

    await db.delete_user(chat_id=chat_id)
    service_message = await message.answer(text=".", reply_markup=ReplyKeyboardRemove())
    await service_message.delete()
    await message.answer("Yaxshi qayta ro'yhatdan o'tishingiz mumkin!\n\n👉/start")

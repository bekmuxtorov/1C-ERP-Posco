
from aiogram import types
from aiogram.types import InputFile

from loader import dp, db, bot
from keyboards.inline import get_years, get_months, get_salary_button
from states.get_salary import GetSalary
from aiogram.dispatcher import FSMContext

from utils.using_api import get_salary_report, get_file, convert_to_png, delete_file


@dp.message_handler(text="💡Oylik hisobotni olish")
async def adding_departmant(message: types.Message, state: FSMContext):
    await message.answer("Yaxshi, quyidan kerakli yilni tanlang:", reply_markup=get_years())
    await GetSalary.year.set()


@dp.callback_query_handler(lambda c: "get_salary" in c.data)
async def adding_departmant(call: types.CallbackQuery):
    await call.message.answer("Yaxshi, quyidan kerakli yilni tanlang:", reply_markup=get_years())
    await GetSalary.year.set()


@dp.callback_query_handler(lambda c: "year" in c.data, state=GetSalary.year)
async def adding_departmant(call: types.CallbackQuery,  state: FSMContext):
    await call.message.delete()
    year = call.data.split("_")[1]
    await state.update_data(year=year)
    await call.message.answer("Yaxshi, quyidan kerakli oyni tanlang:", reply_markup=get_months())
    await GetSalary.month.set()


@dp.callback_query_handler(state=GetSalary.year)
async def adding_departmant(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer("Iltimos kerakli yildan birini quyidan tanglang:", reply_markup=get_years())
    await GetSalary.year.set()


@dp.message_handler(state=GetSalary.year)
async def adding_departmant(message: types.Message):
    await message.delete()
    await message.answer("Iltimos kerakli yildan birini quyidan tanglang:", reply_markup=get_years())
    await GetSalary.year.set()


@dp.callback_query_handler(lambda c: "month" in c.data, state=GetSalary.month)
async def adding_departmant(call: types.CallbackQuery,  state: FSMContext):
    month = call.data.split("_")[1]
    await state.update_data(month=month)
    await call.message.delete()

    data = await state.get_data()
    year = data.get("year")

    user_data = await db.select_user(chat_id=call.from_user.id)
    phone_number = user_data.get("phone_number")
    loadbar_message = await call.message.answer("....")
    response_json = await get_salary_report(phone_number, year, month)
    if not bool(response_json):
        await loadbar_message.delete()
        await call.message.answer("Nimadir xato, birozdan keyin qayta urinib ko'ring![001]", reply_markup=get_salary_button)
        await state.finish()
        return

    if response_json.get("status_code") == 600:
        await loadbar_message.delete()
        await call.message.answer(f"{phone_number} bu raqamga bog'langan ishchi topilmadi, administratorga murojaat qiling!", reply_markup=get_salary_button)
        await state.finish()
        return

    await loadbar_message.delete()
    loadbar_message = await call.message.answer("..")
    status = await get_file(response_json, phone_number)
    if status:
        await loadbar_message.delete()
        file_path = f"reports/{phone_number}.pdf"  # Faylning to'liq manzili
        convert_image_status = await convert_to_png(file_path, phone_number)
        if not convert_image_status:
            await call.message.answer("Nimadir xato, birozdan keyin qayta urinib ko'ring![002]", reply_markup=get_salary_button)
            await state.finish()
            await delete_file(file_path)
            return
        loadbar_message = await call.message.answer(".")
        await loadbar_message.delete()
        caption = f"<b>Telefon raqam</b>: {phone_number}\n"
        caption += f"<b>Davr</b>: {month}.{year}\n"
        photo_path = f"reports/images/{phone_number}.png"
        await bot.send_photo(call.message.chat.id, InputFile(photo_path, filename=f"{phone_number}.png"), caption=caption, reply_markup=get_salary_button)
        await delete_file(photo_path)
        await delete_file(file_path)

    else:
        await call.message.answer("Nimadir xato, birozdan keyin qayta urinib ko'ring![003]", reply_markup=get_salary_button)
    await state.finish()


@dp.callback_query_handler(state=GetSalary.month)
async def adding_departmant(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer("Iltimos kerakli oyni birini quyidan tanglang:", reply_markup=get_months())
    await GetSalary.month.set()


@dp.message_handler(state=GetSalary.month)
async def adding_departmant(message: types.Message):
    await message.delete()
    await message.answer("Iltimos kerakli oyni birini quyida tanglang:", reply_markup=get_months())
    await GetSalary.month.set()

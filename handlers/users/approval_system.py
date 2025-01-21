
from aiogram import types

from loader import dp, db

from utils.using_api import send_approval_system_answer


@dp.callback_query_handler(lambda c: "approval" in c.data)
async def adding_departmant(call: types.CallbackQuery):
    await call.message.delete()
    data = await separate_data(call.data)
    if data:
        programm_user = await db.select_user(chat_id=call.from_user.id)
        if not programm_user:
            return False

        response = await send_approval_system_answer(
            data=data,
            username=programm_user.get("username").encode("utf-8"),
            password=programm_user.get("password").encode("utf-8"),
            status="true"
        )
        if not response:
            await call.message.answer("Tizimda xatolik mavjud!, iltimos keyinroq urinib ko'ring!")
            return
        await call.message.answer(response)


@dp.callback_query_handler(lambda c: "reject" in c.data)
async def adding_departmant(call: types.CallbackQuery):
    await call.message.delete()
    data = await separate_data(call.data)
    if data:
        programm_user = await db.select_user(chat_id=call.from_user.id)
        if not programm_user:
            return False

        response = await send_approval_system_answer(
            data=data,
            username=programm_user.get("username").encode("utf-8"),
            password=programm_user.get("password").encode("utf-8"),
            status="false"
        )
        if not response:
            await call.message.answer("Tizimda xatolik mavjud!, iltimos keyinroq urinib ko'ring!")
            return
        await call.message.answer(response)


async def separate_data(data):
    data_items = data.split("|")
    return {
        "bp_id": data_items[1],
        "level": data_items[2]
    } if len(data_items) > 2 else None

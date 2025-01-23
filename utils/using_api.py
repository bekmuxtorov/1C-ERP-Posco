import os
from PIL import Image
import fitz
import requests
from requests.auth import HTTPBasicAuth
from data.config import IP, PROGRAMM_USERNAME, PROGRAMM_PASSWORD, URL

import base64


async def check_status(chat_id):
    url = f"http://{IP}/{URL}/hs/document_approval/telegram_user"
    params = {
        "chat_id": chat_id,
    }
    auth = HTTPBasicAuth(username=PROGRAMM_USERNAME,
                         password=PROGRAMM_PASSWORD)
    response = requests.get(url, params=params, auth=auth)
    if response.status_code == 200:
        return response.json()
    else:
        return False


async def send_approval_system_answer(data: dict, username: str, password: str, status: str):
    url = f"http://{IP}/{URL}/hs/document_approval"
    params = {
        "UID_BP": data.get("bp_id"),
        "app": status,
        "level": data.get("level")
    }
    auth = HTTPBasicAuth(username=username,
                         password=password)
    response = requests.get(url, params=params, auth=auth)
    if response.status_code == 200:
        return response.text
    else:
        return False


async def get_salary_report(phone_number: str, year: str, month: str) -> dict:
    url = f"http://{IP}/{URL}/hs/payslip"
    if not phone_number.startswith("+"):
        phone_number = "+" + phone_number
    params = {
        "phone_number": phone_number,
        "year": year,
        "month": month
    }
    auth = HTTPBasicAuth(username=PROGRAMM_USERNAME,
                         password=PROGRAMM_PASSWORD)

    print(url)
    response = requests.get(url, params=params, auth=auth)

    if response.status_code == 200:
        return response.json()
    else:
        return False


async def get_file(response_json: dict, phone_number: str) -> bool:
    try:
        base64String = response_json.get("text")
        data = base64.b64decode(base64String)

        with open(f"reports/{phone_number}.pdf", "wb") as f:
            f.write(data)
        return True
    except:
        return False


async def convert_to_png(file_path: str, phone_number: str) -> bool:
    # (left, upper, right, lower)
    crop_dimensions = (100, 100, 2400, 1200)
    dpi = 300
    zoom = dpi / 72
    magnify = fitz.Matrix(zoom, zoom)

    try:
        doc = fitz.open(file_path)
        pix = doc[0].get_pixmap(matrix=magnify)

        temp_png_path = f"reports/images/{phone_number}_temp.png"
        pix.save(temp_png_path)

        with Image.open(temp_png_path) as img:
            if crop_dimensions:
                # Crop the image (left, upper, right, lower)
                img = img.crop(crop_dimensions)
            img.save(f"reports/images/{phone_number}.png")

    finally:
        doc.close()
    await delete_file(temp_png_path)
    return True


async def delete_file(file_path: str):
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Fayl muvaffaqiyatli o'chirildi: {file_path}")
    else:
        print(f"Fayl topilmadi: {file_path}")

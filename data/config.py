from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")  # Bot toekn
ADMINS = env.list("ADMINS")  # adminlar ro'yxati
IP = env.str("ip")  # Xosting ip manzili

PROGRAMM_USERNAME = env.str("PROGRAMM_USERNAME").encode("utf-8")
PROGRAMM_PASSWORD = env.str("PROGRAMM_PASSWORD").encode("utf-8")

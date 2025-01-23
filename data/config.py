from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")
IP = env.str("ip")
URL = env.str("url")

PROGRAMM_USERNAME = env.str("PROGRAMM_USERNAME").encode("utf-8")
PROGRAMM_PASSWORD = env.str("PROGRAMM_PASSWORD").encode("utf-8")

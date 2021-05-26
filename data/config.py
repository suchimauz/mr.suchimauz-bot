import os

from environs import Env

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

ROOT_DIR = os.path.dirname(os.path.abspath(__file__ + "/../"))
BROTHERS = [
    {
        'id': 437399585,  # Вадим
        'column': "A"
    },
    {
        'id': 634731718,  # Спецназ
        'column': "C"
    },
    {
        'id': 1053479523,  # Мужик
        'column': "E"
    },
    {
        'id': 743801096,  # Шибай
        'column': "G"
    },
    {
        'id': 607078788,  # Рустам
        'column': "I"
    },
{
        'id': 798072048,  # Димас Герлов
        'column': "K"
    },
]

BOT_TOKEN = env.str("BOT_TOKEN")  # Забираем значение типа str
ADMINS = env.list("ADMINS")  # Тут у нас будет список из админов
IP = env.str("IP")  # Тоже str, но для айпи адреса хоста

PG_HOST = env.str("PG_HOST")
PG_PORT = env.str("PG_PORT")
PG_USER = env.str("PG_USER")
PG_PASSWORD = env.str("PG_PASSWORD")
PG_DATABASE = env.str("PG_DATABASE")

POSTGRES_URI = f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DATABASE}"

QIWI_API_TOKEN = env.str("QIWI_API_TOKEN")
QIWI_NUMBER = env.str("QIWI_NUMBER")
QIWI_NICKNAME = env.str("QIWI_NICKNAME")

SPREADSHEET_ID = env.str("SPREADSHEET_ID")

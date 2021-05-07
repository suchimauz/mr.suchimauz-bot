from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from data.config import ADMINS
from utils.helpers import is_admin


async def get_menu(user_id):
    first_group = [
        KeyboardButton(text="🛒 Магазин")
    ]

    admin_btn = KeyboardButton(text="👤 Админ-панель")

    if is_admin(user_id):
        first_group.append(
            admin_btn
        )

    menu = ReplyKeyboardMarkup(
        keyboard=[
            first_group,
            [
                KeyboardButton(text="🔒 Личный кабинет"),
                KeyboardButton(text="💵 Пополнить")
            ],
            [
                KeyboardButton(text="☎️ Поддержка"),
                KeyboardButton(text="📕 Правила")
            ]
        ],
        resize_keyboard=True
    )

    return menu

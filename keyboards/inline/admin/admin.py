from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from .check import new_check_cd

admin_cd = CallbackData("admin_cd", "level")


def make_admin_cd_callback_data(level):
    return admin_cd.new(level=level)


async def admin_menu_keyboard():
    CURRENT_LEVEL = 0
    markup = InlineKeyboardMarkup()

    markup.add(
        InlineKeyboardButton(text="Создать чек", callback_data=new_check_cd.new(zaglushka="0"))
    )

    return markup

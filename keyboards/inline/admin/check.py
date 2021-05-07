from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.deep_linking import get_start_link

from utils.db.models.check import Check

new_check_cd = CallbackData("new_check_cd", "zaglushka")


async def check_keyboard(check: Check):
    url = await get_start_link('check:' + str(check.id), encode=True)

    markup = InlineKeyboardMarkup()

    markup.add(
        InlineKeyboardButton(text="Активировать", url=url)
    )

    return markup

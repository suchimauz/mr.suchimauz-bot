from typing import Union

from aiogram.types import Message, CallbackQuery

from keyboards.inline.admin.admin import admin_menu_keyboard
from loader import dp


async def list_admin_menu(message: Union[Message, CallbackQuery], **kwargs):
    text = "Выберите пункт меню"
    markup = await admin_menu_keyboard()

    if isinstance(message, Message):
        await message.answer(text=text, reply_markup=markup)

    elif isinstance(message, CallbackQuery):
        call = message
        await call.message.edit_text(text=text, reply_markup=markup)
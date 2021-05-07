from typing import Union

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from utils.helpers import is_admin as is_admin_func


class AdminFilter(BoundFilter):
    key = 'is_admin'

    def __init__(self, is_admin):
        self.is_admin = is_admin

    async def check(self, message: Union[types.Message, types.CallbackQuery]):
        is_admin = is_admin_func(message.from_user.id)
        if not is_admin:
            await message.answer("Вы не являетесь администратором!")

        return is_admin is self.is_admin

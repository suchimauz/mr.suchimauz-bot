from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware


class LastActivityMiddleWare(BaseMiddleware):
    def __init__(self, message: types.Message):
        print(message.from_user)

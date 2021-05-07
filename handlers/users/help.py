from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp


help_commands = ("Список команд: ",
                 "/start - Инициализация",
                 "/menu - Вызвать меню",
                 "/shop - Купить товары",
                 "/profile - Личный кабинет",
                 "/support - Поддержка",
                 "/rules - Правила")


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = "\n".join(help_commands)

    await message.answer(text)

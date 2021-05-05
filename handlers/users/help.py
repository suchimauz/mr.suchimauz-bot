from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp


help_commands = ("Список команд: ",
                 "/start - Инициализация",
                 "/help - Получить справку",)


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = "\n".join(help_commands)

    await message.answer(text)

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.default import menu
from loader import dp
from utils.db.models.user import add_user
from .help import help_commands


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    text = (f"Привет, {message.from_user.full_name}!\n",
            "\n".join(help_commands))

    await add_user(id=message.from_user.id, username=message.from_user.username)

    await message.answer("\n".join(text), reply_markup=menu)

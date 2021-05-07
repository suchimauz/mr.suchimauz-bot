from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.utils.deep_linking import decode_payload

from keyboards.default.menu import get_menu
from loader import dp
from utils.db.models.check import activate_check_and_return_msg
from utils.db.models.user import add_user
from .help import help_commands


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await add_user(id=message.from_user.id, username=message.from_user.username)

    args = message.get_args()
    payload = decode_payload(args)

    menu = await get_menu(message.from_user.id)

    if payload is not None:
        split_payload = payload.split(":")

        if split_payload[0] == "check":
            check_id = split_payload[1]
            user_id = message.from_user.id
            text = await activate_check_and_return_msg(user_id, check_id)
            await message.answer(text=text, reply_markup=menu)

        else:
            text = (f"Привет, {message.from_user.full_name}!\n",
                    "\n".join(help_commands))
            await message.answer("\n".join(text), reply_markup=menu)

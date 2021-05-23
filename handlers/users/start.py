from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart, Command
from aiogram.utils.deep_linking import decode_payload, get_start_link

from keyboards.default.menu import get_menu
from loader import dp
from utils.db.models.check import activate_check_and_return_msg
from utils.db.models.referral import add_new_referrer_for_user
from utils.db.models.user import add_user
from .help import help_commands


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    new_user = await add_user(id=message.from_user.id, username=message.from_user.username)

    args = message.get_args()
    payload = decode_payload(args)

    start_text = (f"Привет, {message.from_user.full_name}!\n",
                  "\n".join(help_commands))

    menu = await get_menu(message.from_user.id)

    if payload is not None:
        split_payload = payload.split(":")

        if split_payload[0] == "check":
            check_id = split_payload[1]
            user_id = message.from_user.id
            text = await activate_check_and_return_msg(user_id, check_id)
            await message.answer(text=text, reply_markup=menu)

        if split_payload[0] == "ref" and new_user:
            referrer_id = int(split_payload[1])
            user_id = message.from_user.id

            await add_new_referrer_for_user(user_id=user_id, referrer_id=referrer_id)

            await message.answer(text="\n".join(start_text), reply_markup=menu)

        else:
            await message.answer(text="\n".join(start_text), reply_markup=menu)

    else:
        await message.answer(text="\n".join(start_text), reply_markup=menu)


@dp.message_handler(Command("ref"))
async def return_ref_link(msg: types.Message):
    ref_link = await get_start_link('ref:' + str(msg.from_user.id), encode=True)

    await msg.answer(text=ref_link)

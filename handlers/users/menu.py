from aiogram.dispatcher.filters import Text, Command
from aiogram.types import Message
from keyboards.default import menu
from loader import dp


@dp.message_handler(Command("menu"))
async def show_menu(message: Message):
    await message.answer(reply_markup=menu)


@dp.message_handler(text="🛒 Магазин")
@dp.message_handler(Command("shop"))
async def show_shop(message: Message):
    await message.answer(text="Магазин")


@dp.message_handler(text="🔒 Личный кабинет")
@dp.message_handler(Command("profile"))
async def show_profile(message: Message):
    await message.answer(
        text=f"Личный кабинет <b>{message.from_user.full_name}</b>\n\n"
             f"💬 Ваш ChatID: <b>{message.from_user.id}</b>\n"
             f"👤 Ваш логин:  @{message.from_user.username}\n"
             f"💰 Ваш баланс: <code>0 USD</code>")


@dp.message_handler(text="💵 Пополнить")
async def show_fill(message: Message):
    await message.answer(text="Пополнить")


@dp.message_handler(text="☎️ Поддержка")
@dp.message_handler(Command("support"))
async def show_shop(message: Message):
    await message.answer(text="Поддержка")


@dp.message_handler(text="📕 Правила")
@dp.message_handler(Command("rules"))
async def show_rules(message: Message):
    await message.answer(text="Правила")


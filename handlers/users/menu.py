from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from handlers.users.payment import list_payment_methods
from handlers.users.shop import list_product_categories
from keyboards.default import menu

from loader import dp
from utils.db.models.user import get_user, get_user_balance


@dp.message_handler(Command("menu"))
async def show_menu(message: Message):
    await message.answer(reply_markup=menu, text="Выберите пункт меню")


@dp.message_handler(text="🛒 Магазин")
@dp.message_handler(Command("shop"))
async def show_shop(message: Message):
    await list_product_categories(message)


@dp.message_handler(text="🔒 Личный кабинет")
@dp.message_handler(Command("profile"))
async def show_profile(message: Message):
    balance = await get_user_balance(message.from_user.id)
    await message.answer(
        text=f"Личный кабинет <b>{message.from_user.full_name}</b>\n\n"
             f"💬 Ваш ChatID: <b>{message.from_user.id}</b>\n"
             f"👤 Ваш логин:  @{message.from_user.username}\n"
             f"💰 Ваш баланс: <code>{balance} USD</code>")


@dp.message_handler(text="💵 Пополнить")
async def show_fill(message: Message):
    await list_payment_methods(message)


@dp.message_handler(text="☎️ Поддержка")
@dp.message_handler(Command("support"))
async def show_shop(message: Message):
    await message.answer(text="Поддержка: @suchimauz")


@dp.message_handler(text="📕 Правила")
@dp.message_handler(Command("rules"))
async def show_rules(message: Message):
    await message.answer(text="Правила")
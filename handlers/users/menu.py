from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from handlers.users.admin.admin import list_admin_menu
from handlers.users.payment import list_payment_methods
from handlers.users.shop import list_product_categories
from keyboards.default.menu import get_menu

from loader import dp
from utils.db.models.referral import get_referrals_count_by_referrer_id, get_referrals_cost_by_referrer_id
from utils.db.models.user import get_user_balance
from utils.helpers import get_usd_from_cents


@dp.message_handler(Command("menu"))
async def show_menu(message: Message):
    menu = await get_menu(message.from_user.id)

    await message.answer(reply_markup=menu, text="Выберите пункт меню")


@dp.message_handler(text="🛒 Магазин")
@dp.message_handler(Command("shop"))
async def show_shop(message: Message):
    await list_product_categories(message)


@dp.message_handler(text="👤 Админ-панель", is_admin=True)
@dp.message_handler(Command("admin"), is_admin=True)
async def show_admin_menu(message: Message):
    await list_admin_menu(message)


@dp.message_handler(text="🔒 Личный кабинет")
@dp.message_handler(Command("profile"))
async def show_profile(message: Message):
    balance = await get_user_balance(message.from_user.id)
    referrals_count = await get_referrals_count_by_referrer_id(message.from_user.id)
    referrals_cost = await get_referrals_cost_by_referrer_id(message.from_user.id)

    text = f"Личный кабинет <b>{message.from_user.full_name}</b>\n\n" \
           f"💬 Ваш ChatID: <b>{message.from_user.id}</b>\n" \
           f"👤 Ваш логин:  @{message.from_user.username}\n" \
           f"💰 Ваш баланс: <code>{balance} USD</code>"

    if referrals_count > 0:
        text = text + f"\n\n🧍🏻‍♂️ Количество рефералов: <b>{referrals_count}</b>\n" \
                      f"📈 Купили на сумму: <code>{get_usd_from_cents(referrals_cost)} USD</code>"

    await message.answer(
        text=text)


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
    await message.answer(text="Правила:\n\n"
                              "1. Вывод средств не осуществляется!")

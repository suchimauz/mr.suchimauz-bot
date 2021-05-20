from datetime import datetime

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from keyboards.inline.transaction import buy_product, transaction_info_keyboard, set_transaction_status
from loader import dp
from utils.db import db
from utils.db.models.bank_account import get_ba_count_by_product, get_available_ba_for_user, update_purchased_ba
from utils.db.models.product import get_product_by_type
from utils.db.models.transaction import Transaction, get_transaction_by_id
from utils.db.models.user import get_user_balance
from utils.helpers import get_cents_from_usd, get_usd_from_cents, chunks


@dp.callback_query_handler(buy_product.filter())
async def buy_product(call: CallbackQuery, state: FSMContext, callback_data: dict):
    text = f"Введите желаемое количество для покупки (целое число)"
    product_type = callback_data.get('product_type')

    await call.message.answer(text)
    await state.set_state("wait_transaction_count")
    await state.update_data(product_type=product_type)


@dp.message_handler(state="wait_transaction_count")
async def wait_transaction_count(message: Message, state: FSMContext):
    data = await state.get_data()
    product_type = data.get("product_type")
    product = await get_product_by_type(product_type)

    count = int(message.text)

    if product.type == "schwab":
        product_count = await get_ba_count_by_product(product.type)
        user_balance = await get_user_balance(message.from_user.id)
        user_balance_cents = get_cents_from_usd(user_balance)
        transaction_cost = await product.get_price(count=count, user_id=message.from_user.id)
        transaction_status = "waiting"

        if count > product_count:
            await message.answer(text=f"Нет столько товара, укажите меньшее количество еще раз\n"
                                      f"В наличии: <b>{product_count}</b>")
        elif transaction_cost <= user_balance_cents:
            transaction = await Transaction(
                user_id=message.from_user.id,
                product_type=product.type,
                count=count,
                cost=transaction_cost,
                status=transaction_status,
                created_date=datetime.now()
            ).create()

            markup = await transaction_info_keyboard(transaction=transaction)

            await message.answer(
                text=f"Информация о покупке: \n\n"
                     f"Название: <b>{product.name}</b>\n"
                     f"Цена: <i><b>{get_usd_from_cents(transaction_cost)} USD</b></i>\n"
                     f"Количество: <i><b>{count}</b></i>",
                reply_markup=markup
            )
        else:
            await message.answer(text=f"Недостаточно средств для покупки!\n"
                                      f"Не хватает: "
                                      f"<b>{get_usd_from_cents(transaction_cost - user_balance_cents)} "
                                      f"USD</b>")

    else:
        await message.answer("Ошибка, попробуйте заново!")

    await state.reset_state()


@dp.callback_query_handler(set_transaction_status.filter())
async def set_status(call: CallbackQuery, callback_data: dict):
    transaction_id = callback_data.get('transaction_id')
    status = callback_data.get('status')

    transaction = await get_transaction_by_id(transaction_id)

    if transaction.status == 'waiting':
        if status == 'cancelled':
            await transaction.update(
                status=status,
                updated_date=datetime.now()
            ).apply()

            await call.message.answer(text="Покупка успешно отменена!")
            await call.message.delete()
        elif status == 'success':
            await transaction.update(
                status=status,
                updated_date=datetime.now()
            ).apply()

            if transaction.product_type == 'schwab':
                bank_accounts = await get_available_ba_for_user(transaction.count)

                if len(bank_accounts) == transaction.count:
                    await update_purchased_ba(bank_accounts, call.from_user.id)

                    text = f"Bank Name: <b>Charles Schwab</b>\n" \
                           f"Bank Type: <b>Checking</b>\n" \
                           f"Format: <b>[Full Name]</b>:<b>[Routing Number]</b>:" \
                           f"<b>[Account Number]</b>:<b>[Login]</b>:" \
                           f"<b>[Password]</b>:<b>[Zip Code]</b>\n<pre>"

                    if transaction.count <= 40:
                        for ba in bank_accounts:
                            text += f"{ba.full_name}:{ba.routing_number}:" \
                                    f"{ba.account_number}:{ba.bank_login}:" \
                                    f"{ba.bank_password}:{ba.bank_zip}\n"

                        text += "</pre>"

                        await call.message.answer(text=text)

                    else:
                        for chunk in chunks(bank_accounts, 40):
                            for ba in chunk:
                                text += f"{ba.full_name}:{ba.routing_number}:" \
                                        f"{ba.account_number}:{ba.bank_login}:" \
                                        f"{ba.bank_password}:{ba.bank_zip}\n"

                            text += "</pre>"

                            await call.message.answer(text=text)

                            text = "<pre>"

                    await call.message.answer(text="<b><i>Товар успешно выдан!</i></b>")
                    await call.message.delete()
                else:
                    await call.message.answer(text="Ошибка, попробуйте заново!")
                    await call.message.delete()

    else:
        await call.message.answer(text="Транзакция уже недействительна!")
        await call.message.delete()

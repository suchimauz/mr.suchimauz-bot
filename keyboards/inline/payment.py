from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from random import randrange

from utils.db.models.payment import Payment
from utils.db.models.payment_method import get_active_payment_methods

payment_cd = CallbackData("payment", "user_id", "method")
check_payment = CallbackData("check_payment", "user_id", "method", "payment")
cancel_payment = CallbackData("cancel_payment", "payment_id")


def make_check_payment_callback_data(user_id, method, payment):
    return check_payment.new(user_id=user_id, method=method, payment=payment)


def make_payment_cd_callback_data(user_id, method="0"):
    return payment_cd.new(user_id=user_id, method=method)


async def payment_methods_keyboard(user_id):
    markup = InlineKeyboardMarkup()

    methods = await get_active_payment_methods()

    for method in methods:
        button_text = f"{method.name}"
        callback_data = make_payment_cd_callback_data(user_id=user_id, method=method.method)
        markup.row(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )

    return markup


async def qiwi_transaction_keyboard(user_id, payment: Payment):
    markup = InlineKeyboardMarkup()
    payment_method = "qiwi"

    markup.row(
        InlineKeyboardButton(
            text="Проверить оплату",
            callback_data=make_check_payment_callback_data(
                user_id=user_id,
                method=payment_method,
                payment=payment.id
            )
        )
    )
    markup.row(
        InlineKeyboardButton(
            text="Отмена",
            callback_data=cancel_payment.new(
                payment_id=payment.id
            )
        )
    )

    return markup



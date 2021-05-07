from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from utils.db.models.transaction import Transaction

buy_product = CallbackData("buy", "product_type")
set_transaction_status = CallbackData("set_transaction_status", "transaction_id", "status")


async def transaction_info_keyboard(transaction: Transaction):
    markup = InlineKeyboardMarkup()

    markup.row(
        InlineKeyboardButton(
            text="Подтвердить покупку",
            callback_data=set_transaction_status.new(
                transaction_id=transaction.id,
                status="success"
            )
        )
    )

    markup.row(
        InlineKeyboardButton(
            text="Отмена",
            callback_data=set_transaction_status.new(
                status="cancelled",
                transaction_id=transaction.id
            )
        )
    )

    return markup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from keyboards.inline.transaction import buy_product
from utils.db.models.bank_account import get_ba_count_by_product
from utils.db.models.product import get_products_by_category
from utils.db.models.product_category import get_product_categories

product_cd = CallbackData("show_product", "level", "category", "product_type")


def make_callback_data(level, category="0", product_type="0"):
    return product_cd.new(level=level,
                          category=category,
                          product_type=product_type)


async def product_categories_keyboard():
    CURRENT_LEVEL = 0
    markup = InlineKeyboardMarkup()

    categories = await get_product_categories()
    for category in categories:
        button_text = f"{category.name}"
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1,
                                           category=category.category)
        markup.row(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )

    return markup


async def products_keyboard(category, user_id):
    CURRENT_LEVEL = 1
    markup = InlineKeyboardMarkup()

    products = await get_products_by_category(category)

    for product in products:
        number_of_products = await get_ba_count_by_product(product.type)
        price_text = await product.get_price_text(user_id)

        button_text = f"{number_of_products} шт. - {product.name} - {price_text}"
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1,
                                           category=category,
                                           product_type=product.type)
        markup.row(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )

    markup.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=make_callback_data(level=CURRENT_LEVEL - 1)
        )
    )

    return markup


async def products_item_keyboard(category, product_type):
    CURRENT_LEVEL = 2
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(
            text="💰 Купить",
            callback_data=buy_product.new(product_type=product_type)
        )
    )
    markup.row(
        InlineKeyboardButton(
            text="Отмена",
            callback_data=make_callback_data(level=CURRENT_LEVEL - 1, category=category)
        )
    )

    return markup

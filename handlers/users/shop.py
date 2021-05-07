from typing import Union

from keyboards.inline.shop import product_categories_keyboard, products_keyboard, product_cd, \
    products_item_keyboard
from utils.db.models.bank_account import get_ba_count_by_product

from utils.db.models.product import get_product_by_type
from aiogram.types import Message, CallbackQuery
from loader import dp


async def list_product_categories(message: Union[Message, CallbackQuery], **kwargs):
    markup = await product_categories_keyboard()
    text = "Выберите категорию товара"

    if isinstance(message, Message):
        await message.answer(text=text, reply_markup=markup)

    elif isinstance(message, CallbackQuery):
        call = message
        await call.message.edit_text(text=text, reply_markup=markup)


async def list_products(callback: CallbackQuery, category, **kwargs):
    markup = await products_keyboard(category)

    await callback.message.edit_text(text="Выберите товар", reply_markup=markup)


async def show_product(callback: CallbackQuery, category, product_type, **kwargs):
    markup = await products_item_keyboard(category=category, product_type=product_type)

    product = await get_product_by_type(product_type=product_type)

    product_count = 0

    if product.type == "schwab":
        product_count = await get_ba_count_by_product(product.type)

    price_text = await product.get_price_text()

    await callback.message.edit_text(text=f"Информация о товаре: \n\n"
                                          f"Название: <b>{product.name}</b>\n"
                                          f"Цена: <i><b>{price_text}</b></i>\n"
                                          f"Количество: <i><b>{product_count}</b></i>",
                                     reply_markup=markup)


@dp.callback_query_handler(product_cd.filter())
async def navigate(call: CallbackQuery, callback_data: dict):
    CURRENT_LEVEL = callback_data.get('level')
    category = callback_data.get('category')
    product_type = callback_data.get('product_type')

    levels = {
        "0": list_product_categories,
        "1": list_products,
        "2": show_product,
    }
    current_level_function = levels[CURRENT_LEVEL]

    await current_level_function(call,
                                 category=category,
                                 product_type=product_type)
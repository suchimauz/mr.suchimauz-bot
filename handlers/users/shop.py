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
    if category == 'logs':
        text = f"<b>Логи:</b>\n\n" \
                f"🟢 <b>Google:</b>\n" \
                f"🔥 No ADS MIX | 💰 <b>0.9$</b> <i>(от 100 шт по 0.8$)</i>\n" \
                f"🔥 No ADS EU | 💰 <b>1.5$</b> <i>(от 100 шт по 1.3$)</i>\n" \
                f"🔥 No ADS USA | 💰 <b>2$</b> <i>(от 100 шт по 1.8$)</i>\n" \
                f"🔥 Gpay+cc EU TOP | 💰 <b>3.7$</b> <i>(от 50 шт по 3.5$)</i>\n" \
                f"🔥 Gpay+cc USA | 💰 <b>4.5$</b>\n" \
                f"🔥 Gpay+cc MIX | 💰 <b>2.2$</b> <i>(от 100 шт по 2.0$)</i>\n\n" \
                f"🔵 <b>Facebook:</b>\n" \
                f"🔥 MIX | 💰 <b>2.0$</b> <i>(от 100 шт по 1.8$)</i>\n" \
                f"🔥 MIX лимит 250-350$ | 💰 <b>7.0$</b>\n" \
                f"🔥 FB+BM MIX | 💰 <b>3.0$</b> <i>(от 100 шт по 2.9$)</i>\n\n" \
                f"За покупкой обращаться @logs_suchimauz\n" \
                f"❗️Бесплатных тестов нет. Минимальный заказ - <b>10$</b>"

        await callback.message.answer(text=text)
    else:
        markup = await products_keyboard(category=category, user_id=callback.from_user.id)

        await callback.message.edit_text(text="Выберите товар", reply_markup=markup)


async def show_product(callback: CallbackQuery, category, product_type, **kwargs):
    markup = await products_item_keyboard(category=category, product_type=product_type)

    product = await get_product_by_type(product_type=product_type)

    product_count = 0

    if product.type == "schwab":
        product_count = await get_ba_count_by_product(product.type)

    price_text = await product.get_price_text(user_id=callback.from_user.id)

    text = f"Информация о товаре: \n\n" \
           f"Название: <b>{product.name}</b>\n" \
           f"Цена: <i><b>{price_text}</b></i>\n" \
           f"Количество: <i><b>{product_count}</b></i>"

    if product.type == "schwab":
        text = text + f"\n\nТестовый депозит приходит обычно на следующий день после привязки!\n" \
                      f"<b><i>Постарайтесь покупать столько БА, сколько сможете привязать за 8 часов, дабы избежать заблокированных аккаунтов.</i></b>\n" \
                      f"<b>ВАЖНО!</b> " \
                      f"<i>Если привязать на выходных, то тестовый депозит придет в понедельник-вторник!</i>"

    await callback.message.edit_text(text=text,
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
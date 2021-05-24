import math

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.admin.admin import make_admin_cd_callback_data, admin_search_users_cd
from utils.db.models.product import get_products, get_product_count
from utils.db.models.user import get_users, get_users_count, get_user
from utils.helpers import get_usd_from_cents


def markup_paging(markup: InlineKeyboardMarkup, keyboard, prev_keyboard, search, page, obj_count, limit, user_id="0") -> InlineKeyboardMarkup:
    if obj_count > limit:
        min_page = 1
        max_page = math.ceil(obj_count / limit)

        if page == min_page:
            prev_page = max_page
        else:
            prev_page = page - 1

        if page == max_page:
            next_page = min_page
        else:
            next_page = page + 1

        markup.row(
            InlineKeyboardButton(
                text="⬅️ Пред",
                callback_data=make_admin_cd_callback_data(
                    keyboard=keyboard,
                    prev_keyboard=prev_keyboard,
                    search=search,
                    page=prev_page,
                    user_id=user_id
                )
            )
        )

        markup.insert(
            InlineKeyboardButton(
                text=f"{page} / {max_page}",
                callback_data=make_admin_cd_callback_data(
                    keyboard=keyboard,
                    prev_keyboard=prev_keyboard,
                    search=search,
                    page=1,
                )
            )
        )

        markup.insert(
            InlineKeyboardButton(
                text="След ➡️",
                callback_data=make_admin_cd_callback_data(
                    keyboard=keyboard,
                    prev_keyboard=prev_keyboard,
                    search=search,
                    page=next_page,
                )
            )
        )

        markup.row(
            InlineKeyboardButton(
                text="🔎 Поиск",
                callback_data=admin_search_users_cd.new(
                    keyboard=keyboard,
                    prev_keyboard=prev_keyboard,
                    page=page,
                )
            )
        )

        if search != "" and search != "0" and search:
            markup.insert(
                InlineKeyboardButton(
                    text="Отменить поиск",
                    callback_data=make_admin_cd_callback_data(
                        keyboard=keyboard,
                        prev_keyboard=prev_keyboard,
                        search="",
                        page=1,
                    )
                )
            )

        return markup

    else:
        if search != "" and search != "0" and search:
            markup.row(
                InlineKeyboardButton(
                    text="Отменить поиск",
                    callback_data=make_admin_cd_callback_data(
                        keyboard=keyboard,
                        prev_keyboard=prev_keyboard,
                        search="",
                        page=1,
                    )
                )
            )

        return markup


async def admin_users_list_keyboard(prev_keyboard, search, page):
    CURRENT_KEYBOARD = 'admin_users_list'
    markup = InlineKeyboardMarkup()

    page = int(page)
    limit = 10
    offset = limit * (page - 1)
    users = await get_users(limit=limit, offset=offset, search=search)
    users_count = await get_users_count(search=search)

    for user in users:
        if user.username:
            text = user.username
        else:
            text = "Неизвестно"

        markup.row(
            InlineKeyboardButton(
                text=text,
                callback_data=make_admin_cd_callback_data(
                    keyboard="admin_user_show",
                    prev_keyboard=CURRENT_KEYBOARD,
                    search=search,
                    page=page,
                    user_id=user.id
                )
            )
        )

    markup = markup_paging(
        markup=markup,
        keyboard=CURRENT_KEYBOARD,
        prev_keyboard=prev_keyboard,
        search=search,
        page=page,
        obj_count=users_count,
        limit=limit
    )

    markup.row(
        InlineKeyboardButton(
            text="Отмена",
            callback_data=make_admin_cd_callback_data(
                keyboard=prev_keyboard
            )
        )
    )

    return markup


async def admin_user_show_keyboard(prev_keyboard, search, page, user_id):
    CURRENT_KEYBOARD = "admin_user_show"
    markup = InlineKeyboardMarkup()

    markup.row(
        InlineKeyboardButton(
            text="Цены на товары",
            callback_data=make_admin_cd_callback_data(
                keyboard="admin_user_product_prices_list",
                search="",
                page=1,
                user_id=user_id
            )
        )
    )

    markup.row(
        InlineKeyboardButton(
            text="Отмена",
            callback_data=make_admin_cd_callback_data(
                keyboard=prev_keyboard,
                search=search,
                page=page,
            )
        )
    )

    return markup


async def admin_user_product_prices_list_keyboard(prev_keyboard, search, page, user_id):
    CURRENT_KEYBOARD = 'admin_user_product_prices_list'
    markup = InlineKeyboardMarkup()
    page = int(page)
    limit = 10
    offset = limit * (page - 1)

    products = await get_products(limit=limit, offset=offset)
    product_counts = await get_product_count()

    for product in products:
        default_price = await product.get_default_price(user_id=user_id)
        whole_price = await product.get_whole_price(user_id=user_id)

        text = f"{product.name} [{get_usd_from_cents(default_price)}$ | {get_usd_from_cents(whole_price)}$]"

        markup.row(
            InlineKeyboardButton(
                text=text,
                url="https://google.com"
            )
        )

    markup = markup_paging(
        markup=markup,
        keyboard=CURRENT_KEYBOARD,
        prev_keyboard=prev_keyboard,
        search=search,
        page=page,
        obj_count=product_counts,
        limit=limit,
        user_id=user_id
    )

    markup.row(
        InlineKeyboardButton(
            text="Отмена",
            callback_data=make_admin_cd_callback_data(
                keyboard="admin_user_show",
                search="",
                page=1,
                user_id=user_id
            )
        )
    )

    return markup

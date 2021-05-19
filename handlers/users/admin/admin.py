from typing import Union

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram_broadcaster import MessageBroadcaster

from keyboards.inline.admin.admin import admin_menu_keyboard, admin_cd, admin_send_message_to_all_users_cd
from keyboards.inline.admin.users import admin_users_list_keyboard, admin_user_show_keyboard, \
    admin_user_product_prices_list_keyboard
from loader import dp, bot
from utils.db.models.user import get_user, get_user_balance, get_users_ids


async def list_admin_menu(message: Union[Message, CallbackQuery], **kwargs):
    text = "Выберите пункт меню"
    markup = await admin_menu_keyboard()

    if isinstance(message, Message):
        await message.answer(text=text, reply_markup=markup)

    elif isinstance(message, CallbackQuery):
        call = message
        await call.message.edit_text(text=text, reply_markup=markup)


async def list_admin_users(call=CallbackQuery, prev_keyboard=None, search="", page=1, **kwargs):
    if prev_keyboard == '0':
        prev_keyboard = "admin_menu"

    text = "Выберите пользователя"
    markup = await admin_users_list_keyboard(
        prev_keyboard=prev_keyboard,
        search=search,
        page=page,
    )

    await call.message.edit_text(text=text, reply_markup=markup)


async def admin_user_show(call=CallbackQuery, prev_keyboard=None, search="", page=1, user_id=None, **kwargs):
    if prev_keyboard == '0':
        prev_keyboard = "admin_users_list"

    user = await get_user(user_id)
    balance = await get_user_balance(user_id=user_id)

    text = f"Пользователь <b>@{user.username}</b>\n\n" \
           f"💬 ChatID: <b>{user.id}</b>\n" \
           f"💰 Баланс: <code>{balance} USD</code>"

    markup = await admin_user_show_keyboard(
        prev_keyboard=prev_keyboard,
        search=search,
        page=page,
        user_id=user_id
    )

    await call.message.edit_text(text=text, reply_markup=markup)


async def list_admin_user_product_prices(call=CallbackQuery, prev_keyboard=None, search="", page=1, user_id=None, **kwargs):
    if prev_keyboard == '0':
        prev_keyboard = "admin_user_show"

    user = await get_user(user_id)

    text = f"Пользователь <b>@{user.username}</b>\n\n" \
           f"Выберите товар"

    markup = await admin_user_product_prices_list_keyboard(
        prev_keyboard=prev_keyboard,
        search=search,
        page=page,
        user_id=user_id
    )

    await call.message.edit_text(
        text=text,
        reply_markup=markup
    )


@dp.callback_query_handler(admin_cd.filter(), is_admin=True)
async def navigate(call: CallbackQuery, callback_data: dict):
    CURRENT_KEYBOARD = callback_data.get('keyboard')
    prev_keyboard = callback_data.get('prev_keyboard')
    search = callback_data.get('search')
    page = callback_data.get('page')
    user_id = callback_data.get('user_id')

    keyboards = {
        "admin_menu": list_admin_menu,
        "admin_users_list": list_admin_users,
        "admin_user_show": admin_user_show,
        "admin_user_product_prices_list": list_admin_user_product_prices,
    }
    current_level_function = keyboards[CURRENT_KEYBOARD]

    await current_level_function(
        call,
        keyboard=CURRENT_KEYBOARD,
        prev_keyboard=prev_keyboard,
        search=search,
        page=page,
        user_id=user_id,
    )


@dp.callback_query_handler(admin_send_message_to_all_users_cd.filter(), is_admin=True)
@dp.callback_query_handler(admin_send_message_to_all_users_cd.filter(), state="wait_message_to_send_all_users")
async def send_message_to_all_users(call: CallbackQuery, state: FSMContext, callback_data: dict,  **kwargs):
    is_cancel = callback_data.get('cancel')

    if is_cancel == 'True':
        await state.reset_state()
        await call.message.edit_text(
            text="Отправка уведомления успешно отменена!"
        )
    else:
        markup = InlineKeyboardMarkup()
        markup.row(
            InlineKeyboardButton(
                text="Отменить",
                callback_data=admin_send_message_to_all_users_cd.new(
                    cancel="True"
                )
            )
        )

        await call.message.answer(
            text="Введите сообщение",
            reply_markup=markup
        )
        await state.set_state("wait_message_to_send_all_users")


@dp.message_handler(state="wait_message_to_send_all_users")
async def get_new_check(message: Message, state: FSMContext):
    await state.reset_state()

    users = await get_users_ids()

    await MessageBroadcaster(users, message).run()

    await message.answer(text="Уведомление отправлено успешно!")

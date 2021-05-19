from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from .check import new_check_cd

admin_cd = CallbackData(
    "admin_cd",
    "keyboard",
    "prev_keyboard",
    "search",
    "page",
    "user_id",
)
admin_send_message_to_all_users_cd = CallbackData(
    "admin_send_message_to_all_users",
    "cancel"
)
admin_upload_mails_from_file_cd = CallbackData(
    "admin_upload_mails_from_file",
    "cancel"
)


def make_admin_cd_callback_data(keyboard, prev_keyboard="0", search="0", page=1, user_id="0"):
    return admin_cd.new(
        keyboard=keyboard,
        prev_keyboard=prev_keyboard,
        search=search,
        page=page,
        user_id=user_id
    )


async def admin_menu_keyboard():
    CURRENT_KEYBOARD = 'admin_menu'
    markup = InlineKeyboardMarkup()

    markup.add(
        InlineKeyboardButton(text="📃 Создать чек", callback_data=new_check_cd.new(zaglushka="0")),
        InlineKeyboardButton(
            text="🧍‍♂ Пользователи",
            callback_data=make_admin_cd_callback_data(
                keyboard="admin_users_list",
                prev_keyboard=CURRENT_KEYBOARD,
            )
        )
    )
    markup.add(
        InlineKeyboardButton(
            text="✉️ Отправить всем сообщение",
            callback_data=admin_send_message_to_all_users_cd.new(
                cancel="0",
            )
        )
    )
    markup.add(
        InlineKeyboardButton(
            text="💾 Загрузить почты с файла",
            callback_data=admin_upload_mails_from_file_cd.new(
                cancel="0",
            )
        )
    )

    return markup

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType

from keyboards.inline.admin.admin import admin_upload_mails_from_file_cd
from loader import dp, bot

import io

from utils.db.models.mail import Mail


@dp.callback_query_handler(admin_upload_mails_from_file_cd.filter(), is_admin=True)
@dp.callback_query_handler(admin_upload_mails_from_file_cd.filter(), state="wait_mails_file_to_upload")
async def upload_mails(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    is_cancel = callback_data.get('cancel')

    if is_cancel == 'True':
        await state.reset_state()
        await call.message.edit_text(
            text="Вгрузка почт успешно отменена!"
        )
    else:
        markup = types.InlineKeyboardMarkup()
        markup.row(
            types.InlineKeyboardButton(
                text="Отменить",
                callback_data=admin_upload_mails_from_file_cd.new(
                    cancel="True"
                )
            )
        )

        await call.message.answer(
            text="Отправьте текстовый файл",
            reply_markup=markup
        )
        await state.set_state("wait_mails_file_to_upload")


@dp.message_handler(state="wait_mails_file_to_upload", content_types=[ContentType.DOCUMENT], is_admin=True)
async def get_file_to_upload(msg: types.Message, state: FSMContext):
    await state.reset_state()

    separator = msg.caption

    if not separator:
        separator = ":"

    import os
    if not os.path.exists("tmp"):
        os.makedirs("tmp")

    src = "tmp/mails.txt"

    await msg.document.download(destination=src)
    x = open(src, "r")

    mails_count = 0
    count = 0

    await msg.answer(text="Началась загрузка... Подождите")

    for mail_line in x.readlines():
        mail = mail_line.split(separator)

        try:
            created = await Mail(
                email=mail[0],
                password=mail[1],
                reserved_email=mail[2],
                imap="imap.mail.ru"
            ).create()

            if created:
                count += 1

        except Exception:
            pass

        mails_count += 1

    await msg.answer(text=f"Загружено <b>{count}</b> почт из <b>{mails_count}</b>.")




from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.admin.admin import admin_upload_mails_from_file_cd
from loader import dp, bot

import io


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


@dp.message_handler(state="wait_mails_file_to_upload", content_types=['document'])
async def get_file_to_upload(msg: types.Message, state: FSMContext):
    await state.reset_state()

    src = "tmp/mails.txt"

    await msg.document.download(destination=src)
    x = open(src, "r")

    for mail_line in x.readlines():
        print(mail_line)



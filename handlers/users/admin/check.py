from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.admin.admin import new_check_cd
from keyboards.inline.admin.check import check_keyboard
from loader import dp
from utils.db.models.check import add_check
from utils.helpers import get_cents_from_usd, get_usd_from_cents


@dp.callback_query_handler(new_check_cd.filter())
async def new_check_cd(call: types.CallbackQuery, state: FSMContext, **kwargs):
    await call.message.answer(text="Введите сумму в долларах <b>USD</b>")

    await state.set_state("wait_check_cost")


@dp.message_handler(state="wait_check_cost")
async def get_new_check(message: types.Message, state: FSMContext):
    cost = float(message.text)
    cost_cents = get_cents_from_usd(cost)

    check = await add_check(cost_cents)

    text = f"Чек на сумму <b>{get_usd_from_cents(check.cost)} USD</b>\n\n" \
           f"Нажмите на кнопку для активации"
    markup = await check_keyboard(check)

    await message.answer(text=text, reply_markup=markup)
    await state.reset_state()


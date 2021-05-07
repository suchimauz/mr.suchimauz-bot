from random import randrange
from typing import Union

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from data.config import QIWI_NUMBER, QIWI_NICKNAME
from keyboards.inline.payment import payment_methods_keyboard, payment_cd, qiwi_transaction_keyboard, check_payment, \
    cancel_payment
from loader import dp
from utils.db.models.payment import Payment, get_payment_with_id
from utils.db.models.payment_method import get_payment_method_by_method
from utils.helpers import get_usd_from_cents, get_current_usd_from_rub, get_cents_from_usd

from utils.payments.qiwi import check_qiwi_payment


async def list_payment_methods(message: Message, **kwargs):
    markup = await payment_methods_keyboard(message.from_user.id)

    await message.answer(text="Выберите способ пополнения",
                         reply_markup=markup)


@dp.callback_query_handler(payment_cd.filter())
async def payment(call: CallbackQuery, state: FSMContext, callback_data: dict):
    payment_method = callback_data.get('method')
    payment_method = await get_payment_method_by_method(payment_method)

    text = 'Введите сумму пополнения в рублях (целое число)\n' \
           f'Минимум: <b>{payment_method.min} RUB</b>'

    if payment_method.max:
        text = text + f'\nМаксимум: <b>{payment_method.max} RUB</b>'

    await call.message.answer(text=text)
    await state.set_state("wait_payment_cost")
    await state.update_data(payment_method=payment_method.method)


@dp.message_handler(state="wait_payment_cost")
async def payment_cost(message: Message, state: FSMContext):
    data = await state.get_data()
    payment_method = data.get("payment_method")
    payment_method = await get_payment_method_by_method(payment_method)

    try:
        cost_rub = int(message.text)  # RUB

        if cost_rub < payment_method.min or (payment_method.max and cost_rub > payment_method.max):
            raise ValueError("Error!")

        cost_usd = get_current_usd_from_rub(cost_rub)
        cost_cents = get_cents_from_usd(cost_usd)

        wait_comment = str(randrange(100000, 999999))

        new_payment = await Payment(
            user_id=message.from_user.id,
            payment_method=payment_method.method,
            cost_rub=cost_rub,
            cost=cost_cents,
            status="waiting",
            wait_comment=wait_comment
        ).create()

        if payment_method.method == 'qiwi':
            markup = await qiwi_transaction_keyboard(user_id=message.from_user.id, payment=new_payment)
            await message.answer(
                text=f"Для пополнения счета, переведите средства на QIWI по след. реквизитам: \n\n"
                     f"Никнейм: <b>{QIWI_NICKNAME}</b>\n"
                     f"Сумма: <b>{cost_rub} RUB</b>\n"
                     f"Комментарий: <i><b>{wait_comment}</b></i>\n\n"
                     f"Перевод делайте по никнейму! Для пополнения по номеру телефона обратитесь в поддержку\n"
                     f"<b>Обязательно</b> указать комментарий к переводу. "
                     f"При случае, если комментарий не будет указан, средства будут потеряны!\n"
                     f"После оплаты не забудьте нажать кнопку «Проверить оплату»",
                reply_markup=markup
            )
        else:
            await message.answer("Неа :(")

        await state.reset_state()

    except ValueError:
        await message.answer("Допустимы только <b>целые</b> числа! \n"
                             "Либо число за рамками <b>минимума</b> и <b>максимума</b>\n")
        await state.reset_state()

    except Exception:
        await message.answer("Ошибка, попробуйте заново!")
        await state.reset_state()


@dp.callback_query_handler(check_payment.filter())
async def check_payment(call: CallbackQuery, callback_data: dict):
    payment_method = callback_data.get('method')
    payment_id = callback_data.get('payment')
    payment_item = await get_payment_with_id(payment_id)

    if payment_method == "qiwi":
        if payment_item.status == "waiting":
            check_payment_item = await check_qiwi_payment(payment_item)

            if check_payment_item:
                await payment_item.update(
                    status="success"
                ).apply()

                await call.message.edit_text(
                    text=f"Кошелёк успешно пополнен на сумму - "
                         f"<b>{get_usd_from_cents(payment_item.cost)} USD</b>",
                    reply_markup=None
                )
            else:
                await call.answer(text="Платеж не обнаружен либо находится в обработке!")
        elif payment_item.status == "cancelled":
            await call.answer(text="Истёк срок действия платежа!")
        elif payment_item.status == "success":
            await call.answer(text="Платеж уже совершен!")


@dp.callback_query_handler(cancel_payment.filter())
async def payment(call: CallbackQuery, callback_data: dict):
    payment_id = callback_data.get('payment_id')
    payment_item = await get_payment_with_id(payment_id)
    await payment_item.update(
        status="cancelled"
    ).apply()

    await call.message.edit_text('Оплата успешно отменена!', reply_markup=None)

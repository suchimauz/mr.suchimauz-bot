from sqlalchemy import sql, Column, func

from utils.db.database import db
from utils.db.models.payment import Payment
from utils.helpers import get_current_rub_from_usd, get_usd_from_cents


class Check(db.Model):
    __tablename__ = "checks"
    query: sql.Select

    id = Column(db.Integer, primary_key=True)
    cost = Column(db.Integer)  # cents
    status = Column(db.String)  # waiting, success
    created_date = Column(db.DateTime, server_default=func.now())


async def get_check(check_id) -> Check:
    check_id = int(check_id)

    check = await Check.query.where(Check.id == check_id).gino.first()

    return check


async def add_check(cost) -> Check:
    new_check = await Check(
        cost=cost,
        status="waiting"
    ).create()

    return new_check


async def activate_check_and_return_msg(user_id, check_id):
    try:
        check_id = int(check_id)

        check = await Check.query.where(Check.id == check_id).gino.first()

        if check.status == "waiting":
            cost_usd = get_usd_from_cents(check.cost)

            payment = await Payment(
                user_id=user_id,
                payment_method="check",
                cost=check.cost,
                cost_rub=get_current_rub_from_usd(cost_usd),
                status="success"
            ).create()

            await check.update(
                status="success"
            ).apply()

            return f"Баланс успешно пополнен на сумму: <b>{get_usd_from_cents(payment.cost)} USD</b>"

        else:
            return "<b><i>Чек не найден или уже использован</i></b>"

    except ValueError:
        return "<i>Ошибка с поиском чека. Напишите в поддержку</i>"

    except Exception:
        return "<i>Непредвиденная ошибка. Напишите в поддержку</i>"

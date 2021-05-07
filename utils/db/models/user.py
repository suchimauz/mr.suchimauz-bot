from sqlalchemy import sql, Column, and_

from utils.db.database import db
from utils.db.models.payment import Payment
from utils.db.models.transaction import Transaction
from utils.helpers import get_usd_from_cents


class User(db.Model):
    __tablename__ = "users"
    query: sql.Select

    id = Column(db.Integer, primary_key=True)
    username = Column(db.String(50))
    last_activity = Column(db.DateTime, nullable=True)


# Функция для получения юзера по айди
async def get_user(user_id) -> User:
    user = await User.query.where(User.id == user_id).gino.first()
    return user


# Функция для получения баланса юзера
async def get_user_balance(user_id):
    user = await User.query.where(User.id == user_id).gino.first()

    payment_conditions = [
        Payment.user_id == user.id,
        Payment.status == 'success'
    ]

    transaction_conditions = [
        Transaction.user_id == user.id,
        Transaction.status == 'success'
    ]

    payments_sum = await db.select([db.func.sum(Payment.cost)]).where(and_(*payment_conditions)).gino.scalar()
    transactions_sum = await db.select([db.func.sum(Transaction.cost)]).where(and_(*transaction_conditions)).gino.scalar()

    if payments_sum is None:
        payments_sum = 0
    if transactions_sum is None:
        transactions_sum = 0

    return get_usd_from_cents(payments_sum - transactions_sum)


# Функция для создания или обновления пользователя
async def add_user(**kwargs):
    user_id = kwargs.get('id')
    user = await get_user(user_id)

    if user is None:
        new_user = await User(**kwargs).create()
        return new_user

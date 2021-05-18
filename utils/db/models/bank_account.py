from datetime import datetime
from typing import List

from sqlalchemy import sql, Column, Sequence, UniqueConstraint, and_, func

from utils.db.database import db


class BankAccount(db.Model):
    __tablename__ = "bank_accounts"
    query: sql.Select

    id = Column(db.Integer, primary_key=True)
    product_type = Column(db.String)
    bank_name = Column(db.String)
    routing_number = Column(db.String)
    account_number = Column(db.String)
    full_name = Column(db.String, nullable=True)
    bank_address = Column(db.String, nullable=True)
    bank_type = Column(db.String)  # checking, savings
    bank_email = Column(db.String, nullable=True)
    bank_email_pass = Column(db.String, nullable=True)
    bank_login = Column(db.String, nullable=True)
    bank_password = Column(db.String, nullable=True)
    bank_zip = Column(db.String, nullable=True)
    status = Column(db.String)  # waiting, cancelled, success, wait-minik
    status_changed_by = Column(None, db.ForeignKey("users.id"), nullable=True)
    created_date = Column(db.DateTime, server_default=func.now())

    _routing_account = UniqueConstraint('product_type', 'routing_number', 'account_number')


async def get_ba_count_by_product(product, add_conditions=None):
    conditions = [
        BankAccount.product_type == product,
        BankAccount.status == 'waiting'
    ]

    if add_conditions is not None:
        conditions + add_conditions
    total = await db.select([db.func.count()]).where(
        and_(*conditions)
    ).gino.scalar()

    return total


async def update_purchased_ba(bank_accounts: List[BankAccount], user_id):
    return await BankAccount.update.values(
        status="success",
        status_changed_by=user_id
    ).where(
        BankAccount.id.in_(
            list(map(lambda ba: ba.id, bank_accounts))
        )
    ).gino.status()


async def get_available_ba_for_user(count) -> List[BankAccount]:
    return await BankAccount.query.where(BankAccount.status == "waiting")\
        .limit(count)\
        .order_by(BankAccount.created_date.desc())\
        .gino.all()

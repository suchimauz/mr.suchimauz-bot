from typing import List

from sqlalchemy import sql, Column

from utils.db.database import db


class PaymentMethod(db.Model):
    __tablename__ = "payment_methods"
    query: sql.Select

    method = Column(db.String, primary_key=True)
    name = Column(db.String)
    active = Column(db.Boolean)
    min = Column(db.Integer)  # RUB
    max = Column(db.Integer, nullable=True)  # RUB


async def get_active_payment_methods() -> List[PaymentMethod]:
    return await PaymentMethod.query.where(PaymentMethod.active == True).gino.all()


async def get_payment_method_by_method(method) -> PaymentMethod:
    return await PaymentMethod.query.where(PaymentMethod.method == method).gino.first()

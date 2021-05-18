from typing import List

from sqlalchemy import sql, Column

from utils.db.database import db


class Payment(db.Model):
    __tablename__ = "payments"
    query: sql.Select

    id = Column(db.Integer, primary_key=True)
    user_id = Column(None, db.ForeignKey("users.id"))
    payment_method = Column(db.String)
    cost = Column(db.Integer)  # cents
    cost_rub = Column(db.Integer)  # rub
    status = Column(db.String)  # waiting, success, failed, cancelled
    wait_comment = Column(db.String, nullable=True)
    created_date = Column(db.DateTime)


async def get_payment_with_id(payment_id) -> Payment:
    return await Payment.query.where(Payment.id == int(payment_id)).gino.first()


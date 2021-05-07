from sqlalchemy import sql, Column

from utils.db.database import db


class Transaction(db.Model):
    __tablename__ = "transactions"
    query: sql.Select

    id = Column(db.Integer, primary_key=True)
    user_id = Column(None, db.ForeignKey("users.id"))
    product_type = Column(db.String, nullable=True)
    count = Column(db.Integer, nullable=True)
    cost = Column(db.Integer)  # cents
    status = Column(db.String)  # cancelled, success, waiting
    created_date = Column(db.DateTime)
    updated_date = Column(db.DateTime, nullable=True)


async def get_transaction_by_id(transaction_id) -> Transaction:
    return await Transaction.query.where(Transaction.id == int(transaction_id)).gino.first()

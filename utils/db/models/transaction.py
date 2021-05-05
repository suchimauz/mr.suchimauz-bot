from sqlalchemy import sql, Column

from utils.db.database import db


class Transaction(db.Model):
    __tablename__ = "transactions"
    query: sql.Select

    id = Column(db.Integer, primary_key=True)
    username = Column(db.String(50))
    last_activity = Column(db.DateTime, nullable=True)
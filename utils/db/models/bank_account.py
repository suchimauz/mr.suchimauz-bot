from sqlalchemy import sql, Column, Sequence, UniqueConstraint

from utils.db.database import db


class BankAccount(db.Model):
    __tablename__ = "bank_accounts"
    query: sql.Select

    id = Column(db.Integer, primary_key=True)
    product_type = Column(db.String)
    bank_name = Column(db.String)
    routing_number = Column(db.String)
    account_number = Column(db.String)
    bank_address = Column(db.String, nullable=True)
    bank_type = Column(db.String)
    bank_email = Column(db.String, nullable=True)
    bank_email_pass = Column(db.String, nullable=True)
    bank_login = Column(db.String, nullable=True)
    bank_password = Column(db.String, nullable=True)

    _routing_account = UniqueConstraint('product_type', 'routing_number', 'account_number')

from sqlalchemy import sql, Column, UniqueConstraint

from utils.db.database import db


class Price(db.Model):
    __tablename__ = "prices"
    query: sql.Select

    user_id = Column(None, db.ForeignKey("users.id"))
    product_type = Column(db.String)
    price = Column(db.Integer)  # Cents
    whole_price = Column(db.Integer)

    _user_product = UniqueConstraint('user_id', 'product_type')

from sqlalchemy import sql, Column

from utils.db.database import db


class Product(db.Model):
    __tablename__ = "products"
    query: sql.Select

    type = Column(db.String, primary_key=True)
    category = Column(None, db.ForeignKey('products_categories.category'))
    name = Column(db.String(50))
    default_price = Column(db.Integer)

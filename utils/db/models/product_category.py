from typing import List

from sqlalchemy import sql, Column

from utils.db.database import db


class ProductCategory(db.Model):
    __tablename__ = "products_categories"
    query: sql.Select

    category = Column(db.String, primary_key=True)
    name = Column(db.String)


async def get_product_categories() -> List[ProductCategory]:
    return await ProductCategory.query.gino.all()
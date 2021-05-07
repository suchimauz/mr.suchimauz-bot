from typing import List

from sqlalchemy import sql, Column

from utils.db.database import db


class Product(db.Model):
    __tablename__ = "products"
    query: sql.Select

    type = Column(db.String, primary_key=True)
    category = Column(None, db.ForeignKey('products_categories.category'))
    name = Column(db.String(50))
    default_price = Column(db.Integer)
    whole_price = Column(db.Integer)  # >50

    async def get_default_price(self):
        return self.default_price

    async def get_whole_price(self):
        return self.whole_price

    async def get_price(self, count):
        default_price = await self.get_default_price()
        whole_price = await self.get_whole_price()

        if count <= 50:
            price = default_price * count
        else:
            price = whole_price * count

        return price

    async def get_price_text(self):
        default_price = await self.get_default_price()
        whole_price = await self.get_whole_price()

        return f"{default_price / 100}$ (от 50шт. - {whole_price / 100}$)"


async def get_products_by_category(category) -> List[Product]:
    return await Product.query.distinct(Product.type).where(Product.category == category).gino.all()


async def get_product_by_type(product_type) -> Product:
    return await Product.query.where(Product.type == product_type).gino.first()

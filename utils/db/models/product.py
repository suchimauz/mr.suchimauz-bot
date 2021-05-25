from typing import List

from sqlalchemy import sql, Column, and_

from utils.db.database import db
from utils.db.models.price import Price
from utils.helpers import get_usd_from_cents


class Product(db.Model):
    __tablename__ = "products"
    query: sql.Select

    type = Column(db.String, primary_key=True)
    category = Column(None, db.ForeignKey('products_categories.category'))
    name = Column(db.String(50))
    default_price = Column(db.Integer)
    whole_price = Column(db.Integer)  # >50

    async def get_default_price(self, user_id=None):
        default_price = self.default_price

        if user_id:
            user_id = int(user_id)

            conditions = [
                Price.product_type == self.type,
                Price.user_id == user_id
            ]

            price = await Price.query.where(and_(*conditions)).gino.first()

            if price:
                default_price = price.price

        return default_price

    async def get_whole_price(self, user_id=None):
        whole_price = self.whole_price

        if user_id:
            user_id = int(user_id)

            conditions = [
                Price.product_type == self.type,
                Price.user_id == user_id
            ]

            price = await Price.query.where(and_(*conditions)).gino.first()

            if price:
                whole_price = price.whole_price

        return whole_price

    async def get_price(self, count, user_id=None):
        default_price = await self.get_default_price(user_id)
        whole_price = await self.get_whole_price(user_id)

        if count < 50:
            price = default_price * count
        else:
            price = whole_price * count

        return price

    async def get_price_text(self, user_id=None):
        default_price = await self.get_default_price(user_id)
        whole_price = await self.get_whole_price(user_id)

        return f"{get_usd_from_cents(default_price)}$ (от 50шт. - {get_usd_from_cents(whole_price)}$)"


async def get_products(limit=100, offset=0) -> List[Product]:
    return await Product.query.limit(limit).offset(offset).gino.all()


async def get_product_count():
    return await db.select([db.func.count(Product.type)]).gino.scalar()


async def get_products_by_category(category) -> List[Product]:
    return await Product.query.distinct(Product.type).where(Product.category == category).gino.all()


async def get_product_by_type(product_type) -> Product:
    return await Product.query.where(Product.type == product_type).gino.first()

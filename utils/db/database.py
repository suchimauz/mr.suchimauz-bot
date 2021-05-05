from gino import Gino
from gino.schema import GinoSchemaVisitor

from data.config import POSTGRES_URI

db = Gino()

ba_products = [
    {
        "type": "schwab",
        "name": "Charles Schwab",
        "default_price": 100,  # Cents
        "category": "bank_account"
    },
]

product_categories = [
    {
        "category": "bank_account",
        "name": "Банковские Аккаунты"
    }
]


async def create_or_replace_categories_and_ba():
    from utils.db.models.product_category import ProductCategory
    from utils.db.models.product import Product

    await Product.delete.gino.status()
    await ProductCategory.delete.gino.status()

    for product_category in product_categories:
        await ProductCategory(
            category=product_category['category'],
            name=product_category['name']
        ).create()

    for ba_product in ba_products:
        await Product(
            type=ba_product['type'],
            category=ba_product['category'],
            name=ba_product['name'],
            default_price=ba_product['default_price']
        ).create()


async def create_db():
    await db.set_bind(POSTGRES_URI)
    db.gino: GinoSchemaVisitor

    await db.gino.create_all()
    await create_or_replace_categories_and_ba()

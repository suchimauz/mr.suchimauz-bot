from gino import Gino
from gino.schema import GinoSchemaVisitor

from data.config import POSTGRES_URI

db = Gino()

ba_products = [
    {
        "type": "schwab",
        "name": "Charles Schwab",
        "default_price": 150,  # Cents
        "whole_price": 140,
        "category": "bank_account"
    },
]

product_categories = [
    {
        "category": "bank_account",
        "name": "🏦 Банковские Аккаунты"
    }
]

payment_methods = [
    {
        "method": "qiwi",
        "name": "Qiwi (RUB)",
        "active": True,
        "min": 200,
        "max": 40000,
    },
    {
        "method": "crypto",
        "name": "Криптовалюта",
        "active": False,
        "min": 0,
        "max": None
    },
    {
        "method": "yandex",
        "name": "Яндекс.Деньги / Банковская карта",
        "active": False,
        "min": 100,
        "max": None
    },
]


async def create_or_replace_categories_and_ba():
    from utils.db.models.product_category import ProductCategory
    from utils.db.models.product import Product
    from utils.db.models.payment_method import PaymentMethod

    await Product.delete.gino.status()
    await ProductCategory.delete.gino.status()
    await PaymentMethod.delete.gino.status()

    for payment_method in payment_methods:
        await PaymentMethod(
            method=payment_method['method'],
            name=payment_method['name'],
            active=payment_method['active'],
            min=payment_method['min'],
            max=payment_method['max'],
        ).create()

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
            default_price=ba_product['default_price'],
            whole_price=ba_product['whole_price']
        ).create()


async def create_db():
    await db.set_bind(POSTGRES_URI)
    db.gino: GinoSchemaVisitor

    await db.gino.create_all()
    await create_or_replace_categories_and_ba()

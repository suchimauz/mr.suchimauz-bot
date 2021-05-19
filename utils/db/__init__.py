from .database import db
from .models.user import db
from .models.product_category import db
from .models.product import db
from .models.price import db
from .models.bank_account import db
from .models.transaction import db
from .models.payment_method import db
from .models.check import db
from .models.mail import db

__all__ = ["db"]

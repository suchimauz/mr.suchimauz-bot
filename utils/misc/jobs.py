from gino import Gino
from gino.schema import GinoSchemaVisitor
from sqlalchemy import and_

from data.config import POSTGRES_URI
from utils.db.models.bank_account import BankAccount
from datetime import datetime, timedelta
import time


async def cancel_bank_accounts():
    db = Gino()
    await db.set_bind(POSTGRES_URI)

    while True:
        query = db.text(
            "UPDATE bank_accounts SET status = 'cancelled' "
            "WHERE created_date < (CURRENT_TIMESTAMP + '-4 hours') and "
            "status = 'waiting'"
        )

        await db.status(query)

        time.sleep(600)

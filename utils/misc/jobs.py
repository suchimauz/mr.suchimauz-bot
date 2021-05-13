from gino import Gino
from gino.schema import GinoSchemaVisitor
from sqlalchemy import and_

from data.config import POSTGRES_URI
from utils.db.models.bank_account import BankAccount
from datetime import datetime, timedelta
import time


async def send_report_transactions():
    db = Gino()
    await db.set_bind(POSTGRES_URI)

    query = db.text(
        "SELECT u.username"
        ", SUM(t.cost) cost_usd"
        ", sum(t.count) count"
        ", ("
        "   SELECT SUM(cost) "
        "   FROM transactions t "
        "   JOIN users u "
        "   on u.id = t.user_id "
        "   JOIN products p "
        "   ON p.type = t.product_type "
        "   WHERE t.status = 'success' "
        "   AND t.created_date > CURRENT_TIMESTAMP + '-24 hour' "
        "   AND u.username <> 'suchimauz'"
        ") all_cost "
        "FROM transactions t "
        "JOIN users u "
        "ON u.id = t.user_id "
        "JOIN products p "
        "ON p.type = t.product_type "
        "WHERE t.status = 'success' "
        "AND t.created_date > CURRENT_TIMESTAMP + '-24 hour' "
        "AND u.username <> 'suchimauz' "
        "GROUP BY u.id"
    )

    result = await db.all(query)
    print(result)


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

import quopri
import re

from gino import Gino
import imaplib
from data.config import POSTGRES_URI
import time
import email

from loader import bot
from utils.db.models.mail import get_mail_by_email


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


async def check_schwab_miniks():
    db = Gino()
    await db.set_bind(POSTGRES_URI)

    query = db.text(
        "SELECT bank_email AS email, account_number, status_changed_by, id AS user_id "
        "FROM bank_accounts "
        "WHERE status = 'wait-minik'"
    )

    result = await db.all(query)

    for mail_array in result:
        account_number = mail_array[1]
        user_id = mail_array[2]
        bank_account_id = mail_array[3]

        mail = await get_mail_by_email(mail_array[0])

        imap = imaplib.IMAP4_SSL('imap.mail.ru')
        imap.login(mail.email, mail.password)
        imap.list()
        imap.select()
        result, data = imap.search(None, 'ALL')

        for uid in data[0].split():
            result, data = imap.fetch(uid, '(BODY.PEEK[HEADER.FIELDS (SUBJECT)])')
            if "Direct Deposit posted to your account" in data[0][1].decode():
                result, data = imap.fetch(uid, '(BODY[TEXT])')

                account_last_3_numbers = re.search(
                    'your account ending: <b>(.*)</b>',
                    data[0][1].decode()
                ).groups()[0]

                minik = re.search(
                    'A Direct Deposit for\s+(.*)\s+has posted to your',
                    data[0][1].decode()
                ).groups()[0]

                if account_number.endswith(account_last_3_numbers):
                    await bot.send_message(
                        chat_id=user_id,
                        text=f"Deposit for account {account_number}: <b>{minik}</b>"
                    )

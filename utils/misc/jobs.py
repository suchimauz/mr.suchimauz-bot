import quopri
import re

from aiogram import Bot, types
from gino import Gino
import imaplib

from data import config
from data.config import POSTGRES_URI
import time
import email

from loader import bot
from utils.db.models.bank_account import get_bank_account_by_id, BankAccount
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


async def check_minik(db, bot, imap, user_id, account_number, uid, bank_account_id):
    result, data = imap.fetch(uid, '(BODY.PEEK[HEADER.FIELDS (SUBJECT)])')
    print(data[0][1].decode())
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
                text=f"<i><b>Charles Schwab:</b></i> Deposit for account {account_number}: <b>{minik}</b>"
            )

            await db.status(
                db.text(
                    f"UPDATE bank_accounts SET status='success' "
                    f"WHERE id = {int(bank_account_id)}"
                )
            )


async def check_schwab_miniks():
    db = Gino()
    await db.set_bind(POSTGRES_URI)

    while True:
        bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
        query = db.text(
            "SELECT bank_email AS email, account_number, status_changed_by, id AS user_id "
            "FROM bank_accounts "
            "WHERE status = 'wait-minik' "
        )

        result = await db.all(query)
        for mail_array in result:
            login = mail_array[0]
            account_number = mail_array[1]
            user_id = mail_array[2]
            bank_account_id = mail_array[3]

            mail = await db.first(
                db.text(
                    f"SELECT password FROM mails "
                    f"WHERE email = '{login}'"
                )
            )

            password = mail[0]

            imap = imaplib.IMAP4_SSL('imap.mail.ru')
            imap.login(login, password)

            imap.list()
            imap.select()
            r1, inbox = imap.search(None, 'ALL')

            for uid in inbox[0].split():
                await check_minik(db, bot, imap, user_id, account_number, uid, bank_account_id)

            imap.list()
            imap.select("&BCEEPwQwBDw-")
            r2, spam = imap.search(None, 'ALL')

            for uid in spam[0].split():
                await check_minik(db, bot, imap, user_id, account_number, uid, bank_account_id)

        time.sleep(10800)

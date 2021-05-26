import os
import quopri
import re
from pprint import pprint

from aiogram import Bot, types
from gino import Gino
import imaplib
import httplib2
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import UserAccessTokenCredentials

from data import config
from data.config import POSTGRES_URI, ROOT_DIR, SPREADSHEET_ID, BROTHERS
import time
import email

from loader import bot
from utils.db.models.bank_account import get_bank_account_by_id, BankAccount
from utils.db.models.mail import get_mail_by_email
from utils.helpers import get_usd_from_cents


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
            "WHERE created_date < (CURRENT_TIMESTAMP + '-8 hours') and "
            "status = 'waiting'"
        )

        await db.status(query)

        time.sleep(600)


async def check_minik(db, bot, imap, user_id, account_number, uid, bank_account_id):
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

        print(account_last_3_numbers)
        print(account_number)

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
            "AND created_date < (CURRENT_TIMESTAMP + '-10 hour')"
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

        time.sleep(7200)


async def update_brothers_cost_sheet():
    try:
        CREDENTIALS_FILE = os.path.join(ROOT_DIR, 'token.json')
        spreadsheet_id = SPREADSHEET_ID

        credentials = Credentials.from_service_account_file(CREDENTIALS_FILE)
        service = build('sheets', 'v4', credentials=credentials)

        db = Gino()
        await db.set_bind(POSTGRES_URI)

        while True:
            data = []
            for brother in BROTHERS:
                query = db.text(
                    f"SELECT sum(t.cost) "
                    f"FROM referrals r "
                    f"JOIN users u "
                    f"ON u.id = r.user_id "
                    f"JOIN transactions t "
                    f"ON t.user_id = u.id "
                    f"WHERE r.referrer_id = {int(brother['id'])}"
                )
                result = await db.first(query)
                if result[0]:
                    cost = result[0]
                else:
                    cost = 0

                data.append(
                    {
                        "range": f"{brother['column']}3",
                        "values": [[get_usd_from_cents(cost)]]
                    }
                )

            service.spreadsheets().values().batchUpdate(
                spreadsheetId=spreadsheet_id,
                body={
                    "valueInputOption": "USER_ENTERED",
                    "data": data
                }
            ).execute()

            time.sleep(10)
    except FileNotFoundError:
        print("token.json not found")
    except Exception as e:
        print(e)
        pass

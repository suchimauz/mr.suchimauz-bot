import asyncio
import threading
from hashlib import sha256

from aiogram import executor

from handlers import dp
from utils.misc.jobs import cancel_bank_accounts, send_report_transactions, check_schwab_miniks
from utils.notify_admins import on_startup_notify
from utils.db.database import create_db


async def on_startup(dispatcher):
    # Уведомляет про запуск
    await on_startup_notify(dispatcher)

    await create_db()

    await send_report_transactions()

    _thread = threading.Thread(target=asyncio.run, args=(cancel_bank_accounts(),))
    _thread.start()

    _thread = threading.Thread(target=asyncio.run, args=(check_schwab_miniks(),))
    _thread.start()


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)


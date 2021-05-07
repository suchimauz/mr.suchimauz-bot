import asyncio
import threading

from aiogram import executor

from handlers import dp
from utils.helpers import get_current_rub_from_usd, get_cents_from_usd
from utils.misc.jobs import cancel_bank_accounts
from utils.notify_admins import on_startup_notify
from utils.db.database import create_db
from utils.payments.qiwi import payment_history_last


async def on_startup(dispatcher):
    # Уведомляет про запуск
    await on_startup_notify(dispatcher)
    _thread = threading.Thread(target=asyncio.run, args=(cancel_bank_accounts(),))
    _thread.start()

    await create_db()


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)

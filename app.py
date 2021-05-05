from aiogram import executor

from handlers import dp
from utils.notify_admins import on_startup_notify
from utils.db.database import create_db


async def on_startup(dispatcher):
    # Уведомляет про запуск
    await on_startup_notify(dispatcher)
    await create_db()


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)

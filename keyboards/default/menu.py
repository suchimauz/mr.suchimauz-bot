from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🛒 Магазин")
        ],
        [
            KeyboardButton(text="🔒 Личный кабинет"),
            KeyboardButton(text="💵 Пополнить")
        ],
        [
            KeyboardButton(text="☎️ Поддержка"),
            KeyboardButton(text="📕 Правила")
        ]
    ],
    resize_keyboard=True
)
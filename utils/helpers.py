import requests
from aiogram.types import InlineKeyboardMarkup

from data.config import ADMINS


def is_admin(user_id):
    return str(user_id) in ADMINS


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def get_current_rub_from_usd(usd):
    if usd > 0:
        request = requests.get("https://www.cbr-xml-daily.ru/latest.js")
        response = request.json()

        usd_multiplier = response['rates']['USD']

        rub = usd / usd_multiplier

        return round(rub)
    else:
        return 0


def get_current_usd_from_rub(rub):
    request = requests.get("https://www.cbr-xml-daily.ru/latest.js")
    response = request.json()

    usd_multiplier = response['rates']['USD']

    usd = rub * usd_multiplier

    return round(usd, 1)


def get_cents_from_usd(usd):
    cents = usd * 100

    return round(cents)


def get_usd_from_cents(cents):
    if cents > 0:
        usd = cents / 100

        return round(usd, 2)
    else:
        return 0

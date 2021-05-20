import requests
from data.config import QIWI_API_TOKEN, QIWI_NUMBER
from datetime import timedelta, datetime
import pytz


# История платежей - последние и следующие n платежей
from utils.db.models.payment import Payment


def payment_history_last(next_TxnId=None, next_TxnDate=None):
    tz = pytz.timezone('Europe/Moscow')
    now_date = datetime.now(tz)
    login = QIWI_NUMBER

    endDate = now_date
    startDate = now_date - timedelta(hours=5)

    s = requests.Session()
    s.headers['authorization'] = 'Bearer ' + QIWI_API_TOKEN
    parameters = {
        'startDate': startDate.strftime("%Y-%m-%dT%H:%M:%S+03:00"),
        'endDate': endDate.strftime("%Y-%m-%dT%H:%M:%S+03:00"),
        'rows': 10,
        'operation': 'IN',
        'nextTxnId': next_TxnId,
        'nextTxnDate': next_TxnDate
    }
    h = s.get('https://edge.qiwi.com/payment-history/v2/persons/' + login + '/payments', params=parameters)
    return h.json()


async def check_qiwi_payment(payment: Payment):
    next_TxnId = None
    next_TxnDate = None
    payment_success = False
    result = payment_history_last(next_TxnId=next_TxnId, next_TxnDate=next_TxnDate)

    while True:
        next_TxnId = result['nextTxnId']
        next_TxnDate = result['nextTxnDate']
        data = result['data']

        for data_item in data:
            data_item_status = data_item['status']
            data_item_cost_amount = data_item['sum']['amount']
            data_item_cost_currency = data_item['sum']['currency']
            data_item_comment = data_item['comment']

            if data_item_status == "SUCCESS" and data_item_cost_amount == payment.cost_rub and data_item_comment == payment.wait_comment and data_item_cost_currency == 643:
                payment_success = True
                break

        if not next_TxnId:
            break

        result = payment_history_last(next_TxnId=next_TxnId, next_TxnDate=next_TxnDate)

    return payment_success

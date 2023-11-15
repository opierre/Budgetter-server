import datetime
from pprint import pprint

from channels.layers import get_channel_layer
from django.db.models import Sum
from django.dispatch import Signal

from dashboard.models import Transaction, Type

channel_layer = get_channel_layer()

transactions_created = Signal()


def transaction_post_save(**kwargs):
    """
    Callback after transactions creation

    :param kwargs: kwargs
    :return: None
    """

    today = datetime.date.today()
    ws_data = {
        "spending": {}
    }

    for month in range(today.month-5, today.month+1):
        amount = Transaction.objects.filter(
            date__lte=f"{today.year}-{month}-01",
            date__gte=f"{today.year}-{month - 1}-01",
            transaction_type=Type.EXPENSES).aggregate(Sum("amount"))
        ws_data.get("spending").update({
            str(month): amount.get("amount__sum") if amount is not None else 0
        })

    pprint(ws_data)


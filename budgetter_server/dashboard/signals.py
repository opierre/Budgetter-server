import datetime
from calendar import monthrange
from pprint import pprint

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models import Sum
from django.dispatch import Signal

from dashboard.models import Transaction, Type, Account, Status

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
        "accounts": {},
        "spending": {}
    }

    # Build spending data
    start_month = (today.month - 5) % 12
    end_month = (today.month + 1) % 12
    for month in range(start_month, end_month):
        amount = Transaction.objects.filter(
            date__lte=f"{today.year}-{month:02d}-{monthrange(today.year, month)[1]}",
            date__gte=f"{today.year}-{month:02d}-01",
            transaction_type=Type.EXPENSES).aggregate(Sum("amount"))
        amount_dec = amount.get("amount__sum")
        ws_data.get("spending").update({
            str(month): float(amount_dec) if amount_dec is not None else 0.0
        })

    # Build balance data
    accounts = Account.objects.filter(
            status=Status.ACTIVE
    )
    for account in accounts:
        # Check tendency against last month
        # account

        ws_data.get("accounts").update({
            account.name: {
                "balance": account.amount
            }
        })

    pprint(ws_data)

    # Send data on web socket
    async_to_sync(channel_layer.group_send)(
        "debug_dashboard",
        {
            "type": "chat.message",
            "data": ws_data
        }
    )

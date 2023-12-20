import datetime
from calendar import monthrange
from pprint import pprint

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
    for month in range(today.month-5, today.month+1):
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
        account

        ws_data.get("accounts").update({
            account.name: {
                "balance": account.amount
            }
        })


    pprint(ws_data)


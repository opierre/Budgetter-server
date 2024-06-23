import datetime
from calendar import monthrange
from pprint import pprint

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models import Sum, Count
from django.dispatch import Signal

from dashboard.models import Transaction, Type, Account, Status
from dashboard.utils import update_monthly_combined_balances

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
        "spending": {},
        "distribution": {},
        "savings": {}
    }

    # ---------------
    # Build spending data
    # ---------------
    start_month = (today.month - 6) % 13
    end_month = (today.month + 1) % 13
    current_year = today.year - 1 if start_month >= end_month else today.year
    current_month = start_month
    for _ in range(1, 7):
        # Handle start/end month reset for year
        if current_month % 13 == 0:
            current_month = 1
            current_year = today.year
        current_month_name = datetime.date(1900, current_month, 1).strftime('%B')

        # Retrieve all transactions according to date
        transactions = Transaction.objects.filter(
            date__lte=f"{current_year}-{current_month:02d}-{monthrange(current_year, current_month)[1]}",
            date__gte=f"{current_year}-{current_month:02d}-01",
            transaction_type=Type.EXPENSES)
        amount = transactions.aggregate(Sum("amount"))
        amount_dec = amount.get("amount__sum")

        # TODO: Retrieve top five recurrent categories within this date range
        # top_categories = (
        #     transactions.values('category__name')
        #     .annotate(transaction_count=Count('category'))
        #     .order_by('-transaction_count')
        # )

        # Build spending
        ws_data.get("spending").update({
            current_month_name: float(amount_dec) if amount_dec is not None else 0.0
        })

        # Build expenses distribution
        # ws_data.get("spending").update({
        #     current_month_name: float(amount_dec) if amount_dec is not None else 0.0
        # })

        current_month += 1

    # ---------------
    # Build last 12 months savings
    # ---------------
    months_savings = update_monthly_combined_balances()
    ws_data.get("savings").update(months_savings)

    # ---------------
    # Build balance data
    # ---------------
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

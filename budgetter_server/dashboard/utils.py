from django.db.models import Sum
from datetime import datetime, timedelta, date
from .models import Transaction, MonthlyCombinedBalance, TransactionType


def update_monthly_combined_balances() -> dict:
    """
    Update monthly combined balances for all accounts

    :return: last 12 months state
    """

    updated_months = {}
    today = datetime.today()

    # Loop through the last 12 months
    for month_index in range(12):
        # Calculate the target date for each month in the last twelve months
        target_date = (today.replace(day=1) - timedelta(days=month_index * 30)).replace(day=1)

        year = target_date.year
        current_month = target_date.month

        start_date = datetime(year, current_month, 1)
        end_date = (start_date + timedelta(days=32)).replace(day=1) - timedelta(days=1)

        # Fetch all transactions up to the end of the specified month
        transactions = Transaction.objects.filter(date__gte=start_date, date__lte=end_date)

        # Calculate the total amount of all transactions
        total_amount_income = transactions.filter(transaction_type=TransactionType.INCOME).aggregate(Sum('amount'))[
                                  'amount__sum'] or 0.0
        total_amount_expenses = transactions.filter(transaction_type=TransactionType.EXPENSES).aggregate(Sum('amount'))[
                                    'amount__sum'] or 0.0

        # Store the combined balance in the database
        current_month_combined = MonthlyCombinedBalance.objects.update_or_create(
            year=year,
            month=current_month,
            balance=total_amount_income-total_amount_expenses
        )

        # Update result
        current_month_name = date(1900, current_month, 1).strftime('%B')
        updated_months.update(
            {
                f"{current_month_name} {year}": float(current_month_combined[0].balance)
            }
        )

    print("Monthly combined balances for the last 12 months have been updated.")
    return updated_months

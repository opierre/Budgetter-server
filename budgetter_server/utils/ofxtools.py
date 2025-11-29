import io
import re
from datetime import datetime

import pytz
from asgiref.sync import async_to_sync
from django.core.files.uploadedfile import UploadedFile
from django.db import close_old_connections, connection
from ofxtools import OFXTree
from ofxtools.models import CCSTMTRS, STMTRS

from dashboard.models import Mean, TransactionType, Account, Bank, Transaction


def import_ofx_to_database(ofx_file: UploadedFile) -> None:
    """
    Convert OFX file to models

    :param ofx_file: OFX file
    :return: None
    """

    # Close previous connections to make it threadsafe
    close_old_connections()

    content = io.BytesIO(ofx_file.read())

    # Convert to OFX tree for parsing
    ofx_parser = OFXTree()
    ofx_parser.parse(content)
    ofx = ofx_parser.convert()

    utc_timezone = pytz.UTC
    start_date = utc_timezone.localize(datetime.max)
    end_date = utc_timezone.localize(datetime.min)
    bank_id = ""

    account_created_count = 0
    transactions_created_count = 0

    for statement in ofx.statements:
        if bank_id == "" and isinstance(statement, STMTRS):
            bank_id = statement.account.bankid

        # Create account info
        account_inst, account_created = Account.objects.get_or_create(
            account_id=statement.account.acctid,
            bank=Bank.objects.filter(bic__contains=bank_id).first(),
            amount=float(statement.balance.balamt),
            last_update=statement.balance.dtasof.strftime("%Y-%m-%d"),
        )

        # Update occurrence
        account_created_count += 1 if account_created is True else 0

        # Update start date / end date of import
        if statement.transactions.dtstart < start_date:
            start_date = statement.transactions.dtstart
        if statement.transactions.dtend > end_date:
            end_date = statement.transactions.dtend

        # Parse transactions
        exclude_pattern_cb = r"^PRELEVEMENT CARTE DEPENSES CARTE \w{4} AU \d{2}/\d{2}/\d{2}$"

        for transaction in statement.transactions:
            # TODO: fix generic term for internal transaction
            if "VIREMENT EN VOTRE FAVEUR DE OLIVIER PIERRE" in transaction.memo:
                transaction_type = TransactionType.INTERNAL.value
                transaction_mean = Mean.TRANSFER.value
            elif re.match(exclude_pattern_cb, transaction.memo):
                print(transaction.memo)
                continue
            elif float(transaction.trnamt) < 0:
                transaction_type = TransactionType.EXPENSES.value
                transaction_mean = Mean.CARD.value
            else:
                transaction_type = TransactionType.INCOME.value
                transaction_mean = Mean.CARD.value

            # Create transaction and send signal
            transaction_inst, transaction_created = Transaction.objects.get_or_create(
                name=transaction.name,
                amount=abs(float(transaction.trnamt)),
                date=transaction.dtposted.strftime("%Y-%m-%d"),
                account=account_inst,
                comment=transaction.memo,
                mean=transaction_mean,
                transaction_type=transaction_type,
                reference=transaction.fitid,
            )

            # Update occurrence
            transactions_created_count += 1 if transaction_created is True else 0

    # Clean up database connections
    connection.close()

    # Send completed info on web socket
    async_to_sync(channel_layer.group_send)(
        "debug_budgetter",
        {
            "type": "chat.message",
            "data": {
                "function_completed": "import_ofx_to_database",
                "result": {
                    "accounts_created": account_created_count,
                    "transaction_created": transactions_created_count,
                    "start_date": start_date.strftime("%d-%m-%Y"),
                    "end_date": end_date.strftime("%d-%m-%Y")
                }
            }
        }
    )

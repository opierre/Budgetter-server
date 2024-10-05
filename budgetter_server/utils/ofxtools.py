import io
import re
from datetime import datetime

import pytz
from django.core.files.uploadedfile import UploadedFile
from django.db import close_old_connections, connection
from ofxtools import OFXTree
from ofxtools.models import CCSTMTRS, STMTRS

from dashboard.models import Mean, TransactionType, Account, Bank, Transaction
from dashboard.signals import transactions_created


def convert_ofx_to_json(ofx_file: UploadedFile) -> None:
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

    data = {"transactions": []}
    header = {
        "count": 0,
        "accounts": [],
        "start_date": utc_timezone.localize(datetime.max),
        "end_date": utc_timezone.localize(datetime.min),
    }
    bank_id = ""

    for statement in ofx.statements:
        if bank_id == "" and isinstance(statement, STMTRS):
            bank_id = statement.account.bankid

        # Get account info
        account = {
            "account_id": statement.account.acctid,
            "account_type": "CREDIT CARD"
            if isinstance(statement, CCSTMTRS)
            else statement.account.accttype,
            "amount": float(statement.balance.balamt),
            "last_update": statement.balance.dtasof.strftime("%Y-%m-%d"),
            "bank_id": bank_id,
        }
        account_inst, _ = Account.objects.get_or_create(
            account_id=statement.account.acctid,
            bank=Bank.objects.filter(bic__contains=bank_id).first(),
            amount=float(statement.balance.balamt),
            last_update=statement.balance.dtasof.strftime("%Y-%m-%d"),
        )

        # Update header
        header.update({"count": header.get("count") + len(statement.transactions)})
        header.get("accounts").append(account)
        if statement.transactions.dtstart < header.get("start_date"):
            header.update({"start_date": statement.transactions.dtstart})
        if statement.transactions.dtend > header.get("end_date"):
            header.update({"end_date": statement.transactions.dtend})

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
            data.get("transactions").append(
                {
                    "name": transaction.name,
                    "amount": abs(float(transaction.trnamt)),
                    "transaction_type": transaction_type,
                    "date": transaction.dtposted.strftime("%Y-%m-%d"),
                    "comment": transaction.memo,
                    "mean": transaction_mean,
                    "account": account,
                    "reference": transaction.fitid,
                }
            )
            transaction_inst, _ = Transaction.objects.get_or_create(
                name=transaction.name,
                amount=abs(float(transaction.trnamt)),
                date=transaction.dtposted.strftime("%Y-%m-%d"),
                account=account_inst,
                comment=transaction.memo,
                mean=transaction_mean,
                transaction_type=transaction_type,
                reference=transaction.fitid,
            )
            transactions_created.send(transaction_inst.__class__)

    # Clean up database connections
    connection.close()

    # Order transactions by date
    data.update(
        {
            "transactions": list(
                reversed(
                    sorted(
                        data.get("transactions"), key=lambda value: value.get("date")
                    )
                )
            )
        }
    )

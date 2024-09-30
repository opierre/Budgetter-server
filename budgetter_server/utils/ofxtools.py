import io
import os.path
import re
from datetime import datetime
from typing import Tuple

import pytz
from django.core.files.uploadedfile import UploadedFile
from ofxtools import OFXTree
from ofxtools.models import CCSTMTRS, STMTRS

from dashboard.models import Mean, Type, Account, Bank


def convert_ofx_to_json(ofx_file: UploadedFile) -> Tuple[dict, dict, str]:
    """
    Convert OFX file to models

    :param ofx_file: OFX file
    :return: converted data as JSON, header with global info, error message
    """

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
        Account.objects.get_or_create(
            name=,
            account_id=statement.account.acctid,
            bank =Bank.objects.filter(bic=bank_id),
            amount =float(statement.balance.balamt),
            last_update=,
            status =,
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
                transaction_type = Type.INTERNAL.value
                transaction_mean = Mean.TRANSFER.value
            elif re.match(exclude_pattern_cb, transaction.memo):
                print(transaction.memo)
                continue
            elif float(transaction.trnamt) < 0:
                transaction_type = Type.EXPENSES.value
                transaction_mean = Mean.CARD.value
            else:
                transaction_type = Type.INCOME.value
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

    return header, data, ""

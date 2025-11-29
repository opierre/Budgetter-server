from ofxtools.Parser import OFXTree
from decimal import Decimal
import datetime

def parse_ofx(file_obj) -> list[dict]:
    """
    Parses an OFX file and returns a list of transactions.
    """
    parser = OFXTree()
    parser.parse(file_obj)
    ofx = parser.convert()
    
    parsed_data = []
    
    if not ofx.statements:
        return parsed_data

    for stmt in ofx.statements:
        account_data = {
            'account_id': getattr(stmt.account, 'acctid', None),
            'bank_id': getattr(stmt.account, 'bankid', None),
            'account_type': getattr(stmt.account, 'accttype', None),
            'currency': stmt.curdef,
            'balance': getattr(stmt.ledgerbal, 'balamt', None),
            'balance_date': getattr(stmt.ledgerbal, 'dtasof', None),
            'transactions': []
        }
        
        # Retrieve transactions
        txns = stmt.transactions
        
        for txn in txns:
            # Extract relevant fields
            transaction_data = {
                'amount': txn.trnamt,
                'date': txn.dtposted.date(),
                'name': txn.name or txn.memo or "Unknown",
                'reference': txn.fitid,
                'transaction_type': txn.trntype,
                'memo': txn.memo,
                'account_id': account_data['account_id']
            }
            account_data['transactions'].append(transaction_data)
            
        parsed_data.append(account_data)
            
    return parsed_data

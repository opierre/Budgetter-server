import re
from dashboard.models import CategorizationRule, TransactionType
from typing import Optional
from dashboard.models import Category

def categorize_transaction(transaction_data: dict, ai_categorizer=None) -> Optional[Category]:
    """
    Categorizes a transaction based on defined rules or AI.
    Priority: Rules → AI

    Args:
        transaction_data: Dictionary containing transaction data.
        ai_categorizer: Optional AI categorizer instance.
    Returns:
        Category object or None.
    """
    name = (transaction_data.get('name') or '').lower()
    memo = (transaction_data.get('memo') or '').lower()
    
    # Check rules first (highest priority)
    rules = CategorizationRule.objects.all()
    for rule in rules:
        if rule.matches(name, memo):
            # If transaction type is specified in rule, verify it matches
            if rule.transaction_type:
                txn_type = transaction_data.get('transaction_type')
                if txn_type and txn_type != rule.transaction_type:
                    continue
            return rule.category
            
    # If no rule matched, try AI if provided (second priority)
    if ai_categorizer:
        try:
            predicted_category = ai_categorizer.predict(
                transaction_data.get('name', ''),
                transaction_data.get('memo', '')
            )
            if predicted_category:
                return predicted_category
        except Exception:
            pass
            
    return None

# -*- coding: utf-8 -*-
"""Transaction domain"""


class Transaction:
    def __init__(self,
                 transaction_id: str,
                 account_id: str,
                 amount: float,
                 transaction_type: str):
        self.transaction_id: str = transaction_id
        self.account_id: str = account_id
        self.amount: float = amount
        self.transaction_type: str = transaction_type

# -*- coding: utf-8 -*-
"""Account domain"""


class Account:
    def __init__(
            self,
            account_id: str,
            customer_id: str,
            account_number: str,
            balance: float = 0.0,
    ):
        self.account_id: str = account_id
        self.customer_id: str = customer_id
        self.account_number: str = account_number
        self.balance: float = balance

    def deposit(self, value: float):
        self.balance += value

    def withdraw(self, value: float):
        self.balance -= value

    def get_balance(self, value: float, transaction_type: str):
        getattr(self, transaction_type)(value)
        return self.balance

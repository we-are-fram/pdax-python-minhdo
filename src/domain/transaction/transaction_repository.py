# -*- coding: utf-8 -*-
"""Transaction repository"""

from abc import ABC, abstractmethod
from typing import Optional

from .transaction import Transaction


class TransactionRepository(ABC):
    """TransactionRepository defines a repository interface for Transaction entity."""

    @abstractmethod
    def create(self, transaction: Transaction) -> Optional[Transaction]:
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, transaction_id: str) -> Optional[Transaction]:
        raise NotImplementedError

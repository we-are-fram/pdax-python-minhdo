# -*- coding: utf-8 -*-
"""Account repository"""

from abc import ABC, abstractmethod
from typing import Optional

from .account import Account


class AccountRepository(ABC):
    """AccountRepository defines a repository interface for Account entity."""

    @abstractmethod
    def create(self, account: Account) -> Optional[Account]:
        raise NotImplementedError

    @abstractmethod
    def partial_update(self, account_id: str, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, account_id: str) -> Optional[Account]:
        raise NotImplementedError

    @abstractmethod
    def find_by_customer_id(self, customer_id: str) -> Optional[Account]:
        raise NotImplementedError

    @abstractmethod
    def delete_by_id(self, account_id: str):
        raise NotImplementedError

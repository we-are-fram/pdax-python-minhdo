from abc import ABC, abstractmethod
from typing import List, Optional

from .account_query_model import AccountReadModel


class AccountQueryService(ABC):
    """AccountQueryService defines a query service inteface related Account entity."""

    @abstractmethod
    def find_by_id(self, id: str) -> Optional[AccountReadModel]:
        raise NotImplementedError

    @abstractmethod
    def find_all(self) -> List[AccountReadModel]:
        raise NotImplementedError

    @abstractmethod
    def find_accounts_by_customer_id(self, customer_id: str) -> List[AccountReadModel]:
        raise NotImplementedError

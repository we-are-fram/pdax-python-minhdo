from abc import ABC, abstractmethod
from typing import List

from .transaction_query_model import TransactionReadModel


class TransactionQueryService(ABC):
    """TransactionQueryService defines a query service inteface related Transaction entity."""

    @abstractmethod
    def fetch_transactions_by_account_id(self, account_id: str) -> List[TransactionReadModel]:
        raise NotImplementedError

from abc import ABC, abstractmethod
from typing import List

from .transaction_query_model import TransactionReadModel
from .transaction_query_service import TransactionQueryService


class TransactionQueryUseCase(ABC):
    """AccountQueryUseCase defines a query usecase inteface related Transaction entity."""

    @abstractmethod
    def fetch_transactions_by_account_id(self, account_id: str) -> List[TransactionReadModel]:
        """fetch_transactions fetches transactions by using the account_id."""
        raise NotImplementedError


class TransactionQueryUseCaseImpl(TransactionQueryUseCase):
    """AccountQueryUseCaseImpl implements a query usecases related Transaction entity."""

    def __init__(self, transaction_query_service: TransactionQueryService):
        self.transaction_query_service: TransactionQueryService = transaction_query_service

    def fetch_transactions_by_account_id(self, account_id: str):
        try:
            transaction = self.transaction_query_service.fetch_transactions_by_account_id(account_id)
        except Exception as e:
            print(str(e))
            raise

        return transaction
